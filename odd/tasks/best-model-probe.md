# Pinned best-model two-PNG probe

## Objective
Test whether the accuracy-oriented Japanese tessdata_best model improves the existing 24-second crop pair, changing only the trained model. This is a bounded diagnostic, not a general accuracy claim or pipeline-default change.

## Initial M1/M2 authorization and scope
The user explicitly approved downloading the Japanese model and comparing only these existing PNGs:
- `.local/runs/upper-half-roi/crops/sample_000049.png`
- `.local/runs/subtitle-band-roi/crops/sample_000049.png`

Use CPU, Japanese language, OEM 1 and PSM 6 with the existing TSV parser. Do not repeat PSM 11, process video/other images, add preprocessing, install dependencies, modify extraction code or upload private media/text. Preserve originals, all existing runs and the fast model. No staging, commits, push or publishing authorized. New model/license/provenance files stay under ignored `.local/models/tessdata-best-jpn-e12c65a/`; this document and its full memory mirror are progress records only. OCR text/TSV remain local process memory; handoffs contain numerical aggregates only.

## Tasks
- [x] M1: Acquire and verify the pinned Japanese model, license and provenance. Status: done. Route: bounded worker; only the three authorized ignored files created. Checks passed: exact bytes/Git blob identity, SHA-256/provenance/license agreement, ignored paths, unchanged inputs/fast model/repository state and git diff --check. Commit: not authorized.
- [x] M2: Independently verify model provenance and compare exactly two new PSM 6 OCR results to stored fast-model observations. Status: done. Route: read-only verifier. Checks passed: independent pinned model/license/provenance inventory and identities, unchanged images/fast model, both Tesseract return codes 0, whole-output scoring and mapped boxes, postflight integrity and git diff --check. Commit: not authorized.
- [x] M3: Compare three existing upper-half frames against frame-aligned visual references with the pinned best model, OEM 1 and PSM 6. Status: diagnostic completed; usability gate failed. Route: parent visual annotation and bounded read-only verifier. Exactly three new OCR calls returned 0; inputs/models/references/stored observations unchanged; ignore/status/diff checks passed. No source behavior changed. Commit: not authorized.

## Pinned acquisition
Repository: https://github.com/tesseract-ocr/tessdata_best
Revision: `e12c65a915945e4c28e237a9b52bc4a8f39a0cec`
Model: `jpn.traineddata`
Expected bytes: 14,330,109
Expected Git blob SHA-1: `d2a8eab80ba3aba7654ac789b82f70b64d1cf051` (not a file SHA-256).
Repository license verified via public GitHub metadata: Apache-2.0. Obtain LICENSE from the same revision. Compute file SHA-256 after download and retain provenance. Never overwrite an existing destination.

## Baseline and scoring
The same approximate reference window #5, 24–30 seconds, has 16 normalized reference characters. Existing fast-model PSM 6 outputs: upper-half 16 characters / 12 fragments / 0 edits / 0% CER; band 1 character / 1 fragment outside the subtitle box / 16 edits / 100% CER. Score the whole parsed output with existing NFKC/whitespace normalization and edit distance. Geometry is diagnostic, not permission to choose a best line using reference text. Confidence is uncalibrated.

The user-authorized visual comparison showed the complete subtitle and furigana retained in both images. Approximate original-frame blue rectangle is x=408–1512, y=81–220; band coordinates map with y+60. Presence of recognized boxes alone is not a successful transcription or detection-recall measurement.

## Checks and limits
No behavior code changes, so meaningful test-first RED/GREEN does not apply; use provenance/integrity and functional two-image checks. Do not rerun the full video or test suite without need. Baseline output/reference text stays private. Success must reduce the band's full-output error without concealing regressions in the exact upper-half result; a negative experimental result still completes the diagnostic if execution checks pass. Any varied validation set needs separate approval. If the stronger model does not help, stop Tesseract tuning rather than start another sweep.

## Initial repository state
Modified docs/prototype-evaluation.md; untracked odd/tasks/subtitle-band-roi.md, odd/tasks/upper-half-roi.md and unrelated .codegraph/. Preserve all. Model target and task document were absent; model path is ignored.

## Evidence and next step
M1 acquisition completed: model SHA-256 `36bdf9ac823f5911e624c30d0553e890b8abc7c31a65b3ef14da943658c40b79`; license SHA-256 `a6cba85bc92e0cff7a450b1d873c0eaa2e9fc96bf472df0247a26bec77bf3ff9`. Parent read back provenance and matched the pinned metadata. Input PNG hashes: upper-half `b8dde99098fe7421b26ad5b618270d43dc69501bca2f2b68c66187e230ed0922`; band `2641096da2902211a97f1a5dd39800066f74607773406f426fcb3ca000750bab`. The fast model hash remained unchanged.

Historical failed check: an initial multi-path git check-ignore -q invocation was rejected (exit 128); per-file -q and descriptive checks then passed (exit 0). git diff --check and git status checks passed. RED/GREEN is not applicable to data acquisition; test-first is not governed by activation of a toggle.

Native ASSESS was unavailable because untracked paths require an explicit declaration; its read-only plan treats this as high risk and requires an independent verifier, which M2 supplied. No source behavior changed and no native source review was opened.

## Observed M2 result
| Same 24-second frame / PSM 6 model | Normalized characters | Fragments / lines | Words inside / outside approximate subtitle box | Whole-output edits / CER |
|---|---:|---:|---:|---:|
| Upper-half fast | 16 | 12 / 1 | 12 / 0 | 0 / 0% |
| Upper-half best | 16 | 12 / 1 | 12 / 0 | 0 / 0% |
| Band fast | 1 | 1 / 1 | 0 / 1 | 16 / 100% |
| Band best | 22 | 18 / 3 | 13 / 5 | 7 / 43.75% |

Best-model OCR runtimes were 0.195 seconds (upper-half) and 0.219 seconds (band); both Tesseract processes returned 0. These are small single-image timings, not throughput estimates. The upper-half raw and normalized output exactly matched the stored fast-model result. Band errors fell by nine edits but outside-box fragments and seven remaining edits prevent a correct-transcription claim. Known mean confidence was 91.39% and 62.67%; neither is a calibrated probability.

Independent verification confirmed exactly the three expected model-directory files, pinned model and license checksums, preserved image/fast-model identities and unchanged repository status. No OCR text/TSV was printed or saved; no other image or mode was tested. Outer check numeric exit codes were not exposed; outcomes were recorded without inventing them. Parent model SHA-256, CER arithmetic, task completion-marker and fence-balance checks passed (exit 0); git diff --check also passed.

## Next step and remaining limits
The initial probe covers two crops of one frame, not two independent subtitle examples. Keep existing defaults and baseline; the best model is not adopted as a default.

## Approved M3 follow-up and acceptance target
The user asked to continue through bounded local cycles until usable, chose near-ready transcription, and explicitly permitted visual inspection of images originating anywhere under .local/. No video/other-file uploads, dependency installations or new-engine downloads are implicit. Next local unit uses only existing upper-half crops sample_000013.png (6s), sample_000161.png (80s) and sample_000287.png (143s), one best-model OCR call per image, unchanged settings, no new media extraction.

Parent re-inspected these permitted images and prepares `.local/evaluations/best-model-three-frame/references.json`: subtitle main text visually transcribed by the assistant, excluding pronunciation annotations and unrelated signage, with punctuation retained. These are aligned to the actual images, not window-modal snapshots; they are not user-verified ground truth. Compare both stored fast observations and new full best outputs against these same references. Private text stays local and is not included in task docs or Engram.

Usability target is <=10% corpus CER on a fixed varied set of aligned references, no complete subtitle omission, and no spurious output in designated subtitle-free examples. The current three frames are all blue-box positives; they do not cover gray/no-background cases or negatives and cannot establish final acceptance, even if scores pass. No full video run, adopted defaults, detector implementation or new engine setup is authorized by M3. Additional experiments stay bounded; ask before installations or weight acquisitions. M3 evidence is now observed. The diagnostic task is complete; the user's usability goal remains unmet.

## Observed aligned M3 result
| Timestamp | Reference characters | Stored fast edits / CER | Best edits / CER |
|---|---:|---:|---:|
| 6s | 10 | 16 / 160% | 242 / 2,420% |
| 80s | 20 | 7 / 35% | 1,519 / 7,595% |
| 143s | 66 | 59 / 89.39% | 35 / 53.03% |
| Corpus | 96 | 82 / 85.42% | 1,796 / 1,870.83% |

The best model's 80-second output includes one 1,533-character fragment outside the approximate caption box. Its content and internal cause were not inspected; do not infer that the subtitle itself has this length. All three new outputs are nonblank, but this does not prove subtitle retention. Exactly three Tesseract invocations returned 0; their times were 0.763, 0.601 and 0.642 seconds. All references remain assistant-transcribed/userVerified:false. Model/input/reference/observation hashes, sizes and mtimes were unchanged. Outer verification numeric exit codes were unavailable, not invented.

## Blocker and next decision
The <=10% near-ready goal fails even on this limited positive set; negative, gray and no-background gates remain untested. Do not adopt tessdata_best or continue blind model/PSM sweeps. Recommend a separately authorized isolated CPU PaddleOCR detector-plus-recognizer experiment on at most eight existing local frames, using a frozen aligned set including subtitle-free cases where available. PaddleOCR detects text, not semantic subtitle identity; candidate selection must be evaluated separately, not cherry-picked by reference. New dependency/Python runtime/model downloads require explicit approval. No extraction code, project Python policy, defaults, existing runs or UI/API changes are approved by this recommendation.
