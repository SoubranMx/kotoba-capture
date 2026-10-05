# Working in kotoba-capture

## Purpose and language

This repository explores a local, reviewable workflow for extracting Japanese subtitles from video to support language study and Obsidian note-taking. Keep repository artifacts in English. Conversation with the user may be in Spanish.

## Before making changes

1. Read [the project brief](docs/project-brief.md) and [the current task tracking](odd/tasks/project-bootstrap.md) before proposing or making project changes.
2. Confirm the requested scope and permitted files with the user when they are not explicit. Keep work bounded and preserve unrelated changes.
3. For future deterministic behavior changes, use proportionate ODD and test-first development: define observable behavior, add a meaningful failing test before implementation, and verify it afterward. Do not invent or imply check evidence that was not observed. Documentation-only changes can use structural checks instead.

## Scope and privacy

- Prefer local processing. Do not send video, images, or extracted text to external APIs without explicit user approval.
- Do not commit, push, or install dependencies without user authorization. Do not create remotes or publish without explicit authorization.
- Keep the first prototype focused on extracting and reviewing Japanese text. Translation, grammar instruction, APIs, UI, and audio transcription are outside its initial scope unless separately approved.
- Do not introduce broad frameworks or a UI by default. Propose the smallest approach that meets an approved prototype goal.
- Treat proposed technologies and capabilities as plans, not implemented facts. See the brief for limitations and pending decisions.
