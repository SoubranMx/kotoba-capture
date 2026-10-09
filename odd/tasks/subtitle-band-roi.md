# Tighter subtitle-band ROI experiment

## Objective and rationale
Compare a narrower fixed subtitle band with preserved full-frame and upper-half runs. The user approved ROI `0,60,1920,420` after authorizing visual inspection of exactly three existing crops at 6, 80, and 143 seconds. These showed boxes starting near y=80, single-line boxes ending near y=220, and a nearly full-width three-line announcement reaching y=460. Margins were proposed; retention across all frames was not established. Furigana remains a separate concern.

## Authorization and scope
Use the existing uv-managed pipeline/evaluator. No source, model, dependency, PSM, UI/API, network, Obsidian, staging, commit, push, or merge changes. No additional image uploads; previous consent covered only the three named crops. Process the same read-only video/reference over 0–214 seconds at 0.5-second intervals with PSM 6/OEM 1 and the pinned Japanese model. Only ROI changes. Fresh private artifacts stay in ignored `.local/runs/subtitle-band-roi/` and `.local/evaluations/subtitle-band-roi/`; documentation and handoffs contain aggregate metrics only. Preserve all prior artifacts and uncommitted documentation.

## Tasks
- [x] B1: Execute the tighter-band pipeline/evaluation and validate samples, dimensions, links, inputs, model and configuration. Status: done. Route: one bounded worker. Evidence: 26 tests passed; 428 samples/crops at 1920×420; 412 segments; 195.15 seconds; model SHA matched; source size/mtime unchanged; only ROI changed; outputs ignored. Commit: not authorized.
- [x] B2: Independently reproduce the three-way comparison and document results/limits. Status: done. Route: read-only verifier, then inline single-file passive documentation update. Evidence: 26 tests passed independently; all saved summaries reproduced; all 428 crop headers and 412 segment links verified; parent documentation arithmetic/fence/path checks and git diff --check passed. Commit: not authorized.

## Method and acceptance checks
Parameter-only execution and passive docs have no meaningful RED; no behavior code changed. Run the same 28 approximate reference windows and 457 normalized characters through the existing modal-snapshot evaluator. Compare CER, exact and threshold-qualified matches, blanks, segments and runtime without claiming detection recall, exact timing, furigana separation, or signage classification. Preserve originals and baselines. A poor or ambiguous result is a valid experimental outcome, not a failed implementation check.

## Observed comparison
| Metric | Full frame | Upper half | Tighter band |
|---|---:|---:|---:|
| ROI | None | 0,0,1920,540 | 0,60,1920,420 |
| Character edits | 1,736 | 788 | 771 |
| Corpus CER | 379.87% | 172.43% | 168.71% |
| Exact / <=10% windows | 0 / 0 | 3 / 4 | 0 / 0 |
| Blank / missing windows | 2 / 0 | 1 / 0 | 4 / 0 |
| Segments / observations | 425 / 428 | 414 / 428 | 412 / 428 |
| Pipeline runtime | 337.49 s | 225.61 s | 195.15 s |

All runs share 54 samples unassigned to reference windows. Tighter-band min/median/max window CER is 63.16% / 124.55% / 533.33%; crop storage is 218,958,238 bytes. Model SHA-256: `1f5de9236d2e85f5fdf4b3c500f2d4926f8d9449f28f5394472d9e8d83b91b4d`. Source/model/tools and non-ROI parameters match. Evaluation runtime was not separately measured.

## Interpretation
The 3.72-percentage-point reduction in corpus CER is not a clear overall improvement: previous exact/threshold matches disappeared and blanks increased. Do not adopt the tighter band as a demonstrated improvement. Clipping, furigana, background content, page segmentation and modal selection remain possible causes, not established diagnoses. No new visual review or subtitle-retention proof was performed.

## Verification and delivery
Native ASSESS was unassessable because task files are untracked; its required independent-verifier path was followed. No new native source review for this parameter-only run and small passive documentation addition. Prior committed source approvals remain closed. Some verifier interfaces did not expose numeric exit codes; outcomes were recorded without inventing codes. Parent git diff --check and passive documentation checks passed. Existing baseline commits are d60ffa9 and 57b8a73 on feat/sample-prototype. No new commits, staging, push, cleanup or media uploads. Only docs/prototype-evaluation.md and the two experiment task documents have repository changes; local runtime outputs remain ignored.

## Pending checks and next step
Precise timing, signage/furigana/read-order classification, full subtitle retention and generalization remain unverified. Stop automatic ROI narrowing. Inspect a few existing failure cases to separate background contamination, furigana mixing and OCR/layout-selection issues before proposing another bounded experiment; no full rerun or PSM/preprocessing/engine/model change is authorized by this result alone.
