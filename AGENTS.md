# Working in kotoba-capture

## Purpose and language

This repository explores a local, reviewable workflow for extracting Japanese subtitles from video to support language study and Obsidian note-taking. Repository artifacts stay in English; conversation with the user may be in Spanish.

## Before making changes

1. Read [the project brief](docs/project-brief.md) and the current task tracking before proposing or making project changes.
2. Confirm requested scope and permitted files with the user when they are not explicit. Keep work bounded and preserve unrelated changes.
3. For deterministic behavior changes, use proportionate ODD and test-first development. Add a meaningful failing test before implementation and verify it afterward. Do not invent or imply check evidence. Documentation-only changes can use structural checks.

## Current implementation and deferred product work

The approved T1–T3 prototype currently includes a dependency-free Python core, a development-only local FFmpeg/Tesseract runner, and a reference-assisted evaluation tool. This CLI is an experiment, not the final product. The intended local web application may later use TanStack Start with FastAPI, but no UI/API or Obsidian writer is implemented or authorized by this status alone. Furigana separation, translation, audio transcription, and automatic vocabulary work remain outside scope unless separately approved.

## Scope and privacy

- Prefer local processing. Never send video, images, extracted text, or the private reference to external services without explicit user approval.
- Keep video, note, OCR text, model files, crops, and detailed evaluation reports under the ignored `.local/` directory. Repository docs and handoffs may contain aggregate metrics only, never private transcriptions, images, or private absolute paths.
- Treat sampled times as approximate display times, not audio alignment. OCR confidence is an engine heuristic, not a calibrated correctness probability. Mark all text for human review; do not fabricate missing characters or claim furigana extraction.
- Do not commit, stage, push, publish, create remotes, or install dependencies without user authorization. The initial uv setup and Japanese model download were specifically approved for this prototype; that approval does not authorize other installations or network access.
- Do not introduce broad frameworks or unrelated refactors. Any additional preprocessing, detection, API, or UI work needs a separately approved bounded task.
