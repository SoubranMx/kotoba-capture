"""Strict, non-executing machine-local configuration for the opt-in pilot."""
from __future__ import annotations

import json
import math
import os
import re
from dataclasses import dataclass
from pathlib import Path

from .selector import _valid_policy


class ConfigError(ValueError):
    """Configuration failure safe to display without private values."""


def read_env(path: Path) -> dict[str, str]:
    """Read KEY=VALUE, quotes and comments; reject expansion and shell syntax."""
    values = {}
    try:
        lines = path.read_text(encoding='utf-8').splitlines()
    except OSError:
        raise ConfigError('Environment file is unavailable') from None
    for number, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        match = re.fullmatch(r'([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)', line)
        if not match or match[1] in values:
            raise ConfigError(f'Invalid or duplicate environment assignment on line {number}')
        key, raw = match.groups()
        if '$' in raw or '`' in raw or '\\' in raw or '\x00' in raw:
            raise ConfigError(f'Unsupported environment syntax on line {number}')
        if raw.startswith(('"', "'")):
            end = raw.find(raw[0], 1)
            if end == -1 or (raw[end + 1:].strip() and not raw[end + 1:].strip().startswith('#')):
                raise ConfigError(f'Invalid quoted value on line {number}')
            value = raw[1:end]
        else:
            value = raw.split('#', 1)[0].strip()
            if any(c.isspace() for c in value) or any(c in value for c in ';|&<>"\''):
                raise ConfigError(f'Invalid unquoted value on line {number}')
        values[key] = value
    return values


def relative_file(root: Path, alias: str) -> Path:
    path = Path(alias)
    if not alias or path.is_absolute() or '..' in path.parts:
        raise ConfigError('Video must be a relative media-library alias without traversal')
    try:
        resolved = (root / path).resolve(strict=True)
    except OSError:
        raise ConfigError('Video is unavailable') from None
    if not resolved.is_relative_to(root) or not resolved.is_file():
        raise ConfigError('Video must be a file within the configured media library')
    return resolved


def numeric(value, label, minimum, maximum, *, integer=False):
    try:
        parsed = int(value) if integer else float(value)
    except (ValueError, TypeError, OverflowError):
        raise ConfigError(f'{label} must be numeric') from None
    if not minimum <= parsed <= maximum or not math.isfinite(parsed):
        raise ConfigError(f'{label} is outside the supported range')
    return parsed


@dataclass(frozen=True)
class PilotConfig:
    project_root: Path
    media_root: Path
    experiment_root: Path
    video: Path
    video_alias: str
    output: Path
    detector: Path
    recognizer: Path
    policy_file: Path
    profile_id: str
    policy: dict
    interval: float
    threads: int
    device: str

    def runtime_values(self):
        """Relevant resolved values are private and become a frozen hash."""
        return {name: str(getattr(self, name)) for name in self.__dataclass_fields__ if name != 'policy'}


def load_config(project_root, video_alias, output_name, *, env_file=None,
                environment=None, interval=None, profile_id=None) -> PilotConfig:
    root = Path(project_root).resolve(strict=True)
    file = Path(env_file) if env_file is not None else root / '.env'
    if not file.is_absolute():
        file = root / file
    values = read_env(file) if file.exists() else {}
    if env_file is not None and not file.exists():
        raise ConfigError('Explicit environment file is unavailable')
    values.update(os.environ if environment is None else environment)

    def required(name):
        value = values.get(name, '')
        if not value:
            raise ConfigError(f'Missing setting: {name}')
        return value

    def resolve(name, *, directory):
        raw = Path(required(name))
        try:
            path = (raw if raw.is_absolute() else root / raw).resolve(strict=True)
        except OSError:
            raise ConfigError(f'Unavailable configured path: {name}') from None
        if not (path.is_dir() if directory else path.is_file()):
            raise ConfigError(f'Invalid configured path type: {name}')
        return path

    media = resolve('KOTOBA_MEDIA_ROOT', directory=True)
    experiment = resolve('KOTOBA_EXPERIMENT_DATA_DIR', directory=True)
    private = root / '.local'
    if not private.exists() or private.is_symlink() or not experiment.is_relative_to(private):
        raise ConfigError('Experiment storage must be inside the project ignored .local directory')
    if not isinstance(output_name, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', output_name):
        raise ConfigError('Output name must be a safe directory token')
    output = experiment / output_name
    if output.is_symlink() or output.resolve().parent != experiment:
        raise ConfigError('Output must stay within experiment storage')
    detector = resolve('KOTOBA_PILOT_DET_MODEL_DIR', directory=True)
    recognizer = resolve('KOTOBA_PILOT_REC_MODEL_DIR', directory=True)
    policy_file = resolve('KOTOBA_PILOT_POLICY_FILE', directory=False)
    for model in (detector, recognizer):
        if not model.is_relative_to(experiment):
            raise ConfigError('Models must remain inside experiment storage')
        for name in ('inference.json', 'inference.yml', 'inference.pdiparams'):
            asset = model / name
            if not asset.is_file() or asset.is_symlink():
                raise ConfigError('Local model assets are missing or symlinked; downloads are disabled')
    if not policy_file.is_relative_to(experiment):
        raise ConfigError('Manual policy must remain inside experiment storage')
    profile = profile_id or required('KOTOBA_PILOT_PROFILE_ID')
    try:
        policy = json.loads(policy_file.read_text(encoding='utf-8'))['policies'][profile]
        valid = _valid_policy(policy)
    except (OSError, KeyError, TypeError, ValueError, OverflowError):
        raise ConfigError('Manual policy file or profile is invalid') from None
    if not valid or policy.get('background', 'no_constraint') != 'no_constraint':
        raise ConfigError('A valid manual profile without an unsupported blue-panel detector is required')
    cadence = numeric(interval if interval is not None else values.get('KOTOBA_PILOT_INTERVAL', '.5'),
                      'Sampling interval', .001, 3600)
    threads = numeric(values.get('KOTOBA_PILOT_CPU_THREADS', '10'), 'CPU threads', 1, 64, integer=True)
    device = values.get('KOTOBA_PILOT_DEVICE', 'cpu')
    if device not in ('cpu', 'gpu:0'):
        raise ConfigError('Pilot device must be cpu or gpu:0')
    return PilotConfig(root, media, experiment, relative_file(media, video_alias), video_alias,
                       output, detector, recognizer, policy_file, profile, policy, cadence, threads, device)
