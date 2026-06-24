# Repository Recovery Plan

**Sprint:** PUB-002  
**Status:** Active recovery plan  
**Owner:** Lantern Publishing / EchoMedia Content Engine

## Purpose
Recover EchoMedia Content Engine from repository drift while preserving useful work. The target state is a governed publishing operating system capable of supporting hundreds of books, multiple universes, and repeatable AI-assisted production.

## Recovery Principles
1. Preserve first, delete later.
2. Do not merge divergent content wholesale.
3. Classify all drift before moving it.
4. Use canonical folders for new work.
5. Require metadata for book, series, and universe artifacts.
6. Route publishing-impacting work through Producer Review.

## Drift Categories

### Platform Drift
Code, services, scripts, schemas, provider integrations, UI, and automation files that belong under platform areas.

### Publishing Drift
Book, series, canon, character, manuscript, marketing, or production artifacts that belong under `projects/`.

### Experimental Drift
Prototype material that may be useful but is not production-ready.

### Deprecated Drift
Obsolete work retained for traceability but excluded from active pipelines.

## Target Top-Level Areas

```text
config/
docs/
projects/
schemas/
services/
scripts/
templates/
ui/
tests/
archive/
```

## Archive Strategy
Use `archive/drift-recovery/` for recovered legacy content that should not be lost but is not yet approved for canonical placement.

```text
archive/drift-recovery/<date>/<source-area>/
```

Each migrated item should include a short note explaining:

- original location
- recovery classification
- proposed destination
- whether Producer Review is required

## Canonical Publishing Destination
All Lantern fiction work should move toward:

```text
projects/lantern-universe/
```

All series should move toward:

```text
projects/lantern-universe/series/<series-slug>/
```

## Recovery Workflow
1. Inventory current repo contents.
2. Classify each area as platform, publishing, experimental, deprecated, or unknown.
3. Move obvious platform material into platform folders.
4. Move publishing material into universe/series/book folders.
5. Archive uncertain material.
6. Add metadata and README files to every active production area.
7. Validate with folder contracts and schemas.
8. Close recovery sprint only after main is stable.

## Non-Negotiable Rules
- Do not delete unknown content during recovery.
- Do not place books directly under root or generic content folders.
- Do not treat manuscripts as approved without canon/proofread review.
- Do not treat generated assets as release-ready without Producer Review and publishing package validation.

## Completion Definition
Repository recovery is complete when active work is discoverable through registries, drift is archived or migrated, and new book/series creation follows templates instead of ad hoc folders.
