# Sample-prototype evaluation

This is a local exploratory baseline, not an OCR reliability certification. The full-frame run covered 00:00–03:34 at 0.5-second sampling with no guessed region of interest. Outputs containing transcriptions, OCR text, and crops remain in ignored `.local/` directories; this document reports aggregates only.

## Reproduce locally

Set `PROJECT` to the repository root and `VIDEO`/`REFERENCE` to the approved local inputs. Do not copy private paths or transcriptions into repository documentation.

```sh
uv run --directory apps/server --offline --no-python-downloads --python /usr/bin/python3 python -m kotoba_capture \
  --video "$VIDEO" --model-dir "$PROJECT/.local/tessdata" \
  --output "$PROJECT/.local/runs/t3-fullframe" \
  --start 0 --end 214 --interval 0.5 --psm 6 --timeout 1200

uv run --directory apps/server --offline --no-python-downloads --python /usr/bin/python3 python -m kotoba_capture.evaluation \
  --reference "$REFERENCE" --run-dir "$PROJECT/.local/runs/t3-fullframe" \
  --output-dir "$PROJECT/.local/evaluations/t3-fullframe" --start 0 --end 214
```

Each output directory must be new. The full evaluation JSON contains per-window reference and OCR text; keep it local and do not print or upload it. The CLI emits aggregate metrics only.

## Protocol

- The reference parser reads only the Japanese Transcription and Timestamp columns. Untimed populated rows are counted and skipped; translation/vocabulary columns are ignored. Rows must be ordered, populated timestamps must parse, and only fully contained windows in `[0, 214]` are selected.
- Evaluation text uses Unicode NFKC followed by removal of all whitespace. Punctuation is preserved; no Japanese semantic correction or confidence weighting is applied.
- For each half-open timestamp window `[start, end)`, choose the most frequent normalized sampled OCR string, including blank strings. The earliest sample wins ties. Manual reference text does not select the OCR sample; it is used only for subsequent scoring.
- Character error rate (CER) is Levenshtein insertions + deletions + substitutions divided by normalized reference characters. Corpus CER sums edits and reference characters over windows and can exceed 100%.
- The 10% per-window CER cutoff is a provisional diagnostic, not an approved quality guarantee. The proposed 95% phrase coverage goal is not measured as detection recall here.
- Missing windows, blank modal windows, exact modal matches, unassigned samples, raw observation count, and grouped segment count are diagnostics only. Unassigned observations are not classified as signage.

## Observed run

| Item | Result |
|---|---:|
| Evaluation interval | 0–214 s |
| Source video duration | 1068.301 s |
| Sampling | 0.5 s; timestamps strictly before 214 s |
| Frame/ROI | 1920×1080; full-frame, no ROI |
| Tesseract | 5.5.3, `--oem 1`, `--psm 6` |
| FFmpeg | n9.0.1 |
| Japanese model | tessdata_fast commit `87416418657359cb625c412a48b6e1d6d41c29bd`; SHA-256 `1f5de9236d2e85f5fdf4b3c500f2d4926f8d9449f28f5394472d9e8d83b91b4d`; 2,471,260 bytes |
| Sampling runtime | 337.49 s |
| Evaluation CLI runtime (repeat, fresh report directory) | 0.091 s |
| Sampled observations / crops | 428 / 428 |
| Crop storage | 584,504,711 bytes |
| Grouped segments | 425 |
| Reference table rows scanned / selected windows | 51 / 28 |
| Untimed populated rows skipped / outside-interval rows skipped | 22 / 0 |
| Empty table rows ignored | 1 |
| Normalized reference characters | 457 |

| Diagnostic | Result |
|---|---:|
| Windows with no samples / blank modal OCR | 0 / 2 |
| Exact modal-window matches | 0 / 28 |
| Windows at or below provisional 10% CER | 0 / 28 |
| Corpus edits / CER | 1,736 / 379.87% |
| Per-window CER, min / median / max | 60.00% / 333.85% / 1,657.14% |
| Windows above 100% CER | 22 / 28 |
| Samples outside reference windows | 54 / 428 |

The modal-window results are poor and do not meet the provisional 10% CER diagnostic. No 95% phrase-recovery claim is supported. The 54 samples outside reference windows are unassigned timing diagnostics, not confirmed signage or false positives.

## Interpretation and next step

A reference intervention can span changing subtitle screens, while this diagnostic selects one modal snapshot. Its CER can overstate error or miss text that appeared briefly; it is not subtitle detection recall or end-to-end segmentation precision. Coarse timestamps are not independently verified display boundaries. Signage, furigana contamination, reading order, timing, and export usefulness were not visually reviewed, and one sample does not establish behavior across background variants. Confidence scores remain uncalibrated engine heuristics.

Next bounded step: manually review local representative crops for the 28 timestamp windows, focusing on high-error/blank cases and timing boundaries, then decide whether a separately approved region/configuration experiment is justified. Do not infer OCR reliability or add preprocessing from these aggregate metrics alone.
