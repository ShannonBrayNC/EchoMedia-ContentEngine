# Phase 2 Sprint 2 — Manuscript Intake and Story Architecture

## Objective

Convert raw manuscript ideas into structured cinematic story projects.

The system must preserve author intent while building:

- premise
- logline
- synopsis
- treatment
- beat sheet
- chapter map
- canon seed

## Intake Pipeline

### Required Inputs

- title or working title
- genre
- tone
- target audience
- themes
- themes to avoid
- comparable works
- desired format
- rating target
- known ending
- known characters
- franchise intent

### Intake Rules

- AI assumptions must remain marked `AI-PROPOSED` until approved.
- Existing canon must override generated assumptions.
- Locked canon cannot be replaced silently.
- Generated structures must remain editable before approval.

## Story Architecture Support

### Supported Structures

- three-act
- five-act
- hero's journey
- nonlinear
- serialized streaming structure
- thriller escalation
- mystery-box
- anthology

### Structure Outputs

The system must generate:

- opening hook
- inciting incident
- midpoint reversal
- escalation path
- climax
- resolution
- sequel hooks

## Required Artifacts

### Story Folder

Generate:

- `story/idea-brief.md`
- `story/premise.md`
- `story/logline.md`
- `story/synopsis-one-page.md`
- `story/treatment.md`
- `story/beat-sheet.md`
- `story/chapter-map.md`

### Canon Seed

Generate:

- timeline assumptions
- doctrine assumptions
- world rules
- unresolved mysteries
- visual tone assumptions

All generated assumptions must remain editable until approved.

## Beat Sheet Rules

Each beat should contain:

- beat ID
- story function
- involved characters
- emotional movement
- canon dependencies
- sequel implications
- adaptation opportunities

## Chapter Map Rules

Each chapter should define:

- title
- POV
- purpose
- conflict
- emotional turn
- continuity requirements
- storyboard opportunities
- screenplay conversion notes

## Architecture Validation

### Validation Requirements

The system must validate:

- pacing balance
- missing escalation
- unresolved setup/payoff gaps
- character arc alignment
- theme consistency
- continuity conflicts

### Required Reports

Generate:

- `reports/story-architecture-audit.md`
- `reports/theme-alignment-report.md`
- `reports/setup-payoff-report.md`

## Suggested Workflow

```text
Idea Intake
  → Story Seed
  → Story Architecture Options
  → Author Selection
  → Beat Sheet
  → Chapter Map
  → Canon Seed
  → Approval Gate
```

## Approval Gates

### Candidate Story State

Generated structures remain:

```text
candidate
```

until author approval.

### Approved Story State

Once approved:

- beat sheet becomes active canon
- chapter numbering locks
- timeline assumptions lock
- sequel hooks become tracked canon

## Technical Edit Pass

### Improvements Added

- Added explicit AI-proposed labeling.
- Added architecture validation requirements.
- Added setup/payoff tracking.
- Added adaptation opportunity tracking.
- Added sequel hook governance.
- Added continuity validation expectations.

### Remaining Future Work

- automated beat-balance scoring
- pacing heatmap generation
- AI-assisted franchise planning
- visual tone clustering
- chapter runtime estimation
