# Establish an isolated PaddleOCR GPU runtime

Create a local, isolated GPU runtime for a later pilot without changing the stopped CPU pilot, source code, environment files, models, or private run evidence.

## Authorization and boundaries

The user authorizes a new runtime only under `.local/ocr-probes/paddleocr-gpu/` and compatible dependency downloads. Do not overwrite an existing target. Do not edit source, `.env`, existing CPU runtime, model assets, videos, OCR output, or stopped CPU evidence. Do not run inference, download models, process private video, commit, stage, push, or use SSH.

The stopped Prometheus CPU attempt remains preserved at 513/2,608 durable samples and 514 frames. Its runtime identity must not be treated as interchangeable with the new GPU runtime.

## Compatibility decision

Use Python 3.13.14 in the new venv. Pin `paddleocr==3.7.0`, `paddlex==3.7.2`, and `paddlepaddle-gpu==3.3.1` from Paddle's CUDA 12.9 package index if the isolated resolver can satisfy the pins without substitutions. PaddleOCR 3.7.0 requires PaddleX in the `>=3.7.0,<3.8.0` range; PaddleOCR documents PaddlePaddle 3.0+ as its framework minimum. Paddle's official CUDA 12.9 index lists the CPython 3.13 Linux x86_64 wheel for PaddlePaddle GPU 3.3.1. These pins retain the existing CPU pilot's application package versions while changing only the isolated framework build from CPU to GPU.

Official references:

- https://www.paddlepaddle.org.cn/documentation/docs/en/install/index_en.html
- https://www.paddlepaddle.org.cn/packages/stable/cu129/paddlepaddle-gpu/
- https://paddlepaddle.github.io/PaddleOCR/main/en/quick_start.html
- https://github.com/PaddlePaddle/PaddleOCR/blob/main/pyproject.toml

## Forecast and checks

- Forecast before install: reserve up to 8 GiB for the isolated venv, package cache, and unpacked GPU dependencies. Exact Paddle GPU wheel content length was not available from the official index's HTTP metadata; this is a conservative capacity reserve, not an observed download size. Available local space before setup: 263 GiB.
- No model download or OCR inference is authorized in this task.
- Task 1 uses a compatible isolated setup; strict behavior TDD is not applicable because no product behavior changes.
- Task 2 uses a functional GPU smoke proof: package metadata, CUDA compilation support, CUDA device count, `gpu:0` selection, and a tiny synthetic tensor computation followed by synchronization.

## Tasks

- [x] **G1 — Build the compatible isolated runtime.** Route: delegated. Created the previously absent target with Python 3.13.14 and installed the stated pins without substitution: PaddleOCR 3.7.0, PaddleX 3.7.2, and PaddlePaddle GPU 3.3.1. `pip check` reports no broken requirements. Private installer output is under `.local/ocr-probes/paddleocr-gpu/logs/install.log`; no model assets were downloaded.
- [x] **G2 — Prove basic GPU execution without private inputs.** Route: delegated. Paddle reports CUDA compilation support and one visible device. A tiny synthetic tensor ran on `gpu:0`, synchronized, and produced `[8.0, 12.0]`. Private proof is under `.local/ocr-probes/paddleocr-gpu/logs/gpu-smoke.log`; no OCR package import, model initialization, video, image, or inference occurred.

## Acceptance and verification

- The isolated runtime reports PaddleOCR 3.7.0, PaddleX 3.7.2, PaddlePaddle GPU 3.3.1, NumPy 2.3.5, and OpenCV contrib 4.10.0.84 through distribution metadata.
- The target-listed NumPy and OpenCV versions match the stopped CPU runtime's recorded identity; this does not establish equivalent OCR output across CPU and GPU builds.
- Paddle reports CUDA compilation support and one device; the smoke operation selected `gpu:0`, synchronized, and produced the expected synthetic result.
- The stopped remote CPU package/file identity was not re-audited from this local workspace: no SSH, CPU runtime, run artifact, model, source, or environment file was accessed or modified. The local global Python 3.13 installation remains free of Paddle/OCR/NumPy/OpenCV distributions.
- `pip check` and `git diff --check` passed. Concise status shows only this uncommitted tracker; private runtime artifacts remain ignored.

## Recovery and delivery

- Locator: `odd/tasks/gpu-runtime-migration.md`; parent owns the Engram mirror `odd/gpu-runtime-migration/tasks`.
- No commit is authorized. If setup fails or semantics are uncertain, preserve only private diagnostic logs beneath the allowed `.local` directory and report the exact unresolved compatibility issue.
- Actual isolated footprint after setup: 16,335,050,882 bytes (10,190,331,107-byte venv plus 6,144,687,603-byte private pip cache). The original 8 GiB reserve underestimated cache plus installed GPU dependencies; about 249 GiB remained free after setup.
- Setup completed without a model/runtime compatibility blocker. The GPU proof only establishes framework/device execution, not OCR compatibility or pilot authorization.
- Next step: parent reads back and mirrors the completed tracker. Any later pilot must register a separate runtime identity and preserve the stopped CPU evidence.

## Authorized runner and sample comparison extension

The user subsequently authorized explicit GPU support in the runner with tests and a small same-model OCR timing/output comparison. This extends the original setup-only boundary for the tasks below. No full-video execution, model replacement/download, SSH, staging, commit, push, or private-data transmission is authorized. Existing CPU evidence and the three core environment settings must remain untouched.

- [x] **G3 — Enable explicit GPU configuration and frozen identity.** Route: delegated; non-trivial changes to configuration, runtime identity, and synthetic tests triggered the writer route. `KOTOBA_PILOT_DEVICE` now accepts only `cpu` (default) or `gpu:0`; the frozen configuration and runtime identity retain the selected device and `paddlepaddle`/`paddlepaddle-gpu` distribution. GPU initialization verifies CUDA compilation and a visible device before OCR, refuses a wrong backend or unavailable GPU, and has no CPU fallback. Preflight/register remain ML-import-free. The source change intentionally makes historical plans incompatible: use a new output name rather than migrating stopped CPU evidence. RED: added device, GPU constructor, backend identity, unavailable-GPU, and changed-device freeze tests failed before implementation (36 test suite errors/failures for absent config device, hard-coded CPU constructor, unchanged freeze, and old identity signature). GREEN: `PYTHONPATH=. /usr/bin/python3 -B -S -m unittest discover -s tests -p 'test_*pilot*.py' -v` passed 36 tests; full discovery passed 187 tests with 9 optional NumPy/OpenCV skips; `tests/check_selector_stdlib.py` passed 116 tests; CLI `--help` and `git diff --check` passed. No formatter was run or required.
- [x] **G4 — Compare at most five existing snapshots.** Route: delegated; one paired, offline run used three aligned existing positive snapshots and two aligned existing negative snapshots, with the same five inputs in order, the existing CPU model directories, FP32/no-TRT/no-CINN/MKLDNN-disabled adapter settings, and the tracked selector policy. It used the exact `LocalRuntime.initialize`/`predict` adapter and selector path; detailed native OCR/selected outputs and identities are private under `.local/gpu-runner-benchmark/run-20261011-g3/`. CPU and GPU model identities were equal before/after their runs, and the same model tree identity was observed across runs. Aggregate only: initialization was 2.190s CPU and 2.131s GPU; total five-image post-initialization time was 27.025s CPU and 4.127s GPU; first-image total was 3.964s CPU and 0.584s GPU. Native text, boxes, polygons, and detections matched exactly for all five inputs; confidence arrays differed on all five; selected text and status matched for all five. This is one small local measurement, not an accuracy or speed guarantee and not a full-video evaluation. No downloads, retries, tuning, frame extraction, CPU partial changes, or network transmission occurred.

Acceptance: explicit device/backend synthetic tests pass; GPU package identity can be inspected without ML imports; changing device/backend invalidates resume; actual GPU OCR initialization and prediction are observed on the bounded sample; aggregate timing and output differences are honestly reported. Any failed, unavailable, or pending proof remains recorded.

Forecast: approximately 150–250 authored additions/deletions, excluding ignored benchmark artifacts. Delivery strategy: `ask-on-risk`; no PR or commits currently authorized. The parent owns the full Engram mirror before source writes and after each task. RDD is on, but candidate review consent is separate and not inherited.

## Committed runner and authorized full-video GPU test

The user explicitly authorized a commit followed by starting the same single H01 video test. Commit `b56f1b627db192a94d98366f17cbd5534dd3e259` contains the eight reviewed code/test/config/document files, with 154 additions and 14 deletions. Its tree exactly matches the reviewed immutable candidate `d3dd33be3801bebe776065474a7d7d28ccbaaa03`; native review completed without findings and its exact acknowledgement burned authority. The subsequent committed-only assessment was medium, `review_due=false`, reason `under_budget`; it does not replace the completed workspace review. No push or PR was requested or performed.

- [x] **G5 — Start one fresh frozen H01 GPU video test.** Route: delegated; private configuration/asset inspection and foreground execution belong to one bounded worker. Confirm the existing H01 source content, model and policy identities against historical private evidence, preserve CPU partials and all three core environment settings, use the isolated GPU interpreter and process-only `KOTOBA_PILOT_DEVICE=gpu:0`, and require a fresh output name and frozen runtime identity. Run ML-import-free preflight before registration, give one timing/resource forecast before launch, register once, execute once in the foreground, and retain recoverable private outputs. Do not resume historical CPU plans, download models, tune the engine, process another video, or use SSH. Record actual progress, phase timings, interruptions, and terminal status honestly; processing completion alone is not an accuracy or visual-review verdict.

Private GPU execution evidence belongs under `.local/gpu-full-video-pilot/` and the fresh run output under `.local/v17-full-video-pilot-gpu-h01-r1/`. Missing or mismatched assets block launch rather than permitting substitutions. Full-run reliability acceptance still requires the existing separate visual/reference checks; do not claim those from processing or from the five-image benchmark. The parent mirrors this extension before registration and records observed execution evidence afterward. GPU test and metadata are authorized locally; no push, PR, second video, installations, or source changes are authorized by this extension.

## Historical G5 execution checkpoints

The fresh GPU plan registered once with 2,608 samples at a 0.5-second cadence for the existing H01 input. Its frozen source, model, and policy identities matched the preserved CPU evidence; the selected runtime is `gpu:0` with the GPU Paddle distribution. Readback before launch confirmed zero attempts, records, frames, initializations, and predictions.

A first execute invocation was refused before creating an attempt because its reconstructed arguments omitted the runner's explicit `--resume` requirement for an already registered output. It made no OCR/runtime changes. After parent verification, the exact stored execute declaration—with `--resume` bound only to this fresh GPU plan—launched one foreground attempt. This is an argument correction before any OCR attempt, not a CPU resume or an OCR retry.

First-five checkpoint: five durable records, one model initialization, and no reliability or visual-review verdict. The first five completed-record phases totaled 1.983 seconds extraction, 1.257 seconds OCR, 0.233 seconds style measurement, and 0.016 seconds selection; these are early processing observations only.

Historical checkpoint: 611/2,608 durable records, one active foreground attempt, one model initialization, and 611 entered predictions/style measurements/selections. Accumulated phases: initialization 2.064 seconds, extraction 302.178 seconds, OCR 97.031 seconds, style 29.564 seconds, and selection 1.033 seconds. At that checkpoint the process was in progress and G5 was incomplete; the terminal result below supersedes that execution status. Processing does not establish visual accuracy or full-video reliability.

Private aggregate proof locators: `.local/gpu-full-video-pilot/preflight/phase-b-registration-summary.json`, `first-five-checkpoint.json`, and `progress-0611.json`. Detailed run data remains only under the ignored fresh output directory.


## G5 terminal processing checkpoint

The single corrected foreground GPU attempt reached **2,608/2,608 durable records and frames** and completed with one model initialization, 2,608 entered predictions, 2,608 style measurements, 2,608 selections, and zero interrupted calls. The corrected invocation used the already registered fresh GPU identity; it did not register again or resume either CPU partial. Final recorded phase times: initialization 2.064 seconds, extraction 1,312.773 seconds, OCR 408.222 seconds, style 125.328 seconds, selection 3.600 seconds, export 0.031 seconds, and integrity 3.308 seconds; total attempt elapsed time was 1,964.346 seconds.

Final readback confirms the frozen identity still matches current source/runtime inputs and the historical source, model, and policy identities; the selected device remains `gpu:0` with the GPU Paddle distribution. No pilot process remains. The core environment and preserved CPU evidence were only read; neither was changed by this worker. Detailed execution artifacts remain ignored under `.local/`.

This is a processing-completion checkpoint only. All extracted text remains for human review; no visual adjudication, accuracy verdict, or full-video reliability acceptance was performed. Private aggregate terminal proof: `.local/gpu-full-video-pilot/preflight/terminal-summary.json`.
