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

## Controlled upper-half ROI experiment

The user confirmed subtitle placement in the upper half and approved a parameter-only comparison. The only configuration change was ROI `0,0,1920,540`, preserving source resolution. The video interval, 0.5-second sampling, Tesseract OEM 1 / PSM 6, Japanese model, tool versions, reference, and scoring protocol remained unchanged. No source code was changed.

| Diagnostic | Full frame | Upper half |
|---|---:|---:|
| Crop dimensions | 1920×1080 | 1920×540 |
| Observations / crops | 428 / 428 | 428 / 428 |
| Grouped segments | 425 | 414 |
| Reference windows / normalized characters | 28 / 457 | 28 / 457 |
| Character edits | 1,736 | 788 |
| Corpus CER | 379.87% | 172.43% |
| Exact modal-window matches | 0 / 28 | 3 / 28 |
| Windows at or below provisional 10% CER | 0 / 28 | 4 / 28 |
| Blank modal windows / windows without samples | 2 / 0 | 1 / 0 |
| Samples unassigned to reference windows | 54 | 54 |
| Pipeline runtime | 337.49 s | 225.61 s |

Independent read-only verification reproduced both saved summaries and confirmed that ROI was the sole parameter change. All 428 upper-half PNG headers report 1920×540, crop links resolve, and the existing 26 tests pass. Original video/note size and modification times were unchanged; the model hash matched. Evaluation runtime was not separately measured for this experiment.

The upper-half crop improved the corpus diagnostic by 207.44 percentage points, but the output remains poor and does not establish reliable transcription. This comparison does not identify the remaining text as signage, prove that every subtitle was retained, or measure detection recall, precise timing, furigana separation, or reading order. No visual review was performed by the agent.

Private run outputs are under `.local/runs/upper-half-roi/`; detailed comparison and aggregate summaries are under `.local/evaluations/upper-half-roi/`. To reproduce, use the existing commands above with new output directories and add `--roi 0,0,1920,540` to the pipeline command.

## Controlled tighter-band experiment

The user explicitly authorized visual inspection of exactly three existing upper-half crops at approximately 6, 80, and 143 seconds. In those images, subtitle boxes start around y=80; single-line boxes end near y=220, while the three-line announcement reaches about y=460 and almost the full frame width. Furigana appears above the main characters. These observations are specific to those three samples, not a guarantee across the video or other subtitle styles.

The approved next run changed only ROI to `0,60,1920,420`, retaining the full-width band from y=60 to y=480 with margins. The same sample, model, tools, interval, PSM/OEM, reference, and diagnostic protocol were retained. No additional images were uploaded or rendered, and no extraction code was changed.

| Diagnostic | Full frame | Upper half | Tighter band |
|---|---:|---:|---:|
| Character edits / reference characters | 1,736 / 457 | 788 / 457 | 771 / 457 |
| Corpus CER | 379.87% | 172.43% | 168.71% |
| Exact modal-window matches | 0 / 28 | 3 / 28 | 0 / 28 |
| Windows at or below provisional 10% CER | 0 / 28 | 4 / 28 | 0 / 28 |
| Blank modal windows / windows without samples | 2 / 0 | 1 / 0 | 4 / 0 |
| Grouped segments / observations | 425 / 428 | 414 / 428 | 412 / 428 |
| Pipeline runtime | 337.49 s | 225.61 s | 195.15 s |

All runs used the same 28 approximate reference windows and had 54 samples unassigned to those windows. Tighter-band per-window CER min/median/max was 63.16% / 124.55% / 533.33%. Its 428 crops use 218,958,238 bytes. Evaluation runtime was not separately measured.

Independent verification reproduced all three saved summaries, confirmed ROI as the sole configuration difference, checked all 428 band PNG headers at 1920×420 and all 412 segment crop links, and passed the existing 26 tests. Original input size/mtime and model hash checks passed in the run; previous artifacts remain intact.

This is not an unambiguous improvement: corpus CER fell by only 3.72 percentage points versus the upper-half run, while all three exact matches and four threshold-qualified windows disappeared and blank modal windows increased. Do not adopt this tighter band as a demonstrated improvement. The comparison does not identify whether the changes came from clipping, furigana, background content, page segmentation, or modal selection; no such cause or full subtitle retention was independently verified.

Private artifacts are under `.local/runs/subtitle-band-roi/` and `.local/evaluations/subtitle-band-roi/`. Reproduction uses the commands above with new output destinations and `--roi 0,60,1920,420`.

## Isolated spatial association v3 regression

A completed bounded correction now requires rectangle intersection and at least 0.35 selected connected-component closed-mask support during caption association. This replaces trusting broad rectangle overlap or unconditional near-Y proximity; it adds no threshold sweep and preserves the existing configuration values.

| Known-data regression diagnostic | Result |
|---|---:|
| Cases / positive references | 23 / 21 |
| Complete-output edits / characters | 0 / 477 |
| Positive outputs exact | 21 / 21 |
| Known negatives empty | 2 / 2 |
| Synthetic tests | 20 passed |

This is a saved 23-case REGRESSION only: two known cases improved, nineteen were unchanged, and frozen v2 remains intact. No OCR ran for v3, and it does not adopt a production, server, or default behavior.

References were assistant-transcribed and remain marked `userVerified=false`; limited human observations do not verify the full corpus. These results are not fresh validation or a general zero-error guarantee. The known negatives cover only prior designated cases; human review limitations and unsupported sparse, style, interval, or non-blue layouts remain.

Any Git checkpoint covers this documentation only; ignored experimental runtime/source remains uncommitted and is not experiment code in the checkpoint.

Next bounded step: the known geometry correction is complete. A separately authorized fresh negative/style/interval validation and human review are still required before claiming broader usefulness. Do not launch new OCR or make further configuration, model, preprocessing, production, server, or default changes automatically.
