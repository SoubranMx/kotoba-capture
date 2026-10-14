# Reduce known H01 OCR errors without rewriting correct text

## Objective and authorization

The user requests autonomous work to reduce the identified error cases. Implement and evaluate one bounded, opt-in experiment using existing local frames, models, and runtime. Preserve the frozen v17 selector, original GPU run, corrected manual note, and core environment settings. No installs, downloads, new video, full-video rerun, SSH, staging, commits, push, or PR are authorized.

## Problem and baseline

Visual review identified twelve actual/probable OCR error intervals, eight selection/grouping abstentions, three timing/modal artifacts, and one ellipsis representation artifact. Twelve reference cells were corrected separately. The historical 7.057% modal CER used the old reference and is not a current corrected-reference baseline. The eight blank intervals accounted for 192 of 271 historical edits, but relaxing selection could admit signage or fuse unrelated text.

## Approach and constraints

- Keep `selector.py`, existing v17 policy, and `video_pilot.py` unchanged. Introduce an opt-in adapter, not a silent change to the historical pipeline.
- Plan bounded crops from native geometry and existing policy, without reference-text access or global character replacements. Re-recognize with the existing models and preserve separate raw/candidate audits.
- Do not infer caption intent or fix glyphs by replacing valid characters. Preserve ambiguous/style/signage abstention safeguards; evidence must justify any candidate promotion.
- Freeze evaluation membership and a single candidate configuration before inference/scoring. Include existing positive-retention and negative/signage controls, not only known failures. Do not tune repeatedly against the manual note.
- Keep all real crops, OCR, reference text, absolute paths, hashes, and detailed manifests private under `.local/h01-error-reduction/`. Public tests are synthetic; docs contain aggregate metrics only.
- Ellipsis equivalence is a separate explicitly labeled diagnostic, not OCR improvement. Preserve raw historical metric semantics and approximate-timing limitations.

## Tasks and routing

- [x] **E1 — Test-first bounded crop adapter.** Route: delegated; new logic across source/tests/docs requires one writer. RED observed as an absent opt-in module; GREEN synthetic tests cover fixed configuration, finite/bounded geometry, row order, v17 qualification/style abstention, raw-text separation, source-coordinate mapping, and no input mutation. Optional image imports remain lazy. Rollback is removal of the new opt-in module and its synthetic tests/docs, without changes to the frozen pipeline.
- [x] **E2 — Freeze private validation and corrected-reference baseline.** Route: delegated; private input inspection and command execution belong to the same worker. Frozen before candidate inference: 40 target images (24 planned crops, 16 retained abstentions) plus 10 controls. Corrected baseline is 106 / 834 raw CER edits (12.71%); U+2026/U+22EF diagnostic is 103 / 834 (12.35%). The final control set is seven deterministic existing H01 GPU-bound, original-frame-verified positive retention controls plus three independently labelled signage controls. All seven positives are eligible for one crop; all signage controls retain v17 replay abstention. The earlier ten-control GPU-baseline plan remains an explicitly unexecuted diagnostic, not experiment scope.
- [x] **E3 — Run one bounded GPU comparison and gate the candidate.** Route: delegated; exactly one frozen GPU initialization ran 31 crop predictions (24 target, seven retention controls); three signage controls remained abstained without a prediction. All 31 raw crops had nonempty OCR but the frozen v17 policy returned `roi_not_covered` for every crop, so every candidate selection abstained. The target-subset substitution diagnostic worsened from 106 / 834 edits (12.71%) to 145 / 834 (17.39%), recovered zero declared error cases, had seven positive-control regressions and 31 complete-line losses, and had zero signage false positives. Promotion is rejected. No retry, threshold relaxation, model change, selector change, or configuration tuning is authorized.

## Checks and acceptance

Run focused `test_h01_error_reduction.py`, existing selector v17 tests, full server tests with the existing GPU interpreter, and `tests/check_selector_stdlib.py`; check CLI/import boundaries and `git diff --check`. Record exact observed commands/results. Verify the frozen selector/source/model/runtime and original GPU record/observation identities remain unchanged.

Accept experimental improvement only with observed actual error reduction and no observed negative/signage false positives, correct-text corruption, or complete-line loss on the declared controls. An unsuccessful experiment remains a negative result, not a production feature or an excuse to weaken the gate. Human visual checks remain provisional and bounded.

## Forecast and delivery

Forecast about 180–320 authored additions/deletions, excluding ignored artifacts; about 20–40 minutes of implementation/checks and one bounded same-model GPU probe. Reserve time for crop preparation and validation; no full-video compute. Final image/crop count and resource estimate must be reported before inference.

Delivery strategy: `ask-on-risk`; no commits or PR are currently authorized. RDD is on; each new candidate needs its own native consent when applicable. The previous GPU runner review does not cover this experiment. Preserve the pre-existing modified GPU tracker unchanged.

## Recovery

Task locator: `odd/tasks/h01-error-reduction.md`. Full Engram mirror: `odd/h01-error-reduction/tasks`. Parent reads back and mirrors the tracker before source writes and after each task. No local artifacts or references are promoted to Git. Next step: bounded writer resolves the private control set and implements the opt-in experiment within the declared surfaces.

## Current handoff

E1–E3 are complete. Private proof is under `.local/h01-error-reduction/e2-freeze-v2/` and `.local/h01-error-reduction/e3-one-shot/`. The candidate is rejected as a negative result; native review remains parent-held. No configuration may be tuned or retried.

## Scoped source-coordinate contract correction

The first adapter replayed crop-local images through a selector that requires the full source ROI. All 31 raw crop OCR outputs were nonempty, but `roi_not_covered` prevented selection. This is a deterministic integration-contract error, not proof that the recognizer itself regressed. A read-only challenge verified that the saved crop outputs can be composed with the existing full-frame native result and replayed on the actual original image, without bypassing ROI or style checks.

- [x] **E4 — Correct composition and validate by cached replay only.** Route: delegated; RED observed as absent composition APIs, then GREEN synthetic tests cover full-source geometry, crop-edge clipping, selected-row coverage, duplicate geometry, retained outside rows/input immutability, nonplanned signage, and provenance failure. The adapter composes two explicit prediction views, recomputes style only on the original full image, and replays unchanged v17. One deterministic cached replay made zero OCR predictions and zero runtime initializations but stopped before reference evaluation because the 31 saved cases did not all yield a complete reselected result. No candidate metric, recovery, or control-regression count was produced; promotion is rejected for incomplete evidence. The E3 artifact hashes remained unchanged; the separate private partial audit records the stop. No rerun, crop/model/config/membership change, threshold relaxation, or follow-up correction is authorized.

The corrected replay is a new postprocessing candidate over the same one-shot inference evidence. It is not a second OCR/model hypothesis and must not be presented as part of the old E3 identity. The initial authored-line forecast was low; the explicit provenance and regression checks add about 70–100 implementation lines plus focused tests. Preserve readable tests and audit contracts rather than compressing the change to match the forecast. No commits or publication are authorized.

## Independent verification and disposition

Independent functional verification passed the 9 focused tests, 196 GPU tests, 116 selector tests, import boundary, stdlib guard, and diff check. It also found a malformed-input defect: provenance canonicalization with non-finite data can raise outside the fail-closed boundary. The E4 partial report does not retain a per-case failure reason, so no exact cause or quality improvement can be claimed from that incomplete replay.

No recognition or selection improvement has been validated. Do not integrate or promote this rejected experiment. Preserve the new experiment module, tests, and documentation only as private reproducibility artifacts under `.local/h01-error-reduction/rejected-source/`, remove those newly created untracked files from production source/test/docs directories, and leave original code, run data, models, reference, and the pre-existing GPU tracker unchanged. The public task tracker remains the aggregate negative-result handoff. No additional OCR, cached-replay attempt, parameter tuning, commit, or publication is authorized in this round.

## Final cleanup disposition

The experiment is rejected: no recognition or selection improvement was validated, and independent verification found non-finite provenance canonicalization can raise outside the intended fail-closed boundary. The incomplete E4 audit has no per-case failure reason, so its cause and any quality effect remain unproven. The three newly created untracked module, test, and public-document files were moved byte-for-byte into the private rejected-source reproducibility artifact; production source, test, and documentation paths no longer contain this experiment. No replay, OCR, model/config change, or corrective patch was performed. The original evidence and pre-existing GPU tracker remain untouched.

## Renewed round: cached temporal review proposals

The user subsequently requested continuing. This authorizes a new bounded cached-data approach, not a retry of the rejected crop experiment. Single-frame geometry/style cannot safely disambiguate the eight target cases: competing groups include unknown or matching typography. Existing selected neighboring records can corroborate a unique current native group in seven of sixteen representative records, across five of eight intervals. No representative has matching anchors on both sides, so continuity is unproven and automatic filling is not justified.

Keep the frozen v17 selector and original results unchanged. Add an explicit opt-in temporal proposal sidecar using the established two-second/eight-attempt contract. A proposed text must come from the current frame's native group, match a selected neighboring anchor in normalized text and stable geometry, and retain all competing groups and provenance. Never use the manual reference, confidence ranking, semantic text rules, or group merging to choose an output. Directional changed-caption barriers and unknown/provenance failures must be audited. Every proposal remains `reviewRequired=true`, `continuityVerified=false`, and `captionIntentVerified=false`.

- [x] **R1 — Test-first bounded temporal proposal contract.** Route: delegated; new source and synthetic tests require one writer. Observe RED before implementing timestamp admission, attempted-slot budgets, provenance/style/native/ROI validation, unique matching group, changed-caption barriers, selected-baseline retention, non-finite rejection, input immutability, and explicit review-only semantics.
- [x] **R2 — Freeze and replay saved records with controls.** Route: delegated; one frozen CPU-only cached replay used sixteen target records with 128 frozen context slots, seven original GPU-bound positive controls, and three separately provenanced cached CPU signage controls. It made zero OCR predictions, model initializations, and image extractions. The actual replay produced one review-only proposal and fifteen abstentions; the pre-replay mapper estimate was not met and no parameters were changed. All seven positives retained their original selected baseline. The three CPU controls remain limited cached abstention evidence, not a full-frame GPU negative corpus.
- [x] **R3 — Verify sidecar and report measured coverage honestly.** Focused sidecar tests passed 7/7; selector-v17 passed 116/116; full CPU tests passed 194 with 9 skipped; full GPU-environment tests passed 194; legacy temporal-policy tests passed 31/31; and the stdlib guard passed. Cached integrity validation rechecked all 2,608 original records/frames without OCR. The observed target outcomes were one proposal, four ordinary no-safe abstentions, and eleven invalid-current-group abstentions; no automatic recovery, CER improvement, or whole-video reliability claim is made.

Forecast approximately 150–220 new source/test lines plus short documentation. Runtime is a bounded cached-data CPU replay, with no GPU inference and no full-video execution. A successful result may reduce review effort, but does not solve the remaining three target intervals or the recognizer's glyph errors. No staging, commits, push, PR, installs or note edits are authorized. Native review remains candidate-specific when the opt-in source change is ready; old review consent does not transfer. Full tracker mirror remains `odd/h01-error-reduction/tasks`.

## Temporal contract verification correction

- [x] **R5 — Validate selected baselines before pass-through.** RED demonstrated that a selected baseline could bypass configuration, frozen identity, canonical record, source, timestamp, and replay checks. GREEN now validates all of those gates before preserving a selected result. Valid selected originals remain unchanged; malformed, non-finite, oversized, or non-JSON values fail closed without raising. The v3 replay retained six review-only proposals and unchanged membership/settings; no recognition or tuning occurred.

Independent verification reproduced a defect in candidate parsing: an unknown-style competing group invalidated every group, including a distinct style-matched group that legitimately matched an anchor. The rule requires the proposed group to qualify; competitors must remain audited, not become an automatic veto merely because they do not qualify. The first replay's one proposal remains historical evidence. A seventh initial mapper match is correctly blocked by a nearer changed-caption boundary and must not be recovered.

- [x] **R4 — Fix candidate-local eligibility and verify a new cached replay.** RED used a canonically rebound ambiguous synthetic record with one matched proposed group and one unknown competitor; it failed as `invalid_current_groups`. GREEN now audits every structurally valid competitor while limiting proposal matching to individually style-qualified groups. A new frozen replay retained the same configuration, membership, context, and source hashes; it produced six review-only proposals and ten abstentions. The seventh mapper match remains blocked by its nearer changed-caption boundary. No OCR, model initialization, image extraction, tuning, commit, or publication occurred.

## R1 observed implementation

- [x] **R1 — Test-first bounded temporal proposal contract.** Route: delegated writer; RED was the absent opt-in module import, then GREEN was seven synthetic tests. `temporal-review/v1` is a standalone stdlib sidecar that preserves selected baselines, replays the frozen v17 selector and style bindings, verifies canonical record/source bindings, and can emit only a separate review-required proposal from the current native group. The fixed rule is two seconds, eight attempted in-window slots, and source-normalized box IoU of at least 0.85. Unknown or ineligible slots consume the budget; directional changed-caption selected anchors block only that direction. No cached inputs, original records, frames, models, OCR, or replay outputs were touched while implementing R1.
- [x] **R2 — Freeze and replay saved records with controls.** Parent released the frozen membership/provenance manifest for exactly one CPU-only replay. The replay completed with zero OCR/model/image operations and no parameter adjustment.
- [x] **R3 — Verify sidecar and report measured coverage honestly.** Completed after the single replay. Claims remain limited to review-only proposals and control retention/abstention evidence.

### R1 exact evidence and R2 freeze

- R1 RED: `PYTHONPATH=. /usr/bin/python3 -B -S -m unittest discover -s tests -p 'test_temporal_selector_recovery.py' -v` failed before implementation because the opt-in module did not exist.
- R1 GREEN: the same focused command passed 7 synthetic tests after implementation. `PYTHONPATH=. /usr/bin/python3 -B -S tests/check_selector_stdlib.py` passed, and the existing selector-v17 suite passed 116 tests. These checks did not run cached data or OCR.
- R2 freeze is complete and replay remains pending parent release. The private manifest freezes 16 target records, 128 timestamp-context slots, 7 original GPU-bound positive controls, 3 separately provenanced CPU signage controls, two seconds, eight attempts, fixed 0.85 IoU, source/plan/model/policy/module/legacy-policy/reference-snapshot hashes, and `replayExecuted: false`. The CPU signage controls are intentionally not represented as GPU full-frame controls.

A visual check of the one proposed target against its current original frame matched the current-group proposal. This is a single-frame review observation only; it does not establish continuity, caption intent, or automatic acceptance.


## R4 observed contract correction

- R4 focused RED: the new canonically rebound unknown-competitor fixture failed before the fix because parsing every competitor required every style status to be `match`.
- R4 GREEN: focused sidecar tests passed 9/9; selector-v17 passed 116/116; full CPU tests passed 196 with 9 optional-dependency skips; the repository GPU interpreter passed 196/196 with zero skips; legacy temporal-policy tests passed 31/31; and the stdlib guard and diff check passed.
- The v2 freeze preserved the fixed two-second/eight-attempt/0.85-IoU configuration, original membership and context slots, predecessor v1 artifacts, and reference snapshot. It binds the old and corrected sidecar hashes. The single CPU-only replay produced six review-only proposals and ten abstentions; all seven original selected controls were retained. Three separately provenanced CPU signage controls remain limited cached-abstention evidence, not GPU-negative proof.
- Cached integrity validation rechecked all 2,608 original records/frames. Five newly proposed target frames received single-frame visual checks. These observations do not establish continuity, intent, automatic acceptance, CER improvement, or whole-video reliability.


## R5 observed validation-order correction

- Focused RED: selected synthetic baselines with invalid hash, timestamp, source, replay result, frozen identity, non-finite configuration, zero budget, huge integer, or non-JSON content were incorrectly preserved before the correction.
- GREEN: selected pass-through now follows the same configuration, frozen identity, canonical record, style, native, and selector-replay validation as review baselines. Focused tests passed 11/11; selector-v17 passed 116/116; the exact repository GPU interpreter passed 198/198 with zero optional skips; legacy temporal-policy tests passed 31/31; and the stdlib guard, privacy/import scan, and diff check passed.
- The v3 freeze preserved configuration, membership, context, and provenance while binding old/new module hashes and every predecessor artifact. Its one cached CPU-only replay again produced six proposals and ten abstentions, retained all seven selected controls, and revalidated all 2,608 original records/frames. No OCR, model initialization, image extraction, parameter tuning, or automatic integration occurred.
- Independent R5 verification passed the focused 11, selector 116, GPU full 198 (zero skips), and legacy 31 tests. It confirmed fail-closed invalid selected baselines, unchanged valid pass-through, candidate-local style qualification, and v3 integrity. The parent focused spot-check also passed 11 tests. Native candidate review remains pending; these checks do not grant review authority.
