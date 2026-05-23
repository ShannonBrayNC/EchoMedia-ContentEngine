# Phase 2 Sprint 5 — Screenplay Conversion and Movie Workflow

## Objective

Build the screenplay conversion and cinematic production orchestration layer.

The system must convert approved chapter material into:

- screenplay scenes
- Fountain-compatible screenplay exports
- production planning artifacts
- scene orchestration plans
- trailer structures
- continuity-aware cinematic workflows

## Screenplay Conversion Workflow

### Conversion Sequence

1. Load approved chapter canon
2. Load chapter storyboard
3. Build scene map
4. Convert chapters into screenplay scenes
5. Generate screenplay batches
6. Generate Fountain export
7. Run screenplay continuity audit
8. Run adaptation audit
9. Await author approval

## Screenplay Requirements

Each screenplay scene must include:

- scene ID
- source chapter
- source beat IDs
- location
- involved characters
- emotional purpose
- visual intent
- adaptation notes
- continuity notes

## Adaptation Governance

The system must track:

- removed scenes
- merged scenes
- expanded scenes
- reordered scenes
- newly invented scenes

No structural adaptation may silently alter locked canon.

## Screenplay Audit Requirements

The screenplay audit must validate:

- manuscript-to-scene mapping
- continuity preservation
- character consistency
- timeline correctness
- dialogue consistency
- screenplay pacing

## Required Screenplay Artifacts

Generate:

- `screenplay/scaffold.md`
- `screenplay/drafts/`
- `screenplay/fountain/`
- `screenplay/exports/`
- `reports/screenplay-audit.md`
- `reports/adaptation-audit.md`

## Cinematic Production Workflow

### Production Sequence

1. Load approved screenplay
2. Load visual continuity references
3. Build scene orchestration plan
4. Build shot planning artifacts
5. Build trailer structure
6. Build audio/dialogue plan
7. Build edit assembly plan
8. Run continuity validation
9. Await approval

## Scene Orchestration Requirements

Each scene plan must define:

- source screenplay pages
- story objective
- emotional objective
- location
- involved characters
- wardrobe state
- environmental state
- continuity risks
- cinematic references
- trailer suitability

## Shot Planning Requirements

Each shot entry should define:

- shot ID
- framing
- movement
- lighting style
- emotional intent
- continuity dependencies
- transition behavior

## Trailer Planning

The trailer workflow should support:

- teaser structure
- emotional escalation
- reveal pacing
- soundtrack timing
- dialogue fragments
- title-card timing
- sequel hook placement

## Audio and Dialogue Planning

Track:

- dialogue references
- emotional tone progression
- sound motifs
- environmental sound design
- music escalation timing

## Edit Assembly Planning

The edit assembly plan should support:

- sequence ordering
- pacing strategy
- emotional pacing
- transition strategy
- climax pacing
- runtime estimation

## Required Production Artifacts

Generate:

- `movie-generation/production-plan.md`
- `movie-generation/scene-generation-plan.md`
- `movie-generation/shot-list.md`
- `movie-generation/trailer-structure.md`
- `movie-generation/audio-plan.md`
- `movie-generation/edit-decision-list.md`

## Continuity Gates

### Screenplay Gate

Validate:

- screenplay traces to approved manuscript
- no locked canon drift exists
- adaptation changes are documented

### Production Gate

Validate:

- visual continuity preserved
- character continuity preserved
- environmental continuity preserved
- scene order valid

## Technical Edit Pass

### Improvements Added

- Added adaptation governance.
- Added scene orchestration planning.
- Added trailer structure workflow.
- Added edit assembly planning.
- Added screenplay-to-production traceability.
- Added continuity validation at production stage.

### Remaining Future Work

- automated screenplay assembly tooling
- Fountain export automation
- shot runtime estimation
- cinematic pacing analysis
- production scheduling integration
