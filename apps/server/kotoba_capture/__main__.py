"""Development CLI for bounded local OCR sampling runs."""

from __future__ import annotations

import argparse
import json
import sys

from .pipeline import PipelineError, ROI, run_pipeline


def _roi_argument(value: str) -> ROI:
    try:
        parts = [int(part) for part in value.split(",")]
    except ValueError as error:
        raise argparse.ArgumentTypeError("ROI must be x,y,width,height integers") from error
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("ROI must be x,y,width,height integers")
    return ROI(*parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sample local video frames and export human-reviewed Japanese OCR")
    parser.add_argument("--video", required=True, help="local video file")
    parser.add_argument("--model-dir", required=True, help="directory containing jpn.traineddata")
    parser.add_argument("--output", required=True, help="new output directory for this run")
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--end", type=float, required=True, help="exclusive sample limit in seconds")
    parser.add_argument("--interval", type=float, default=0.5, help="exploratory sampling interval in seconds")
    parser.add_argument("--roi", type=_roi_argument, help="original-resolution pixel crop x,y,width,height")
    parser.add_argument("--psm", type=int, default=6, help="Tesseract page segmentation mode (0-13)")
    parser.add_argument("--timeout", type=float, default=60.0, help="per-subprocess timeout in seconds")
    args = parser.parse_args(argv)
    try:
        summary = run_pipeline(
            args.video,
            args.output,
            args.model_dir,
            start=args.start,
            end=args.end,
            interval=args.interval,
            roi=args.roi,
            psm=args.psm,
            timeout=args.timeout,
        )
    except (PipelineError, ValueError) as error:
        print(f"kotoba-capture: {error}", file=sys.stderr)
        return 2
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
