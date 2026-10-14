"""Local FFmpeg/Tesseract sampling pipeline for human-reviewed OCR observations."""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
import hashlib
import io
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import time
from typing import Any

from .core import Observation, group_observations, segments_to_json, segments_to_markdown


class PipelineError(RuntimeError):
    """A clear local-tool, input, or output failure."""


@dataclass(frozen=True)
class ROI:
    """Pixel crop in original-frame coordinates."""

    x: int
    y: int
    width: int
    height: int


def validate_roi(roi: ROI | None, frame_width: int, frame_height: int) -> ROI | None:
    if roi is None:
        return None
    if not isinstance(roi, ROI):
        raise ValueError("roi must be an ROI or None")
    values = (roi.x, roi.y, roi.width, roi.height)
    if any(not isinstance(value, int) or isinstance(value, bool) for value in values):
        raise ValueError("ROI coordinates and dimensions must be integers")
    if roi.x < 0 or roi.y < 0 or roi.width <= 0 or roi.height <= 0:
        raise ValueError("ROI origin must be nonnegative and dimensions positive")
    if roi.x + roi.width > frame_width or roi.y + roi.height > frame_height:
        raise ValueError("ROI must fit within the original video frame")
    return roi


def parse_tesseract_tsv(tsv: str) -> tuple[str, float | None]:
    """Return line-ordered Japanese text and mean known word confidence.

    Confidence is Tesseract's engine heuristic normalized to 0..1, not a
    calibrated probability. Japanese TSV word fragments are concatenated
    without injecting spaces; separate detected lines remain newline-separated.
    """
    if not isinstance(tsv, str):
        raise PipelineError("Tesseract TSV output was not text")
    reader = csv.DictReader(io.StringIO(tsv), delimiter="\t")
    if not reader.fieldnames or not {"level", "text", "conf"}.issubset(reader.fieldnames):
        raise PipelineError("Tesseract returned malformed TSV output")
    lines: dict[tuple[str, str, str, str], list[str]] = {}
    confidences: list[float] = []
    for row in reader:
        if row.get("level") != "5":
            continue
        text = (row.get("text") or "").strip()
        if not text:
            continue
        key = (row.get("page_num", ""), row.get("block_num", ""), row.get("par_num", ""), row.get("line_num", ""))
        lines.setdefault(key, []).append(text)
        try:
            confidence = float(row.get("conf", "-1"))
        except (TypeError, ValueError):
            continue
        if math.isfinite(confidence) and 0 <= confidence <= 100:
            confidences.append(confidence / 100)
    text = "\n".join("".join(words) for words in lines.values())
    confidence = sum(confidences) / len(confidences) if confidences else None
    return text, confidence


def _finite(value: float, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")


def _decode(value: bytes | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return value.decode("utf-8", errors="replace")


def _diagnostic(stderr: bytes | str | None) -> str:
    return _decode(stderr).strip()[:500]


def _run(command: list[str], *, timeout: float, input_data: bytes | None = None, label: str) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(
            command,
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
            shell=False,
        )
    except subprocess.TimeoutExpired as error:
        raise PipelineError(f"{label} timed out after {timeout:g} seconds") from error
    except OSError as error:
        raise PipelineError(f"Could not run {label}: {error}") from error
    if result.returncode != 0:
        detail = _diagnostic(result.stderr)
        suffix = f": {detail}" if detail else ""
        raise PipelineError(f"{label} failed with exit code {result.returncode}{suffix}")
    return result


def _probe(ffprobe: str, video: Path, timeout: float) -> tuple[int, int, float]:
    command = [
        ffprobe,
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height:format=duration",
        "-of", "json",
        str(video),
    ]
    result = _run(command, timeout=timeout, label="ffprobe")
    try:
        data = json.loads(_decode(result.stdout))
        stream = data["streams"][0]
        width, height = int(stream["width"]), int(stream["height"])
        duration = float(data["format"]["duration"])
    except (KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise PipelineError("ffprobe returned invalid video dimensions or duration") from error
    if width <= 0 or height <= 0 or not math.isfinite(duration) or duration <= 0:
        raise PipelineError("Video must have positive dimensions and finite duration")
    return width, height, duration


def _which(name: str) -> str:
    executable = shutil.which(name)
    if executable is None:
        raise PipelineError(f"Required executable not found: {name}")
    return executable


def _version(executable: str, argument: str, timeout: float, label: str) -> str:
    result = _run([executable, argument], timeout=timeout, label=f"{label} version check")
    return _decode(result.stdout).splitlines()[0][:200] if _decode(result.stdout).splitlines() else "unknown"


def _sha256(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as model:
        while chunk := model.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def _sample_times(start: float, end: float, interval: float) -> list[float]:
    times: list[float] = []
    index = 0
    while True:
        timestamp = start + index * interval
        if not timestamp < end:
            return times
        times.append(timestamp)
        index += 1


def _ffmpeg_command(ffmpeg: str, video: Path, timestamp: float, roi: ROI | None) -> list[str]:
    command = [ffmpeg, "-v", "error", "-ss", f"{timestamp:.9f}", "-i", str(video), "-frames:v", "1"]
    if roi is not None:
        command.extend(["-vf", f"crop={roi.width}:{roi.height}:{roi.x}:{roi.y}:exact=1"])
    command.extend(["-f", "image2pipe", "-vcodec", "png", "pipe:1"])
    return command


def run_pipeline(
    video_path: str | os.PathLike[str],
    output_dir: str | os.PathLike[str],
    model_dir: str | os.PathLike[str],
    *,
    start: float = 0.0,
    end: float,
    interval: float = 0.5,
    roi: ROI | None = None,
    psm: int = 6,
    timeout: float = 60.0,
) -> dict[str, Any]:
    """Sample local video and write crops, observations, segments, and review Markdown.

    The destination must not already exist. All text is OCR output requiring
    human review; requested sample timestamps are approximate display times.
    """
    _finite(start, "start")
    _finite(end, "end")
    _finite(interval, "interval")
    _finite(timeout, "timeout")
    if interval <= 0:
        raise ValueError("interval must be positive")
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    if not isinstance(psm, int) or isinstance(psm, bool) or not 0 <= psm <= 13:
        raise ValueError("psm must be an integer from 0 through 13")

    video = Path(video_path)
    output = Path(output_dir)
    model = Path(model_dir)
    if not video.is_file():
        raise PipelineError(f"Video file does not exist: {video}")
    if output.exists():
        raise PipelineError(f"Output directory already exists: {output}")
    if not model.is_dir() or not (model / "jpn.traineddata").is_file():
        raise PipelineError(f"Japanese Tesseract model not found: {model / 'jpn.traineddata'}")

    ffprobe, ffmpeg, tesseract = (_which(name) for name in ("ffprobe", "ffmpeg", "tesseract"))
    width, height, duration = _probe(ffprobe, video, timeout)
    if not (0 <= start < end <= duration):
        raise ValueError(f"require 0 <= start < end <= video duration ({duration:g})")
    roi = validate_roi(roi, width, height)
    ffmpeg_version = _version(ffmpeg, "-version", timeout, "ffmpeg")
    tesseract_version = _version(tesseract, "--version", timeout, "tesseract")
    model_hash, model_size = _sha256(model / "jpn.traineddata")
    timestamps = _sample_times(start, end, interval)

    try:
        output.mkdir(parents=True, exist_ok=False)
        crops_dir = output / "crops"
        crops_dir.mkdir()
    except OSError as error:
        raise PipelineError(f"Could not create fresh output directory: {error}") from error

    started = time.monotonic()
    observations: list[Observation] = []
    for index, timestamp in enumerate(timestamps, start=1):
        frame = _run(
            _ffmpeg_command(ffmpeg, video, timestamp, roi),
            timeout=timeout,
            label=f"ffmpeg sample {index}",
        )
        png = frame.stdout if isinstance(frame.stdout, bytes) else _decode(frame.stdout).encode("utf-8")
        if not png:
            raise PipelineError(f"ffmpeg sample {index} returned an empty frame")
        relative_crop = Path("crops") / f"sample_{index:06d}.png"
        (output / relative_crop).write_bytes(png)
        tesseract_command = [
            tesseract, "stdin", "stdout",
            "--tessdata-dir", str(model),
            "-l", "jpn",
            "--oem", "1",
            "--psm", str(psm),
            "-c", "tessedit_create_tsv=1",
        ]
        result = _run(tesseract_command, timeout=timeout, input_data=png, label=f"tesseract sample {index}")
        text, confidence = parse_tesseract_tsv(_decode(result.stdout))
        observations.append(Observation(timestamp, text, relative_crop.as_posix(), confidence))

    segments = group_observations(observations, interval, sample_end=end)
    observation_data = {
        "review_status": "all_text_requires_review",
        "timing": "requested_sample_times_approximate_not_audio_alignment",
        "observations": [asdict(observation) for observation in observations],
    }
    (output / "observations.json").write_text(
        json.dumps(observation_data, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    (output / "segments.json").write_text(segments_to_json(segments) + "\n", encoding="utf-8")
    (output / "review.md").write_text(segments_to_markdown(segments), encoding="utf-8")
    runtime = time.monotonic() - started
    metadata = {
        "review_status": "all_text_requires_review",
        "video_name": video.name,
        "video_duration_seconds": duration,
        "frame_dimensions": {"width": width, "height": height},
        "parameters": {
            "start": start,
            "end": end,
            "interval": interval,
            "roi": asdict(roi) if roi is not None else None,
            "psm": psm,
            "oem": 1,
        },
        "tools": {"ffmpeg": ffmpeg_version, "tesseract": tesseract_version},
        "model": {"name": "jpn.traineddata", "sha256": model_hash, "bytes": model_size},
        "sample_count": len(observations),
        "segment_count": len(segments),
        "runtime_seconds": runtime,
        "timing_note": "requested sample timestamps are approximate display times, not audio alignment",
    }
    (output / "run.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "sample_count": len(observations),
        "segment_count": len(segments),
        "frame_dimensions": metadata["frame_dimensions"],
        "runtime_seconds": runtime,
        "output_dir": str(output),
    }
