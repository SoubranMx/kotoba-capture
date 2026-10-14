# Bounded saved-observation temporal fallback

## Objective and authorization
User explicitly approved implementing an isolated temporal fallback experiment using saved observations and tests only, no new OCR. Prefer nearby same-caption observations before alternative selector parameters, preserve successful cases and original failed outputs. Future monorepo scoped-reprocessing consideration remains Engram `product/scoped-reprocessing-profiles`; no UI/API/video-wide runtime integration authorized.

## Scope and conservative contract
New dependency-free policy consumes saved timestamped observations and existing selector/raw OCR evidence; it never samples video, imports ML or invokes OCR. Frozen v3/v4 and all source images/models/native outputs/previous reports remain read-only. No network/install/remote/staging/commits/push.

Default window at most two seconds and attempt budget at most eight neighbor observations. Rank nearest timestamp, earlier tie; reject duplicate/nonfinite/invalid observations and record deterministic attempt/rejection reasons. Preserve nonempty successful original results exactly, do not route by true CER or OCR confidence as correctness. Trigger only explicit known selector abstention; malformed/ambiguous anchor stays review-needed.

Candidate text must exactly match a non-reference anchor derived conservatively from original raw horizontal OCR (NFKC/whitespace normalization). Single unambiguous horizontal detection is supported first; multiple conflicting/multiline/furigana detections require review rather than invented aggregation. A known intervening changed caption blocks crossing it in that direction. Missing/invalid continuity evidence must not be silently treated as proof; matching endpoints cannot prove uninterrupted subtitle continuity. Preserve reviewRequired, baseline, proposed candidate, timestamps/offsets/structural reasons and budget audit. Keep candidate proposal separate from automatic replacement when continuity is uncertain.

No text oracle/manual-reference/known-ID/time exceptions inside policy; image-derived references are evaluation-only and never policy inputs. No punctuation fabrication, semantic translation or digital filtering. A saved nearest-neighbor match can demonstrate feasibility but not general reliability or genuine temporal continuity.

## Tasks and routing
- [x] T1: Isolated policy frozen after RED31tests/37errors exit1 against pending stub and GREEN31tests exit0. Successful pass-through, conservative single-horizontal raw anchor, change-text boundaries in both directions, gaps/radius/budget/tie/provenance covered synthetically. Delegated writer; preparation/new logic/multiple nontrivial files trigger.
- [x] T2: Independent31tests pass and guarded once-only saved demonstration exit0. Original230s remains blank; saved231s is a separate review-only proposal.36complete baseline audits byte-equivalent,140protectedfiles unchanged. No reference-fed policy. Delegated verifier; independent functional proof trigger.
- [x] T3: Parent safeJSONspotcheck passed, Gitdiff-check passed, aggregate report and mirror updated. Inline bounded synthesis. Zero new OCR, no global policy adoption.

## Allowed surfaces and verification
Writer: `.local/ocr-probes/paddleocr-cpu/temporal-fallback/policy.py`, `tests/test_policy.py`, `README.md`, and `results/preparation/*`. Verifier: new `results/demo_driver.py` and reports under `results/verification/*`. Parent owns this document and mirror `odd/temporal-fallback/tasks`. Existing untracked fresh/v4 public documents preserved.

Use existing Python with `-B` and standard library only for policy/tests; cv2/numpy only if saved-image integrity verification requires them, no ML. Observe meaningful behavioral RED before implementation and GREEN afterward, freeze policy/tests/README, verify all used source-record hashes before/after. Independent check confirms the old230s omission is not overwritten, successful existing results byte-equivalent, nearby changed-caption records rejected, attempt cap/radius enforced. Driver must not rerun originalOCR/replayattempts. Private text-bearing demo outputs ignored; public docs contain aggregate evidence only.

## Delivery and progress
Forecast about 80 public tracking lines; private policy/tests estimated200–350 lines, advisory only. Delivery strategy ask-on-risk. No commits authorized; project privacy/commit policy overrides general ODD work-unit defaults. Native review cannot certify ignored policy through unrelated docs; independent verification required, no fabricated PASS. Inherited model permitted by user.

## Verified API and evidence
`propose_neighbor(baseline, neighbors, radius_seconds=2.0, attempt_budget=8)` consumes timestamp-ascending saved observations. Hash syntax and common video identity are checked; caller independently verifies actual source artifacts. Processed observations carry timestampSeconds, videoSha256/imageSha256/sourceRecordSha256, sourceKind=saved_ocr, original nativeResult and complete selectorResult. Planned slots carry timestamp/sourceKind=planned; no manual reference or visual same-caption annotation is fed to policy.

Output preserves full baseline and unchanged result; optional candidate is a proposal only. reviewRequired=true and continuityVerified=false always, even if sampled endpoints agree. This intentionally does not implement automatic replacement or OCR orchestration. Known caption changes block crossing in their direction; unknown slots/gaps consume budget and stay explicit. Text-bearing boundary/candidate inspection is capped; metadata ordering/validity checks are separate.

Actual230s/231s saved pair yields candidate231s with4/8attempts in2s window and unprocessed230.5s gap recorded. Original230s remains omitted and no prior corpusCER is recomputed.35saved baseline audits plus231s remain byte-equivalent (36total,32nonempty,including29previouslyexact nonempty corpus cases). One genuine temporal pair only; changed-caption safety validated synthetically, not by new OCR on earlier frames. Endpoint agreement cannot prove uninterrupted subtitle continuity.

Writer protected102 existing artifacts; independent verifier extended protection to140 files including8verifiedmodelassets and actualvideo/image/source-record hashes. All unchanged. Zero OCR/model imports/selector invocations/previous guarded replay executions/network/install/commits. Temporal policy suite is31tests independently repeated; the unrelated231s OCR harness was not executed.

Frozen policySHA`c4a6d9223213f50281ce0afdf38f307a56dc31d50c329939b315713951184fa7`; tests`e0ce18d2094cc967ddf62c09f8cbb3431923b9141e6051a28e598025426ab8f0`; README`e54172bef032b27d90979e3cf47ca47fed6b257ee8765c1cdcbe3184c8d184a6`. Private summary `.local/ocr-probes/paddleocr-cpu/temporal-fallback/results/verification/summary.json` SHA`2937af09bbebd7a2e9224281ad57645c02adbeab49bc2ff5c623180e542fede8`; proposal.json/preservation.json/integrity.json/logs/review-notes private. `results/demo_driver.py` attempted-run ledger consumed, do not rerun.

Next: report offline mechanism and limits. Before production automation, independently validate more actual temporal pairs and changed-caption boundaries under separately authorized OCR budget. Current artifacts provide review-only proposals; no video-wide orchestration, new automatic sampling or monorepo integration authorized.

## Authorized six-prediction validation
User explicitly approved up to six new local predictions after scope clarification. Fixed timestamps before image/OCR selection:229.5,230.5,301.5,302.5,1057.5,1058.5seconds, compared with saved230/302/1058baselines and231neighbor. Same models/runtime/defaultv3selector; policy unchanged. Use existing neighbor229.5/230.5images read-only; extract exactly four new upper-half frames at remaining times. Image-derived references frozen before OCR,userVerified=false,evaluation-only.

- [x] T4: Allsixoriginalimages visually reviewed, pre-OCR152referencechars/five same-caption/one changed-caption (229.5), no uncertain readings. Fournewextractions/reusedtwoimages. Harness RED10tests/7failures6errors then GREEN10pass; genuine no-MLpreflight passed,197protectedidentities. Delegated writer; preparation/new files trigger.
- [x] T5: Independent10tests/preflight passed; captured execute once exit0,oneinitialization/sixpredictions. Independent sixaudit replay matches frozenv3. Diagnostic FAILED:152/152edits100%CER,0/6exact,4empty plus2signage-only outputs. Real changed-boundary recognition unproven; policy cannot form unambiguous raw anchor there. Delegated verifier/executor; no repeat/tuning.
- [x] T6: ParentJSONaggregate/hash spotcheck confirms sixoncepredictions/failedmetrics/sourcepreservation; Gitdiffcheckpassed. Report failure/proposals/limitations and updated mirror. Inline synthesis; completed checks do not mean acceptance passed.

New writer surfaces only under `.local/ocr-probes/paddleocr-cpu/temporal-fallback/validation-six/`: runner.py, tests/test_runner.py, README.md, dataset/*.json, frames/*.png and results/preparation/*. Verifier may create results/prediction/* and results/verification/*. Existing policy/tests/README/freeze/selectors/models/video/sourceoutputs remain read-only. No ledger/replay bypass or extra frames/predictions authorized. No staging/commit/publishing.

Evaluate all six complete outputs against pre-OCR image references; report same-caption/changed-caption conditions before trying policy, never feed those references into policy. Nearby visual continuity is not guaranteed in all cases. Existing nonempty erroneous scene output at1058s may pass through unchanged by conservative policy: record as limitation, not correct recovery. No automatic replacement, retroactive corpusCER change or monorepo integration.

## Six-prediction diagnostic outcome
Actualmodels31.502swall/30.727smodelruntime,peakRSS1492128KiB;oneinit/sixcompletedpredictions/exit0. Newdefaultv3complete-outputscore152/152edits=100%,146deletions/6substitutions/0insertions. Allsixmaincaptions are present correctly in nativeOCR butlostbyselection; fourliteralemptyoutputs andtwo nonempty scene-sign outputs must not be confused with onlyfour lostcaptions.

229.5empty12/12edits (actualchangedcaption);230.5empty8/8;301.5empty7/7;302.5empty7/7;1057.5and1058.5eachsignage-only59/59. No positive outcome from these sixnew frames; unchanged models/params/defaultselection deliberately expose limits, not successful global recovery.

Frozenpolicythreegroups:230 stillproposessaved231(after3attempts),notnewneighbors;230.5rawanchoragreementremovescandidate-direction unknowngap,butcontinuityVerified staysfalse.302 returns ambiguous_or_missing_anchor/noattempts due multiple rawdetections/furigana.1058 returnsbaseline_nonempty_preserved, retainingwrongsceneoutput, notqualityapproval. All original results preserved, no automatic replacement.

229.5visible/rawOCRcaptionchanged butmultiple rawdetections+emptyselectedoutput preventpolicyboundaryclassification: no_admissible_selected_caption instead ofchanged_caption_boundary. Isolatedactualendpointproducesnocandidate butdoesNOTvalidate directionalboundarydetection. Do not use image reference/furigana-stripped oracle as policy input. Real-boundary safety remains unresolved; synthetic coverage alone insufficient.

All197protectedfiles/eightmodels/policy/core/sourcevideo/images/pre-OCRreferencehashes intact;36oldcompletebaselineaudits byte-equivalent. Allsix images independentlyviewed before/after inference; referencesunchanged userVerified=false. No tuning/sourcecorrections/OCRrepeats/oldguardeddrivers/installs/network/Gitmutations. Prior corpusCER not rewritten. Theseare controlled known-neighbor diagnostics, notgeneral freshvalidation.

Private result root `.local/ocr-probes/paddleocr-cpu/temporal-fallback/validation-six/results/`; prediction/raw-results.jsonl preservesallnative/selectorrecords; verification/policy-proposals.json andchanged-boundary.json recordexactdecisions; verification/summary.json SHA`0f1cb495ab5edd04131133cc5c8ca72e8cf02d2843984b810abb571a5996ca57`. Ledgerconsumed:neverexecuteagain. Preparationpins runner`261f746e83b2e052ade6bf0c516294687c74776802f677be7e713ce59bfacc70`,freeze`bf3ab3395ba300e3b9a842beab82a02a435ebcf7aa741c9b96a4b5e357849443`,tests`01e4bf332dd8c5629624c701f1ffd0a0998728405ee616a0f143de6de0801ce7`,manifest`cac2752a39b112f4a006ec37966c84b8624b3fb3ecc147b8b822aebccaf1f085` remain unchanged.

Next: report failedneighborgeneralization and blocked real-boundaryproof. Anyanchor/panel/classificationcorrection requires separateboundedapproval and saved-record-onlydesign; no additionalpredictions orautomaticpolicydeployment fromthisbatch.
