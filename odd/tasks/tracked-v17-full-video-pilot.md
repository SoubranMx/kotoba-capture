# Track v17 and evaluate complete videos

## Objective and scope

Preserve the frozen experimental v17 selector in Git, then build a separately reviewed local video workflow and measure errors in exactly one complete video. Code, synthetic tests and documentation are public; media, models, snapshots, OCR, references and detailed runs remain ignored under `.local/`. No push, PR, network access, dependency installation, UI/API or Obsidian integration is authorized.

The user explicitly authorizes local work-unit commits, assistant visual adjudication, and an oversized coherent selector-plus-tests unit. The updated user scope authorizes exactly one complete-video pilot. When it finishes, stop and summarize observed results and actual elapsed time, whether favorable or not; do not evaluate a second video or automatically refine the engine.

## Delivery and recovery

- Branch: `feat/tracked-v17-full-video-pilot`.
- Initial review boundary: `4a5bce5f6c980e44088867df18b6596cfdfba3e6`.
- Delivery strategy: `exception-ok`; selector and synthetic tests stay together despite exceeding about 400 authored lines. Adapter and video runtime remain separate units. No PR is planned.
- Forecast: T1 about 1,100 authored lines; T2 about 83 existing adapter lines plus tests/docs; T3 not yet estimable until bounded exploration. Actual committed line count: zero pending parent commit.
- RDD enabled by user request; native candidate consent and review remain pending. Global/clone mode enables future review but does not grant blanket session consent. Candidate consent applies only to the exact frozen candidate; no session-wide approval is supported. Checkboxes are not review approval.
- Recovery mirror: Engram topic `odd/tracked-v17-full-video-pilot/tasks`; full document plus this repository-relative locator.

## Tasks

- [ ] **T1 — Preserve the dependency-free selector.** Delegated direct: reading prepares a write and multiple nontrivial files. Promote frozen bytes, relocate 116 synthetic tests, add a standard-library-only import guard and usage docs. Acceptance: exact selector SHA-256 preserved, original CLI untouched, baseline and selector checks pass, no private artifacts promoted. Commit and native RDD evidence pending.
- [ ] **T2 — Preserve the optional style adapter.** Delegated direct; separate code/tests/docs unit. No dependency installation or default engine change. Determine exact surface and checks before writing.
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

T1 implementation and functional checks PASS; commit/RDD remain pending, so T1 is not checked off. Frozen selector SHA-256: `b679cf553ba75261b9c3af92ee6891be9e5d4b66bcefb3d0cc4dc7f48f694eb9` (522 lines, byte-identical). Twelve relocated test modules preserve all function/class ASTs and 116 methods; package imports replace the experimental dynamic loader. New import guard observed RED before promotion (missing tracked selector, exit 1), then GREEN with the tracked selector and all 116 tests; no algorithm change or artificial algorithm RED.

Observed checks from `apps/server`:

- Baseline full suite before promotion: 26 tests PASS.
- Required full suite after promotion: 142 tests PASS (26 existing plus 116 selector tests).
- Required focused selector suite: 116 tests PASS.
- Required standard-library guard: 116 tests PASS; NumPy, OpenCV and PaddleOCR imports rejected.
- Documented synthetic example: PASS (selected synthetic text, native audit unchanged, review required).
- Frozen portable core package before/after hashes: all unchanged; selector equality PASS.
- Public artifact scan: 18 allowed files, syntax and private-locator/transcript checks PASS; English synthetic fixtures manually inspected.
- `git diff --check`: PASS. No normalizer required; no private assets or models copied.

T1 authored forecast realized: 1,191 new/added lines before this progress update (including feature document); final parent commit count will supersede this intermediate count. Parent owns Git staging/commits and native review. T2–T5 are pending under the updated exactly-one-video scope. Next: parent spot check, work-unit commit and native RDD candidate consent. No video runtime was launched.
