# Fresh frozen-v3 validation

## Objective and authorization
User approved a new local OCR validation of frozen v3, including caption positives, negatives, numbers and differing layouts/styles where actually available. No selector tuning, downloads, network, remote operations, defaults or product changes. Preserve all prior evidence. Private media, references, predictions and detailed reports stay under ignored `.local/`.

## Scope and method
Use the existing local video after the previously sampled first 214 seconds. Extract 24 upper-half frames at 230 + 36k seconds, k=0..23 (last 1058s). Images and references were inspected/transcribed before OCR. The original eight-positive/four-negative coverage gate found no negatives. User explicitly approved evaluating twelve fresh positives instead, leaving negative/non-blue coverage pending. Select score-independently using all numeric cases, the three-row case, representative two-row cases and remaining temporal coverage; document the rule before predictions. All references remain `userVerified=false`.

Positive-only acceptance: complete-output character error strictly below 10% and no complete positive omissions. Negative false-positive rate and non-blue acceptance are unmeasured, not passed. Report individual/layout results so a pooled score cannot conceal poor cases. References are assistant-transcribed, not human-verified ground truth.

## Tasks and routing
- [x] F0: Read-only feasibility. Delegated explorer found 1068.301s local source; every existing 0–213.5s crop already had baseline OCR. Old runner pins v2/eight positives and cannot validate this batch unchanged.
- [x] F1: Extract/inspect 24 new images and freeze twelve-positive-only batch after explicit scope approval. Selected times: 230,302,374,446,482,590,662,734,806,878,1022,1058 seconds. Includes all three numeric cases, sole three-row case, first/last two-row cases and temporal endpoints; fill by maximum minimum timestamp distance with earlier ties, deduplicate/order chronologically. No OCR-score selection. Route: delegated writer, preparation/new private artifacts trigger.
- [x] F2: Isolated v3 harness/freeze complete. Initial missing-module RED exit1; old harness behavioral RED23tests/22errors exit1; GREEN25tests exit0, independently repeated25pass. Genuine pinned no-ML preflight exit0 independently, 117 protected identities. Route: delegated writer/verifier; new logic/multiple nontrivial files and independent checking trigger.
- [x] F3: Twelve once-only predictions completed exit0, one initialization, 88.57s, maximumRSS1512972KiB. Independent no-OCR replay/scoring exit0, all twelve outputs identical,117 protected identities unchanged. Acceptance FAILED:75/230edits=32.61%CER,8/12exact,2literalemptyoutputs plus one nonempty but entirely lost caption. No retry/tuning. Route: delegated execution/verifier; functional proof trigger.
- [x] F4: Report aggregate failure/limits and four frame locators, preserve private detailed reports, update mirror. Parent spotcheck verified aggregate tuple and all twelve completed ledger calls; Git diff-check passed. Route: inline bounded synthesis. Test completion is not product acceptance.

## Allowed surfaces
New private artifacts only under `.local/ocr-probes/paddleocr-cpu/caption-selector-v3-fresh/`: README.md, runner.py, tests/test_runner.py, dataset/*.json, frames/*.png and results/*, narrowed per delegation. Parent owns this document and mirror `odd/caption-selector-v3-fresh/tasks`. Existing v3/v2/runner/models/data/reports are read-only.

## Checks and preservation
Existing offline Python/Paddle environment and explicitly installed local models only. Record command exit status and prediction count; fail closed on manifest/hash drift before ML import/init/predict. Keep exact source/model/image identities before and after execution. Model confidence is not correctness probability. Public tracking contains aggregates only. Dataset selection must not consult OCR outputs or past transcription. Unsupported styles remain included/flagged rather than silently removed.

Test-first applies to new deterministic harness behavior; image extraction/reference preparation has no meaningful behavioral RED and uses structural/integrity checks. No changed selector behavior is authorized.

## Delivery and progress
Feature branch remains `feat/sample-prototype`. Forecast approximately 100 public tracking lines; private harness size unknown and excluded from publishing. Delivery strategy ask-on-risk. No new staging/commits/push authorized by this validation approval; prior commit request was completed. Private experimental code cannot receive a meaningful native review by reviewing unrelated public docs; independent functional checks remain necessary. Mirror saved to Engram and updated after preparation.

## Preparation evidence and blocker
All 24 FFmpeg extractions exited 0; all original crops were visually inspected before any OCR. Image-derived references retain `userVerified=false` and uncertainty flags privately. Every image is 1920x540, all hashes unique, about 11 MiB total. Frozen v3 four-file hashes remain intact. Initial system-Python structural attempt exited 1 because Pillow was absent; corrected standard-library PNG-header checks exited 0 without installing anything. Parent spot-check confirms 24 unique image hashes/dimensions and manifest hash. No model inventory, harness, ML import, initialization or prediction was performed.

Private availability manifest: `.local/ocr-probes/paddleocr-cpu/caption-selector-v3-fresh/dataset/availability.json`; SHA256 `fc929dd9af1bcd2f9849482f80a1d4b57875857401f39892a12bc03787dcab86`. Additional private extraction/protected-selector records and README remain in that new directory. Do not publish image-derived text.

## Frozen harness identities
Manifest `806f05b1d72f990e21350355dd90f3c2af858b91db8c213a53c38c65c3a91660`; runner `4c16bf392730ab561220ff041ad1603e5541a6e496d8437c9dc838013dbf4d85`; tests `51f09bfdf3ef68dfaf025efb1b12a1873791506e79bccf8ce493efd772da5227`; freeze `df20bcd90864b09313826247a4fdd8bbecc1f4f3d4cbb20d282a3f28641b82cb`. Protected inventory includes eight detector/recognizer files and prior evidence. Exact offline invocation/env is private `results/preparation/commands.json`; execution admission validates pins before deferred ML import and refuses existing fixed-directory results/ledger. Local explicit models and socket/DNS-denial guard used; no network/install/remote operations.

## Fresh result and failure diagnosis
Nine one-row cases:16/108edits=14.81%,6exact,2empty. Two two-row cases:0/63edits,2exact. Sole three-row case:59/59edits=100%,nonempty scene text instead of caption. All three numeric cases exact. These fresh results contradict extrapolating the previous known-data zero-error regression to general reliability.

- pool-01@230s and pool-03@302s: correct main caption exists in raw OCR, but selector returns empty with `no_coherent_blue_panel`. Exact failing panel constraint still unisolated.
- pool-17@806s: visible comma missing from raw and selected OCR; one deletion,12.5%caseCER.
- pool-24@1058s: vertical scene sign selected; all three main rows rejected as auxiliary typography. Scene detection167px high sets maximum-height-derived threshold113.56px (0.68ratio), rejecting main74/77/74px rows. Raw indices3/5/8 contain captions; first also includes a surplus background digit. Nonempty output conceals entire caption loss.

Independent verifier inspected all twelve images against references/results, retaining original assistant references and uncertainty flags with `userVerified=false`. Diagnostic confidence is high for these observed failure classes, not a calibrated probability; exact panel constraint remains unknown. Negative/non-blue reliability remains unmeasured. No reference revisions, threshold tuning or prediction repeats.

Private reports under `results/verification/`: aggregate-summary.json SHA`34b56c0ab9b1816a43e0d427791ab292028d808f83a95cdc85cc99baf0fedca8`, independent-summary.json SHA`f7b464b5a4b26b1d219ae0ea4e1231b38dec11509c19ba96b911b8f0e0a7bf55`, execution.json and logs; original outputs/ledger in `results/prediction/`. These remain ignored/unpublished.

Next: report failed fresh acceptance. A separately approved bounded saved-record diagnosis/correction could address panel abstention and maximum-height scene anchoring without new OCR; punctuation is a raw-recognition limitation. Preserve frozen v3 and all fresh evidence. No further implementation or new predictions automatically authorized.
