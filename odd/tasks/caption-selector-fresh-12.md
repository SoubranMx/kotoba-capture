# Fresh caption-positive selector validation

## Outcome
The authorized eight-positive diagnostic is complete: independently verified complete-output CER is **4/173 edits (2.31%)**, seven of eight frames are exact, and no positive caption is completely omitted. This passes the strictly below 10% numerical criterion for this fixed sample only. General-use acceptance remains unproven: references are assistant-transcribed/userVerified=false, all sampled positives have blue panels, and negatives were not measured.

## Authorization and boundaries
The user first approved eight positives and four negatives from distinct intervals. A bounded visual search found only positives; the user then explicitly approved an eight-positive-only diagnostic with false-positive verification pending. After a harness serialization failure, the user explicitly approved one repeat of the failed first image and seven previously uncalled predictions, without changing model or selector.

- Existing local OCR only; no installations, downloads, external services, server/default/vault changes, staging, commits, publishing or remote operations.
- Private images, OCR, references, detailed reports and logs remain under ignored `.local/`.
- Preserve frozen v1/v2, models, prior references/results and unrelated Git changes. No tuning against these scores.
- Parent owns this task document and full Engram mirror `odd/caption-selector-fresh-12/tasks`. Retain feature filename/subtree for continuity.
- Commit evidence: not authorized; no work-unit commits or PRs created. Delivery strategy: ask-on-risk; approximately 100 public documentation lines, no source delivery authorized.

## Tasks and routing
- [x] F1: Freeze eight deterministic positive inputs and frame-aligned private references. Delegated writer; preparation/mapping trigger. IDs/times and reference/source fingerprints fixed before prediction; historical viewed/OCR IDs excluded.
- [x] F2: Correct the bounded harness defect, independently preflight and execute the authorized corrected batch once. Delegated writer; execution/new-runner trigger. All eight corrected ledger entries completed and raw records persisted. Prior failed evidence retained. Native process exit status was not captured because the tool boundary timed out; do not claim exit 0.
- [x] F3: Independently replay saved native records with frozen v2, recompute complete-output score and verify integrity/accounting. Delegated verifier; independent experimental evidence trigger. All eight outputs/audits reproduced exactly; no OCR during verification.
- [ ] Human verification of references and review of residual scene-text insertions.
- [x] V1: User-requested assistant visual comparison of all eight original images against generated text completed by fresh image-first reviewer. Seven complete without surplus; 120.5s main caption complete with four platform-sign insertions. Reading confidence high except the dense 147.5s three-line caption (medium, no confirmed missing characters). Parent spot-viewed that original at full resolution. Private visual-review.json/md saved, original/scored artifacts unchanged, no OCR. Assistant review does not mark userVerified=true. Commit not authorized.
- [ ] Fresh negative and non-blue-style evaluation, only under separately approved bounded scope.

## Fixed sample and score
Selection used pool quantile indexes 0,5,11,16,22,27,33,39, not OCR or error scores.

| ID | Time (s) | Edits / reference characters |
| --- | ---: | ---: |
| 3 | 1 | 0/10 |
| 58 | 28.5 | 0/16 |
| 122 | 60.5 | 0/11 |
| 175 | 87 | 0/20 |
| 242 | 120.5 | 4/10 |
| 296 | 147.5 | 0/66 |
| 360 | 179.5 | 0/19 |
| 426 | 212.5 | 0/21 |

Frame 242 retains all ten normalized main-caption characters; two flanking background-sign detections add four insertions in the same row. There are zero substitutions or deletions in that frame. Score the entire emitted output, including these insertions; do not filter with reference knowledge.

Aggregate: 4/173 edits, CER 0.023121387283236993, seven exact positives, zero complete omissions. Zero sampled negatives means not measured, never a passing negative gate.

## Observed checks and accounting
- Final runner checks: 12/12 passed; frozen selector: 16/16 passed, independently confirmed. Parent reran all twelve runner tests successfully.
- Test-first: writer observed failures at the dict-subclass/NumPy boundary before normalization correction. Independent verifier confirmed final boundary behavior, not historical RED timing.
- Pure preflight loaded zero PaddleOCR modules; enforced caller raw-manifest SHA before parsing/import, exact ordered IDs/times and runner/test identities.
- Four frozen-v2 hashes, six model hashes, eight source images, reference/source fingerprints and prior successful CPU/runtime settings verified unchanged before/after corrected execution.
- Original failed manifest and four failed artifacts (log/preflight/ledger/raw) remain unchanged.
- Prior attempt: first prediction completed but JSON persistence failed; one failed ledger entry, seven never-called reserved entries, zero raw records.
- Corrected attempt: eight completed ledger entries, eight raw records, complete score. Nine predictions total across both attempts; no additional calls or hidden-retry evidence. No execution processes remained running.
- Original failure: `TypeError: Object of type ndarray is not JSON serializable`. Dict-subclass PaddleX OCRResult bypassed its JSON view. Repair prefers JSON view, safely unwraps the real res schema and recursively converts arrays/scalars before selector and persistence.
- Tool timeout prevented capture of corrected process exit status. Terminal artifacts and independent replay prove functional completion, not an exit code.
- Native assessment was unassessable/high because of untracked inventory; ignored experimental source is not covered by review of unrelated tracked docs. No native approval claimed.
- Server suite not rerun: server code, dependencies and defaults unchanged. Negative/style checks deferred, not passed.

## Recovery and freshness history
Before restart, forty historical viewed samples were excluded. Forty spaced fresh candidates and twenty-four reference-gap candidates were visually positive, with two overlaps: sixty-two unique fresh inspections and 102 total future-view exclusions. Temporal reference gaps did not prove caption absence. Those same-selection fresh candidates remained eligible because no new OCR or selector changes occurred before selection; they are not future blind tests after this experiment.

PC restart pause preserved manifest/runner/test fingerprints; resumed work reconciled the actual file and full mirror before proceeding. An initial independent preflight found missing execution-time dataset/self-hash guards, which were corrected and checked before the first run. The later result-normalization failure consumed one prediction; explicit user approval preceded the bounded corrected attempt. Preserve all evidence, do not clear ledgers or warm caches.

## Frozen corrected identities
- Manifest: `3c5af36f6905bd6a26e8682859413b4fe8c4d1a7a4b90a55ff1d54c45e31b872`
- Runner: `298bcebf8ab8dfe993a2f7b28073f35a06d7ea73e508cef112427f768d9aa368`
- Runner tests: `ee3161cc80ce8fca0152ea834a0b1f22f7db3336d4080ea6e1c4e40f0d04d14d`
- Canonical references: `25a324c35773f5cd3e97073a3b1b1d485081069c3d42fb461bbd2b98f6d3cadb`
- Source provenance: `859d32e6595b6cef1e372d5ac92c0574c2eec22379b155cabfc2e23160debf7b`
- Independent numeric report: `850b06765906c8ecb4ae0042ce345528bd6f05fbcdb524c670916ad0d217d80e`

## Private artifacts
Root: `.local/ocr-probes/paddleocr-cpu/caption-selector-fresh-12/`.

- `dataset/corrected-attempt.json`: frozen eight sources/references/settings/harness identities; references embedded at selectedFrames[*].reference.
- `dataset/manifest.json`: original failed-attempt freeze, unchanged.
- `runner.py`, `tests/test_runner.py`: corrected harness and synthetic checks.
- `results/`: original failed log/preflight/ledger/empty raw, retained.
- `results/corrected-attempt/`: preflight.json, call-ledger.json, raw-results.jsonl, complete-score.json, ocr-runtime.log, independent-verification.json.

Do not dump text-bearing private reports into tools, memory or repository documentation.

## Next step
Assistant review V1 is complete. Report by timestamp, emphasizing confirmed surplus platform-sign text at 120.5s and precautionary medium reading confidence for the dense three-line caption at 147.5s. The latter's generated line breaks match the image, while the frozen reference is flattened; no extra character errors were established. Main-caption reading confidence is high on the remaining six frames. Human verification remains pending, with no userVerified edits.

Inspection regions in the original 1920x540 images: 120.5s left sign [503,120,586,198], right sign [1325,100,1400,198]; 147.5s lines [128,119,1760,194], [130,236,1760,307], [495,344,1435,420]. Qualitative visual confidence is not a calibrated OCR probability. Private report hashes: visual-review.json ae597611bb4becb69acbeb5a87aecdf535c1e29d298ed22c96132c33adfa658b; visual-review.md 44dd65b4540972895022667a96adec4bf3a363add1f12b32521b4136c473681b. Corrected manifest and independent scoring report identities unchanged. No additional OCR, edits to scored data or installs.

Next human inspection priority: 120.5s (confirmed selection defect), then 147.5s (long three-line/furigana layout); other cases are lower priority. Negatives/non-blue coverage and any selector correction require separate bounded approval. No automatic model/default adoption, extra OCR, installs, commits or publication.
