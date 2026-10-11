"""Mock full-video runs with no OCR, media extraction or private fixtures."""
import json
import os
import subprocess
import sys
import struct
import unittest
from pathlib import Path
from unittest.mock import patch
import test_pilot_config as fixtures
from kotoba_capture.video_pilot import PilotError, run_pilot, atomic_json, sha256


class FakeRuntime:
    def __init__(self):
        self.initializations = 0
        self.predictions = []
        self.fail_at = None
        self.duration = 1.5
        self.texts = ['First\nSecond', '', 'First\nSecond']

    def probe(self, config): return 100, 100, self.duration
    def identity(self): return {'runtime': 'synthetic immutable runtime', 'ffmpeg': 'mock', 'ffprobe': 'mock'}
    def initialize(self, config): self.initializations += 1; return self
    def extract(self, config, timestamp, path):
        path.write_bytes(b'\x89PNG\r\n\x1a\n' + b'\0\0\0\rIHDR' + struct.pack('>II', 100, 100) + b'synthetic')
    def predict(self, engine, path):
        index = int(path.stem)
        self.predictions.append(index)
        if self.fail_at == index: raise RuntimeError('private sensitive error')
        texts = self.texts[index].splitlines()
        polys = [[[10, 10 + i*25], [90, 10 + i*25], [90, 30 + i*25], [10, 30 + i*25]] for i in range(len(texts))]
        return dict(rec_texts=texts, rec_scores=[.9]*len(texts), rec_boxes=[[p[0][0], p[0][1], p[2][0], p[2][1]] for p in polys], rec_polys=polys, dt_polys=polys)
    def style(self, path, native, geometry):
        from kotoba_capture.selector import _style_binding
        return dict(schema='caption-style-evidence/v1', adapterVersion='light-outline-components-v2',
                    style='light_fill_dark_outline', imageSha256=sha256(path), nativeSha256=_style_binding(native),
                    geometrySha256=_style_binding(geometry), entries=[dict(index=i, status='match', reason='synthetic') for i in range(len(native['rec_texts']))])


class VideoPilotTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.ConfigTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.config = self.fixture.config()
        self.runtime = FakeRuntime()

    def execute(self, **kwargs): return run_pilot(self.config, runtime=self.runtime, **kwargs)
    def read(self, name): return json.loads((self.config.output / name).read_text())

    def test_whole_video_blank_splits_repetitions_rows_review_flags(self):
        result = self.execute()
        self.assertEqual(result['status'], 'completed')
        self.assertEqual(result['completed'], 3)
        self.assertEqual(self.runtime.initializations, 1)
        self.assertEqual(self.runtime.predictions, [0, 1, 2])
        records = [self.read(f'records/{i:06}.json') for i in range(3)]
        self.assertEqual([r['timestamp'] for r in records], [0, .5, 1])
        self.assertEqual(records[0]['selected']['text'], 'First\nSecond')
        self.assertTrue(records[0]['selected']['reviewRequired'])
        segments = self.read('segments.json')['segments']
        self.assertEqual(len(segments), 2)
        self.assertEqual(segments[0]['text'], 'First\nSecond')
        self.assertIn('review', (self.config.output / 'review.md').read_text().lower())

    def test_interrupted_resume_only_missing_records_lifetime_counts(self):
        self.runtime.fail_at = 1
        result = self.execute()
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(result['completed'], 1)
        original = (self.config.output / 'records/000000.json').read_bytes()
        self.runtime.fail_at = None
        resumed = self.execute(resume=True)
        self.assertEqual(resumed['completed'], 3)
        self.assertEqual(self.runtime.predictions, [0, 1, 1, 2])
        self.assertEqual(self.runtime.initializations, 2)
        self.assertEqual(original, (self.config.output / 'records/000000.json').read_bytes())
        ledger = self.read('ledger.json')
        self.assertEqual(ledger['enteredPredictions'], 4)
        self.assertEqual(ledger['interruptedCalls'], 1)
        self.assertEqual(len(ledger['attempts']), 2)
        self.assertGreaterEqual(ledger['attempts'][0]['phases']['ocr'], 0)
        self.assertNotIn('private sensitive', json.dumps(ledger))

    def test_completed_run_is_consumed_without_model_initialization(self):
        self.execute()
        self.execute(resume=True)
        self.assertEqual(self.runtime.initializations, 1)
        with self.assertRaises(PilotError): self.execute()

    def test_preflight_does_not_create_output_or_initialize(self):
        self.assertEqual(self.execute(mode='preflight')['samples'], 3)
        self.assertFalse(self.config.output.exists())
        self.assertEqual(self.runtime.initializations, 0)

    def test_register_freezes_without_ml_and_execute_uses_registered_identity(self):
        self.execute(mode='register')
        self.assertEqual(self.runtime.initializations, 0)
        self.assertTrue((self.config.output / 'plan.json').exists())
        self.assertEqual(self.execute(resume=True)['completed'], 3)

    def test_freeze_rejects_source_model_policy_runtime_and_config_mutation(self):
        for kind in ('video', 'model', 'policy', 'runtime', 'code', 'config'):
            with self.subTest(kind=kind):
                self.setUp()
                self.execute(mode='register')
                if kind == 'video': self.config.video.write_bytes(b'changed')
                elif kind == 'model': (self.config.detector / 'inference.json').write_bytes(b'changed')
                elif kind == 'policy': self.config.policy_file.write_text('{}')
                elif kind == 'runtime': self.runtime.identity = lambda: {'runtime': 'changed'}
                elif kind == 'config': object.__setattr__(self.config, 'interval', .25)
                else:
                    with patch('kotoba_capture.video_pilot.code_identity', return_value={'changed': 'identity'}):
                        with self.assertRaises(PilotError): self.execute(resume=True)
                    continue
                with self.assertRaises(PilotError): self.execute(resume=True)
                self.assertEqual(self.runtime.initializations, 0)

    def test_corrupt_missing_extra_or_reordered_record_refused(self):
        for change in ('corrupt', 'missing', 'extra', 'timestamp', 'selected', 'image', 'native', 'style'):
            with self.subTest(change=change):
                self.setUp(); self.execute()
                path = self.config.output / 'records/000000.json'
                record = self.read('records/000000.json')
                if change == 'corrupt': path.write_text('{')
                elif change == 'missing': path.unlink()
                elif change == 'extra': (self.config.output / 'records/000003.json').write_bytes(path.read_bytes())
                elif change == 'image': (self.config.output / record['imagePath']).write_bytes(b'changed')
                else:
                    if change == 'timestamp': record['timestamp'] = 1
                    if change == 'selected': record['selected']['text'] = 'tampered'
                    if change == 'native': record['nativeResult']['rec_scores'].append(.9)
                    if change == 'style': record['styleEvidence']['imageSha256'] = '0'*64
                    atomic_json(path, record)
                with self.assertRaises(PilotError): self.execute(resume=True)
                self.assertEqual(self.runtime.initializations, 1)

    def test_abstention_is_retained_not_ground_truth(self):
        self.runtime.texts[0] = 'Square'
        original = self.runtime.predict
        def square(engine, path):
            native = original(engine, path)
            if path.stem == '000000':
                native['rec_boxes'][0] = [10, 10, 30, 30]
                native['dt_polys'][0] = native['rec_polys'][0] = [[10,10],[30,10],[30,30],[10,30]]
            return native
        self.runtime.predict = square
        self.execute()
        record = self.read('records/000000.json')
        self.assertEqual(record['selected']['status'], 'review')
        self.assertEqual(record['nativeResult']['rec_texts'], ['Square'])
        self.assertNotIn('cer', self.read('summary.json'))

    def test_record_durable_before_ledger_resume_reconciles(self):
        from kotoba_capture import video_pilot
        real = video_pilot.atomic_json
        failed = False
        def fail(path, value):
            nonlocal failed
            if path.name == 'ledger.json' and value.get('completed') == 1 and not failed:
                failed = True
                raise OSError('simulated power interruption after record commit')
            return real(path, value)
        with patch.object(video_pilot, 'atomic_json', side_effect=fail): self.execute()
        self.execute(resume=True)
        self.assertEqual(self.runtime.predictions.count(0), 1)

    def test_symlink_record_or_image_refused(self):
        self.execute()
        p = self.config.output / 'records/000000.json'
        raw = p.read_bytes(); p.unlink()
        external = self.fixture.root / 'external.json'; external.write_bytes(raw); p.symlink_to(external)
        with self.assertRaises(PilotError): self.execute(resume=True)

    def test_invalid_duration_or_excessive_sample_count(self):
        for duration in (float('nan'), 0, 1000000):
            self.runtime.duration = duration
            with self.assertRaises(PilotError): self.execute(mode='preflight')

    def test_unobserved_power_loss_time_not_claimed_as_known_downtime(self):
        self.runtime.fail_at = 1
        self.execute()
        ledger = self.read('ledger.json')
        ledger['attempts'][-1]['endedAt'] = None
        atomic_json(self.config.output / 'ledger.json', ledger)
        self.runtime.fail_at = None
        result = self.execute(resume=True)
        self.assertTrue(result['activeTimeIsLowerBound'])
        self.assertIsNone(result['interruptionDowntimeSeconds'])
        self.assertGreater(result['unobservedIntervalSeconds'], 0)

    def test_concurrent_writer_refused(self):
        from kotoba_capture.video_pilot import exclusive_run
        with exclusive_run(self.config):
            with self.assertRaises(PilotError): self.execute()
        self.assertEqual(self.runtime.initializations, 0)

    def test_initialization_failure_is_partial_without_prediction(self):
        self.runtime.initialize = lambda config: (_ for _ in ()).throw(RuntimeError('sensitive model path'))
        result = self.execute()
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(result['completed'], 0)
        self.assertEqual(self.read('ledger.json')['modelInitializations'], 1)
        self.assertFalse(self.runtime.predictions)
        self.assertNotIn('sensitive', json.dumps(result))

    def test_native_serialization_prefers_json_view_preserves_extra_audit(self):
        from kotoba_capture.video_pilot import serializable_prediction
        native = self.runtime.predict(None, Path('000001.png'))
        native['extra'] = {'engine': 'synthetic'}
        class Result(dict):
            json = {'res': native}
        self.assertEqual(serializable_prediction(Result(invalid='dict subclass')), native)
        with self.assertRaises(PilotError): serializable_prediction({'rec_texts': []})

    def test_stdout_cli_whole_video_and_interrupted_resume_in_fresh_processes(self):
        program = """import sys
from pathlib import Path
from kotoba_capture import video_pilot as p
from test_video_pilot import FakeRuntime
original = p.load_config
root = Path(sys.argv[1])
p.load_config = lambda ignored, *args, **kwargs: original(root, *args, **kwargs)
runtime = FakeRuntime()
if sys.argv[2] == 'interrupt': runtime.fail_at = 1
p.LocalRuntime = lambda: runtime
raise SystemExit(p.main(sys.argv[3:]))
"""
        env = {**os.environ, **self.fixture.env}
        env['PYTHONPATH'] = os.pathsep.join([str(Path(__file__).resolve().parents[1]), str(Path(__file__).resolve().parent)])
        command = [sys.executable, '-B', '-S', '-c', program, str(self.fixture.root)]
        arguments = ['execute', '--video', 'sample.mp4', '--output-name', 'cli-run']
        first = subprocess.run([*command, 'interrupt', *arguments], env=env, capture_output=True, text=True)
        self.assertEqual(first.returncode, 1, first.stderr)
        self.assertEqual(json.loads(first.stdout)['completed'], 1)
        second = subprocess.run([*command, 'resume', *arguments, '--resume'], env=env, capture_output=True, text=True)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(json.loads(second.stdout)['completed'], 3)
        for result in (first, second):
            self.assertNotIn(str(self.fixture.root), result.stdout + result.stderr)
            self.assertNotIn('First', result.stdout)
        ledger = json.loads((self.fixture.root / '.local/cli-run/ledger.json').read_text())
        self.assertEqual(ledger['enteredPredictions'], 4)
        self.assertEqual(ledger['modelInitializations'], 2)

    def test_cpu_constructor_contract_with_mock_optional_imports(self):
        from types import SimpleNamespace
        from kotoba_capture.video_pilot import LocalRuntime
        calls = []
        def constructor(**kwargs): calls.append(kwargs); return 'synthetic engine'
        modules = {'paddleocr': SimpleNamespace(PaddleOCR=constructor),
                   'paddleocr._common_args': SimpleNamespace(parse_common_args=lambda *a, **k: {'use_pptrt': False, 'pptrt_precision': 'fp32'})}
        with patch.dict(sys.modules, modules), patch('kotoba_capture.video_pilot.offline'):
            runtime = object.__new__(LocalRuntime)
            self.assertEqual(runtime.initialize(self.config), 'synthetic engine')
        self.assertEqual(calls[0]['cpu_threads'], 10)
        self.assertFalse(calls[0]['enable_mkldnn'])
        self.assertFalse(calls[0]['enable_cinn'])
        self.assertFalse(calls[0]['use_tensorrt'])
        self.assertFalse(calls[0]['use_doc_orientation_classify'])
        self.assertFalse(calls[0]['use_doc_unwarping'])
        self.assertFalse(calls[0]['use_textline_orientation'])
        self.assertEqual(calls[0]['text_detection_model_dir'], str(self.config.detector))

    def test_local_ffmpeg_boundary_commands_are_argument_lists(self):
        from types import SimpleNamespace
        from kotoba_capture.video_pilot import LocalRuntime
        runtime = object.__new__(LocalRuntime)
        runtime.tools = {'ffprobe': 'mock-probe', 'ffmpeg': 'mock-extract'}
        probe = json.dumps({'streams': [{'width': 100, 'height': 100}], 'format': {'duration': '1.5'}}).encode()
        png = b'\x89PNG\r\n\x1a\n' + b'\0\0\0\rIHDR' + struct.pack('>II', 100, 100)
        with patch('kotoba_capture.video_pilot.subprocess.run', side_effect=[SimpleNamespace(stdout=probe), SimpleNamespace(stdout=png)]) as command:
            self.assertEqual(runtime.probe(self.config), (100, 100, 1.5))
            target = self.fixture.root / 'synthetic.png'
            runtime.extract(self.config, .5, target)
            self.assertEqual(target.read_bytes(), png)
        argv = command.call_args_list[1].args[0]
        self.assertIsInstance(argv, list)
        self.assertIn('0.500000000', argv)
        self.assertEqual(argv[-1], 'pipe:1')
        self.assertNotIn('shell', command.call_args.kwargs)

    def test_missing_frame_and_invalid_json_object_fail_closed(self):
        self.execute()
        (self.config.output / 'frames/000000.png').unlink()
        with self.assertRaises(PilotError): self.execute(resume=True)
        atomic_json(self.config.output / 'ledger.json', [])
        with self.assertRaises(PilotError): self.execute(resume=True)

    def test_invalid_style_binding_preserves_partial_not_completed_sample(self):
        original = self.runtime.style
        def invalid(*args):
            value = original(*args)
            value['imageSha256'] = '0'*64
            return value
        self.runtime.style = invalid
        self.assertEqual(self.execute()['status'], 'partial')
        self.assertEqual(self.read('ledger.json')['completed'], 0)
