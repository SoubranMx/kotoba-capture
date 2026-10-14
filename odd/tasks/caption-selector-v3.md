# Isolated spatial caption association v3

## Objective and authorization
User explicitly approved isolated experimental v3 to correct detection-to-caption association, preserving frozen v2, legitimate caption numbers and three-line layout. Use saved OCR records only; no new OCR, model initialization/prediction, installations/downloads/network, server/default/vault changes, staging, commits or publication.

Acceptance for known-data regression: complete-output CER strictly below 10%, no complete positive omissions, no nonempty designated negatives, no new main-caption losses, preserved legitimate numbers and all three rows at 147.5s. Remove scene insertions structurally, not with reference text, known indices, timestamps or digit filtering. Existing data are now known; improved regression is not fresh independent validation.

## Diagnosis and design
- At 120.5s, broad panel rectangle [446,69,1462,150] overlaps both platform-number detections. They pass rectangle overlap, not near-Y. Their closed panel-mask support is approximately 0.199/0.265, while central caption support is 0.681.
- At 100s, the two-character residual detection has zero rectangle overlap and zero mask support; the 54px near-Y fallback admits its 43px gap. Main detections have support approximately 0.795/0.683.
- Proposed v3 checks actual selected panel/component mask support during association using the existing minPanelOverlap value 0.35, instead of trusting broad rectangles/unconditional near-Y proximity. Explicitly document this overlap-to-mask-support semantic change; no parameter sweep or hidden new threshold.
- Preserve public API, original HSV/morphology/panel thresholds, confidence/typography/row settings, audit/provenance/review-required semantics and unsupported-layout abstention. Precisely define which component mask is used and avoid unrelated blue components; a global-blue test alone is not selected-panel evidence.
- Risk: sparse/glyph-heavy true panels may abstain. Synthetic retention tests and all known-record replay are required before claiming improvement. Stop for a real unsupported-design issue rather than relax thresholds to fit scores.

## Tasks and routing
- [x] A1: Create isolated v3 copy; reproduce low-mask overlap, zero-mask near-Y and unrelated-blue-component defects with meaningful synthetic RED, implement minimal structural association, observe GREEN and freeze before score replay. Writer observed 17 passing/3 failing copied-v2 synthetic tests, then 20/20 GREEN; original sixteen test-method ASTs preserved. Route: delegated writer; preparation/new logic/multiple non-trivial files trigger. Commit not authorized.
- [x] A2: Independently inspect candidate/tests and replay all 23 saved cases once with original image/reference integrity. Replay exit 0: 0/477 edits, 21/21 positives exact, no full omissions or partial deletions, 0/2 nonempty negatives. Two cases improved, nineteen unchanged, zero worsened. Independent 20/20 synthetic tests pass; original sixteen test ASTs intact. Route: delegated verifier; independent functional evidence trigger. No OCR. Commit not authorized.
- [x] A3: Assess outcome and limits, record exact checks and report to user. Parent reran all twenty tests (exit 0), read report identities and Git diff-check. Known-data gates pass, general-use reliability remains unproven. Route: inline synthesis of bounded worker evidence. Stop at authorized scope; further corrections/validation need approval. Commit not authorized.

## Allowed surfaces and preservation
Writer may create only the new ignored caption-selector-v3 selector.py, selector-config.json, tests/test_selector.py and README.md. Private new results are under caption-selector-v3/results/; no writes to v1/v2/fresh dataset/runner/references/raw/evaluations/models. Parent owns this document and mirror odd/caption-selector-v3/tasks. Preserve unrelated Git changes. No commits authorized; work-unit commit evidence is explicitly unavailable by policy, not omitted silently.

## Verification
Existing Python 3.13/NumPy/OpenCV offline uv environment only, private HOME/XDG/UV caches, python -B, no ML runtime imports. Preserve all sixteen v2 test methods/behavior; add synthetic low-mask overlap, zero-mask near-Y, legitimate digit-containing captions, fragments, three-line retention, selected-component isolation, ambiguity and full audit checks as applicable. Observe behavioral RED before implementation, then GREEN/refactor. Synthetic fixtures are nonprivate English, never saved Japanese strings/coordinates/IDs as selection logic.

Freeze selector/config/tests/README hashes after GREEN and before replay. Check old v1/v2/fresh data and model identities before/after; full raw records and references processed locally, never dumped to tools/model/memory/public docs. Save detailed outputs privately, report aggregate metrics only. Any failure remains partial; no repeat-until-clean loop or scoring-driven tuning.

## Regression corpus
- Original seven saved records: five positives/133 reference characters and two designated negatives; raw results-no-mkldnn/raw-results.jsonl and original dataset/references.json.
- Former-held-out eight saved positives: 171 reference characters; caption-selector/results/api-restored/raw-results.jsonl and caption-selector/dataset/references.json.
- Latest eight saved positives: 173 reference characters; caption-selector-fresh-12/results/corrected-attempt/raw-results.jsonl and dataset/corrected-attempt.json embedded frame-aligned references.
- Combined: 23 known cases, 21 positives/477 reference characters, two known negatives. Preserve v2 2/304 and latest-eight 4/173 historical scores; compare complete outputs without oracle filtering. The 100s main-caption recovery and 147.5s legitimate number/three-line output must not regress.

## Delivery and next step
Forecast approximately 150 new implementation/test lines beyond a private copied baseline; isolated copy naturally adds several hundred private file lines. Advisory line budget is not a reason to omit tests or collapse readable code. Public artifact is this recovery document only; delivery strategy ask-on-risk, no commit/PR/publishing authorized.

RDD mode is on. Ignored experimental source was previously outside native review selection; do not manufacture approval by reviewing unrelated tracked docs or changing privacy/staging scope. Independently verify the candidate regardless; retain unavailable/unassessable native status honestly. Parent spot-checks one reported command before delivery.

Completed candidate requires rectangle intersection AND >=0.35 selected connected-component closed-mask support. Component support can extend beyond density-band rectangle; unrelated global-blue components do not qualify. Config version changed to 3, all numeric thresholds unchanged. Candidate source 254 lines/tests 265/README 26; imports math/cv2/numpy only. Old v1/v2/fresh/model/data inventory unchanged.

Frozen identities, independently parent-read from actual files: selector.py 7e92ee368586acd5da6cc8e1f8976b34301c1ed6b6f1352688475ac976ce1ac1; selector-config.json 01e80401312d359aaa30fef4fe5720426edee140e52ba9cffc46404223e435a3; tests/test_selector.py 8a3c06b96bab8e8a80c749b6a4dc6033f5a423e6f14fce0018498defc89cb6ea; README.md d530aa8bf82a5c7e3178b877d941ebee41bbab9fe3109e962a4073414a4551b4.

## Verified outcome and limits
Independent replay ran once, exit 0, with zero OCR calls and no Paddle/PaddleX modules loaded. Original positives: 0/133 edits; former eight positives: 0/171; latest eight positives: 0/173. Combined 0/477 (0% CER), all 21 positive outputs exact and both designated negatives empty. Frame242 rejects side indices2/4 and retains main3; 100s retains main4/5 and rejects scene19; frame296 retains indices8/13/16 across all three rows including legitimate numbers. These indices are observations only, never selector rules.

All twenty synthetic tests pass independently and in parent spot-check; original sixteen v2 methods AST-unchanged. Public API, all numeric thresholds, row concatenation, complete audit/provenance and review-required semantics remain preserved. All 23 source-image hashes/bytes/dimensions matched metadata, frozen v3 files unchanged, and the 76-file protected v1/v2/fresh/model/data/report inventory remained unchanged. Git status/unrelated changes preserved; git diff-check passed. No source mutation after freeze.

Native assessment remains unavailable/unassessable because of untracked inventory; ignored experimental source is not represented by reviewing unrelated tracked docs. Independent functional evidence is recorded, not native approval. Server checks were not rerun because server code/dependencies/defaults were untouched.

This is perfect known-data REGRESSION, not fresh independent validation or a universal zero-error guarantee. References remain assistant-transcribed except limited human observations; negative examples cover only prior designated cases, and sparse/unsupported/non-blue panels may abstain. Do not adopt defaults, launch new OCR, tune thresholds or claim general-use acceptance from these scores.

Private reports under .local/ocr-probes/paddleocr-cpu/caption-selector-v3/results/: summary.json, private-evaluation.json, selector-audit.jsonl, integrity.json, test-log.txt, replay-log.txt and reproducible replay_driver.py. Complete selected text is stored privately in each selector-audit.jsonl record's result; never dump text-bearing reports into tools/model/memory/public docs. Numeric summary SHA-256: 0e43b6d994d96255f202aa2263e9f6f1286c620b50afdd8818ab537498a3c921.

Next: report completed bounded correction and optional human review of the new saved output; separately authorized fresh negative/style validation would establish broader usefulness. Preserve frozen v2 and v3/all evidence. No further work or new OCR automatically.
