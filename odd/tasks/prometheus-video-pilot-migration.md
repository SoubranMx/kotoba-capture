# Move the single-video pilot to Prometheus

## Objective and authorization

Version the existing code and ODD history, push without a PR, and continue exactly one full-video pilot on Prometheus instead of Osiris. The user reports overheating and shutdowns on Osiris; the thermal cause has not been independently diagnosed. Keep local inference stopped and preserve its incomplete evidence.

The user explicitly authorizes commits, push, necessary private asset transfer, remote pull, private environment setup, and the one-video execution through the configured SSH destination `prometheus`. Resolve the repository through `z kotoba-capture`, using `pwd` only if needed. Never put its actual remote absolute path in Git or Engram.

## Scope and constraints

- Git contains code, synthetic tests, documentation, and historical ODD specs only. Videos, models, snapshots, OCR, transcripts, logs and detailed runs remain ignored and private.
- Preserve Prometheus's existing `KOTOBA_MEDIA_ROOT`, `KOTOBA_OBSIDIAN_VAULT_ROOT` and `KOTOBA_EXPERIMENT_DATA_DIR` values. Add only required missing pilot settings privately, using destination-local values.
- Use the configured SSH connection only; do not inspect ambient keys, agents or alternate sessions. Authentication failure blocks remote work, not permission to repair SSH.
- No PR, dependency installation, engine tuning, new model, UI/API or Obsidian integration. Missing runtime dependencies require a reported gap.
- Exactly one source, H01. Confirm its content identity before processing; do not substitute another video. Stop after processing and visual adjudication, regardless of outcome.
- Preserve the frozen local plan and all 50 durable records. Remote runtime, package, tool, environment or path identities may differ: audit before deciding whether exact resume is valid. Never forge identities or disable freeze checks. If a new remote plan is necessary, preserve local history separately and distinguish its timing and coverage.

## Tasks and routing

- [x] **M1 — Version history and push.** Delegated direct for the ODD audit/document preparation; parent staged all eight historical specs, the updated original tracker and this document in commit `ead9a71aee27eacd8fefa7ac3516318de6051416` (ten ODD documents, 571 additions). Native assessment: passive, `non_executable_only`, `review_due=false` with reason `passive`. Push to the existing feature branch succeeded; upstream HEAD matches the commit. No PR was created. Historical failures and pending items remain preserved.
- [x] **M2 — Locate and inventory Prometheus.** Delegated read-only inspection succeeded using the configured connection and authorized directory command. The clean existing branch is an ancestor of the published feature branch. All three core env keys, the source and six model assets already exist; source/model SHA identities match. Existing CPU runtime metadata is present; no dependency installation is needed at this inventory boundary. Functional runtime compatibility is pending M4.
- [x] **M3 — Transfer necessary inputs and synchronize code.** Observed exact remote checkout `925947b67d3c0246d81996d4f6808916f6509d35`: bounded fetch, new tracking feature branch and `pull --ff-only` succeeded; the old human branch remains at its original commit. All 73 tracked files match published SHA-256 bytes. Transferred only the missing 6,888-byte policy JSON, atomically without overwrite; existing source and all model hashes match. No video, model, venv, local run or whole `.local` copy. Remote Git is clean. Parent metadata commit boundary is pending.
- [x] **M4 — Configure and preflight.** Backed up private `.env`, preserved its exact original byte prefix and all three core parsed values, and added only six missing pilot keys. Process precedence checks match the private file; private files use mode 600. Existing-runtime checks: 182 full-suite tests PASS with no skips, 31 focused tests PASS, 116 stdlib-guard tests PASS and CLI help PASS. Preflight PASS in 2.37 seconds: 2,608 samples, duration 1,303.941 seconds, 1920×1080 geometry, 10 threads and 0.5-second cadence; zero ML imports and no run directory. Metadata EOF check covers the final sample. A fresh host-specific plan is prepared, not registered. Parent metadata commit boundary is pending.
- [ ] **M5 — Complete one remote pilot and stop.** Run the approved frozen engine, retain recoverable private outputs, visually compare snapshots and selected text, classify errors and uncertainty, report aggregate coverage and actual phase timings, then stop. Assistant references remain provisional.

## Checks and acceptance

For this passive documentation unit, deterministic behavior RED and source tests are not applicable: no source behavior changes. Check English aggregate-only content, Markdown structure, links, privacy, unchanged source/env/private-run JSON identities and `git diff --check`. Historical specs describe past checks; versioning them is not new algorithm verification.

Runtime acceptance remains the preregistered sampled-pilot criteria: all planned records durable and visually reviewed; positive aggregate CER below 10%; zero confirmed complete sample omissions; zero confirmed sample false positives; no unresolved presence/text ambiguities. Report gaps and ambiguities separately. Sampling does not prove every fleeting subtitle or unseen-source reliability.

Record extraction, OCR and review time separately from interruptions and transfer/setup. Preserve unobserved power-loss intervals; never silently classify them as downtime or add local/remote times as an uninterrupted run.

## Delivery and recovery

- Existing feature branch: `feat/tracked-v17-full-video-pilot`; source review boundary remains the approved `c9b8f92` unit.
- Public forecast: 495 existing historical spec lines, about 60 new migration lines and about 30 tracker additions. Preserve this coherent documentation-history unit rather than splitting code from tests or compressing history. No PR is authorized; parent applies the native passive assessment.
- Every task records observed proof and its commit boundary before being checked off. RDD remains enabled; no blanket future candidate consent is inferred.
- Recovery mirror: `odd/prometheus-video-pilot-migration/tasks`, including this full document and repository-relative locator.
- Rollback boundary for this preparation is the new migration document and appended migration checkpoint; existing history, source, env and private evidence remain unchanged.

## Current checkpoint and next step

Local processing is paused: 50 durable records and 51 frames, with pending sample index 50 not durably completed. No active local pilot remains. Previous healthy-foreground descriptions are historical, not current status. Full-video quality and completion are still unmeasured.

Authentication succeeded after reading only the user-designated Hyprland configuration and using its explicitly configured agent socket ephemerally. No SSH or desktop configuration was changed, and no private keys or alternate agents were inspected. The socket and remote absolute repository path are not persisted in Git or Engram. Inventory verified 12 logical CPUs, about 23 GB available memory and 282 GB free disk. Only the private policy JSON is missing; source, models and runtime already exist. Synchronization, minimal policy transfer, private env setup and code-only preflight now passed. Next: parent commits/pushes the passive checkpoint, remote fast-forwards that metadata, then registers a fresh plan and runs exactly one video. No remote inference has started.

Local preparation checks passed: all ten ODD documents have valid heading/fence structure, the new tracker link resolves, and the public scan found no private machine paths, asset filenames, Japanese transcription or credential material. All 92 captured source/document/env/private-run JSON hashes remained unchanged. The eight historical specs were audited read-only. Both full task mirrors were read back exactly; `git diff --check` passed. No source tests or model execution were needed for this passive unit. Parent observed a clean worktree after the history commit and successful push. M2–M4 now have observed proof; their checkpoint commit is pending. M5 has not started.

M2 inventory is observed complete; its metadata commit boundary is pending the parent checkpoint. The remote pilot will use a fresh host-specific frozen plan for the same H01 source, not reinterpret the 50 local results as a cross-host resumed run. Local incomplete timing remains separate. RDD remains enabled by the existing user decision; no new candidate approval is inferred.

## Remote setup proof and execution boundary

Private proof locator on Prometheus: `.local/prometheus-video-pilot-migration/setup/`. It contains git synchronization and asset manifests, env preservation proof and backup, test/help logs, preflight output, a host identity preview, host-boundary proof and ordered commands. All locators are repository-relative; actual host root and socket remain ephemeral. Remote `AGENTS.md` SHA matches the local instructions.

The installed runtime identity matches the local package/tool identity (PaddleOCR 3.7.0, PaddleX 3.7.2, Paddle 3.3.1, NumPy 2.3.5 and OpenCV contrib 4.10.0.84). Configuration locations and host file stat bindings still require a separately registered plan; matching source/package bytes do not authorize editing the original local plan. The exact H01 manual policy and model/source content identities remain unchanged. The existing 50 local records and 51 frames are untouched and will not be counted as remote progress or combined into uninterrupted timing.

Two setup-harness checks initially stopped after successful preflight: a system-Python identity inspection lacked optional packages, and a short packet seek ended before EOF because seeking starts at an earlier keyframe. Read-only diagnosis corrected the inspection interpreter and enlarged the metadata-only EOF interval. No application source, model, algorithm or env correction was required; the final packet at 1,303.869 seconds covers the final planned sample at 1,303.5 seconds. All required checks subsequently passed.

No real engine initialization, prediction, frame extraction, plan registration or full-video evaluation occurred. Live constructor/alias compatibility remains untested until authorized execution. Prepared output token: `v17-full-video-pilot-prometheus-h01-r1`; its run directory does not exist. Preserve the prior 10–15.4-hour OCR forecast as an extrapolation, not a Prometheus measurement, and keep setup/transfer time separate. RDD approval for tracked source already closed on Osiris; checkout does not copy or imply native review authority on Prometheus.

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
