# Project brief

## Goal

Help a Japanese learner study from video by listening and reading Japanese subtitles, transcribing them into Obsidian, and collecting vocabulary they do not know. The desired output is reviewable, not a claim of perfect transcription or automatic vocabulary diagnosis.

## What the subtitles look like

The main Japanese text is white, with smaller furigana, on translucent blue rectangles. Rectangles usually sit in the upper part of the frame, but their size and position vary. A frame may contain several adjacent rectangles or multiple quoted interventions at once. The camera also moves past Japanese signage, which can resemble subtitle text.

Two clipboard images were supplied as temporary evidence. They are not durable project fixtures and must not be copied into the repository.

## Proposed first-prototype workflow

Python, FFmpeg, and OpenCV are proposed building blocks; no extractor exists yet, and the OCR engine is undecided.

1. Prefer an existing subtitle track when available. Otherwise sample video frames with timestamps. A 0.5-second initial sampling interval is only a trial: it can miss shorter subtitles.
2. Detect candidate blue regions using multiple visual cues, not color alone. Support variable and multiple regions, ordered for reading.
3. Crop at original resolution. Compare text-shaped features across frames rather than relying on the moving background.
4. OCR the main text and furigana separately when possible, preserving relative positions and confidence if the engine supports them.
5. Deduplicate only consecutive equivalent segments. A phrase repeated later should remain. Preserve a representative crop and approximate on-screen interval.
6. Mark uncertain text for review; never invent missing characters. Export reviewable UTF-8 Markdown and optionally structured segment data. Apply language enrichment only after user review.

## Interpretation limits

Displayed subtitle times are not audio alignment. A group interval does not align its individual interventions to the audio. The system cannot guarantee OCR reliability or automatically know which words the learner does not know. Sampling may miss brief subtitles; signage may contaminate results; furigana can be mixed with main text.

## First evaluation milestone

Use a short, representative, user-supplied sample and a manually checked reference. Evaluate:

- Missing phrases, including brief appearances.
- Consecutive duplicates and preservation of later repeated phrases.
- Signage contamination and region/reading order.
- Furigana mixed with main text and confidence/uncertainty handling.
- Approximate display timing and usefulness of the reviewable export.

Sampling interval, thresholds, output details, acceptable accuracy, and the OCR engine remain pending decisions. Agree on them against the sample; do not imply a reliability guarantee.

## Explicitly outside the first prototype

Translation, grammar instruction, external APIs, a UI, and audio transcription require separate approval. Any external transmission of video, images, or text requires explicit user approval.
