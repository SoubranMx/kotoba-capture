"""Deterministic primitives and local sampling for subtitle review."""

from .core import Observation, Segment, group_observations, normalize_text
from .pipeline import PipelineError, ROI, parse_tesseract_tsv, run_pipeline, validate_roi

__all__ = [
    "Observation",
    "PipelineError",
    "ROI",
    "Segment",
    "group_observations",
    "normalize_text",
    "parse_tesseract_tsv",
    "run_pipeline",
    "validate_roi",
]
