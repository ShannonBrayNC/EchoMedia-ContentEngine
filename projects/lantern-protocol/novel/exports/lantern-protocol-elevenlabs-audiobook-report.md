# Lantern Protocol — ElevenLabs Audiobook Export Report

**Status:** WARN
**Output DOCX:** `exports/Lantern_Protocol_Book_One_ElevenLabs.docx`
**Front matter files included:** 2
**Chapters included:** 24
**Reader-facing words exported:** 38806

## Validation Gates

- Book title is emitted with the Word `Title` style and explicit bold run formatting.
- Chapter headings are emitted with Word heading style and explicit bold run formatting.
- Chapter bodies are taken only from `## Manuscript` through the next continuity/revision section boundary.
- Internal planning sections are omitted from the audiobook export.
- Markdown code fences are normalized into styled in-world insert paragraphs.

## Findings

- Internal marker leaked into export text: `Continuity Requirements`.
