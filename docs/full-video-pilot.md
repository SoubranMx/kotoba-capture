# Run one frozen, reviewable whole-video pilot

The opt-in pilot samples a complete local video with existing CPU OCR, applies the tracked v17 selector and saves every result for review. Completion means sample processing finished, **not** that subtitle accuracy was established. The original Tesseract CLI is unchanged.

## Configure first

Copy `.env.example` to the ignored project `.env` and replace its portable placeholders. No asset is promoted to Git.

| Variable | Contract |
|---|---|
| `KOTOBA_MEDIA_ROOT` | Existing local library; `--video` is a relative alias inside it. |
| `KOTOBA_EXPERIMENT_DATA_DIR` | Existing directory inside the project's ignored `.local/`; stores outputs. |
| `KOTOBA_PILOT_DET_MODEL_DIR` | Existing local PP-OCRv6_medium_det directory inside experiment storage. |
| `KOTOBA_PILOT_REC_MODEL_DIR` | Existing local PP-OCRv6_medium_rec directory inside experiment storage. |
| `KOTOBA_PILOT_POLICY_FILE` | Private JSON inside experiment storage: `{"policies": {"manual": <policy>}}`. |
| `KOTOBA_PILOT_PROFILE_ID` | Explicit manual policy key; optionally overridden by `--profile-id`. |
| `KOTOBA_PILOT_CPU_THREADS` | Integer 1–64; defaults to 10. |
| `KOTOBA_PILOT_INTERVAL` | Finite seconds, 0.001–3600; defaults to 0.5, optionally overridden by `--interval`. |
| `KOTOBA_OBSIDIAN_VAULT_ROOT` | Unused; no vault is needed or written. |

The environment loader accepts `KEY=VALUE`, single/double quoted values and `#` comments. It rejects duplicate keys, shell expressions, interpolation, backticks and escapes. It never evaluates commands, expands variables or follows shell `export` syntax. Existing process environment wins. Relative configuration paths and `--env-file` resolve from the repository root, not the current directory. The default `.env` may be absent if all settings are already exported; an explicit missing file is an error.

A profile uses the [selector's existing manual policy contract](experimental-selector.md). No source-specific profile is inferred. Blue-panel profiles are rejected because this runner has no panel detector. The profile file and models must remain private; videos, snapshots, native OCR, references, logs and detailed results never belong in Git.

## Preflight, freeze and execute

From `apps/server`, using the **existing** interpreter with the optional dependencies:

```sh
python -m kotoba_capture.video_pilot preflight --video relative/video.mp4 --output-name pilot-one
python -m kotoba_capture.video_pilot register --video relative/video.mp4 --output-name pilot-one
python -m kotoba_capture.video_pilot execute --video relative/video.mp4 --output-name pilot-one --resume
```

`preflight` probes and hashes inputs without importing ML or creating a run. `register` durably freezes the plan without ML. A fresh `execute` may also register and execute in one operation. `execute --resume` validates exactly the registered identity, consumes already durable records, and runs only missing samples. A completed run is consumed: resume returns its summary without initializing a model. Never reuse an output name for changed inputs.

Before launching, forecast OCR time **and** snapshot storage: preflight reports sample count, duration and an uncompressed RGB frame-byte estimate. PNG disk usage varies with the scene and is not that exact estimate. Full-frame PNGs are retained to support independent review; do not launch if private storage is insufficient. One foreground engine is initialized per execution attempt, never per frame. There is no retry loop after an execution error; the CLI exits nonzero with `partial`. Resume is a separate explicit operation.

The plan samples `[0, duration)` at the configured cadence, with a 100,000-sample safety bound. Full-frame geometry and image hashes bind the native arrays, style evidence and selected audit. All samples survive, including blanks and abstentions. Blank samples break repeated-text groups, and original row breaks remain in exported text.

## Freeze and durability

The plan binds source bytes/stat/mode, every model file, manual policy bytes and selected profile, relevant resolved configuration, tracked Python module bytes, Python interpreter/version, installed package versions/code and FFmpeg tool binaries/versions. Identity is checked before every launch/resume and again after processing. Model/code hashes are not recomputed before every individual prediction. Inputs must not be modified during execution. Changed inputs refuse reuse instead of silently recalibrating.

A local advisory lock prevents concurrent writers through this CLI. Every stage entry is durably checkpointed before extraction, prediction, style measurement and selection. Each complete record is atomically written, fsynced and directory-fsynced **before** the completed count advances. Resume validates exact ordered record coverage, record/image hashes, geometry/style bindings and a pure selector replay. A record durable just before a ledger interruption is reconciled without another prediction. An entered but nondurable call remains an interrupted attempt, not a completed result.

| Private output | Purpose |
|---|---|
| `plan.json` | Immutable input/runtime identity, geometry and sample plan. |
| `ledger.json` | Attempts, entered-call counters, pending stage and durable record hashes. |
| `frames/` | Every full-frame sampled PNG. |
| `records/` | Native OCR arrays, bound style evidence, exact selected audit and per-sample phase timings. |
| `observations.json` | Every selected/blank/abstained sample with native audit links. |
| `segments.json`, `review.md` | Consecutive reviewable groups; not audio-aligned subtitles. |
| `summary.json` | Aggregate coverage and actual recorded processing timings; no reliability verdict. |
| `runtime/` | Private runtime caches, engine log and redacted-public/private-detail failure diagnostics. |

## Offline runtime boundary

Existing PaddleOCR 3.7.0 uses CPU PP-OCRv6_medium_det/rec, with MKLDNN, CINN, TensorRT, orientation classifiers and unwarping disabled. The public `use_tensorrt=False` / `precision=fp32` aliases must map to `use_pptrt=False` / `pptrt_precision=fp32` in the installed runtime. The runner checks this contract but never patches installed packages. The frozen package-code hashes capture any existing local modifications.

Model directories must contain `inference.json`, `inference.yml` and `inference.pdiparams`; missing models/dependencies refuse execution, not trigger installation. Caches stay inside the private run. Model-source checks are disabled before optional imports; a process-local Python audit hook rejects socket connections, DNS resolution and bind operations. This hook is not a system-wide firewall or a guarantee covering arbitrary native code outside Python's audit surface. No installer, remote invocation or download command exists in the runner.

## Interpret timing and errors honestly

The summary separates initialize, extract, OCR, style, selection, export and final-integrity seconds, active attempt time and start/end timestamps. Wall elapsed time starts at the first execution attempt; registration and read-only preflight hashing are excluded. Visual review has a separate unset duration until measured externally. Normal handled interruptions preserve phase time and permit measuring the later downtime.

A power loss cannot reveal how much time between the last checkpoint and restart was processing versus downtime. Such an interval is explicitly **unobserved**, active time becomes a lower bound, and exact interruption downtime is reported as unknown instead of fabricated. Final identity checks may invalidate a run after predictions; preserved outputs remain a partial diagnostic, not approved evidence.

No reference is read during prediction. Assistant visual adjudication remains provisional and must record omissions, false positives, transcription errors, ambiguities and reviewed coverage separately. Finishing all samples is not continuous detection recall: discrete sampling may miss fleeting subtitles. No CER, success threshold, subtitle presence or human confirmation is inferred from the OCR output itself.

## Synthetic verification

No real model or media is needed for these commands from `apps/server`:

```sh
PYTHONPATH=. /usr/bin/python3 -B -S -m unittest discover -s tests -p 'test_*pilot*.py' -v
PYTHONPATH=. /usr/bin/python3 -B -S -m kotoba_capture.video_pilot --help
```

The tests mock tools and OCR with synthetic files, including full three-sample coverage and interrupted resume. The current authorization is exactly one complete-video pilot, then a timing/error handoff and stop; no second video, engine refinement, UI/API or Obsidian work is included.
