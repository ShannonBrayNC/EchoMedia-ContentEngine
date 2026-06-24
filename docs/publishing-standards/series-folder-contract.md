# Series Folder Contract

**Sprint:** PUB-001  
**Status:** Active standard  
**Owner:** Lantern Publishing / EchoMedia Content Engine

## Purpose
This contract defines how universes, series, trilogies, anthologies, case-file collections, and individual books are organized. It supports hundreds of books without losing canon, production status, or publishing readiness.

## Canonical Series Path

```text
projects/<universe-slug>/series/<series-slug>/
```

Example:

```text
projects/lantern-universe/series/silver-bullet-trilogy/
```

## Required Series Structure

```text
<series-slug>/
├── README.md
├── metadata.yaml
├── series-bible/
├── books/
│   ├── book-01-<slug>/
│   ├── book-02-<slug>/
│   └── book-03-<slug>/
├── continuity/
├── producer-review/
├── publishing-package/
└── marketing/
```

## Folder Responsibilities

### README.md
Human-readable entry point for the series. Must describe premise, genre, production status, canon relationship, and book list.

### metadata.yaml
Machine-readable series registry record.

### series-bible/
Series premise, recurring themes, major arcs, rules, antagonists, motifs, and recurring symbols.

### books/
Canonical home for each book. Books must follow the Book Folder Contract.

### continuity/
Cross-book continuity notes, timeline conflicts, unresolved mysteries, character state changes, and canon dependencies.

### producer-review/
Series-level Producer Review findings and approval records.

### publishing-package/
Series-level metadata, trilogy/collection descriptions, box-set planning, reader order, and vendor package references.

### marketing/
Series positioning, launch strategy, visual identity, comparison titles, reader promises, and audience segments.

## Series Types
Supported series types:

- `standalone`
- `duology`
- `trilogy`
- `anthology`
- `case-files`
- `shared-universe-series`
- `novella-collection`

## Required Series Metadata
Every series must include:

- `series_id`
- `title`
- `universe_id`
- `series_type`
- `status`
- `canon_status`
- `primary_genre`
- `book_count_planned`
- `book_count_active`
- `producer_review_status`
- `release_strategy`

## Scale Rule
No book should be placed directly under `projects/` once assigned to a universe or series. All production content must be discoverable through the universe and series registry.

## Governance Rule
Series-level changes that alter canon, chronology, major characters, IP risk, likeness risk, or release sequencing require Producer Review before release packaging.
