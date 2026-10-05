# Project bootstrap

## Objective
Initialize kotoba-capture as a standalone documentation-only project for extracting Japanese burned-in video subtitles into reviewable Obsidian notes.

## Scope and constraints
Create README.md, AGENTS.md, and docs/project-brief.md in English. The user additionally authorized a starter .gitignore. No extractor code, dependency installation, API calls, media copying, commits, remote, or publishing is authorized. The user selected the repository name and location. Python, FFmpeg and OpenCV are proposed; the Japanese OCR engine remains undecided and must be evaluated on representative samples. Existing clipboard screenshots are temporary evidence, not durable fixtures.

## Task
- [x] T1: Write and structurally verify the starter documentation and .gitignore. Route: delegated gentle-ai-worker for three documents; inline mechanical .gitignore addition; delegated gentle-ai-verify independent verification. Status: done.

## Acceptance and checks
Git initialized locally. All three documents exist and have valid local document links. Clearly distinguish planned capabilities from implemented ones. Preserve the agreed pipeline and known limitations. Provide a ready-to-use next-session prompt, without granting blanket future implementation authorization.

## Evidence
Target did not exist before initialization. `git init -b main` succeeded. Passive documentation has no meaningful test-first RED/GREEN; use structural readback and local-link checks instead. No commit identity: commits were not requested and will not be made.

## Delivery
Forecast: approximately 180 authored documentation lines. Strategy: ask-on-risk. No remote, push or pull request planned. Native review is skipped for this passive documentation-only bootstrap.

## Verification progress
Worker completed three documents and passed its nonempty-file/local-link checks. Parent read back documents and verified .gitignore exclusions plus trackable .env.example, README.md and tests/fixtures/sample.png. Native assessment was unavailable because all files are untracked; its returned plan required independent verification. Independent verifier passed nonempty-file and inline local Markdown link checks (fenced blocks excluded), ignore-pattern checks, and confirmation that docs, .env.example and prospective fixtures remain trackable. Git lists exactly five untracked starter files, with no implementation. Link checks do not cover all Markdown syntaxes. No review transaction was started.

## Next step
Bootstrap complete. Open Pi in this repository and authorize a bounded sample-based extraction prototype. Media input and OCR choice remain pending.
