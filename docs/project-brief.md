# Project brief

## Goal

Help a Japanese learner study from video by reading subtitles and collecting reviewable text for later note-taking. The system should support human review, not claim perfect transcription or diagnose which vocabulary a learner knows.

## Subtitle and video characteristics

Subtitle backgrounds vary: blue, gray, or absent. Text position, size, and line count are relatively stable in some stretches but can vary. Frames may contain several adjacent lines or simultaneous interventions, and the camera may pass Japanese signage that resembles subtitles. These are evaluation risks, not cues the current prototype claims to solve.

## Intended product direction

The longer-term local application is expected to be a monorepo with a TanStack Start web interface and a FastAPI service. That product UI/API is future work, not part of the current prototype. The present implementation is a development CLI and dependency-free Python core for sampling, conservative consecutive grouping, local review exports, and comparison with a manual reference.

## Current prototype behavior

1. FFmpeg samples requested timestamps; the current evaluation used a full-frame baseline at 0.5-second intervals over the first 214 seconds.
2. Tesseract OCR output is retained as sampled observations with crop links and engine-provided confidence where available.
3. Only consecutive equivalent nonblank text is grouped. Equivalence is Unicode NFKC plus whitespace normalization; original text is retained. Later repetitions remain separate.
4. JSON and UTF-8 Markdown exports mark all OCR text for review. Approximate sample intervals are not audio alignment.
5. A local evaluation compares a deterministic modal OCR string within each timestamped reference window to the manually transcribed text using character-level edit distance.

The pipeline does not detect subtitle regions, assume a particular background color, separate furigana, identify signage, infer missing characters, translate, transcribe audio, or write to Obsidian. The full-frame run is an exploratory baseline, not a reliability guarantee.

## Interpretation limits

Sampling can miss brief subtitle changes. A reference window may cover several changing subtitle screens, while the evaluation chooses one modal sampled snapshot; its CER can therefore overstate error or miss text that appeared briefly. Reference-assisted modal-window CER is not subtitle-detection recall, and unassigned samples are not classified as signage. OCR confidence is not calibrated correctness probability. No audio alignment is provided.

## Prototype evaluation

The approved sample run, aggregate-only results, methodology, limitations, and next bounded recommendation are in [prototype-evaluation.md](prototype-evaluation.md). The observed results are poor and do not meet the provisional 10% modal-window CER diagnostic. The proposed 95% phrase-coverage goal was not measured as detection recall and is not an approved guarantee.

## Deferred work

Any web UI/API, subtitle-region detection, furigana separation, visual classification of signage, translation, audio transcription, Obsidian writes, or broader video evaluation requires a separately approved task. Manual checks of signage, furigana, reading order, timing, and export usefulness remain pending.
