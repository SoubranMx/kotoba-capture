# Isolated same-panel fragment consolidation

## Objective and authorization
User approved the next structural correction after read-only diagnosis: distinguish fragments of one subtitle panel from genuinely competing panels. Preserve frozen v4, baseline v3, temporal policy and all existing OCR/images/references/models/results. No new OCR, model imports/predictions, network, installs, global default changes, staging, commits or publishing. Inherited subagent model permitted.

## Diagnosis and design bounds
At 229.5s two vertically disjoint local candidates in the same blue component are corroborated by one horizontal main OCR row. Their area ratio about0.901 exceeds competing-panel ratio0.78, even though top confidence0.4901 passes0.42. They are pieces of one physical panel, not separate subtitle panels. At original230s similar fragmentation also depresses individual geometric confidence, so removing ambiguity alone is insufficient; rebuilt geometry must satisfy existing checks.

Keep all numeric settings unchanged. Candidate consolidation requires positive geometric evidence from the same independently qualified horizontal main row crossing relevant fragments and supporting their rebuilt region. Same component alone, proximity alone, OCR confidence alone or reference agreement cannot justify merging. Preserve genuine competing/connected panels and reject unsupported or ambiguous evidence. Do not concatenate private strings, strip embedded digits, fabricate punctuation or use IDs/times/reference text as rules.

Use a separate opt-in version/profile or entrypoint; existing v4 APIs/defaults/output must remain unchanged. First preserve a successful v4 profile result exactly; only attempt consolidation for the known structural fragment-ambiguity abstention. Retain full earlier baseline/attempted result, consolidation evidence/reason and all original detection audit entries. Empty-but-unsupported cases remain review-needed rather than force-admitted. No temporal policy modifications or automatic final replacement.

## Tasks and routing
- [x] S0: Saved-case diagnosis and authorization. Read-only exploration found v4 already recovers5/6 six-neighbor cases; remaining229.5s has false fragment competition, not furigana filtering failure. User approved correction.
- [x] S1: Frozen isolated v5 after behavioral RED41tests/1failure exit1 then GREEN45tests exit0. Original31v4test-method ASTs and entire source prefix unchanged; numeric configuration unchanged.162writer-protected identities unchanged. Delegated writer; preparation/new logic/multiple nontrivial files trigger.
- [x] S2: Independent45tests pass and once-only guarded42record replay exit0. Actual inventory40positives/867chars/2negatives. Known-regression gates pass:2/867edits=0.2307%,38/40exact,0omissions,0worsened,2negativesempty.230protectedfiles unchanged. Delegated verifier; independent functional proof trigger.
- [x] S3: ParentJSONaggregate/preservation/hash spotcheck passed and Gitdiffcheck passed. Aggregate report and mirror updated; known-data only, no fresh/general guarantee. Inline bounded synthesis.

## Verification and acceptance
Use all available saved observations without modifying any previous driver/ledger: prior35records (33positives/707chars,2negatives), six temporal neighbors (6positives/152chars), and independent231s observation (1positive/8chars). Expected total42 records,40positives/867referencechars,2negatives; verifier must establish exact inventory before relying on totals.

Require strictly below10% complete-output CER, no full positive omissions, no remaining nonempty scene-only loss, designated negatives empty, no worsened previously correct v4-profile results, legitimate digits and three rows preserved. Compare original groups separately and include whole selected output, not oracle-filtered fields. Raw comma deletion/embedded background digit may remain; do not silently repair reference/native text. All references remain assistant-transcribed/userVerified=false and cases now known. General compact-sign/vertical/non-blue safety remains unproven.

Tests use English synthetic data: disjoint bands crossed by one horizontal main row, two real panels sharing a connected background, two independently supported rows/panels, oversized OCR box spanning unrelated regions, low local mask support, confidence still failing after rebuild, square numeric fragments, furigana, pass-through immutability/full audit. Preserve original31v4tests/default behavior where applicable. Observe behavioral RED before GREEN; freeze source/config/tests/README before ANY private score replay. Existing offline Python/NumPy/OpenCV only; no Paddle/PaddleX imports or OCR.

## Allowed surfaces
Writer: `.local/ocr-probes/paddleocr-cpu/caption-selector-v5/selector.py`, `selector-config.json`, `tests/test_selector.py`, `README.md`, `results/preparation/*`. Verifier: new `results/replay_driver.py`, reports under `results/verification/*`. Parent owns this file and mirror `odd/caption-selector-v5/tasks`. All existing selectors/policy/raw data/images/references/models/reports are read-only.

## Delivery and next step
Public tracking forecast about80lines; copied private source/test size advisory, not a reason to minify or omit proof. Delivery strategy ask-on-risk. No commits authorized; ignored code cannot obtain meaningful native review by reviewing unrelated docs, so independent verification is required and native approval is not fabricated. Preserve three existing untracked task documents.

## Explicit profile and verified behavior
`select_caption_profile_v5(image_bgr, native_result, config=None)` calls the frozen-equivalent v4 scoped profile first, preserves its entire wrapper in `v4`, and retains successful chosen outputs exactly. Only empty multiple_competing_panels outcomes attempt reconstruction. Output records result/consolidationAttempted/reason and optional full consolidationResult; original baseline/attempted results and every raw detection remain reviewable. Legacy APIs/defaults unchanged, temporal policy untouched.

Exactly one eligible same-component fragment pair crossed by exactly one independently qualified main horizontal box is required. Rebuilt local mask area/aspect/fill/strength and remaining competitors are reevaluated. Gap/overlap/box constraints derive existing settings, numeric sections unchanged. Ordinary density versus retry local-window candidate branches remain distinct; no blanket component union, time/reference/ID routing or text surgery.

## Known-record outcome
Original7:0/133edits,5/5positiveexact. Former8:0/171,8/8exact. Latest8:0/173,8/8exact. Fresh12nowknown:2/230,10/12exact. Sixneighbors:0/152,6/6exact. Independent231s:0/8,1/1exact. Total42observations/40positives/867chars/two designated negatives:2/867=0.2307%CER,38/40positiveexact,0completeomissions,0scene-onlymainloss;both negativesempty.

Two improved,40unchanged,zero worsened. Original230s recoveredexact index0,reconstructedconfidence0.6772;229.5s genuinely different caption recoveredexact index4,confidence1.0,fourfurigana detections rejected. These scores are geometric heuristics, not correctness probability. All42complete v4 wrappers/audits unchanged inside retained v4 field; all38previously nonemptyv4 results fullyidentical. Legitimate numeric captions and mainthree-row outputs preserved.

Independent visual review ofboth improved andbothresidual cases:806s rawOCR comma deletion persists;1058s embedded background digit insertion persists whileallthree mainrows retained. No reference edits, globaldigitfilters, character fabrication or oracle scoring. References userVerified=false. Allcases are now known; passing these gates does not demonstrate general connected-sign/non-blue/vertical safety or genuine temporal continuity. Temporal policy still lacks a proven multi-detection anchor/change-boundary solution.

## Frozen and integrity evidence
SelectorSHA`c945c9f8486905005dc71c518a13884be4bfa1ad13c1b0f57d20030862316ea4`; config`22639a4d5df4c2444b9860c52116c1e905cdc4dcf8e73f210d4390b849a688de`; tests`7d40a3189cbe6df2d162fe6c432ec510768870ea3836482484ce93f958ca1e42`; README`40d31a53f8fb7ebecc32e1f43557c84b670282bf84bf78c48b3d8f2c3933bbd6`. All before/after matches;230protectedfiles including162writerinventory unchanged. No Paddle/PaddleX modules, zero predictions/OCR/install/network/Gitmutations.

Private results under `.local/ocr-probes/paddleocr-cpu/caption-selector-v5/results/verification/`: summary.json SHA`5e4e82d623ce2e81958fea0e6d01fcac4945e4bafe6e33d79f637f51efef7c6d`, selector-audit.jsonl, private-evaluation.json, visual-review.json, integrity.json, logs. New replay_driver.py has consumed exclusive replay-started.json: do not rerun or bypass. Parent verified exactaggregate tuple and summaryhash, olduntrackedtaskdocuments preserved.

Next: report passed known-record acceptance with raw-recognition residuals and fresh-safety limits. A separately approved fresh validation is needed before global/monorepo adoption. No automatic newOCR, retries, thresholdchanges or policyintegration.
