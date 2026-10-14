# Fresh v5 validation with user-provided references

## Objective and authorization
User requests a 34-minute internal wait, then continuing fresh frames for frozen v5. Eight manual reference strings were supplied; preserve them exactly in ignored private data before processing. User's content endpoint is16:13=973seconds, so N08@1000s is excluded. Current confirmed eligible timestamps: N01=250,N02=350,N03=450,N04=550,N05=649.5,N06=750,N07=850seconds; original650s image/reference preserved but not predicted. No global defaults, monorepo implementation, network/install/remote/staging/commits or old-driver replay authorized.

Future UI selectable transcription endpoint is saved in Engram decision1394/topic `product/transcription-time-range`; apply endpoint before sample/OCR/export. Scope is feature consideration, not UI/API implementation. User-requested wait is recorded in1395; timer does not guarantee provider quota renewal.

## Reference and evaluation rules
Private `dataset/user-references.json` retains all eight strings as received, including excludedN08, with userProvided=true and imageAlignmentVerified=false. No auto-correction of kana/typos/wording. Inspect exact eligible images after wait before any OCR; if text or line boundaries differ, disclose mismatch and ask user before scoring. User-provided reference is not necessarily aligned to a sampled instant; verify against image rather than treating a phrase-window transcription as frame ground truth.

Freeze v5 source/config/tests/README and images/user-confirmed references before inference; no reference-fed selector/tuning/oracle cleanup. All seven frames remain unseen to OCR; check prior manifests/time/hash identities. No N08 image extraction/prediction. Negatives/non-blue are not guaranteed; classify actual available images honestly and do not claim coverage absent from sample.

## Tasks and routing
- [x] H0: Persist exact user references, endpoint and timer; wait until UTC2026-10-09 21:35:43 (34minutes after clock21:01:43). Internal clock sleep, no Python timer file required. Inline bookkeeping/mechanical files.
- [x] H1: After timer, extract seven exact upper-half frames, inspect/compare user reference alignment and dimensions/hash. Stop before OCR on mismatches or unknowns; no silent replacement/extra timestamps. Delegated preparation writer; reading/images/extraction/analysis trigger.
- [x] H1b: User confirms one reference correction and authorizes nearby-frame search for the empty650s image. Preserve originals. Search at most8 nearby upper-half frames within2seconds, fixed nearest-first order, no OCR; choose first clearly visible main caption, verify wording and disclose mismatch before scoring. Delegated extraction/visual preparation.
- [x] H2: If references confirmed aligned, isolated guarded harness/preflight and independently observed tests; freeze artifacts/model/core/images. Delegated writer/verifier; any meaningful deterministic behavior uses RED/GREEN.
- [x] H3: Only after alignment/preflight gates, once-only bounded seven-prediction run and independent complete-output/image/reference verification. No OCR repeats/tuning; no excluded content.
- [x] H4: Parent spotcheck, honest fresh metrics/coverage/mismatch report and full mirror. Inline synthesis. References stay userProvided; record image alignment confirmation separately.

## Allowed surfaces
Private new root `.local/ocr-probes/paddleocr-cpu/caption-selector-v5-fresh/`: dataset/user-references.json, dataset/*.json, frames/*.png, README.md, runner.py, tests/test_runner.py, results/preparation/*, results/prediction/* and results/verification/*, narrowed per delegation. Parent owns this document and mirror `odd/caption-selector-v5-fresh/tasks`. All prior cores/raw/models/references/reports/task documents read-only; preserve user excluded reference rather than discard it.

## Checks and delivery
Same explicit local models/runtime/settings; frozen v5 explicit API only, no new threshold/profile changes. Preserve all previous artifacts/video/model identities; exact predicted/init counts and actual command exit evidence required. Standard crop matches previous upper-half1920x540 input; timestamps approximate display times, not audio alignment. All output review-required, geometric/OCR confidence uncalibrated. References used only after selection to score complete strings; no inference reference inputs.

Forecast about80public tracking lines, private harness unknown; advisory only. Delivery strategy ask-on-risk. No commits authorized by this request; ignored source cannot be meaningfully certified by reviewing unrelated docs, independent verification required. Inherited subagent model allowed. Stop for user reference conflicts; failed/partial gates never become PASS by waiting for quota.

H0 evidence: clock.sleep completed 1879.0148 seconds after bookkeeping; UTC readback2026-10-09 21:35:50 is after deadline21:35:43. No task processing occurred during wait. Quota reset is not asserted.

H1 evidence: seven FFmpeg extractions exit0,1920x540, all seven visually inspected. Five references aligned; one two-line reference mismatch; one sampled crop has no visible subtitle. Parent inspected both exceptions. Private dataset/alignment.json records ocrGatePassed=false. User references remain unchanged. No N08 or OCR.

User confirms the missing-character correction for N04, rejects treating N05 as blank and authorizes a nearby-frame selection. Store confirmed reference separately; no silent N05 spelling correction.

H1b evidence: first nearest candidate649.5s has visible one-line caption differing from provided N05 phrase; stopped after one extraction, exit0,1920x540. Ten protected file hashes unchanged. Parent visually confirms difference. N04 user-confirmed correction stored separately in dataset/confirmed-references.json; original references untouched. dataset/neighbor-alignment.json records blocked OCR gate.

User explicitly confirms the visible nearby-frame phrase as N05 reference. N04 correction and N05 replacement are confirmed; record independent image alignment and preserve original references.

H2 writer evidence: observed admission-test RED1failure/exit1, GREEN16tests/exit0; no-MLpreflightexit0 and240protectedfiles. Frozenrunner ad8c14a5df943a44bb54392fb39e2a6b4a59fb68a1e5e13172fb0aa2e5eb5520,freeze9a37b3050639a751c697a6afe36832edc338a036b3759218f587d5540f026382; exactcommands/environment in ignoredpreparation/commands.json. NoOCRyet.

H2 independent evidence: all seven exact images visually aligned,16tests/no-MLpreflight exit0; parent16testspotcheck exit0. Actual local model assets are six (three detector,three recognizer), not eight. RDD effective on; native assessment high/unassessable due unrelated untracked task documents; no review certification claimed for ignored implementation.

H3 evidence: execute once exit0,1initialization/7predictions,37.2seconds; guard consumed NEVER rerun. Independent complete-output NFKC/remove-whitespace CER0/114=0%,7/7exact,zero fullomissions/furigana/signage/extra-digit contamination. N04two-row order retained,N02digit width normalized. All7fullv4outputs preserved;zero v5fragment-consolidation attempts.240protectedfiles/sixownfrozenfiles/video unchanged,noN08/original650sprediction.

H4 evidence: parent readback summary SHAe5caec6d6012c9902aedb9033fd6b87aa8d114f71183137bdea44328a37261e6 matches independent report. Private summary, independent-evaluation,integrity under results/verification; raw-results.jsonl andnative-results.jsonl under results/prediction. Alloutputs review-required.

Limits: seven blue positives,zero negatives/non-blue; not general reliability or temporal continuity proof. N03panel extends into cyan architecture,N07into blue sky despite correcttext; geometry requires review. Fresh batch does not independently exercise v5fragmentfix. No tuning or adoption.

Next recommendation only: separately authorized negative/non-blue evaluation and geometry checks; no additional sampling or OCR authorized by completion.
