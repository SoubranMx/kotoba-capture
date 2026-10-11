"""Opt-in frozen, resumable whole-video sampling; never a reliability verdict."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.metadata
import json
import math
import os
import shutil
import struct
import subprocess
import sys
import time
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

from .core import Observation, group_observations, segments_to_json, segments_to_markdown
from .pilot_config import ConfigError, load_config, relative_file
from .selector import _valid_style_evidence, select_caption_profile_v17

SCHEMA = 'kotoba-video-pilot/v1'
PACKAGES = ('paddleocr', 'paddlex', 'paddlepaddle', 'numpy', 'opencv-python', 'opencv-contrib-python')
PHASES = ('initialize', 'extract', 'ocr', 'style', 'selection', 'export', 'integrity')


class PilotError(RuntimeError):
    """Safe public diagnostic, excluding private paths, text and exception detail."""


def now():
    return datetime.now(timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def binding(value):
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_bytes(path, raw):
    """Only replace after bytes are durable, then make the rename durable."""
    temporary = path.with_name(path.name + '.tmp')
    if path.is_symlink() or temporary.is_symlink():
        raise PilotError('Symlinked output is forbidden')
    with temporary.open('wb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    sync_directory(path.parent)


def atomic_json(path, value):
    atomic_bytes(path, (canonical(value) + '\n').encode('utf-8'))


def read_json(path):
    if path.is_symlink():
        raise PilotError('Symlinked audit data is forbidden')
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(value, dict):
            raise PilotError('Audit data must be one JSON object')
        return value
    except (OSError, ValueError):
        raise PilotError('Audit data is unavailable or invalid') from None


def file_identity(path):
    before = path.stat()
    digest = sha256(path)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns, before.st_mode) != (after.st_size, after.st_mtime_ns, after.st_mode):
        raise PilotError('Input changed during identity capture')
    return dict(sha256=digest, bytes=after.st_size, mtimeNs=after.st_mtime_ns, mode=after.st_mode & 0o777)


def tree_identity(folder):
    files = {}
    for path in sorted(folder.rglob('*')):
        if path.is_symlink():
            raise PilotError('Model assets must not contain symlinks')
        if path.is_file():
            files[path.relative_to(folder).as_posix()] = file_identity(path)
    if not files:
        raise PilotError('Local model assets are missing')
    return files


def code_identity():
    folder = Path(__file__).resolve().parent
    return {p.name: sha256(p) for p in sorted(folder.glob('*.py'))}


def png_dimensions(path):
    raw = path.read_bytes()[:24]
    if len(raw) != 24 or raw[:8] != b'\x89PNG\r\n\x1a\n' or raw[12:16] != b'IHDR':
        raise PilotError('Extracted frame is not a PNG')
    return list(struct.unpack('>II', raw[16:24]))


def serializable_prediction(value):
    view = getattr(value, 'json', None)
    view = view() if callable(view) else view
    if view is None:
        view = value
    if isinstance(view, str):
        view = json.loads(view)
    if not isinstance(view, dict):
        raise PilotError('OCR did not return one JSON object')
    if isinstance(view.get('res'), dict):
        view = view['res']

    def safe(item):
        if isinstance(item, dict):
            return {str(k): safe(v) for k, v in item.items()}
        if isinstance(item, (list, tuple)):
            return [safe(v) for v in item]
        if hasattr(item, 'tolist'):
            return safe(item.tolist())
        if hasattr(item, 'item'):
            return safe(item.item())
        if item is None or isinstance(item, (str, int, float, bool)):
            return item
        raise PilotError('Unsupported OCR JSON value')

    native = safe(view)
    keys = ('rec_texts', 'rec_scores', 'rec_boxes', 'rec_polys', 'dt_polys')
    if any(not isinstance(native.get(k), list) for k in keys):
        raise PilotError('OCR result is missing required arrays')
    if any(len(native[k]) != len(native['rec_texts']) for k in keys):
        raise PilotError('OCR native array counts disagree')
    canonical(native)
    return native


def offline(config):
    """Process-local network/DNS deny before any optional ML import."""
    cache = config.output / 'runtime'
    for key, suffix in {'HOME': 'home', 'XDG_CACHE_HOME': 'xdg', 'PADDLE_HOME': 'paddle',
                        'PADDLE_PDX_CACHE_HOME': 'paddlex', 'HF_HOME': 'hf', 'UV_CACHE_DIR': 'uv'}.items():
        path = cache / suffix
        path.mkdir(parents=True, exist_ok=True)
        os.environ[key] = str(path)
    os.environ.update(PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK='True', HF_HUB_OFFLINE='1',
                      UV_OFFLINE='1', OMP_NUM_THREADS=str(config.threads),
                      OPENBLAS_NUM_THREADS=str(config.threads), FLAGS_use_mkldnn='0',
                      PYTHONDONTWRITEBYTECODE='1')

    def deny(event, args):
        if event in ('socket.connect', 'socket.connect_ex', 'socket.getaddrinfo', 'socket.bind'):
            raise PilotError('Network and DNS are disabled for this local pilot')
    sys.addaudithook(deny)


class LocalRuntime:
    """Lazy existing-tool adapter; no installer, URLs, auto-download or package patch."""

    def __init__(self):
        self.tools = {}
        for name in ('ffprobe', 'ffmpeg'):
            executable = shutil.which(name)
            if executable is None:
                raise PilotError('Required local FFmpeg tools are unavailable')
            self.tools[name] = executable

    def command(self, args):
        try:
            return subprocess.run(args, capture_output=True, check=True, timeout=120).stdout
        except (OSError, subprocess.SubprocessError):
            raise PilotError('A local FFmpeg command failed; no private arguments were logged') from None

    def probe(self, config):
        data = json.loads(self.command([self.tools['ffprobe'], '-v', 'error', '-select_streams', 'v:0',
                                       '-show_entries', 'stream=width,height:format=duration', '-of', 'json', str(config.video)]))
        stream = data['streams'][0]
        return stream['width'], stream['height'], float(data['format']['duration'])

    def identity(self):
        packages = {}
        for name in PACKAGES:
            try:
                distribution = importlib.metadata.distribution(name)
            except importlib.metadata.PackageNotFoundError:
                continue
            h = hashlib.sha256()
            for relative in sorted(distribution.files or [], key=str):
                path = Path(distribution.locate_file(relative))
                if path.is_file() and path.suffix in ('.py', '.so', '.json', '.yml', '.yaml'):
                    h.update(str(relative).encode()); h.update(bytes.fromhex(sha256(path)))
            packages[name] = dict(version=distribution.version, codeSha256=h.hexdigest())
        if packages.get('paddleocr', {}).get('version') != '3.7.0' or not all(k in packages for k in ('paddlex', 'paddlepaddle', 'numpy')):
            raise PilotError('Existing PaddleOCR 3.7.0 CPU runtime is required; installation/download is disabled')
        if not any(k in packages for k in ('opencv-python', 'opencv-contrib-python')):
            raise PilotError('Existing OpenCV runtime is required; installation is disabled')
        return dict(python=sys.version, executableSha256=sha256(Path(sys.executable).resolve()),
                    packages=packages, tools={name: dict(sha256=sha256(Path(path).resolve()),
                    version=self.command([path, '-version']).decode(errors='replace').splitlines()[0])
                    for name, path in self.tools.items()})

    def initialize(self, config):
        offline(config)
        try:
            from paddleocr import PaddleOCR
            from paddleocr._common_args import parse_common_args
            kwargs = dict(device='cpu', text_detection_model_name='PP-OCRv6_medium_det',
                          text_detection_model_dir=str(config.detector), text_recognition_model_name='PP-OCRv6_medium_rec',
                          text_recognition_model_dir=str(config.recognizer), use_doc_orientation_classify=False,
                          use_doc_unwarping=False, use_textline_orientation=False, enable_mkldnn=False,
                          mkldnn_cache_capacity=10, cpu_threads=config.threads, enable_cinn=False,
                          use_tensorrt=False, precision='fp32')
            aliases = parse_common_args({'use_tensorrt': False, 'precision': 'fp32'}, default_enable_hpi=False)
            if aliases.get('use_pptrt') is not False or aliases.get('pptrt_precision') != 'fp32':
                raise PilotError('Installed PaddleOCR argument aliases are incompatible; packages were not patched')
            return PaddleOCR(**kwargs)
        except ImportError:
            raise PilotError('Existing optional OCR dependencies are unavailable; installation is disabled') from None

    def extract(self, config, timestamp, path):
        raw = self.command([self.tools['ffmpeg'], '-v', 'error', '-ss', f'{timestamp:.9f}', '-i', str(config.video),
                            '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', 'pipe:1'])
        atomic_bytes(path, raw)

    def predict(self, engine, path):
        outputs = list(engine.predict(str(path)))
        if len(outputs) != 1:
            raise PilotError('Exactly one native prediction is required per frame')
        return serializable_prediction(outputs[0])

    def style(self, path, native, geometry):
        from .style_evidence import from_path
        return from_path(path, native, geometry)


def make_identity(config, runtime):
    if relative_file(config.media_root, config.video_alias) != config.video:
        raise PilotError('Media alias binding changed')
    try:
        current_policy = read_json(config.policy_file)['policies'][config.profile_id]
    except (KeyError, TypeError):
        raise PilotError('Manual policy binding is unavailable') from None
    if current_policy != config.policy:
        raise PilotError('Manual policy changed after configuration resolution')
    width, height, duration = runtime.probe(config)
    if (any(type(v) is not int or v <= 0 for v in (width, height)) or
            not isinstance(duration, (float, int)) or isinstance(duration, bool) or
            not math.isfinite(duration) or duration <= 0):
        raise PilotError('Video dimensions and duration must be positive and finite')
    count = math.ceil(duration / config.interval)
    if not 1 <= count <= 100000:
        raise PilotError('Sampling plan exceeds the supported 100000-sample bound')
    timestamps = [i * config.interval for i in range(count) if i * config.interval < duration]
    return dict(schema=SCHEMA, configSha256=binding(config.runtime_values()), code=code_identity(),
                source=file_identity(config.video), policyFile=file_identity(config.policy_file),
                profileId=config.profile_id, policy=copy.deepcopy(config.policy), interval=config.interval,
                models={'detector': tree_identity(config.detector), 'recognizer': tree_identity(config.recognizer)},
                runtime=runtime.identity(), frameGeometry=dict(sourceWidth=width, sourceHeight=height, crop=[0, 0, width, height]),
                duration=duration, timestamps=timestamps)


@contextmanager
def exclusive_run(config):
    """Linux advisory lock serializes all writers using this entry point."""
    import fcntl
    path = config.experiment_root / ('.' + config.output.name + '.lock')
    if path.is_symlink():
        raise PilotError('Symlinked run lock is forbidden')
    fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise PilotError('This pilot already has an active writer') from None
        yield
    finally:
        os.close(fd)


def selected_for(record, identity):
    geometry = identity['frameGeometry']
    return select_caption_profile_v17(dict(width=geometry['crop'][2], height=geometry['crop'][3]),
                                     record['nativeResult'], identity['policy'], geometry,
                                     style_evidence=record['styleEvidence'], expected_image_sha256=record['imageSha256'])


def validate_record(record, index, identity, output):
    geometry = identity['frameGeometry']
    if (record.get('schema') != SCHEMA or record.get('index') != index or
            record.get('timestamp') != identity['timestamps'][index] or
            record.get('identitySha256') != binding(identity) or record.get('frameGeometry') != geometry or
            record.get('imagePath') != f'frames/{index:06}.png'):
        raise PilotError('Sample record identity or ordered coverage is invalid')
    image = output / record['imagePath']
    if image.is_symlink() or sha256(image) != record['imageSha256'] or png_dimensions(image) != geometry['crop'][2:]:
        raise PilotError('Sample image identity or dimensions changed')
    native = serializable_prediction(record['nativeResult'])
    if not _valid_style_evidence(record['styleEvidence'], record['imageSha256'], native, geometry, 'light_fill_dark_outline'):
        raise PilotError('Sample style bindings are invalid')
    if record['selected'].get('reason') in ('malformed_native', 'invalid_geometry', 'invalid_policy', 'invalid_style_evidence'):
        raise PilotError('Malformed OCR or selector input cannot be admitted')
    if record['selected'] != selected_for(record, identity):
        raise PilotError('Selected audit cannot be reproduced from the frozen inputs')
    if record.get('recordSha256') != binding({k: v for k, v in record.items() if k != 'recordSha256'}):
        raise PilotError('Sample audit bytes changed')


def read_records(output, identity, ledger):
    if (ledger.get('schema') != SCHEMA or ledger.get('identitySha256') != binding(identity) or
            type(ledger.get('completed')) is not int or ledger['completed'] < 0 or
            not isinstance(ledger.get('recordHashes'), list) or len(ledger['recordHashes']) != ledger['completed'] or
            ledger.get('status') not in ('registered', 'running', 'partial', 'completed') or
            not isinstance(ledger.get('attempts'), list) or
            any(type(ledger.get(k)) is not int or ledger[k] < 0 for k in
                ('modelInitializations', 'enteredPredictions', 'enteredStyleMeasurements', 'enteredSelections', 'interruptedCalls'))):
        raise PilotError('Run ledger identity, status or completed coverage is invalid')
    paths = sorted((output / 'records').glob('*.json'))
    expected = [f'{i:06}.json' for i in range(len(paths))]
    if [p.name for p in paths] != expected or len(paths) > len(identity['timestamps']):
        raise PilotError('Sample records are duplicate, extra, missing or out of order')
    if not len(paths) >= ledger['completed'] or len(paths) > ledger['completed'] + 1:
        raise PilotError('Durable record and ledger counts disagree')
    records = []
    for index, path in enumerate(paths):
        record = read_json(path)
        try:
            validate_record(record, index, identity, output)
        except (OSError, ValueError, KeyError, TypeError, OverflowError):
            raise PilotError('Sample audit data is missing or invalid') from None
        if index < len(ledger['recordHashes']) and record['recordSha256'] != ledger['recordHashes'][index]:
            raise PilotError('Completed audit hash changed')
        records.append(record)
    return records


@contextmanager
def private_log(path):
    fd = os.open(path, os.O_CREAT | os.O_APPEND | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'a', encoding='utf-8') as stream:
        yield stream


@contextmanager
def timed(attempt, phase):
    start = time.monotonic()
    try:
        yield
    finally:
        attempt['phases'][phase] += time.monotonic() - start


def public_summary(ledger, samples):
    return dict(status=ledger['status'], completed=ledger['completed'], samples=samples,
                attempts=len(ledger['attempts']), activeSeconds=sum(a['elapsedSeconds'] for a in ledger['attempts']),
                phaseSeconds={p: sum(a['phases'][p] for a in ledger['attempts']) for p in PHASES},
                registeredAt=ledger['registeredAt'], startedAt=ledger['startedAt'], endedAt=ledger.get('endedAt'),
                wallElapsedSeconds=(datetime.fromisoformat(ledger['endedAt']) - datetime.fromisoformat(ledger['startedAt'])).total_seconds() if ledger.get('endedAt') and ledger['startedAt'] else None,
                interruptionDowntimeSeconds=ledger['interruptionDowntimeSeconds'] if ledger['unobservedIntervalSeconds'] == 0 else None,
                knownDowntimeSeconds=ledger['interruptionDowntimeSeconds'],
                unobservedIntervalSeconds=ledger['unobservedIntervalSeconds'],
                activeTimeIsLowerBound=ledger['unobservedIntervalSeconds'] > 0,
                reviewStatus='all_text_requires_review', visualReviewSeconds=None,
                reliabilityMeasured=False, timing='requested_display_samples_not_audio_alignment')


def export_review(output, records, identity):
    observations = [Observation(r['timestamp'], r['selected']['text'], r['imagePath']) for r in records]
    segments = group_observations(observations, identity['interval'], sample_end=identity['duration'])
    atomic_bytes(output / 'segments.json', (segments_to_json(segments) + '\n').encode('utf-8'))
    atomic_bytes(output / 'review.md', segments_to_markdown(segments).encode('utf-8'))
    atomic_json(output / 'observations.json', dict(reviewStatus='all_text_requires_review', observations=[
        dict(timestamp=r['timestamp'], text=r['selected']['text'], imagePath=r['imagePath'],
             status=r['selected']['status'], reason=r['selected']['reason'], audit=f"records/{r['index']:06}.json") for r in records]))


def run_pilot(config, *, runtime=None, mode='execute', resume=False):
    """Preflight/register do not import ML; execute initializes once per attempt."""
    runtime = runtime or LocalRuntime()
    identity = make_identity(config, runtime)
    count = len(identity['timestamps'])
    if mode == 'preflight':
        return dict(status='preflight_passed', samples=count, duration=identity['duration'], mlImports=0,
                    estimatedRawFrameBytes=count * identity['frameGeometry']['crop'][2] * identity['frameGeometry']['crop'][3] * 3)
    if mode not in ('register', 'execute'):
        raise PilotError('Unknown pilot mode')
    with exclusive_run(config):
        output = config.output
        if output.exists():
            if not resume or output.is_symlink():
                raise PilotError('Existing output requires explicit resume')
            for folder in ('records', 'frames', 'runtime'):
                if (output / folder).is_symlink() or not (output / folder).is_dir():
                    raise PilotError('Run storage is unavailable or symlinked')
            plan = read_json(output / 'plan.json')
            if plan['identity'] != identity or plan['identitySha256'] != binding(identity):
                raise PilotError('Frozen code, source, model, profile, configuration or runtime changed')
            ledger = read_json(output / 'ledger.json')
            records = read_records(output, identity, ledger)
            if ledger['status'] == 'completed':
                if len(records) != count:
                    raise PilotError('Completed run has incomplete coverage')
                return public_summary(ledger, count)
            if mode == 'register':
                raise PilotError('Run registration is already consumed')
        else:
            output.mkdir()
            sync_directory(output.parent)
            for folder in ('records', 'frames', 'runtime'):
                (output / folder).mkdir()
            sync_directory(output)
            plan = dict(schema=SCHEMA, registeredAt=now(), identity=identity, identitySha256=binding(identity))
            atomic_json(output / 'plan.json', plan)
            ledger = dict(schema=SCHEMA, identitySha256=binding(identity), status='registered', registeredAt=plan['registeredAt'], startedAt=None, completed=0,
                          recordHashes=[], attempts=[], modelInitializations=0, enteredPredictions=0,
                          enteredStyleMeasurements=0, enteredSelections=0, interruptedCalls=0,
                          pending=None, interruptionDowntimeSeconds=0, unobservedIntervalSeconds=0)
            atomic_json(output / 'ledger.json', ledger)
            records = []
        if mode == 'register':
            return dict(status='registered', samples=count, mlImports=0)
        if ledger['pending'] is not None and ledger['pending']['index'] >= len(records):
            ledger['interruptedCalls'] += 1
        ledger['completed'] = len(records)
        ledger['recordHashes'] = [r['recordSha256'] for r in records]
        if ledger['attempts']:
            previous = ledger['attempts'][-1]
            abrupt = previous.get('endedAt') is None
            if abrupt:
                previous['status'] = 'interrupted'
                previous['endedAt'] = previous['checkpointAt']
                previous['elapsedSeconds'] = previous['checkpointElapsedSeconds']
            gap = max(0, (datetime.fromisoformat(now()) - datetime.fromisoformat(previous['endedAt'])).total_seconds())
            ledger['unobservedIntervalSeconds' if abrupt else 'interruptionDowntimeSeconds'] += gap
        attempt = dict(startedAt=now(), endedAt=None, status='running', elapsedSeconds=0,
                       checkpointAt=now(), checkpointElapsedSeconds=0, phases={p: 0.0 for p in PHASES})
        if ledger['startedAt'] is None:
            ledger['startedAt'] = attempt['startedAt']
        ledger['attempts'].append(attempt)
        ledger['status'] = 'running'
        ledger['pending'] = None
        start = time.monotonic()

        def checkpoint():
            attempt['checkpointAt'] = now()
            attempt['checkpointElapsedSeconds'] = time.monotonic() - start
            atomic_json(output / 'ledger.json', ledger)

        def enter(index, phase, counter=None):
            ledger['pending'] = dict(index=index, phase=phase, enteredAt=now())
            if counter:
                ledger[counter] += 1
            checkpoint()

        try:
            checkpoint()
            if len(records) < count:
                ledger['modelInitializations'] += 1
                checkpoint()
                with private_log(output / 'runtime/engine.log') as log, redirect_stdout(log), redirect_stderr(log), timed(attempt, 'initialize'):
                    engine = runtime.initialize(config)
                checkpoint()
                for index in range(len(records), count):
                    timestamp = identity['timestamps'][index]
                    case_started = now()
                    phases_before = attempt['phases'].copy()
                    image = output / f'frames/{index:06}.png'
                    enter(index, 'extract')
                    with timed(attempt, 'extract'):
                        runtime.extract(config, timestamp, image)
                        if png_dimensions(image) != identity['frameGeometry']['crop'][2:]:
                            raise PilotError('Extracted image dimensions differ from the frozen geometry')
                    enter(index, 'ocr', 'enteredPredictions')
                    with private_log(output / 'runtime/engine.log') as log, redirect_stdout(log), redirect_stderr(log), timed(attempt, 'ocr'):
                        native = serializable_prediction(runtime.predict(engine, image))
                    pristine = copy.deepcopy(native)
                    enter(index, 'style', 'enteredStyleMeasurements')
                    with timed(attempt, 'style'):
                        evidence = runtime.style(image, native, identity['frameGeometry'])
                    record = dict(schema=SCHEMA, index=index, timestamp=timestamp, identitySha256=binding(identity),
                                  imagePath=f'frames/{index:06}.png', imageSha256=sha256(image),
                                  frameGeometry=identity['frameGeometry'], nativeResult=native, styleEvidence=evidence)
                    enter(index, 'selection', 'enteredSelections')
                    with timed(attempt, 'selection'):
                        record['selected'] = selected_for(record, identity)
                    if native != pristine:
                        raise PilotError('OCR arrays were mutated')
                    record['startedAt'] = case_started
                    record['endedAt'] = now()
                    record['attempt'] = len(ledger['attempts'])
                    record['phaseSeconds'] = {p: attempt['phases'][p] - phases_before[p] for p in PHASES}
                    record['recordSha256'] = binding(record)
                    validate_record(record, index, identity, output)
                    atomic_json(output / f'records/{index:06}.json', record)
                    records.append(record)
                    ledger['completed'] = len(records)
                    ledger['recordHashes'].append(record['recordSha256'])
                    ledger['pending'] = None
                    checkpoint()
            with timed(attempt, 'integrity'):
                if make_identity(config, runtime) != identity:
                    raise PilotError('Frozen input identity changed during execution')
            with timed(attempt, 'export'):
                export_review(output, records, identity)
            ledger['status'] = 'completed'
            attempt['status'] = 'completed'
        except BaseException as error:
            ledger['status'] = 'partial'
            attempt['status'] = 'partial'
            attempt['failure'] = dict(type=type(error).__name__, reason='local_execution_failed_private_details_not_public')
            # Preserve privately for diagnosis, never send exception text to stdout.
            atomic_json(output / 'runtime/failure.json', dict(type=type(error).__name__, message=str(error), at=now()))
            if isinstance(error, (KeyboardInterrupt, SystemExit)):
                attempt['failure']['reason'] = 'interrupted'
        finally:
            attempt['elapsedSeconds'] = time.monotonic() - start
            attempt['endedAt'] = now()
            ledger['endedAt'] = attempt['endedAt']
            checkpoint()
            summary = public_summary(ledger, count)
            atomic_json(output / 'summary.json', summary)
        return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('preflight', 'register', 'execute'))
    parser.add_argument('--video', required=True, help='Relative alias inside configured media library')
    parser.add_argument('--output-name', required=True, help='Safe directory token inside experiment storage')
    parser.add_argument('--env-file', help='Strict KEY=VALUE file; defaults to project .env')
    parser.add_argument('--profile-id', help='Explicit manual profile identifier')
    parser.add_argument('--interval', type=float, help='Positive finite cadence in seconds (default .5)')
    parser.add_argument('--resume', action='store_true', help='Validate frozen identities and resume missing samples only')
    args = parser.parse_args(argv)
    try:
        root = Path(__file__).resolve().parents[3]
        config = load_config(root, args.video, args.output_name, env_file=args.env_file,
                             interval=args.interval, profile_id=args.profile_id)
        result = run_pilot(config, mode=args.mode, resume=args.resume)
        print(canonical(result))
        return 0 if result['status'] != 'partial' else 1
    except (ConfigError, PilotError):
        print('Pilot refused: configuration, frozen identity, audit or local runtime validation failed.', file=sys.stderr)
        return 2
    except (OSError, ValueError, KeyError, TypeError, OverflowError):
        print('Pilot refused: invalid local input or audit data.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
