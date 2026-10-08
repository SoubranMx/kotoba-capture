"""Reference-assisted local OCR diagnostics; metrics do not measure detection recall."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import re
import sys
import unicodedata
from typing import Iterable, Sequence

from .core import Observation


PROVISIONAL_CER_THRESHOLD = 0.10


@dataclass(frozen=True)
class ReferenceWindow:
    start: float
    end: float
    text: str
    source_row: int


@dataclass(frozen=True)
class ReferenceData:
    windows: tuple[ReferenceWindow, ...]
    rows_seen: int
    untimed_rows_skipped: int
    outside_interval_rows_skipped: int
    evaluation_start: float = 0.0
    evaluation_end: float = 214.0


def normalize_evaluation_text(text: str) -> str:
    """Apply NFKC and remove whitespace; punctuation is deliberately preserved."""
    if not isinstance(text, str):
        raise TypeError("evaluation text must be a string")
    return "".join(unicodedata.normalize("NFKC", text).split())


def levenshtein_edits(reference: str, observed: str) -> int:
    """Return character-level insertion, deletion, and substitution distance."""
    if len(reference) < len(observed):
        reference, observed = observed, reference
    previous = list(range(len(observed) + 1))
    for row_index, reference_char in enumerate(reference, start=1):
        current = [row_index]
        for column_index, observed_char in enumerate(observed, start=1):
            current.append(min(
                current[-1] + 1,
                previous[column_index] + 1,
                previous[column_index - 1] + (reference_char != observed_char),
            ))
        previous = current
    return previous[-1]


def _finite(value: float, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")


def _bounds(start: float, end: float) -> None:
    _finite(start, "start")
    _finite(end, "end")
    if not 0 <= start < end:
        raise ValueError("evaluation bounds must satisfy 0 <= start < end")


def _markdown_cells(line: str) -> list[str]:
    text = line.strip()
    if not text.startswith("|"):
        return []
    cells: list[str] = []
    current: list[str] = []
    index = 1
    while index < len(text):
        char = text[index]
        if char == "\\" and index + 1 < len(text) and text[index + 1] == "|":
            current.append("|")
            index += 2
        elif char == "|":
            cells.append("".join(current).strip())
            current.clear()
            index += 1
        else:
            current.append(char)
            index += 1
    if current:
        cells.append("".join(current).strip())
    elif text.endswith("|") and cells:
        # The final delimiter closes the last cell rather than adding another.
        pass
    return cells


def _is_separator(cells: Sequence[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def _column_indexes(headers: Sequence[str]) -> tuple[int, int] | None:
    timestamps: list[int] = []
    transcriptions: list[int] = []
    for index, header in enumerate(headers):
        normalized = " ".join(unicodedata.normalize("NFKC", header).casefold().split())
        if "timestamp" in normalized or normalized in {"time", "時刻"}:
            timestamps.append(index)
        if (
            ("transcription" in normalized or "transcript" in normalized or "日本語" in normalized)
            and "translation" not in normalized
            and "翻訳" not in normalized
        ):
            transcriptions.append(index)
    if not timestamps and not transcriptions:
        return None
    if len(timestamps) != 1 or len(transcriptions) != 1:
        raise ValueError("reference table must have one Timestamp and one Japanese Transcription column")
    return transcriptions[0], timestamps[0]


def _parse_time(value: str) -> float:
    match = re.fullmatch(r"\s*(\d{1,3}:\d{2}(?::\d{2}(?:\.\d+)?)?)\s*", value)
    if match is None:
        raise ValueError("timestamp must use MM:SS or HH:MM:SS format")
    pieces = match.group(1).split(":")
    if len(pieces) == 2:
        minutes, seconds = int(pieces[0]), float(pieces[1])
        if seconds >= 60:
            raise ValueError("timestamp seconds must be below 60")
        return minutes * 60 + seconds
    hours, minutes, seconds = int(pieces[0]), int(pieces[1]), float(pieces[2])
    if minutes >= 60 or seconds >= 60:
        raise ValueError("HH:MM:SS minutes and seconds must be below 60")
    return hours * 3600 + minutes * 60 + seconds


def _parse_time_range(value: str) -> tuple[float, float]:
    parts = re.split(r"\s*(?:-|–|—|\bto\b)\s*", value.strip(), maxsplit=1, flags=re.IGNORECASE)
    if len(parts) != 2:
        raise ValueError("timestamp must contain a start and end time")
    start, end = _parse_time(parts[0]), _parse_time(parts[1])
    if start >= end:
        raise ValueError("timestamp window must have start before end")
    return start, end


def parse_reference_markdown(markdown: str, *, start: float = 0.0, end: float = 214.0) -> ReferenceData:
    """Parse the Japanese Transcription and Timestamp columns of a Markdown table."""
    _bounds(start, end)
    if not isinstance(markdown, str) or not markdown.strip():
        raise ValueError("reference note is empty")

    selected: list[tuple[int, str, str]] = []
    table_found = False
    lines = markdown.splitlines()
    index = 0
    while index + 1 < len(lines):
        headers = _markdown_cells(lines[index])
        separator = _markdown_cells(lines[index + 1])
        if headers and _is_separator(separator):
            columns = _column_indexes(headers)
            if columns is not None:
                if table_found:
                    raise ValueError("reference note contains multiple matching transcription tables")
                table_found = True
                text_index, time_index = columns
                index += 2
                while index < len(lines):
                    cells = _markdown_cells(lines[index])
                    if not cells:
                        break
                    if max(text_index, time_index) >= len(cells):
                        raise ValueError(f"reference table row {index + 1} has missing required cells")
                    selected.append((index + 1, cells[text_index], cells[time_index]))
                    index += 1
                continue
        index += 1
    if not table_found:
        raise ValueError("reference note has no Japanese Transcription/Timestamp table")

    windows: list[ReferenceWindow] = []
    untimed = 0
    outside = 0
    previous_start: float | None = None
    for source_row, text, timestamp in selected:
        text = text.strip()
        timestamp = timestamp.strip()
        if not text and not timestamp:
            continue
        if not timestamp:
            untimed += 1
            continue
        if not text or not normalize_evaluation_text(text):
            raise ValueError(f"timestamped reference row {source_row} has empty transcription")
        try:
            row_start, row_end = _parse_time_range(timestamp)
        except ValueError as error:
            raise ValueError(f"malformed timestamp in reference row {source_row}: {error}") from error
        if previous_start is not None and row_start < previous_start:
            raise ValueError(f"reference timestamps are out of order at row {source_row}")
        previous_start = row_start
        if row_start >= start and row_end <= end:
            windows.append(ReferenceWindow(row_start, row_end, text, source_row))
        else:
            outside += 1
    if not windows:
        raise ValueError("reference has no usable timestamped rows fully contained in the evaluation interval")
    return ReferenceData(tuple(windows), len(selected), untimed, outside, start, end)


def _validate_reference(reference: ReferenceData) -> None:
    if not isinstance(reference, ReferenceData) or not reference.windows:
        raise ValueError("evaluation requires at least one reference window")
    _bounds(reference.evaluation_start, reference.evaluation_end)
    previous_start: float | None = None
    for window in reference.windows:
        _finite(window.start, "reference start")
        _finite(window.end, "reference end")
        if (
            window.start < reference.evaluation_start
            or window.start >= window.end
            or window.end > reference.evaluation_end
        ):
            raise ValueError("reference windows must be positive and fully within the evaluation interval")
        if previous_start is not None and window.start < previous_start:
            raise ValueError("reference windows must be ordered")
        if not normalize_evaluation_text(window.text):
            raise ValueError("reference transcription must not be empty")
        previous_start = window.start


def evaluate_reference(
    reference: ReferenceData,
    observations: Iterable[Observation],
    *,
    segment_count: int,
    cer_threshold: float = PROVISIONAL_CER_THRESHOLD,
) -> dict[str, object]:
    """Compute per-window modal-sample CER diagnostics against a manual reference.

    The reference selects time windows only. Within each, the most frequent
    normalized OCR string is selected, with the earliest sample winning ties;
    reference text is used only afterward for scoring. This is not detection
    recall or end-to-end segmentation precision.
    """
    _validate_reference(reference)
    _finite(cer_threshold, "cer_threshold")
    if cer_threshold < 0:
        raise ValueError("cer_threshold must be nonnegative")
    if not isinstance(segment_count, int) or isinstance(segment_count, bool) or segment_count < 0:
        raise ValueError("segment_count must be a nonnegative integer")

    samples = list(observations)
    if not samples:
        raise ValueError("evaluation requires at least one OCR observation")
    previous_timestamp: float | None = None
    for observation in samples:
        if not isinstance(observation, Observation):
            raise TypeError("observations must contain Observation values")
        _finite(observation.timestamp, "observation timestamp")
        if not isinstance(observation.text, str):
            raise TypeError("observation text must be a string")
        if previous_timestamp is not None and observation.timestamp < previous_timestamp:
            raise ValueError("observations must be ordered by timestamp")
        previous_timestamp = observation.timestamp

    window_reports: list[dict[str, object]] = []
    total_edits = 0
    total_reference_characters = 0
    missing_windows = 0
    blank_modal_windows = 0
    exact_windows = 0
    at_or_below_threshold = 0
    assigned_sample_indices: set[int] = set()

    for window_index, window in enumerate(reference.windows, start=1):
        selected = [
            (index, observation)
            for index, observation in enumerate(samples)
            if window.start <= observation.timestamp < window.end
        ]
        assigned_sample_indices.update(index for index, _ in selected)
        reference_text = normalize_evaluation_text(window.text)
        if selected:
            modes: dict[str, tuple[int, int, str]] = {}
            for sample_index, observation in selected:
                key = normalize_evaluation_text(observation.text)
                if key in modes:
                    count, first_index, first_text = modes[key]
                    modes[key] = (count + 1, first_index, first_text)
                else:
                    modes[key] = (1, sample_index, observation.text)
            modal_key = min(modes, key=lambda key: (-modes[key][0], modes[key][1]))
            modal_text: str | None = modes[modal_key][2]
            observed_text = modal_key
            blank_modal = not modal_key
            missing = False
        else:
            modal_text = None
            observed_text = ""
            blank_modal = False
            missing = True
            missing_windows += 1
        if blank_modal:
            blank_modal_windows += 1
        edits = levenshtein_edits(reference_text, observed_text)
        cer = edits / len(reference_text)
        exact = edits == 0 and not missing
        if exact:
            exact_windows += 1
        if cer <= cer_threshold:
            at_or_below_threshold += 1
        total_edits += edits
        total_reference_characters += len(reference_text)
        window_reports.append({
            "window_index": window_index,
            "source_row": window.source_row,
            "start": window.start,
            "end": window.end,
            "reference_text": window.text,
            "modal_ocr_text": modal_text,
            "sample_count": len(selected),
            "missing_sample_window": missing,
            "blank_modal_window": blank_modal,
            "exact_match": exact,
            "edits": edits,
            "reference_characters": len(reference_text),
            "cer": cer,
        })

    outside_interval = sum(
        observation.timestamp < reference.evaluation_start or observation.timestamp >= reference.evaluation_end
        for observation in samples
    )
    unassigned = len(samples) - len(assigned_sample_indices)
    summary: dict[str, object] = {
        "evaluation_start": reference.evaluation_start,
        "evaluation_end": reference.evaluation_end,
        "reference_rows_seen": reference.rows_seen,
        "untimed_reference_rows_skipped": reference.untimed_rows_skipped,
        "reference_rows_outside_interval_skipped": reference.outside_interval_rows_skipped,
        "reference_window_count": len(reference.windows),
        "sample_count": len(samples),
        "segment_count": segment_count,
        "missing_sample_windows": missing_windows,
        "blank_modal_windows": blank_modal_windows,
        "exact_match_windows": exact_windows,
        "windows_at_or_below_threshold": at_or_below_threshold,
        "provisional_cer_threshold": cer_threshold,
        "corpus_edits": total_edits,
        "corpus_reference_characters": total_reference_characters,
        "corpus_cer": total_edits / total_reference_characters,
        "samples_outside_evaluation_interval": outside_interval,
        "samples_unassigned_to_reference_windows": unassigned,
    }
    return {
        "method": {
            "normalization": "Unicode NFKC then remove all whitespace; punctuation preserved",
            "sample_selection": "most frequent normalized OCR text per half-open reference window; earliest sample wins ties, including blank text",
            "cer_definition": "sum character-level Levenshtein edits divided by normalized reference characters",
            "threshold_note": "10% CER is a provisional diagnostic threshold, not an approved guarantee",
            "confidence_usage": "engine confidence is not used for sample selection or scoring and is not a calibrated probability",
            "interpretation_limit": "reference-assisted modal-snapshot text diagnostic, not detection recall or end-to-end segmentation precision",
        },
        "summary": summary,
        "windows": window_reports,
    }


def _read_run(run_directory: Path) -> tuple[list[Observation], int]:
    try:
        observations_data = json.loads((run_directory / "observations.json").read_text(encoding="utf-8"))
        segments_data = json.loads((run_directory / "segments.json").read_text(encoding="utf-8"))
        observations = [
            Observation(
                timestamp=item["timestamp"],
                text=item["text"],
                crop_path=item.get("crop_path"),
                confidence=item.get("confidence"),
            )
            for item in observations_data["observations"]
        ]
        segments = segments_data["segments"]
        if not isinstance(segments, list):
            raise TypeError("segments must be a list")
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise ValueError("run directory must contain valid observations.json and segments.json") from error
    return observations, len(segments)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate local OCR samples against timestamped Japanese transcription")
    parser.add_argument("--reference", required=True, help="local read-only Markdown reference")
    parser.add_argument("--run-dir", required=True, help="pipeline run with observations.json and segments.json")
    parser.add_argument("--output-dir", required=True, help="new directory for private full evaluation report")
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--end", type=float, default=214.0)
    args = parser.parse_args(argv)
    output = Path(args.output_dir)
    if output.exists():
        print("evaluation output directory must be new", file=sys.stderr)
        return 2
    try:
        markdown = Path(args.reference).read_text(encoding="utf-8")
        reference = parse_reference_markdown(markdown, start=args.start, end=args.end)
        observations, segment_count = _read_run(Path(args.run_dir))
        result = evaluate_reference(reference, observations, segment_count=segment_count)
        output.mkdir(parents=True, exist_ok=False)
        (output / "evaluation.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        (output / "summary.json").write_text(
            json.dumps(result["summary"], ensure_ascii=False, indent=2, allow_nan=False) + "\n",
            encoding="utf-8",
        )
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
        print(f"evaluation failed: {error}", file=sys.stderr)
        return 2
    # Never print private transcription or OCR content to the terminal.
    print(json.dumps(result["summary"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
