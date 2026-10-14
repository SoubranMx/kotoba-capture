# Opt-in ROI-guided v6 selector

## Objective and current authorization
Implement an isolated opt-in ROI-guided selector without changing frozen v5 or adopting it into the application. Current known-data target: strictly below 10% complete-output normalized CER on three confirmed nonblue cases separately, seven blue positives preserved, and zero false-positive outputs on two covered negatives. This is not a generalization guarantee.

User authorized core implementation, one native-polygon correction, then a general boundary-affinity improvement and exactly two new CPU OCR predictions on existing fullframes at 0.0/0.5 seconds. No other OCR, new images/timestamps/sampling, dependencies/install/network, UI/API, staging/commits/publishing or automatic adoption. Prior policies, references, native results and consumed guards remain immutable. Artifacts are English and public content aggregate only; raw text/images/policies/code/results remain ignored.

## Scope, routing and delivery
- Tracker: odd/tasks/caption-selector-v6-roi.md; full Engram mirror: odd/caption-selector-v6-roi/tasks.
- Isolated implementation: .local/ocr-probes/paddleocr-cpu/caption-selector-v6/{selector.py,selector-config.json,README.md,replay.py,tests/**,fixtures/**,results/**}.
- Current additional evidence: isolated v6 results/target-under-10/** and .local/osiris-v6-covered-negatives/**; historical results are read-only.
- Delegated direct for preparation/new logic/multiple nontrivial files and execution verification. Forecast under 100 public authored lines; private code is not planned for publication. The approximately 400-line task heuristic is advisory, not a test/docs cap.
- Ask-on-risk delivery; commits explicitly not authorized by project policy. No review of a public tracker certifies ignored private implementation.

## Tasks
- [x] V1: Synthetic RED → GREEN/refactor; dependency-free core with source/crop/ROI/native admission, conservative grouping, digits/auxiliary audit and frozen-v5 preservation.
- [x] V2: Visually freeze broad shared policies before scoring; once-only 13-record cached replay and independent stored-output metrics/identity checks.
- [x] C1: Scoped malformed-polygon RED → GREEN correction; admission-only cached validation and successful independent verification.
- [x] V3: Generic boundary-affinity RED → GREEN/refactor; unrelated exterior off-row signs do not globally veto supported rows while plausible clipping/ambiguity remains conservative.
- [x] V4: Fresh pins/preflight; exactly one CPU initialization/two offline negative predictions, then exactly twelve cached selections, independent metrics and immutable prior artifacts.
- [x] V5: Independent proof and parent spotcheck passed: 58 tests; nonblue 1/41 edits (2.44%), blue 7/7 exact, zero false positives on two covered negatives; authorized known-data target achieved.

## Acceptance and checks
Explicit normalized ROI uses original-source geometry; no implicit whole-frame fallback. Main-height band and row/alignment/gap limits are explicit. Invalid native/geometry/policy, unsupported orientation, overlapping/competing groups and credible clipping require review/abstention. Preserve complete observations, raw strings, punctuation and legitimate digits. Smaller upper glyphs are auxiliary candidates only, not furigana separation. Optional blue restriction requires validated caller evidence; no color detector is executed.

Every output requires human review; identical signage inside ROI remains an unsupported intent distinction. Evaluation references load only after selected outputs are retained. Normalization is NFKC then whitespace removal, retaining punctuation/digits; complete selected strings are scored. Native residual and known-index contamination audits are separate from selection metrics.

Exact test runner: .local/ocr-probes/paddleocr-cpu/venv/bin/python -B -m unittest discover -s .local/ocr-probes/paddleocr-cpu/caption-selector-v6/tests -v. Applicable checks: observed RED/GREEN/refactor/closure, no-ML preflight, fresh one-shot guards, actual initialization/prediction/selection counts, offline/DNS denial, source/model/image/native/reference/policy identities, independent metric recomputation, git diff --check and ignored private artifacts. Failed one-shot runs are retained without blind retries.

## Historical V1/V2 evidence
V1 behavioral RED: 37 tests, failures 40 plus error 1 across subcases, exit 1; GREEN 37 and refactor GREEN 39, exit 0. Replay geometry-admission RED: 45 tests/1 failure/exit 1; GREEN 45/exit 0. No ML imports, reference inputs or frozen-v5 edits in the core.

All 13 existing images were visually inspected; broad policies were frozen before selection/scoring: shared upper regime for three distinct nonblue sources, upper baseline regime for seven blue positives, lower ROI unavailable in three signage crops. No tight per-frame policies or native/reference-driven tuning.

Original preflight and cached replay exit 0: 13 selections in 0.415 seconds, zero ML imports/model initializations/OCR predictions. Historical metrics belong exclusively to the original pre-correction executable:

| Historical group | Exact | Complete normalized edits/reference characters |
| --- | --- | --- |
| Nonblue positives | 1/3; one conservative omission | 10/41 (24.39% CER) |
| Blue positives | 7/7 | 0/114 |
| Signage upper crops | 3 untestable: intended lower ROI not covered | Not negatives |

Historical positive total: 8/10 exact, 10/155 edits. Nonblue native main captions were available in all three cases: 2/3 exact, 1/41 residual edits. Original omission was selector boundary veto, not OCR failure. No observed extra selected detections against prior known main-index annotations; these are known-data audits, not independent intent ground truth.

Independent stored-output metrics agreed; all 13 native and cached-v5 records were preserved, 51 prior protected files/61 original total pins unchanged after replay/tests. Consumed guard denied callback replay. Original 45 tests and git diff --check passed. Private evidence remains in original results/replay/, commands.json, independent-verification.json, native-residual-assessment.json and original test logs. No original replay was repeated or reset.

## Historical C1 correction
Independent P2 finding: finite crop-bounded points could still be repeated, collinear or self-intersecting. Admission formerly lacked positive-area/simple-geometry validation. One authorized correction added distinct vertices, positive absolute area and opposite-edge intersection checks to both polygon arrays, accepting both winding orders and not requiring exact box/polygon agreement.

C1 RED: 48 tests/6 malformed-polygon subcase failures/exit 1; GREEN 48/exit 0. Admission-only validation passed 13 saved records, 121 detections/242 polygons with selector disabled; zero selection/OCR/init. All 51 prior hashes and original execution pin report were unchanged. Independent targeted verification and parent spotcheck passed. Original freeze is retained as historical identity evidence, not a valid freeze for corrected execution.

C1 identities: selector.py `2893e4a3d7789a23dd818fdd86640a97cbf055ccc479f6df38f81ed632dda6f3`; tests/test_selector.py `e558e6137915ad6604fbbd7d50fc6d63084a696157b0b189e673402967905906`; README.md `d879d4ff693a5d6f4696371a1c6e872cb071c679628df8a8a02c9f1c6ea891b7`.

C1 evidence remains under results/correction/. Parent closure scoped native assessment of this public tracker was passive/non_executable_only; ignored implementation was independently verified instead. No commit/integration occurred.

## V3 boundary-affinity evidence and tradeoff
Root cause: a single normal-sized scene box intersecting the ROI edge globally vetoed contained caption rows before grouping. Boundary affinity now uses existing ROI, height and row/inline limits, not text, known indices, video identity or new tuned thresholds.

Crossings remain vetoes with no supported anchor, oversized geometry, center inside ROI, vertical overlap with a supported row, or bounded same-row center/inline gap. Normal-sized mostly exterior off-row boxes remain audited as boundary_crossing_unaffiliated, never selected, without blanking a contained caption. Clipped/wrapped center-inside rows, same-row signlike evidence, side clipping, nearby small glyphs and oversized crossing cases have synthetic tests; native C1 rules remain covered.

V3 observed RED 55 tests/1 failure/exit 1; GREEN 55/exit 0; refactor/guard checks GREEN 58/exit 0. Original policies remain unchanged. Limitation: a genuine vertically separated wrapped continuation centered outside the configured ROI can also be excluded. ROI must cover intended caption placement; this is not automatic intent recognition.

## V4 fresh execution and metrics
Two-image no-ML preflight exit 0 with 93 protected identities. Fresh guarded CPU engine execution exit 0: one initialization, exactly two predictions, 10 native detections per fullframe, 40.515 seconds, 10 CPU threads, network/DNS denied. Images were existing fullframes only; no extraction or additional OCR occurred. Forecast before launch was approximately one minute.

Fresh cached preflight exit 0 with 102 pins; once-only cached replay exit 0: exactly 12 selections, zero ML imports/model initializations/OCR predictions, 0.374 seconds. References entered evaluation only after all twelve outputs were retained. No ROI, reference or output edits/tuning followed scoring.

| Current group | Complete normalized error | Exact/negative outcome |
| --- | --- | --- |
| Nonblue positives, scored separately | 1/41 = 2.44% CER, strictly below 10% | 2/3 exact; no omissions |
| Blue positives | 0/114 = 0% CER | 7/7 exact; preserved |
| Covered negatives | Not CER; both actual caption ROIs covered | 0/2 false positives; empty review/abstention outputs |

The remaining nonblue error is the retained native residual; C02 is now exact. Known-main index audits show no extra/missing selected detections. Independent stored-output matrix edit-distance recomputation agrees; native residual remains 1/41 nonblue and 0/114 blue. All twelve saved native inputs remain unchanged.

All 51 prior protected hashes and 102 fresh frozen identities remain unchanged after final 58 tests/exit 0. Original v5/models/images/native/references/policies/results/guards are preserved. git diff --check passed; private artifacts are ignored. Two easy correlated empty-ROI negatives do not establish signage discrimination; the three prior uncovered crops remain untestable and are not counted as true negatives.

Current selector SHA256: `9ac80bb05231ac98772ce9449ecf901833a39f0a2c8d334e53d32a3dee39fc4e`.
Fresh replay summary SHA256: `6ffe0b55bd5002d0566fb8a60558b8e9220965a4fe9f1eb98073b563274fa331`.
Fresh pin manifest SHA256: `58122c14760c35a728cab4f16a94f2f4d6ee597c90bb89f0ac5ffff6536341bd`.

Private exact commands/pins/logs/native output: .local/osiris-v6-covered-negatives/{commands.json,pins.json,run.py,results/native/**}. Fresh cached candidate/evidence: isolated v6 results/target-under-10/{commands.json,freeze.json,cases.json,references.json,replay.py,replay/**,independent-verification.json,*-tests.log,red.log,green.log,refactor-green.log}. These guards are consumed; do not rerun either execute.

## Next step
V5 independent verification and parent spotcheck confirm the authorized known-data target. All 102 candidate pins, 93 OCR pins and 51 prior protected identities matched; 12 native arrays/policies/references preserved; source/summary hashes matched. Parent re-ran 58 tests successfully. Historical execution evidence was independently checked, not repeated. The active user goal can be marked complete for this known-data scope. No additional inference, policy tuning, adoption or general reliability claim is warranted. Future behavior changes or stronger covered-region signage fixtures require separately bounded authorization.
