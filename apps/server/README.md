# Kotoba Capture sampled-text core

This dependency-free Python core turns sampled OCR observations into approximate, reviewable text segments. A local development runner samples video with FFmpeg/Tesseract; there is no product UI/API or audio alignment.

## Quick check

From the repository root, run:

```sh
uv run --directory apps/server --offline --no-python-downloads --python /usr/bin/python3 python -m unittest discover -s tests -v
```

## Core contract

- `Observation(timestamp, text, crop_path=None, confidence=None)` represents one sampled result. Confidence stays unknown when omitted.
- `normalize_text(text)` uses Unicode NFKC and collapses whitespace only for equivalence; segment output retains the representative observation's original text.
- `group_observations(observations, sampling_interval, sample_end=None)` merges only consecutive equivalent nonblank samples whose adjacent gap is no larger than the interval, allowing a relative `1e-12` tolerance for floating-point boundary noise. Blank samples, changed text, and materially larger gaps split groups. Each segment prefers the first sample with a crop and keeps that sample's confidence (unknown if absent); when no crop exists, the first supplied confidence is retained. Its approximate end extends one interval past the last sample, optionally clipped to `sample_end`. If `sample_end` equals the final sample timestamp, clipping yields a zero-duration point segment.
- `segments_to_json(segments)` and `segments_to_markdown(segments)` provide local-review exports. All text is marked as requiring review; intervals are not audio alignment. Markdown OCR text, including both angle brackets, is escaped as literal text; crop paths are local relative links.

The core does not infer missing characters, extract furigana, or make accuracy claims. The automated tests use synthetic inputs; the authorized bounded smoke and full-frame evaluation process local media and compare against the read-only manual note without external transfer.

## Local sampling runner

The callable entry point is `kotoba_capture.pipeline.run_pipeline(video_path, output_dir, model_dir, *, start, end, interval=0.5, roi=None, psm=6, timeout=60)`. It probes duration/frame dimensions, validates the optional original-resolution pixel ROI, samples timestamps strictly before `end`, and invokes local FFmpeg and Tesseract with argument lists and per-process timeouts. Japanese OCR uses Tesseract LSTM (`--oem 1`); confidence is the mean of available engine word scores normalized to 0–1, not a correctness probability.

A development CLI is available with `python -m kotoba_capture`. For example:

```sh
uv run --directory apps/server --offline --no-python-downloads --python /usr/bin/python3 python -m kotoba_capture \
  --video /path/to/video.webm --model-dir /path/to/tessdata \
  --output /path/to/new-run --start 0 --end 1.5 --interval 0.5
```

`--end` is required; the runner does not assume a 214-second duration. Omit `--roi` for the full-frame baseline or pass `--roi x,y,width,height` in source pixels. FFmpeg uses `exact=1` so odd ROI sizes and offsets are not rounded for subsampled video. Each destination must be new. A run writes every sampled PNG under `crops/`, every raw OCR result to `observations.json`, grouped `segments.json`, review `review.md`, and parameter/tool/model/runtime `run.json`. A blank OCR result remains an observation and breaks groups. Outputs remain local and require human review; timestamps are requested display samples, not audio alignment. No model auto-download occurs in the runner. The approved `jpn.traineddata` asset, license, and SHA-256 provenance record are kept under the ignored repository `.local/tessdata/` directory.

## Reference evaluation

Set `PROJECT` to the repository root and `VIDEO`/`REFERENCE` to the approved local inputs. Run the local pipeline with a new output directory:

```sh
uv run --directory apps/server --offline --no-python-downloads --python /usr/bin/python3 python -m kotoba_capture \
  --video "$VIDEO" --model-dir "$PROJECT/.local/tessdata" \
  --output "$PROJECT/.local/runs/new-run" --start 0 --end 214 --interval 0.5 --psm 6
```

Then run `python -m kotoba_capture.evaluation` with a local Markdown reference, that pipeline run directory, and another new output directory:

```sh
uv run --directory apps/server --offline --no-python-downloads --python /usr/bin/python3 python -m kotoba_capture.evaluation \
  --reference "$REFERENCE" --run-dir "$PROJECT/.local/runs/new-run" \
  --output-dir "$PROJECT/.local/evaluations/new-evaluation" --start 0 --end 214
```

The evaluator reads only the Japanese Transcription and Timestamp columns; untimed vocabulary rows are counted and skipped. Its sample protocol and aggregate-only results are in [the prototype evaluation guide](../../docs/prototype-evaluation.md).

The evaluator applies Unicode NFKC and removes whitespace while preserving punctuation. It chooses the most frequent normalized OCR string, including blanks, inside each half-open timestamp window; the earliest sample wins ties. Character error is summed Levenshtein edits divided by reference characters and may exceed 100%. The 10% CER threshold is provisional. Detailed per-window reports contain private reference/OCR text and must remain under ignored `.local/`; the CLI prints aggregate metrics only. This reference-assisted modal-snapshot diagnostic is not detection recall, and confidence is not used as a correctness probability.
