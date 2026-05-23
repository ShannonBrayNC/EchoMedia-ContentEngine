# Phase 2 Sprint 4 — Chapter Pipeline, Storyboards, and 10-Image System

## Objective

Build the chapter production pipeline that converts approved story architecture into chapter-level creative packets.

Each chapter packet must support:

- chapter brief
- canon source mapping
- manuscript planning
- storyboard planning
- 10 image prompts
- visual continuity checks
- screenplay conversion notes
- approval status

## Chapter Production Workflow

Each chapter should move through this sequence:

1. Chapter brief
2. Canon source load
3. Character state load
4. Location state load
5. Scene outline
6. Manuscript draft
7. Storyboard draft
8. Image prompt pack
9. Continuity audit
10. Technical edit
11. Author approval

## Chapter Brief Requirements

Each chapter brief must include:

- chapter number
- chapter title
- canon state
- source beat IDs
- primary POV
- secondary POV
- chapter purpose
- opening state
- closing state
- required plot beats
- emotional turn
- conflict
- continuity risks
- visual opportunities
- screenplay notes

## Storyboard Requirements

Each chapter storyboard must include:

- sequence summary
- scene beats
- shot list
- camera language
- emotional progression
- visual continuity references
- image prompt references
- transition notes
- estimated screen time

## 10-Image Chapter System

Each chapter must support up to 10 approved image prompts.

Recommended image slots:

1. establishing shot
2. protagonist moment
3. supporting character moment
4. relationship beat
5. key location shot
6. prop or clue shot
7. conflict shot
8. emotional turn shot
9. climax shot
10. closing image

## Image Prompt Requirements

Each prompt must include:

- chapter number
- image number
- story moment
- canon source
- characters present
- approved physical traits
- wardrobe state
- location state
- camera framing
- lighting
- mood
- color palette
- negative prompts
- continuity notes
- approval status

## Generated Image Ledger

The generated image ledger must track:

- image ID
- chapter number
- prompt file
- generation provider
- generation date
- seed/reference ID
- approval state
- continuity notes
- file location or artifact reference

## Continuity Gates

### Manuscript Gate

Validate:

- chapter follows beat sheet
- character states are correct
- timeline is valid
- canon sources are cited

### Storyboard Gate

Validate:

- storyboard matches chapter
- emotional progression is preserved
- shots align to plot events

### Visual Gate

Validate:

- character appearance consistency
- wardrobe continuity
- location continuity
- no locked visual traits changed

## Required Artifacts

Generate or support:

- `manuscript/chapter-briefs/`
- `manuscript/chapters/`
- `storyboards/chapters/`
- `storyboards/shots/`
- `visual-bible/chapter-image-prompts/`
- `visual-bible/generated-image-ledger.md`
- `reports/chapter-continuity-audit.md`
- `reports/visual-consistency-audit.md`

## Technical Edit Pass

### Improvements Added

- Added chapter packet model.
- Added image slot taxonomy.
- Added generated image ledger requirements.
- Added manuscript, storyboard, and visual gates.
- Added screenplay conversion notes at chapter level.
- Added approval state tracking for image prompts.

### Remaining Future Work

- automated image prompt generation
- provider-specific image prompt adapters
- storyboard-to-video shot generation
- chapter runtime estimation
- per-chapter asset packaging
