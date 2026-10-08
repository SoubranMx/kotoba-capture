# kotoba-capture

A local-first experiment for turning Japanese video subtitles into reviewable text for language study. The current implementation is an exploratory Python extraction/evaluation core with a development CLI; it is not the intended finished product and makes no OCR reliability guarantee.

## Current status

- T1–T3 prototype core is implemented: deterministic observation grouping/exports, local FFmpeg/Tesseract sampling, and reference-assisted evaluation.
- The approved 214-second full-frame baseline has been run and evaluated locally. Its modal-window diagnostics are poor; every output still requires human review.
- No web UI/API, Obsidian writing, translation, furigana separation, or audio transcription is implemented.

## Quick path

Read the [prototype evaluation and run guide](docs/prototype-evaluation.md) for the sample protocol, aggregate results, limitations, and exact local commands. The dependency-free Python core and offline unittest command are documented in [apps/server](apps/server/README.md).

## Project documents

- [Agent and contributor guidance](AGENTS.md)
- [Project brief and interpretation limits](docs/project-brief.md)
- [Prototype evaluation, results, and next step](docs/prototype-evaluation.md)

Video, the manually checked reference, OCR text, model data, crops, and detailed evaluation reports are local-only. Do not send them to hosted services or include transcriptions/images in repository-facing reports.
