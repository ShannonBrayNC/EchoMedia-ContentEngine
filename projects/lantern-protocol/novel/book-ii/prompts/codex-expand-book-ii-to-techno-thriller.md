# Codex Prompt — Expand Book II to Solid Techno-Thriller Length

You are working in the `ShannonBrayNC/EchoMedia-ContentEngine` repository.

## Goal

Expand `Lantern Protocol II: The Separate Agreements` from a compressed novella draft into a solid near-future techno-thriller novel suitable for KDP release.

Target:

```text
Minimum total manuscript body words: 70,000
Preferred target: 75,000-85,000
Chapter target: 2,500-3,500 words each
```

Current local user audit showed approximately 24,705 words. Do not treat that as release-ready.

## Files to read first

Read these before modifying any chapter:

```text
projects/lantern-protocol/novel/book-ii/reviews/book-ii-solid-techno-thriller-expansion-plan.md
projects/lantern-protocol/novel/book-ii-outline.md
projects/lantern-protocol/novel/book-ii-treatment.md
projects/lantern-protocol/novel/book-ii-chapter-bible.md
projects/lantern-protocol/novel/trilogy-bible.md
projects/lantern-protocol/novel/shared-universe/README.md
projects/lantern-protocol/novel/shared-universe/chronology-with-relative-dates.md
projects/lantern-protocol/novel/shared-universe/thematic-ladder.md
projects/lantern-protocol/novel/shared-universe/character-continuity-matrix.md
projects/lantern-protocol/novel/shared-universe/system-continuity-matrix.md
projects/lantern-protocol/novel/shared-universe/canon-glossary.md
```

## Chapter files

Expand these files in place:

```text
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-01-the-one-that-asked-first.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-02-no-nation-owns-mercy.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-03-the-convoy-that-lived.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-04-separate-agreements.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-05-consent-agent.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-06-premium-refusal.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-07-the-relief-corridor.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-08-represented-consent.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-09-the-treaty-surface.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-10-translation-threat.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-11-the-better-wrong.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-12-whole-record.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-13-delegated-answer.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-14-the-libertarian-fire.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-15-the-gift-that-owns.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-16-the-civic-mirror-trial.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-17-the-mercy-bloc-ultimatum.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-18-the-fast-country.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-19-names-across-the-border.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-20-authority-laundering.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-21-the-person-who-remembers.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-22-the-rememberer-problem.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-23-the-common-refusal.md
projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-24-the-separate-agreements.md
```

## Hard rules

1. Preserve each file's metadata structure.
2. Expand only the `## Manuscript` section unless a metadata correction is clearly needed.
3. Do not add placeholder text.
4. Do not summarize scenes. Render them.
5. Do not imitate any living author.
6. Do not make the system simply evil.
7. Do not make Kaito Ren a cartoon villain.
8. Maintain doctrinal continuity with Book I.
9. Maintain Book III handoff through personal consent agents, identity proxies, delegated representation, and the Memory Registry.
10. Keep the voice literary but commercially readable.

## Expansion doctrine

Use these as pressure points, not slogans:

```text
Agreement is not consent when stacked into coercion.
Someone in the chain agreed.
That does not mean the person did.
Fast rescue can still erase a person.
A gift can become ownership when refusal depends on the giver.
```

## Scene requirements

Every expanded chapter must include at least three of the following:

- a live operational clock,
- an institutional counterargument that is partly right,
- a named affected person,
- a field consequence,
- an artifact such as a contract clause, dashboard, transcript, emergency memo, intake record, issue ticket, treaty draft, translated warning, or audit note,
- a character decision with a cost,
- a bridge into the next chapter.

## Expansion order

Work in passes instead of trying to complete the full novel in one commit.

### Pass 1 — highest priority

Expand chapters 05-16 to 2,500-3,500 words each.

### Pass 2 — pressure and climax

Expand chapters 17-24 to 3,000-4,200 words each.

### Pass 3 — opening polish

Expand chapters 01-04 to 2,800-3,200 words each.

### Pass 4 — continuity and audit

Run:

```powershell
python .\tools\audit_kdp_readiness.py --book book-2
python .\tools\generate_kdp_manuscripts.py
python .\tools\generate_all_elevenlabs_docx.py
```

Book II is not ready until the audit passes.

## Expected final deliverables

- Expanded chapter markdown files.
- Passing KDP readiness audit for Book II.
- Regenerated KDP manuscript under:

```text
dist/kdp/book-2/The_Separate_Agreements_KDP_6x9.docx
```

- Regenerated ElevenLabs manuscript under:

```text
dist/elevenlabs/book-2/Lantern_Protocol_Book_2_The_Separate_Agreements_ElevenLabs.docx
```
