# Track v17 and evaluate complete videos

## Objective and scope

Preserve the frozen experimental v17 selector in Git, then build a separately reviewed local video workflow and measure errors in exactly one complete video. Code, synthetic tests and documentation are public; media, models, snapshots, OCR, references and detailed runs remain ignored under `.local/`. No push, PR, network access, dependency installation, UI/API or Obsidian integration is authorized.

The user explicitly authorizes local work-unit commits, assistant visual adjudication, and an oversized coherent selector-plus-tests unit. The updated user scope authorizes exactly one complete-video pilot. When it finishes, stop and summarize observed results and actual elapsed time, whether favorable or not; do not evaluate a second video or automatically refine the engine.

## Delivery and recovery

- Branch: `feat/tracked-v17-full-video-pilot`.
- Initial review boundary: `4a5bce5f6c980e44088867df18b6596cfdfba3e6`.
- Delivery strategy: `exception-ok`; selector and synthetic tests stay together despite exceeding about 400 authored lines. Adapter and video runtime remain separate units. No PR is planned.
- Forecast: T1 about 1,100 authored lines; T2 about 83 existing adapter lines plus tests/docs; T3 not yet estimable until bounded exploration. Actual T1 committed line count: 1,204 authored additions.
- Current reviewed boundary: `6766776618ea5e3ad394d3d478e65bb141001dc1`.
- RDD enabled by user request; T1 consent/review completed; T2 under-budget slice and T3 applicable candidate consent/review remain pending. Global/clone mode enables future review but does not grant blanket session consent. Candidate consent applies only to the exact frozen candidate; no session-wide approval is supported. Checkboxes are not review approval.
- Recovery mirror: Engram topic `odd/tracked-v17-full-video-pilot/tasks`; full document plus this repository-relative locator.

## Tasks

- [x] **T1 — Preserve the dependency-free selector.** Delegated direct: reading prepares a write and multiple nontrivial files. Promote frozen bytes, relocate 116 synthetic tests, add a standard-library-only import guard and usage docs. Acceptance: exact selector SHA-256 preserved, original CLI untouched, baseline and selector checks pass, no private artifacts promoted. Commit `6766776618ea5e3ad394d3d478e65bb141001dc1`; user granted native review `review-a8b1db0a7877da41`, approved and exact acknowledgement burned authority. Parent repeated the 116-test stdlib guard successfully.
- [x] **T2 — Preserve the optional style adapter.** Delegated direct; separate code/tests/docs unit. Commit `d7aa88807bc2241a7577e5711eed4b3ff89c78d6`; native assessment medium, 163 authored lines, `under_budget`. T2 remains in the pending slice after reviewed boundary `6766776618ea5e3ad394d3d478e65bb141001dc1`. Functional checks passed; no dependencies installed or default engine change.
- [ ] **T3 — Add an experimental complete-video runner.** Delegated direct; reproducible parameters, recoverable progress, local review outputs and explicit profiles. Determine surface and runnable test-first checks before writing; keep v17 algorithm frozen.
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

T1 authored forecast realized: 1,191 new/added lines before this progress update (including feature document); final parent commit count will supersede this intermediate count. Parent owns Git staging/commits and native review. T2 implementation, functional checks and commit PASS; native assessment is medium, 163 authored lines and `under_budget`, pending in the slice after the T1 reviewed boundary. T3 implementation/mock verification PASS, but parent spot check, commit and applicable native review remain pending. T4–T5 have not started. No real video runtime was launched.

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

No dependency installation, model/media execution, source profile promotion or optional package initializer import occurred. Parent committed T2 and recorded the medium under-budget assessment; applicable slice review remains pending. Rollback removes the opt-in adapter, isolated pixel tests and its docs without changing core/default CLI behavior.

## T3 implementation scope and checks

Delegated direct: configuration and runner introduce multiple nontrivial files and require prepared reading. Allowed surfaces: `.env.example`, `apps/server/kotoba_capture/{pilot_config,video_pilot}.py`, `apps/server/tests/test_{pilot_config,video_pilot}.py`, `apps/server/README.md`, `docs/full-video-pilot.md`, and this task document. Forecast about 900–1,300 authored lines; parent must resolve size before committing, with no artificial code/test split. No real OCR, model import, extraction or complete-video run is permitted in this code-only unit.

The new opt-in CLI loads a strict non-executing environment file with process-environment precedence, confines outputs/models/policies to ignored experiment storage, freezes inputs before predictions, records atomic per-case outputs, and resumes missing samples only after exact identity validation. One engine per execution attempt. Mock tests exercise complete-video sampling, interruptions, immutable replay, blank/ambiguous results and review exports. T3 remains unchecked pending parent commit, spot check and native review. T4 has not started.

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

T3 forecast realized before this final tracking update: about 1,230 authored lines including configuration, runner, tests and docs. The cohesive runtime/durability/configuration boundary exceeds the planning heuristic; parent must resolve delivery sizing before commit rather than dropping tests or splitting executable code from proof. Rollback removes the new opt-in modules/tests/guide and added env definitions/README section, preserving existing Tesseract CLI and promoted v17 selector/adapter.

Next: parent structural spot check, independent verification when native tier requires it, T3 commit and applicable native RDD consent/review. Exactly-one H01 pilot remains planned for the existing 1,303.941-second source at 0.5-second cadence (2,608 samples); no run or visual review has started. Do not launch T4 before that gate or infer favorable metrics from these mock tests.
