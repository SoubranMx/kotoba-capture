"""Small deterministic primitives for sampled OCR observations.

Text equivalence uses Unicode NFKC followed by collapsing all Unicode
whitespace runs to one ASCII space. Original text is never rewritten in output.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import PurePosixPath
from typing import Iterable
import unicodedata
from urllib.parse import quote


@dataclass(frozen=True)
class Observation:
    """OCR text sampled at a time, with optional local crop and confidence."""

    timestamp: float
    text: str
    crop_path: str | None = None
    confidence: float | None = None


@dataclass(frozen=True)
class Segment:
    """A consecutive group with an approximate sampled display interval."""

    start: float
    end: float
    text: str
    crop_path: str | None = None
    confidence: float | None = None


def normalize_text(text: str) -> str:
    """Return the conservative NFKC/whitespace key used only for grouping."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return " ".join(unicodedata.normalize("NFKC", text).split())


def _finite_number(value: float, name: str) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")


def _validate_observation(observation: Observation) -> None:
    if not isinstance(observation, Observation):
        raise TypeError("observations must contain Observation values")
    _finite_number(observation.timestamp, "timestamp")
    if not isinstance(observation.text, str):
        raise TypeError("observation text must be a string")
    if observation.crop_path is not None and not isinstance(observation.crop_path, str):
        raise TypeError("crop_path must be a string or None")
    if observation.confidence is not None:
        _finite_number(observation.confidence, "confidence")
        if not 0 <= observation.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")


def group_observations(
    observations: Iterable[Observation],
    sampling_interval: float,
    sample_end: float | None = None,
) -> list[Segment]:
    """Group only consecutive equivalent nonblank observations.

    A changed/blank observation or a gap materially larger than
    ``sampling_interval`` ends a group. A relative tolerance of 1e-12 absorbs
    floating-point subtraction noise at the interval boundary. Segment ends
    extend one interval after their final sample, clipped to ``sample_end``;
    clipping at the final sample can produce a zero-duration point segment.
    These are approximate display times, not audio alignment. The first sample
    with a crop is representative; if no crop exists, the first confidence
    sample supplies confidence. Missing confidence on a selected crop stays
    unknown.
    """
    _finite_number(sampling_interval, "sampling_interval")
    if sampling_interval <= 0:
        raise ValueError("sampling_interval must be positive")
    if sample_end is not None:
        _finite_number(sample_end, "sample_end")

    items = list(observations)
    previous_timestamp: float | None = None
    for item in items:
        _validate_observation(item)
        if previous_timestamp is not None and item.timestamp < previous_timestamp:
            raise ValueError("observation timestamps must be ordered")
        previous_timestamp = item.timestamp
    if sample_end is not None and items and sample_end < items[-1].timestamp:
        raise ValueError("sample_end must not precede the final observation")

    groups: list[Segment] = []
    current: list[Observation] = []
    current_key = ""

    def finish() -> None:
        if not current:
            return
        first, last = current[0], current[-1]
        representative = next((item for item in current if item.crop_path is not None), None)
        if representative is None:
            representative = next(
                (item for item in current if item.confidence is not None),
                first,
            )
        end = last.timestamp + sampling_interval
        if sample_end is not None:
            end = min(end, sample_end)
        groups.append(Segment(first.timestamp, end, first.text, representative.crop_path, representative.confidence))

    for item in items:
        key = normalize_text(item.text)
        if not key:
            finish()
            current.clear()
            current_key = ""
            continue
        if current:
            gap = item.timestamp - current[-1].timestamp
            exceeds_interval = gap > sampling_interval and not math.isclose(
                gap, sampling_interval, rel_tol=1e-12, abs_tol=0.0
            )
            if key != current_key or exceeds_interval:
                finish()
                current.clear()
        if not current:
            current_key = key
        current.append(item)
    finish()
    return groups


def segments_to_json(segments: Iterable[Segment]) -> str:
    """Serialize segments as UTF-8-friendly JSON with explicit review status."""
    payload = {
        "review_status": "all_text_requires_review",
        "timing": "approximate_sampled_display_intervals_not_audio_alignment",
        "segments": [asdict(segment) for segment in segments],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False)


def _escape_markdown_text(text: str) -> str:
    escaped = "".join("\\" + char if char in r"\\`*_{}[]()#+-.!|<>~" else char for char in text)
    return escaped.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "  \n")


def _format_time(seconds: float) -> str:
    milliseconds = round(seconds * 1000)
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def segments_to_markdown(segments: Iterable[Segment]) -> str:
    """Render local-review Markdown without interpreting OCR text as markup."""
    lines = ["# Sampled OCR review", "", "All text requires review. Times are approximate sampled display intervals, not audio alignment.", ""]
    for index, segment in enumerate(segments, start=1):
        lines.append(f"## {index}. {_format_time(segment.start)}–{_format_time(segment.end)}")
        lines.append("")
        lines.append(_escape_markdown_text(segment.text))
        if segment.crop_path is not None:
            path = PurePosixPath(segment.crop_path).as_posix()
            lines.extend(["", f"[Representative crop]({quote(path, safe='/:')})"])
        lines.append("")
    return "\n".join(lines)
