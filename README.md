# kotoba-capture

A local-first project to help Japanese learners turn video subtitles into reviewable notes: listen and read along, transcribe Japanese text into Obsidian, and collect vocabulary they do not yet know.

## Status

This repository currently contains starter documentation only. There is no extractor implementation, selected OCR engine, or OCR reliability guarantee.

## Local quick path

From this repository, launch Pi locally:

```sh
pi
```

Ask it to read the project guidance and propose a bounded plan before any implementation. Do not provide video or other private material to external services without explicit approval.

## Project documents

- [Agent and contributor guidance](AGENTS.md)
- [Project brief, proposed pipeline, and limitations](docs/project-brief.md)

## Next step

Choose a short representative sample and define a bounded prototype plan, including how to evaluate OCR and compare output against a manually checked reference. Sample media, OCR engine, and product thresholds are still undecided.

Ready-to-paste prompt for the next session:

> Lee `AGENTS.md` y `docs/project-brief.md`. Antes de implementar nada, propón un plan acotado para un prototipo basado en una muestra corta y representativa. Incluye decisiones pendientes, criterios de evaluación frente a una referencia revisada manualmente, riesgos y archivos que tocarías. No escribas código ni modifiques archivos hasta que yo apruebe explícitamente el plan.
