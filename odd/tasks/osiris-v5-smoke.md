# Osiris frozen-v5 single-image smoke

## Objective and authorization
Repair copied interpreter relocation without installation, then run frozen v5 on exactly one existing N01 image to verify local readiness. User explicitly authorizes diagnosis/repair on failure. No commits, staging, push, network, downloads, source/config changes, or consumed batch-guard resets are authorized.

## Scope and routing
- Interpreter alias, venv/bin/python and venv/pyvenv.cfg only for relocation.
- New private backups, harness and outputs under ignored `.local/osiris-smoke/`.
- This tracker and Engram topic `odd/osiris-v5-smoke/tasks` contain aggregate evidence only.
- Route: delegated direct for R1/R2; environment repair, preparation and command execution trigger delegation.
- Forecast: under 100 public tracking lines; private harness excluded from publication. Delivery strategy: ask-on-risk; commits explicitly not authorized by project policy.

## Tasks
- [x] R1: Back up original links/config, observe broken-interpreter RED, relocate two link targets/config, verify interpreter and existing package imports without network.
- [x] R2: Pin frozen selector/config/models/N01, create fresh one-shot harness, initialize once and predict exactly once, retain full native/selector output privately, verify unchanged identities and aggregate summary.

## Acceptance and checks
Interpreter and required imports work; exactly one initialization/prediction completes successfully; explicit frozen `select_caption_profile_v5` used; source/config/model/image hashes unchanged; output review-required. No second OCR for verification. Run `git diff --check` and bounded Git status. Parent independently checks interpreter and summary only. Existing deterministic failure provides RED; no behavioral selector changes need new selector RED. New guard must refuse replay before ML imports.

## Evidence and next step
Baseline configured venv interpreter failed with exit 127; bundled CPython 3.13.14 works. Four broken links trace to two old absolute-root targets. Source/config match frozen tracking. Repair and exactly-one smoke completed; old batch guards remain consumed.

R1 evidence: re-observed interpreter RED exit127, then GREEN Python3.13.14 and offline package imports exit0 (NumPy2.3.5/Paddle3.3.1/PaddleOCR3.7.0). Private original-links.json/pyvenv.cfg backups retained. Two relative-link changes and relocated config home; no installs. No-ML identity/model/image preflight exit0. Package import emits existing missing-ccache/10-thread warnings; no failure.

R2 evidence: new one-shot guard refuses replay before ML; exact execute exit0,1initialization/1prediction,11.98seconds. Frozen v5 same-row-fragment-retry selected3of4native detections; normalized complete-output13characters,0/13edits,exact reference match. No consolidation attempted; this tests v5 entrypoint/environment, not independent fragment-fix coverage. Full native/selector output,ledger/summary/identity logs retained under ignored .local/osiris-smoke/results/. Source/config/helper/image/sixmodelassets verified before/after; all text review-required. No network,install,extraOCR,selectorchanges or Gitmutations.

Commands: `.local/ocr-probes/paddleocr-cpu/venv/bin/python --version`; same interpreter with `-B .local/osiris-smoke/run.py imports`, `preflight`, then once-only `execute`. Do not rerun execute. Functional smoke complete; parent independent Python version and summary SHA-256 readback passed, matching 3656b7e89f2f82f238750efe6626ed10c26b13647712be96b928e65c940b3f83. git diff --check passed. Next project recommendation remains bounded non-blue inspection or separately authorized position coverage (odd/tasks/caption-selector-v5-signage-negatives.md:31).
