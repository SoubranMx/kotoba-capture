# Track v17 and evaluate complete videos

## Objective and scope

Preserve the frozen experimental v17 selector in Git, then build a separately reviewed local video workflow and measure errors in exactly one complete video. Code, synthetic tests and documentation are public; media, models, snapshots, OCR, references and detailed runs remain ignored under `.local/`. No push, PR, network access, dependency installation, UI/API or Obsidian integration is authorized.

The user explicitly authorizes local work-unit commits, assistant visual adjudication, and an oversized coherent selector-plus-tests unit. The updated user scope authorizes exactly one complete-video pilot. When it finishes, stop and summarize observed results and actual elapsed time, whether favorable or not; do not evaluate a second video or automatically refine the engine.

## Delivery and recovery

- Branch: `feat/tracked-v17-full-video-pilot`.
- Initial review boundary: `4a5bce5f6c980e44088867df18b6596cfdfba3e6`.
- Delivery strategy: `exception-ok`; selector and synthetic tests stay together despite exceeding about 400 authored lines. Adapter and video runtime remain separate units. No PR is planned.
- Forecast: T1 about 1,100 authored lines; T2 about 83 existing adapter lines plus tests/docs; T3 not yet estimable until bounded exploration. Actual T1 committed line count: 1,204 authored additions.
- Current reviewed boundary: `c9b8f92f4a37b44eecfc03f25dedca61303fcd1f` (T2 + T3 slice approved and exact acknowledgement burned).
- RDD enabled by user request; T1 and T2 + T3 candidate consent/review completed; RDD remains enabled for later candidates. Global/clone mode enables future review but does not grant blanket session consent. Candidate consent applies only to the exact frozen candidate; no session-wide approval is supported. Checkboxes are not review approval.
- Recovery mirror: Engram topic `odd/tracked-v17-full-video-pilot/tasks`; full document plus this repository-relative locator.

## Tasks

- [x] **T1 — Preserve the dependency-free selector.** Delegated direct: reading prepares a write and multiple nontrivial files. Promote frozen bytes, relocate 116 synthetic tests, add a standard-library-only import guard and usage docs. Acceptance: exact selector SHA-256 preserved, original CLI untouched, baseline and selector checks pass, no private artifacts promoted. Commit `6766776618ea5e3ad394d3d478e65bb141001dc1`; user granted native review `review-a8b1db0a7877da41`, approved and exact acknowledgement burned authority. Parent repeated the 116-test stdlib guard successfully.
- [x] **T2 — Preserve the optional style adapter.** Delegated direct; separate code/tests/docs unit. Commit `d7aa88807bc2241a7577e5711eed4b3ff89c78d6`; native assessment medium, 163 authored lines, `under_budget`. The later T2 + T3 slice is now covered by approved native review `review-a4da4235f1b8e946`, with exact acknowledgement burned. Functional checks passed; no dependencies installed or default engine change.
- [x] **T3 — Add an experimental complete-video runner.** Delegated direct; reproducible parameters, recoverable progress, local review outputs and explicit profiles. Commit `c9b8f92f4a37b44eecfc03f25dedca61303fcd1f`; 182 tests pass with existing optional dependencies, parent repeated the 31-test focused suite. User approved the coherent size exception and granted actual native RDD consent; four concurrent provider-owned reviewer captures approved the T2 + T3 slice and exact acknowledgement burned authority (`review-a4da4235f1b8e946`). v17 algorithm remains frozen.
- [ ] **T4 — Evaluate the first complete video.** Delegated execution and visual adjudication; retain snapshots and detailed error ledger privately. Record omissions, false positives, transcription errors, ambiguities and reviewed coverage separately. Assistant references are provisional. Define favorable criteria before evaluating, not after seeing outputs.
- [ ] **T5 — Hand off the single-video error and timing summary.** No additional evaluation. Report aggregate errors, actual elapsed wall time, extraction/OCR/review durations, ambiguities, reviewed coverage and any interruption downtime separately. Assistant visual references remain provisional. Stop after the one complete-video pilot finishes; leave refinement and other features for the user to decide.

## Verification policy

T1 is byte-identical preservation, not a behavior change: no artificial algorithm RED is required. New relocation/import-guard behavior receives applicable meaningful checks. Baseline command from `apps/server`: `PYTHONPATH=. /usr/bin/python3 -B -S -m unittest discover -s tests -v` (26 tests passed before source promotion).

Required T1 checks from `apps/server`:

1. `PYTHONPATH=. /usr/bin/python3 -B -S -m unittest discover -s tests -v`
2. `PYTHONPATH=. /usr/bin/python3 -B -S -m unittest discover -s tests/selector_v17 -t tests -v`
3. `/usr/bin/python3 -B -S tests/check_selector_stdlib.py`
4. Execute the documented synthetic example; verify original frozen files are unchanged, exact hash, synthetic test method count, privacy boundary and `git diff --check`.

T1 rollback removes the opt-in selector, its isolated tests/guard and related docs; existing Tesseract CLI and grouping/export core remain unchanged. Runtime harness: synthetic selector call only; real OCR/video is intentionally unavailable in T1.

## Runtime forecast and limits

First full-video OCR forecast: about 10–15.4 hours for 2,608 requested samples at 0.5-second cadence, extrapolated from 13.84–21.28 seconds/frame; this is not a guarantee. No second video is authorized. Visual review adds unmeasured time. Record actual elapsed wall time from the pilot start to completion, plus extraction, OCR and review phase durations; distinguish interruption downtime from active processing and do not substitute forecasts for observed times. Do not launch model/media work in T1. Sampling timestamps are approximate display times; discrete samples cannot prove all fleeting subtitles were recovered.

## Progress and next step

T1 implementation, functional checks, commit and native RDD completed; T1 is checked off. Frozen selector SHA-256: `b679cf553ba75261b9c3af92ee6891be9e5d4b66bcefb3d0cc4dc7f48f694eb9` (522 lines, byte-identical). Twelve relocated test modules preserve all function/class ASTs and 116 methods; package imports replace the experimental dynamic loader. New import guard observed RED before promotion (missing tracked selector, exit 1), then GREEN with the tracked selector and all 116 tests; no algorithm change or artificial algorithm RED.

Observed checks from `apps/server`:

- Baseline full suite before promotion: 26 tests PASS.
- Required full suite after promotion: 142 tests PASS (26 existing plus 116 selector tests).
- Required focused selector suite: 116 tests PASS.
- Required standard-library guard: 116 tests PASS; NumPy, OpenCV and PaddleOCR imports rejected.
- Documented synthetic example: PASS (selected synthetic text, native audit unchanged, review required).
- Frozen portable core package before/after hashes: all unchanged; selector equality PASS.
- Public artifact scan: 18 allowed files, syntax and private-locator/transcript checks PASS; English synthetic fixtures manually inspected.
- `git diff --check`: PASS. No normalizer required; no private assets or models copied.

T1 authored forecast realized: 1,191 new/added lines before this progress update (including feature document); final parent commit count will supersede this intermediate count. Parent owns Git staging/commits and native review. T2 and T3 implementation, functional checks, commits and native slice review completed. T4 local setup/preflight passed; inference and visual review have not started. T5 remains pending. No real model initialization, prediction or frame extraction occurred during setup.

## Follow-up and runtime configuration

Native T1 advisory `R3-numeric-overflow`: very large integers such as `10**400` can raise during `math.isfinite` checks. This was nonblocking; approved receipt stands. Record a future bounded hardening task if authorized, not a change to this frozen candidate.

T3 must use explicit environment-variable configuration documented in `.env.example`, including host-specific model and policy locations, rather than hardcoded absolute paths. No environment configuration is needed by the pure in-memory T2 adapter. Exactly one full-video pilot uses the existing 0.5-second sampling plan (2,608 requested samples); stop afterward and report actual extraction/OCR/review time and interruption downtime separately. Assistant references remain provisional.

## T2 verification evidence

Optional adapter is byte-identical to the frozen 41-line module (SHA-256 `5d50fdaf3966e811e08dc5dde87d0158f7fc460fac111674083dffa8128acc83`). Two synthetic test modules preserve all function ASTs and nine methods; import availability alone controls skips, never a caught broken API. Meaningful relocation RED observed before tracked adapter existed (two discovery errors, exit 1), then GREEN after promotion; no algorithm change.

From `apps/server`:

- `PYTHONPATH=. /usr/bin/python3 -B -S -m unittest discover -s tests -v`: 151 discovered, 142 PASS and nine optional dependency skips.
- `/usr/bin/python3 -B -S tests/check_selector_stdlib.py`: 116 PASS with optional imports blocked.
- Existing optional-dependency interpreter, `PYTHONPATH=. python -B -m unittest discover -s tests -v`: 151 PASS, zero skips.
- Same interpreter, `PYTHONPATH=. python -B -m unittest discover -s tests/selector_style -t tests -v`: nine PASS, zero skips.
- Both documented synthetic API examples: PASS.
- Adapter byte equality, original portable core/adapter package checksums, test function AST semantics, public privacy/syntax scan and `git diff --check`: PASS.

No dependency installation, model/media execution, source profile promotion or optional package initializer import occurred. Parent committed T2 and recorded the medium under-budget assessment; the later T2 + T3 slice review is approved and exact acknowledgement burned. Rollback removes the opt-in adapter, isolated pixel tests and its docs without changing core/default CLI behavior.

## T3 implementation scope and checks

Delegated direct: configuration and runner introduce multiple nontrivial files and require prepared reading. Allowed surfaces: `.env.example`, `apps/server/kotoba_capture/{pilot_config,video_pilot}.py`, `apps/server/tests/test_{pilot_config,video_pilot}.py`, `apps/server/README.md`, `docs/full-video-pilot.md`, and this task document. Forecast about 900–1,300 authored lines; parent must resolve size before committing, with no artificial code/test split. No real OCR, model import, extraction or complete-video run is permitted in this code-only unit.

The new opt-in CLI loads a strict non-executing environment file with process-environment precedence, confines outputs/models/policies to ignored experiment storage, freezes inputs before predictions, records atomic per-case outputs, and resumes missing samples only after exact identity validation. One engine per execution attempt. Mock tests exercise complete-video sampling, interruptions, immutable replay, blank/ambiguous results and review exports. T3 is complete after parent commit, spot check and native review. T4 setup has passed; its full run and visual review remain pending.

Configuration relocation RED: new `test_pilot_config.py` discovery failed with missing `kotoba_capture.pilot_config` before implementation (exit 1).

## T3 verification evidence (code only)

New config/video modules observed meaningful RED before implementation (each discovery failed with its missing module, exit 1). GREEN and subsequent refactors passed all 31 new synthetic tests. The mock entrypoint test invokes fresh Python subprocesses through `main`: a three-timestamp complete-video plan is interrupted after one durable record (exit 1), then explicit resume completes three records (exit 0), with four entered predictions over two engine initializations and no re-prediction of completed records. No real model/media/import execution occurred.

From `apps/server`:

- `PYTHONPATH=. /usr/bin/python3 -B -S -m unittest discover -s tests -p 'test_*pilot*.py' -v`: 31 PASS.
- `PYTHONPATH=. /usr/bin/python3 -B -S -m unittest discover -s tests -v`: 182 discovered, 173 PASS, nine explicit optional-dependency skips.
- `/usr/bin/python3 -B -S tests/check_selector_stdlib.py`: 116 PASS with optional imports blocked.
- Existing optional interpreter, `PYTHONPATH=. ../../.local/ocr-probes/paddleocr-cpu/venv/bin/python -B -m unittest discover -s tests -v`: 182 PASS, zero skips.
- `PYTHONPATH=. /usr/bin/python3 -B -S -m kotoba_capture.video_pilot --help`: PASS without optional dependencies.
- New Python AST parsing, public machine-locator/privacy checks, preserved `.env.example` existing definitions, exact selector/adapter hashes and `git diff --check`: PASS.

Implemented configuration: portable media/experiment settings, strict `.env` parsing with environment precedence, private local model/policy settings, explicit manual profile, threads and cadence. No new dependencies, model assets or snapshots were added. Runtime constructor uses the existing PaddleOCR 3.7.0 public aliases and verifies their installed mapping without patching packages.

Durability evidence covers source/model/profile/runtime/code/config mutation rejection, consumed completed runs, corrupt/missing/extra/reordered records, image/style/selection binding mismatch, symlink escape, concurrent writer refusal, blank-separated repetition, multiline text, abstention retention, initialization failure and durable-record-before-ledger reconciliation. Actual phase timings are retained per sample and attempt. Abrupt power-loss intervals cannot be split honestly into processing/downtime and are explicitly unobserved; active time is then a lower bound.

T3 committed authored size: 1,258 additions plus deletions across eight files. The user explicitly accepted the coherent oversized runtime/durability/configuration unit; tests stayed with behavior and no PR/push was authorized. Rollback removes the new opt-in modules/tests/guide and added env definitions/README section, preserving existing Tesseract CLI and promoted v17 selector/adapter.

Next: parent commits this passive setup checkpoint before registering the immutable run, then authorizes the bounded exactly-one-video execution surface. H01 is the existing known 1,303.941-second source at 0.5-second cadence (2,608 samples); inference and visual review have not started. Do not infer favorable metrics from mock tests or preflight.

## T4 setup checkpoint (no inference)

The existing ignored `.env` was backed up privately and gained only the six missing pilot configuration keys: detector/recognizer model directories, manual policy file/profile ID, CPU threads (10), and cadence (0.5). Original media, vault and experiment settings were preserved byte-for-byte and by parsed-value readback. No host values or private transcription appear in tracked documents. The explicit H01 policy matches its historical frozen caller profile; no shared-profile substitution or new model occurred.

Private setup locator: `.local/v17-full-video-pilot/setup/`. `commands.json` retains exact preflight/register/execute commands; configuration provenance, source/model hashes, resource/EOF proof, preflight results and evaluation protocol are separate private JSON files. Planned output token: `v17-full-video-pilot-h01-r1`, resolving to `.local/v17-full-video-pilot-h01-r1`; that run directory does not exist yet and must receive an explicit delegated edit surface before execution. Registration is intentionally deferred until after the parent's metadata commit.

Observed preflight: exit 0, 2,608 samples, duration 1,303.941 seconds, zero ML imports; setup made zero model initializations, predictions or extractions. Source SHA/stat/mode and all six historical model asset hashes match prior provenance; historical/promoted selector and adapter bytes remain unchanged. Read-only preflight took 4.85 seconds; this is not OCR runtime. No new model, network access, package installation, code change or review cycle occurred.

Disk capacity at setup: about 219 GB free. Six prior full-frame PNGs average 2.68 MB (range 2.43–2.91 MB); extrapolated upper storage is about 7.60 GB for 2,608 PNGs plus an equal safety buffer. This estimate is scene-dependent, not guaranteed. The CLI separately reports 16.22 GB of uncompressed RGB bytes. Available memory was about 4.76 GB and CPU count eight; configured ten threads preserves the already evaluated engine contract, rather than tuning after results. OCR forecast remains 10.03–15.42 hours plus extraction/export/visual review; actual timings are not available.

EOF advisory checked before launch using local `ffprobe` packet metadata only. The last video packet has PTS 1,303.869 seconds and extends to about 1,303.902 seconds; it covers the final planned sample at 1,303.5 seconds despite the slightly longer container duration. The first short packet interval ended relative to its earlier keyframe seek position; the corrected bounded interval reaches true EOF. No frame extraction was used.

Before viewing outputs, the conservative sampled-pilot favorable criteria are fixed privately: every planned record durable and visually reviewed; positive aggregate CER below 10%; zero confirmed complete sample omissions; zero confirmed sample false positives; no unresolved presence/text ambiguities. Report ambiguity and coverage separately, not as automatic negatives. These criteria concern sampled frames of a known video, not proof of every fleeting subtitle or unseen-source reliability. Assistant references are provisional, not human ground truth. Stop after this one video regardless of favorable/unfavorable outcome; no second video or automatic engine refinement.

Native T3 advisories remain follow-ups only: selector guide freshness, container-versus-video EOF handling, and interrupted initial registration recovery. No correction was offered or applied. T1 numeric-overflow hardening remains separately deferred. T4 and T5 stay unchecked until actual processing, visual adjudication and timing/error handoff are observed.

## T4 registered execution checkpoint

Parent metadata commit `fc880785a9a327700440586f6c550c10a6d44679` was assessed passive (34 authored lines), with no review due. Current metadata boundary advances to that commit; approved source remains `c9b8f92f4a37b44eecfc03f25dedca61303fcd1f`. The run edit surface `.local/v17-full-video-pilot-h01-r1/**` is explicitly authorized. Fresh preflight passed; exact retained registration succeeded once and complete durable plan, empty storage directories and zero-initialization ledger were read back before launch. Frozen plan: 2,608 ordered samples from 0 through 1,303.5 seconds at 0.5-second cadence, duration 1,303.941 seconds, exact historical H01 profile. Foreground execution is next; no OCR has started at this checkpoint. Private prelaunch plan/ledger copies reside under the setup directory. No registration retry, new video, profile change or code patch is authorized.

Foreground T4 execution started at 2026-10-11T19:44:32.115848+00:00; registered frozen identity is unchanged. Initial observed checkpoint: one model initialization and first entered prediction; no reference, profile tuning, second video or code change. T4 remains in progress until all 2,608 durable outputs and separate visual review are verified.

First-five progress checkpoint: six durable records after 117.69 seconds, one model initialization, seven entered predictions and six style/selection calls. Execution remains healthy and foreground; these counts measure processing only, not subtitle reliability.

## T4 power-loss recovery checkpoint

Read-only recovery verified 23 durable records and 24 valid frames; the 24th OCR call was interrupted before its record became durable. No pilot process remains active. Frozen source, models, policy, configuration, runtime and code identities exactly match the registered plan. Private byte-preserving backups of the plan, ledger, progress documents and protected-artifact hashes were written and read back before resuming.

The first attempt has an observed active-time lower bound of 423.75 seconds; the interval after its last checkpoint is unobserved, not proven downtime. Exactly 2,585 missing samples remain. The stored foreground `execute --resume` invocation will reuse the 23 completed records and atomically regenerate only the pending frame as needed. No source, environment, profile, model or Git changes are authorized during this frozen attempt. T4 visual adjudication and T5 remain pending; processing counts are not quality metrics.

Recovery first-new checkpoint: 39 durable records (16 newly completed), two lifetime model initializations and one interrupted call. All 23 prior records and completed frames retain their original hashes; the regenerated pending frame is also byte-identical. Resumed processing remains foreground. The interruption interval is recorded as unobserved, not silently assigned to downtime.

## T4 migration checkpoint: local processing paused

The latest recovery contains 50 durable records and 51 frames; sample index 50 has no durable OCR record. No local pilot remains active. The earlier healthy-foreground checkpoints describe historical observations, not current execution. Preserve the original frozen plan, ledger, frames, records and interruption history; T4 and T5 remain incomplete, with no full-video quality claim.

The user reports overheating and shutdowns and explicitly authorizes moving exactly one video to Prometheus. This supersedes the initial local-only/no-push/no-transfer scope for the migration only: commit all existing code and ODD specs, push without a PR, privately transfer necessary inputs, pull on Prometheus, preserve its three core env values, add missing pilot configuration and continue the one-video evaluation. No dependency installation or engine refinement is authorized.

Use the configured SSH destination `prometheus` and `z kotoba-capture` to find the repository. If needed, use `pwd` transiently; never persist the actual remote absolute path in Git or Engram. The configured SSH attempt currently fails with `Permission denied (publickey)`; no remote changes or inference have been verified. Do not inspect alternative keys or sessions to bypass this blocker.

Remote runtime, package, tool, environment and path identities must be audited before resume. The original frozen local plan may reject a different host; never forge hashes or bypass its guards. If a separately frozen remote plan is necessary, keep all 50 local records and timings as distinct historical evidence, not an uninterrupted remote execution or unseen-source validation.

Migration tasks and acceptance are tracked in [prometheus-video-pilot-migration.md](prometheus-video-pilot-migration.md), mirrored at `odd/prometheus-video-pilot-migration/tasks`. Local processing remains stopped while the parent completes the public-history audit, commit/push and connection handoff. Historical failures, advisories and unchecked evaluation tasks remain unchanged.

Migration M1 is complete: parent committed all ten ODD documents as `ead9a71aee27eacd8fefa7ac3516318de6051416` (571 additions), observed a passive native assessment (`non_executable_only`, no review due), and successfully pushed the existing feature branch with matching upstream HEAD. No PR was created; the post-push worktree was clean. Source approval remains unchanged. M2 is blocked by configured SSH authentication; transfer, remote pull, remote environment setup and inference have not started. Next: the user makes the configured SSH connection usable; do not ask again for the already-authorized repository locator or request credentials.

## Prometheus inventory checkpoint

The configured connection now succeeds through the agent socket explicitly designated in the user-provided desktop configuration. Read-only inventory confirms the same source and all six model files are already present with matching hashes, a clean ancestor checkout, existing runtime packages and sufficient memory/disk. Only the private policy JSON is missing. No configuration or inference has changed yet. A fresh Prometheus-specific plan is necessary; keep the 50 local records and their interrupted timings separate. Metadata commit boundary is pending the parent checkpoint.

## Prometheus synchronized preflight checkpoint

Migration M2–M4 have observed proof; metadata commit boundary is pending. Prometheus has the exact published `925947b67d3c0246d81996d4f6808916f6509d35` checkout and a clean tracking feature branch, preserving its old human branch. All 73 tracked file hashes match. Only the missing 6,888-byte policy was transferred; source and models already match. Private `.env` gained six pilot keys while preserving its original bytes and three core values. No host paths appear in Git or Engram.

Remote code-only verification passed 182 full-suite tests (no skips), 31 focused tests, 116 stdlib-guard tests and CLI help. Preflight passed in 2.37 seconds for 2,608 samples and the exact H01 manual policy; no ML import or run directory was created. EOF packet metadata covers the last sample. The package/tool runtime identity matches local bytes, but host-specific resolved configuration/stat bindings need a fresh plan. Keep all 50 local records and interrupted timing separate.

Private remote setup proof and ordered commands: `.local/prometheus-video-pilot-migration/setup/`. Output token `v17-full-video-pilot-prometheus-h01-r1` is prepared but unregistered. Parent must commit/push this passive checkpoint and fast-forward the remote metadata before registration. No engine initialization, prediction, extraction or accuracy evaluation occurred. T4/T5 remain pending, and no remote native-review authority is inferred from Git synchronization.

## Prometheus registered execution checkpoint

Parent committed the M2–M4 metadata as `60b1494a38388bfdea9987bebbc45e0266074383`, observed passive native assessment (34 authored lines, no review due), pushed it and verified remote fast-forward to the same boundary. Parent repeated the remote 31-test focused suite successfully. No tracked source or configuration changed during this checkpoint.

The fresh Prometheus run was registered exactly once at 2026-10-12T00:34:24.873894+00:00. Registration took 1.40 seconds and readback confirmed all 2,608 timestamps (0 through 1,303.5 seconds), exact prepared identity, empty frames/records, no attempts, and zero initialization/prediction/style/selection counters. Frozen identity SHA-256: `6268438b3b4f9ee1743a52ce37f7bde24c903a54bb5a1e9e81cfacc1b1ae51e2`. Private registration proof: `.local/prometheus-video-pilot-migration/execution/registration-proof.json`.

M5 is now in progress, not complete: foreground execution is authorized next for exactly this one registered H01 run. No engine initialization, prediction, extraction or visual review has happened at registration. Keep the 50 local records and their interrupted timings separate. No source/model/env/package changes, automatic retry, second video or tuning are authorized during this frozen attempt.

## Prometheus first-five foreground checkpoint

Execution launched at 2026-10-12T00:37:03.614138+00:00; the tracked CLI attempt began at 2026-10-12T00:37:04.955941+00:00. At 80.01 seconds since launch, five of 2,608 records were durable, with one model initialization, six entered predictions, five style/selection calls, and one running attempt. Recorded phase time at that checkpoint: initialize 3.51 s, extract 2.85 s, completed OCR 66.50 s, style 0.29 s and selection 0.021 s. This is processing evidence only; zero samples have been visually adjudicated.

The first five imply approximately 9.6 hours of OCR alone or 11.6 hours extrapolated from launch-to-checkpoint throughput; these are small-sample forecasts, not actual completion times or quality measurements. Keep waiting on the same foreground attempt; do not start another execution.

Before this actual launch, an orchestration process guard matched its own decoded command text and stopped without running the CLI. Read-only diagnosis confirmed zero attempts, initializations and predictions; the guard was narrowed to exact CLI argument tokens. No engine retry, source change, model change or frozen configuration modification occurred. Private progress proof and sanitized SSH stream remain under `.local/prometheus-video-pilot-migration/execution/`.

Prometheus processing checkpoint: 250/2,608 durable records at 2,700.13 seconds since launch (45.00 minutes), one initialization, 251 entered predictions and 250 style/selection calls. Same foreground attempt remains running. Recorded extraction 131.34 s, OCR 2,538.81 s, style 14.61 s and selection 0.679 s. No visual adjudication or reliability verdict; local historical evidence remains separate.

## Prometheus CPU pilot stopped by user

The user explicitly requested stopping CPU execution and handing GPU work to a future session. A targeted SIGINT was sent only to the matching foreground pilot CLI at 2026-10-12T02:03:57.398829+00:00. The tracked CLI handled `KeyboardInterrupt`, durably finalized a `partial` attempt and ended at 2026-10-12T02:04:03.008348+00:00. Read-only post-stop audit verified zero surviving pilot CLI processes. No automatic resume, re-registration, second video, GPU implementation or engine tuning occurred.

Preserved remote coverage: **513/2,608 durable records and 514 frames**. Last durable display timestamp is 256.0 seconds; sample index 513 at 256.5 seconds was interrupted in OCR before its record became durable. One model initialization and one attempt were observed, with 514 entered predictions and 513 style/selection calls. `interruptedCalls` remains zero because that reconciliation counter advances only on a later resume; the pending OCR and handled interruption are explicitly retained.

Actual remote wall elapsed time: **5,218.052 seconds (1 hour 26 minutes 58 seconds)**; active attempt time 5,218.052 seconds. Recorded phases: initialize 3.511 s, extract 254.778 s, OCR 4,908.645 s, style 30.395 s and selection 1.176 s; export/final-integrity phases zero because the complete run did not finish. Terminal orchestration independently verified unchanged frozen identities and replayed all 513 durable records' native/style/image/geometry/selection bindings. Handled-stop downtime and unobserved interval are both zero for this attempt. Do not combine this timing with the separate interrupted Osiris history.

Private storage at stop: 818,175,427 frame bytes and 9,491,366 record bytes, excluding engine logs and metadata. No final review exports were produced. **Zero samples visually adjudicated; reference coverage zero; accuracy and full-video reliability remain unmeasured.** T4, T5 and M5 remain incomplete.

Recovery locators on Prometheus: `.local/v17-full-video-pilot-prometheus-h01-r1/` preserves the CPU plan, ledger, summary, frames and records; `.local/prometheus-video-pilot-migration/execution/` contains `user-stop-proof.json`, `execution-terminal-proof.json`, `stopped-audit-proof.json` and private logs. The local sanitized stream is `.local/prometheus-video-pilot-migration/execution/ssh-progress.jsonl`. Remote Git remains clean at `60b1494a38388bfdea9987bebbc45e0266074383`; source, env, model and policy bytes were not altered.

Next session: decide and implement GPU execution as a separately scoped change with applicable tests/review and a newly frozen runtime identity. Preserve this CPU attempt rather than claiming it is interchangeable with a different engine/runtime. Parent handles checkpoint/memory export, commit/push and future import; this worker does not start GPU work.
