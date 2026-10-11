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

- [ ] **M1 — Version history and push.** Delegated direct for the ODD audit/document preparation; parent owns staging, coherent Conventional Commit, native assessment and push. Include all eight existing untracked ODD specs, the updated original tracker and this document; preserve historical failures and pending items.
- [ ] **M2 — Locate and inventory Prometheus.** Delegated read-only remote inspection only after the configured connection succeeds. Use the authorized directory command; inspect repository state, core env key presence and runtime availability without disclosing private values or storing the remote path.
- [ ] **M3 — Transfer necessary inputs and synchronize code.** Derive the minimal media/model/policy/evidence set, verify content identities, transfer privately without overwrite of unrelated files, and pull the pushed code without discarding remote changes. Record mismatches before proceeding.
- [ ] **M4 — Configure and preflight.** Preserve the three core env values, add missing pilot keys privately, check dependencies/resources, and validate frozen identity compatibility before selecting an exact resume or separately frozen remote plan.
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

The configured SSH attempt currently fails with `Permission denied (publickey)`. No remote inventory, transfer, pull, env mutation or inference is verified. Preserve all consumer state; remote tasks remain pending until the configured connection is usable. Next: finish the local public-history audit and commit/push; report the connection blocker without probing alternate credentials.

Local preparation checks passed: all ten ODD documents have valid heading/fence structure, the new tracker link resolves, and the public scan found no private machine paths, asset filenames, Japanese transcription or credential material. All 92 captured source/document/env/private-run JSON hashes remained unchanged. The eight historical specs were audited read-only. Both full task mirrors were read back exactly; `git diff --check` passed. No source tests or model execution were needed for this passive unit. M1 remains unchecked until the parent observes commit and push; no remote task is complete.
