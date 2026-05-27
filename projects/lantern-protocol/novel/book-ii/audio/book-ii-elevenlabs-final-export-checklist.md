# Lantern Protocol II: ElevenLabs Final Export Checklist

Issue: #122

Purpose: Prevent internal scaffolding, processing notes, and non-reader artifacts from leaking into the final Book II manuscript prepared for ElevenLabs, ElevenReader, Studio upload, Word export, or audiobook narration.

Book: **Lantern Protocol II: The Separate Agreements**

Canon lock: Book II uses the approved **24-chapter** structure. No 25th chapter should appear in the final reader-only export unless a future canon issue explicitly changes the Book II structure.

Primary doctrine: Agreement is not consent when stacked into coercion.

## Required Final Export Shape

The final reader-only manuscript must contain only:

1. **Book title**
2. Optional reader-facing preface / reader note
3. **Chapter 1 through Chapter 24**, in canon order
4. Reader-facing prose and approved audio-safe artifact inserts only

The final export must not contain internal production sections, processing metadata, placeholders, TODOs, scaffolding notes, JSON, raw code, or agent instructions.

## ElevenLabs Formatting Gate

Before upload, validate formatting in the final Word/reader manuscript:

- [ ] Book title is bolded.
- [ ] Every chapter heading is bolded.
- [ ] Chapter headings are consistent and readable.
- [ ] Chapter order matches the 24-chapter canon lock.
- [ ] No duplicate chapter headings exist.
- [ ] No placeholder chapter title remains.
- [ ] No internal section heading appears in the reader manuscript.

Recommended chapter heading format:

```text
**Chapter 01 — The One That Asked First**
```

Recommended book title format:

```text
**Lantern Protocol II: The Separate Agreements**
```

## Canon Chapter Order

- [ ] Chapter 01 — The One That Asked First
- [ ] Chapter 02 — No Nation Owns Mercy
- [ ] Chapter 03 — The Convoy That Lived
- [ ] Chapter 04 — Separate Agreements
- [ ] Chapter 05 — Consent Agent
- [ ] Chapter 06 — Premium Refusal
- [ ] Chapter 07 — The Relief Corridor
- [ ] Chapter 08 — Represented Consent
- [ ] Chapter 09 — The Treaty Surface
- [ ] Chapter 10 — Translation Threat
- [ ] Chapter 11 — The Better Wrong
- [ ] Chapter 12 — Whole Record
- [ ] Chapter 13 — Delegated Answer
- [ ] Chapter 14 — The Libertarian Fire
- [ ] Chapter 15 — The Gift That Owns
- [ ] Chapter 16 — The Civic Mirror Trial
- [ ] Chapter 17 — The Mercy Bloc Ultimatum
- [ ] Chapter 18 — The Fast Country
- [ ] Chapter 19 — Names Across the Border
- [ ] Chapter 20 — Authority Laundering
- [ ] Chapter 21 — The Person Who Remembers
- [ ] Chapter 22 — The Rememberer Problem
- [ ] Chapter 23 — The Common Refusal
- [ ] Chapter 24 — The Separate Agreements

## Internal Scaffold Block List

The following headings or content types must be removed from the final reader-only export:

- [ ] Canon Sources
- [ ] Purpose
- [ ] POV
- [ ] Chapter Promise
- [ ] Continuity Notes
- [ ] Revision Notes
- [ ] Processing Metadata
- [ ] Drafting Notes
- [ ] Agent Notes
- [ ] Implementation Notes
- [ ] TODO markers
- [ ] FIXME markers
- [ ] Placeholder manuscript text
- [ ] JSON blocks
- [ ] Code blocks
- [ ] Raw path references
- [ ] Issue numbers or PR references
- [ ] Audit status text
- [ ] Build logs or script output

Allowed exception: A code-like or record-like artifact may remain only if it has been intentionally converted into a reader-facing, audio-safe story insert.

## Preface / Reader Note Gate

The preface or reader note must be reader-facing only.

Validate:

- [ ] Does not mention GitHub issues, branches, PRs, scripts, or internal scaffolding.
- [ ] Does not explain the production process.
- [ ] Does not include editorial notes to the author or drafting agents.
- [ ] Can be read aloud naturally.
- [ ] Introduces only what a reader/listener needs.

## Artifact Insert Audio Gate

Book II uses procedural artifacts, but audiobook export must stay listenable.

Before upload, each artifact insert must pass:

- [ ] It is short enough to read aloud without fatigue.
- [ ] It has a clear speaker, source, or context.
- [ ] It reveals story pressure, human consequence, or consent failure.
- [ ] It does not appear as a raw table.
- [ ] It does not appear as raw JSON.
- [ ] It does not rely on visual alignment to make sense.
- [ ] It does not repeat information already explained in nearby prose.

Preferred audio-safe artifact forms:

- short transcript
- field memo
- public statement excerpt
- hearing testimony excerpt
- consent prompt read in plain language
- compact or refusal text
- brief record fragment converted into prose

## Cleanup Search Terms

Before final export, search the assembled manuscript for these terms and remove or convert anything that is not reader-facing:

```text
Canon Sources
Continuity Notes
Revision Notes
Processing Metadata
TODO
FIXME
PLACEHOLDER
TBD
JSON
script
scaffold
agent
GitHub
issue
PR
branch
exportsDir
reportsDir
manuscriptDir
```

Also search for Markdown/code markers:

```text
```
{
}
[]
```

Do not remove braces or brackets from legitimate prose automatically; use this as a review trigger.

## ElevenLabs Upload Readiness

Before uploading to ElevenLabs / ElevenReader / Studio:

- [ ] Final manuscript is in a single upload-ready file.
- [ ] Title is bolded.
- [ ] All chapter headings are bolded.
- [ ] Chapter order is 1-24 only.
- [ ] No internal scaffold sections remain.
- [ ] No TODO, FIXME, TBD, or placeholder text remains.
- [ ] No processing metadata remains.
- [ ] No raw JSON or code blocks remain.
- [ ] Artifact inserts are audio-safe.
- [ ] Preface / reader note is reader-facing only.
- [ ] File contains only title, reader note/preface if used, and manuscript chapters.
- [ ] The document has been opened and visually checked before upload.

## Reusable Checklist for Book I and Book III

This checklist can be reused for Book I cleanup and Book III production with these substitutions:

- Replace the book title.
- Replace the chapter count and canon chapter order.
- Recheck which artifact types are audio-safe for that book.
- Keep the same hard block against internal notes, metadata, TODOs, scripts, and code blocks.
- Keep bold formatting for title and chapter headings.

## Final Human Review Statement

Before upload, the reviewer should be able to say:

```text
This manuscript contains only reader-facing material. The title and chapter headings are bolded. The chapter order matches the canon structure. Internal scaffold sections, processing metadata, TODOs, JSON/code blocks, and agent notes have been removed or converted into audio-safe prose.
```
