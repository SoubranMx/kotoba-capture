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
