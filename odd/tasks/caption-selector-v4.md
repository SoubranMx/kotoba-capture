# Isolated fallback-profile selector v4

## Objective and authorization
User approved a compact-horizontal-panel admission exception and continuing saved-record corrections, conditional on recording scoped reprocessing profiles as a future monorepo feature. Engram decision1280/topic `product/scoped-reprocessing-profiles` records that consideration; no production monorepo/UI/API implementation is authorized.

Preserve frozen v3 and all original OCR, references, images, models and reports. No new OCR, model imports/initialization/prediction, network, installs, defaults, staging, commits, push or publication. User permits inherited subagent model/effort.

## Diagnosis and design bounds
- A true 512px horizontal panel fails only existing 1920x0.28 width admission. Authorized compact exception must require coherent area/aspect/fill/confidence and independently supported horizontal text, not lower the global width threshold or change its denominator silently.
- A 576px horizontal panel joins tall narrow blue background; whole-component aspect and whole-band column projection fail. Derive localized vertical-window candidates with existing panel tests; do not merge all background windows indiscriminately.
- Vertical 68x167px scene detection anchors typography and rejects 74/77/74px horizontal main rows. Qualify both anchor and output by horizontal-or-square orientation while preserving legitimate square numeric fragments; vertical captions remain unsupported.
- A missing comma and background digit embedded within an OCR detection are raw-recognition limitations. Do not fabricate punctuation, split text by reference or filter digits globally.

Prefer baseline-first scoped retry: existing successful v3 output remains byte-equivalent unless observable structural evidence identifies a vertical-only result. Default v3 algorithm/config/output remains frozen; new opt-in experimental profile records baseline output and reason for alternative selection. No per-frame IDs/timestamps/reference-based routing, score-driven threshold sweeps or unbounded retries. If strict baseline preservation cannot coexist with structural correction, stop and explain rather than silently change successful cases.

## Tasks and routing
- [x] V0: Read-only root diagnosis and compact-admission decision. Delegated explorer confirmed width-only failure, connected-background failure and vertical-height anchoring. Parent/user approved bounded compact semantics; saved future-feature requirement before source writes.
- [x] V1: Isolated baseline-first opt-in v4 complete/frozen. Final-fixture baseline RED31tests/6failures exit1; GREEN31tests exit0. Earlier RED28tests/4failures included two faulty synthetic assumptions, corrected before final RED; no saved-score replay by writer. Original20test ASTs unchanged, v3 source byte-identical prefix, numeric settings unchanged. Delegated writer; preparation/new logic/multiple nontrivial files trigger.
- [x] V2: Independent inspect/tests and once-only no-ML replay of all35 saved records exit0. Independent31tests pass;137protectedidentities unchanged. Default35outputs/audits matchv3; all previously correct profileoutputs/audits unchanged. Result PARTIAL: CER below10%, but one full omission remains. Delegated verifier; independent functional proof trigger.
- [x] V3: Parent spotcheck31tests OK, aggregate report and mirror update. Git diff-check passed. Inline bounded synthesis; no fresh validation or future-product implementation claim. Completed verification tasks do not mean acceptance passed.

## Acceptance and verification
All 35 are known-data regression: 33 positives/707 reference characters and two designated negatives. Require complete-output CER strictly below 10%, no complete positive omissions, both designated negatives empty, no worsened previously correct positive outputs, legitimate numbers and three-row retention. Report original23 and latest12 separately, full omissions and nonempty-but-lost captions separately; passing pooled CER cannot mask regressions. References remain assistant-transcribed/userVerified=false. Fresh negative/non-blue safety remains unproven.

Use existing offline Python/NumPy/OpenCV only; no Paddle/PaddleX imports. Preserve all twenty v3 test-method ASTs where prior semantics remain applicable; default baseline behavior must be tested unchanged, add opt-in profile tests. Tests use synthetic English fixtures, not private text/IDs/timestamps. Observe behavioral RED then GREEN before any private score replay. Freeze selector/config/tests/README/profile metadata before replay. Independent replay compares all actual outputs and audits, never oracle-filtered fields.

## Allowed surfaces
Writer: `.local/ocr-probes/paddleocr-cpu/caption-selector-v4/selector.py`, `selector-config.json`, `tests/test_selector.py`, `README.md`; preparation logs/identities only under `results/preparation/`. Verifier: new no-ML `results/replay_driver.py` and reports under `results/verification/`. Parent owns this document and mirror `odd/caption-selector-v4/tasks`. Existing paths outside new v4 are read-only.

## Delivery and next step
Public tracking forecast about 100 lines; copied private baseline/new tests excluded from publishing. Delivery strategy ask-on-risk. Work-unit commit unavailable by project policy; no new commit authorization and private code remains ignored. RDD cannot validate ignored source by reviewing unrelated docs; independent functional verification is required, no native PASS fabricated. Preserve existing untracked fresh-validation document.

## Profile API and preservation
`select_caption_profile(image, native_result, config, profile="scoped-horizontal-retry")` explicitly activates the experimental profile; default profile is `baseline`. Original `select_main_caption` is unchanged. Wrapper keeps complete baseline, chosen result, structural reason, retryAttempted and attempted retryResult. Retry only empty `no_coherent_blue_panel` or nonempty outputs with every selected box strictly vertical. Mixed/horizontal successes, malformed inputs, ambiguous baseline panels and detected-panel typography abstentions pass through unchanged. No true runtime CER-based routing.

Five retries observed: four panel-abstention attempts (including both designated negatives), one vertical-only attempt. Two improved,33unchanged,zero worsened across35records. Default algorithm and successful prior outputs/audits remain unchanged; opt-in profile is not a new global default.

## Verified metrics and remaining gaps
Prior23:0/477edits,21/21positiveexact,0omissions,2negativesempty. Latest12:10/230edits=4.35%,9/12exact,1completeomission. Combined35:10/707edits=1.41%,30/33positiveexact,1omission. No remaining nonempty output conceals full main-caption loss. All original numeric and correct three-row outputs remain exact; recovered latest three-row output retains all rows but one surplus native character.

- pool-03@302s: compact exception recovers main row exactly; panel confidence0.4589.
- pool-24@1058s: restores all three main rows, edits59to1; remaining background digit is embedded within native OCR row and cannot be reliably stripped by selecting complete detections.
- pool-01@230s: still empty,8edits. Retry reports competing-panel ambiguity; candidate confidence0.3294 fails admission. No tuning/replay repeats performed.
- pool-17@806s: unchanged one raw-recognition comma deletion.

Acceptance is PARTIAL, not passed: pooled and latest CER gates pass but full-omission gate fails. All35cases now known, no independent fresh-validation claim. References remain `userVerified=false`; two existing negatives do not establish general compact-sign safety. Genuine vertical captions, non-blue styles and indistinguishable compact blue signage remain unsupported/risks.

## Frozen evidence
Selector `362bf3814ad04faed852d0ca1c76bf08b1172a7ba92b435ddf00c2dc92cf5e1b`; config `e60ba498f565c41a6551b089a250e2c7202c62f4e4fd446626619dc5e31af4f9`; tests `8d3699ad8d7a86a11140c7e42ea26154d4bf45fe7c4fdd187b426a212c3608ef`; README `3a831977ea6bc0b3e06d7af3a844d7246b67caf5a02f7638a46b159b4f778777`. Independent before/after matches,137protected previous/model/image/reference/report identities unchanged, no Paddle/PaddleX imports and zero OCR.

Private summary `.local/ocr-probes/paddleocr-cpu/caption-selector-v4/results/verification/summary.json`, final SHA`874d7d9ccd664233aa33bc4bb9fd0be517af693d2ed67f1a38357c6181067926`; full outputs in selector-audit.jsonl, visual-review/integrity/logs private. Replay driver attempted-run guard refuses repeats: do not rerun it. Model/UI/API/monorepo changes not implemented.

Next: report partial outcome and the remaining230s omission; any additional diagnosis/correction requires a separate bounded step, not silent threshold relaxation. Preserve frozenv4/v3/all evidence and future-profile requirement1280. No new predictions or global defaults.

## Authorized temporal-alternative check
User clarified another frame means another nearby timestamp, not spatial ROI, and approved an eight-frame visual search at228..232seconds. Same-caption231s is the nearest frame passing frozenv3default panel admission (confidence0.5973,noambiguity);231.5also passes. Prior228..229.5frames show different text,230.5fails and232has insufficient panelconfidence. Geometry success alone did not verify OCR.

- [x] N1: User said continue after pending-OCR report; ONE prediction on231s with unchanged explicitlocalmodels/runtime parameters and frozenv3default selector completed exit0. One init/one predict,5.759s,maximumRSS1458612KiB; result exact0/8edits,index0,unambiguouspanelconfidence0.5973. Route: delegated bounded writer/executor then independent saved-record verifier; new harness/preparation/execution triggers. No additional times/predictions/reruns. Original230s omission unchanged.

Allowed new artifacts only under `.local/ocr-probes/paddleocr-cpu/caption-selector-v4/results/neighbor-search/ocr-231s/`: runner.py, tests/test_runner.py, freeze.json and results/*. Originalneighborimage/manifest/video/models/core/priorharnesses are read-only. Preserve privateHOME/XDG/cache directories, reject identity drift and existing attempted-run ledger before ML imports, localmodels only/offline connectiondenial. Test any new deterministic admission logic RED/GREEN; no tuning or reference-fed inference. Parent owns document/mirror.

Single-frame hypothesis reference comes from independently viewed originalimage and is unchanged from230s, userVerified=false. Independent verification must compare rawOCR/selection/image andreportzero/fullerrors without extrapolating allframes. No fullmonorepo implementation/globalfallback policy or commit authorized.

N1 proof: new guarded runner observed RED6tests/5errors exit1, GREEN6mock-onlypass exit0; ML-freepreflight exit0; actualonceattemptexit0. Independent6mocktestspass, once savedv3selectorreplay auditidentical, zeroMLimports/predictionsduringverification.165protectedhashes plus11savedresultfiles unchanged. Explicitkwargs/runtime settings match originalfreshv3 run. ParentJSONspotcheck confirms verifiedtuple. Allsource/models/original231simage/230sfailure preserved; no defaults/policy/corpusmetrics modified.

Private N1 result `.local/ocr-probes/paddleocr-cpu/caption-selector-v4/results/neighbor-search/ocr-231s/results/record.json` keys nativeResult/selectorResult/completeText andprovenance; verification/independent-verification.json is independentreport. Ledgerconsumed, neverexecuteagain. RunnerSHA635c199a799ab8105cac940abf84cea4103a7b2fd04fbfa3c57bb72da17c17a5; testsbcddd3d1f575e49932604664c1006ef1efaaebd78c2ac5edbf5cfd3e115b31d4; freeze3ce5b6c52ff46e4264f7dac0284d01ce1141a001e06c0a3e76e7b5fe09c43623; image29d8e645f9cb4afd2bd23f4a9c3a9ff7b33ebd127c7363970a5f272f0a05d795.

Temporalalternative succeeded for this pairedcase withoutchangedselectorparameters. It does not replacefailed230srecord or retroactively pass35-recordomissiongate. Futureboundedtemporalretry withtextcontinuitychecks/attemptbudget/provenancefits scoped-reprocessingconsideration1280 but is not implemented or generallyvalidated. Stop atauthorizedoneprediction; futureimplementationrequiresboundedapproval.
