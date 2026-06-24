# Book Folder Contract

**Sprint:** PUB-001  
**Status:** Active standard  
**Owner:** Lantern Publishing / EchoMedia Content Engine

## Purpose
This contract defines the required folder structure for every book managed by EchoMedia Content Engine. It exists so hundreds of books can be discovered, validated, edited, reviewed, packaged, and published by humans, Codex, Christina, and future Lantern agents without ambiguity.

## Required Book Root
Every book must live under a series or collection root.

```text
projects/<universe>/series/<series-slug>/<book-slug>/
```

Example:

```text
projects/lantern-universe/series/silver-bullet-trilogy/book-01-silver-bullet/
```

## Required Folders
Each book root must contain the following folders:

```text
book-01-example/
├── manuscript/
├── chapters/
├── outlines/
├── characters/
├── locations/
├── research/
├── continuity/
├── producer-review/
├── publishing-package/
├── audiobook/
├── marketing/
└── metadata.yaml
```

## Folder Responsibilities

### manuscript/
Full-book manuscript exports, compiled drafts, proofread editions, and release candidates.

### chapters/
One file per chapter or scene unit. Chapter files should be stable enough for review, diffing, and targeted rewrite work.

### outlines/
Beat sheets, act structure, chapter summaries, plot maps, escalation plans, and rewrite plans.

### characters/
Book-local character notes. Shared or recurring character truth belongs in the universe character registry.

### locations/
Book-local setting notes. Shared locations belong in the universe location registry.

### research/
Research notes, source summaries, historical context, technical references, legal/medical/political sensitivity notes, and domain-specific grounding.

### continuity/
Continuity checks, cross-book references, timeline impacts, canon conflicts, and unresolved story dependencies.

### producer-review/
Producer Review checklists, approval notes, risk findings, revision directives, and final gate decisions.

### publishing-package/
Files prepared for publishing: synopsis, back cover copy, metadata exports, ISBN notes, format manifests, release checklist, and vendor-specific package assets.

### audiobook/
Narration plan, voice notes, pronunciation guides, audio scene segmentation, and audiobook production package.

### marketing/
Launch copy, blurbs, social copy, email copy, ads, visual prompts, trailer concepts, and reader-facing positioning.

## Required Metadata
Every book must include `metadata.yaml` at the book root. The metadata file must include at minimum:

- `book_id`
- `title`
- `series_id`
- `universe_id`
- `book_number`
- `status`
- `canon_status`
- `producer_review_status`
- `publishing_status`
- `primary_genre`
- `content_warnings`
- `rights_status`

## Status Values
Recommended book status values:

- `concept`
- `outlined`
- `drafting`
- `rewrite`
- `canon-review`
- `producer-review`
- `proofread`
- `publishing-package`
- `released`
- `archived`

## Governance Rule
No generated book artifact may be treated as final until it passes:

1. Canon review
2. Continuity review
3. Producer Review
4. Publishing package validation
5. Rights/release gate

## Scale Rule
The folder contract must remain stable across hundreds of books. Add new folders only through a publishing standards update, not ad hoc per-book drift.
