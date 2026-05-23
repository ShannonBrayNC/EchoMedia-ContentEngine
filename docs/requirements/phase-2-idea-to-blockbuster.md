# EchoMedia Content Engine — Phase 2 Requirements

## Working Title

**Idea to Blockbuster Engine**

## Purpose

Phase 2 turns the existing Content Engine project structure into a governed story-production platform. The system must take a raw manuscript idea and progressively produce a controlled creative package: story concept, canon, backstories, character profiles, physical character descriptions for image consistency, chapter outlines, chapter storyboards, chapter image packs, manuscript drafts, screenplay exports, and AI-assisted movie generation instructions.

The central design rule is simple: **creative expansion is allowed; canon drift is not allowed unless the author approves it.**

## Current Repository Context Reviewed

The repository already contains the foundation for a cinematic story pipeline:

- `projects/lantern-protocol/screenplay/00-master-story-bible.md` — active canon, doctrine, characters, and core story law.
- `projects/lantern-protocol/screenplay/01-feature-treatment.md` — feature treatment.
- `projects/lantern-protocol/screenplay/02-feature-screenplay-scaffold.md` — screenplay structure.
- `projects/lantern-protocol/screenplay/drafts/` — page-batched screenplay output.
- `projects/lantern-protocol/storyboards/chapters/` — chapter-level storyboards.
- `projects/lantern-protocol/visual-bible/` — visual style, character image prompts, location image prompts.
- `projects/lantern-protocol/trailer/` — teaser storyboard and shot prompts.
- `projects/lantern-protocol/pitch/` — synopsis, treatment, deck, and query-letter assets.
- `projects/lantern-protocol/novel/` — novel expansion plan, manuscript workspace, chapter status, POV map, and continuity map.
- `projects/lantern-protocol/reports/` — continuity audit, issues, and revision plan.

Phase 2 should generalize this Lantern Protocol structure into a reusable project system for any book, screenplay, or cinematic franchise package.

## Product Outcomes

Phase 2 must let an author move through this path:

```text
Idea → Story Seed → Canon Bible → Character/World Bible → Chapter Plan → Manuscript Draft → Storyboards → Image Pack → Screenplay → Trailer Plan → Movie Generation Plan → Review/Approval → Export Package
```

## Author-Controlled Canon Governance

### Requirement: Canon Lock System

The system must support explicit canon states:

- `draft` — content can change freely.
- `candidate` — content is proposed but not canon.
- `approved` — content becomes active canon.
- `locked` — content cannot change without an author approval record.
- `superseded` — content is replaced but preserved for audit history.
- `archived` — content is retained but cannot be used as active canon.

### Requirement: Canon Change Requests

Any proposed change to approved or locked canon must create a canon change request containing:

- project ID
- affected canon file
- old value
- proposed value
- reason for change
- story impact
- affected chapters/scenes/images
- author approval status
- approval timestamp
- approving user

### Requirement: Canon Drift Detection

The system must detect drift across:

- character names
- relationship facts
- ages and timelines
- backstory events
- physical descriptions
- locations
- doctrine/theme rules
- plot-critical events
- chapter summaries
- screenplay scenes
- image prompts
- video prompts

Outputs that violate locked canon must be marked `blocked` until the author approves a change or the generation is revised.

### Requirement: Canon Manifest

Each project must include a machine-readable canon manifest:

```text
projects/{project-slug}/canon/canon-manifest.json
```

The manifest must identify:

- active canon files
- locked canon fields
- allowed ambiguity fields
- visual consistency keys
- prohibited terms/names
- approved themes/doctrines
- project-specific drift rules

## Project Template

Each new story project should follow this structure:

```text
projects/{project-slug}/
  README.md
  canon/
    canon-manifest.json
    story-bible.md
    world-bible.md
    timeline.md
    continuity-map.md
    canon-change-log.md
    canon-change-requests/
  characters/
    character-index.md
    profiles/
    physical-descriptions/
    visual-consistency-prompts/
  story/
    idea-brief.md
    premise.md
    logline.md
    synopsis-one-page.md
    treatment.md
    beat-sheet.md
    chapter-map.md
  manuscript/
    chapters/
    inserts/
    exports/
    reports/
  storyboards/
    chapters/
    shots/
    exports/
  visual-bible/
    style-guide.md
    character-image-prompts.md
    location-image-prompts.md
    prop-image-prompts.md
    generated-image-ledger.md
  screenplay/
    scaffold.md
    drafts/
    fountain/
    exports/
  movie-generation/
    production-plan.md
    scene-generation-plan.md
    shot-list.md
    ai-video-prompts.md
    voice-and-dialogue-plan.md
    music-and-sound-plan.md
    edit-decision-list.md
  pitch/
    one-page-synopsis.md
    two-page-treatment.md
    pitch-deck-outline.md
    pitch-deck.md
  reports/
    continuity-audit.md
    visual-consistency-audit.md
    screenplay-audit.md
    technical-edit-report.md
```

## Feature 1: Manuscript Idea Intake

### Objective

Accept a raw idea and convert it into a structured project seed.

### Inputs

- one-line idea
- genre
- tone
- target audience
- author goals
- comparable works
- desired format: novel, novella, screenplay, series, graphic novel, short film, feature film
- rating target: G, PG, PG-13, R, mature
- themes to include
- themes to avoid
- known characters
- known ending, if any

### Outputs

- logline
- premise
- one-page concept brief
- story risks
- audience promise
- initial canon assumptions
- recommended project structure

### Acceptance Criteria

- System creates a new project folder using the template.
- System produces a clear story seed without overwriting author intent.
- Any invented material is marked as AI-proposed, not canon.

## Feature 2: Story Architecture Builder

### Objective

Build the story from concept into a structured narrative spine.

### Requirements

- Generate multiple story architecture options.
- Support three-act, five-act, hero's journey, mystery-box, thriller escalation, romance arc, episodic season, and nonlinear structures.
- Produce beat sheets and chapter maps.
- Track character arcs against plot beats.
- Track theme beats against plot beats.
- Allow the author to approve one structure as active canon.

### Outputs

- `story/beat-sheet.md`
- `story/chapter-map.md`
- `story/treatment.md`
- `canon/timeline.md`

## Feature 3: Canon Bible Builder

### Objective

Define and protect the story rules.

### Required Canon Sections

- premise
- genre contract
- themes
- doctrines/rules
- world rules
- technology/magic/science rules, if applicable
- political/social rules
- timeline
- glossary
- locations
- factions
- unresolved mysteries
- prohibited contradictions
- sequel hooks

### Acceptance Criteria

- Every generated chapter must cite its canon sources.
- Every screenplay scene must cite the chapter or beat that generated it.
- Every image prompt must cite the character/location/style source used.

## Feature 4: Character Profile System

### Objective

Build durable characters that remain consistent across prose, images, screenplay, trailer, and movie generation.

### Character Profile Fields

Each character profile must include:

- full name
- aliases
- role in story
- age or age range
- occupation/function
- public identity
- private wound
- external goal
- internal need
- fear
- contradiction
- moral line
- speaking style
- relationship map
- backstory timeline
- secrets
- first appearance
- final state
- arc summary
- approved dialogue samples
- prohibited behavior unless canon changes

### Physical Character Fields

Each major visual character must include:

- apparent age
- height/build
- face shape
- skin tone
- hair color/style/length
- eye color
- signature expressions
- posture/body language
- wardrobe rules
- color palette
- distinguishing marks
- accessories
- visual references text description
- negative prompt rules
- image consistency seed or reference ID when available

### Acceptance Criteria

- Image prompts must pull from the approved physical profile.
- The system must flag generated prompts that alter locked visual traits.
- Author can approve controlled aging, injury, costume changes, disguise, or alternate-era variants.

## Feature 5: Backstory and Relationship Engine

### Objective

Generate backstories and relationship maps without accidental contradiction.

### Requirements

- Create individual backstory files.
- Create relationship graph files.
- Track relationship status by chapter/scene.
- Track hidden knowledge: who knows what and when.
- Track secrets and reveals.
- Flag premature reveals.
- Flag relationship drift.

### Outputs

- `characters/backstories/{character}.md`
- `characters/relationships.md`
- `canon/knowledge-map.md`

## Feature 6: Chapter Generation Pipeline

### Objective

Generate chapter plans and manuscript drafts governed by canon.

### Chapter Workflow

For each chapter:

1. Generate chapter brief.
2. Identify canon sources.
3. Identify required character states.
4. Identify locations and time period.
5. Generate scene-by-scene chapter outline.
6. Generate prose draft.
7. Run continuity audit.
8. Run technical edit.
9. Produce revision plan.
10. Await author approval before promoting to canon.

### Chapter File Requirements

Each chapter file must contain:

- chapter title
- chapter number
- canon sources
- POV strategy
- chapter purpose
- character states entering chapter
- character states leaving chapter
- required plot beats
- continuity requirements
- visual opportunities
- manuscript body
- revision notes
- approval status

## Feature 7: Ten Images Per Chapter

### Objective

Generate a controlled image plan for each chapter, with up to 10 images per chapter.

### Image Types

Each chapter should support:

- establishing shot
- main character portrait/action shot
- supporting character shot
- key object/prop shot
- emotional beat shot
- conflict shot
- location shot
- cinematic transition shot
- climactic chapter moment
- closing image

### Image Prompt Requirements

Each image prompt must include:

- chapter number
- image number
- story moment
- canon source
- characters present
- approved physical traits
- location description
- wardrobe state
- emotional tone
- camera framing
- lens/camera style
- lighting
- color palette
- negative prompts
- continuity notes
- approval status

### Acceptance Criteria

- System can create exactly 10 image prompts per chapter unless the author chooses fewer.
- Character visuals must not drift from approved physical profiles.
- Generated image metadata must be logged in `visual-bible/generated-image-ledger.md`.

## Feature 8: Chapter Storyboard Builder

### Objective

Convert each chapter into a visual storyboard suitable for image generation, trailer planning, comic adaptation, or AI film generation.

### Storyboard Requirements

Each chapter storyboard must include:

- sequence summary
- scene beats
- shot list
- camera direction
- emotional progression
- visual continuity references
- image prompt references
- dialogue fragments where needed
- transition notes
- estimated screen time

### Outputs

- `storyboards/chapters/chapter-{nn}-{slug}.md`
- `storyboards/shots/chapter-{nn}-shot-list.md`

## Feature 9: Screenplay Conversion

### Objective

Convert approved manuscript/chapter material into screenplay format.

### Requirements

- Produce screenplay scaffold from approved beat sheet.
- Convert chapters to scenes.
- Preserve canon and approved character voice.
- Export Markdown and Fountain.
- Track source chapter for every scene.
- Identify adaptation compression decisions.
- Produce author approval list for changed, merged, removed, or invented scenes.

### Outputs

- `screenplay/scaffold.md`
- `screenplay/drafts/feature-screenplay-pages-{range}.md`
- `screenplay/fountain/{project}.fountain`
- `screenplay/exports/{project}-screenplay.md`
- `reports/screenplay-audit.md`

## Feature 10: AI Movie Generation Plan

### Objective

Generate detailed steps to turn the approved story package into AI-assisted movie assets.

### Required Movie Plan Sections

- production assumptions
- tools/providers to be configured
- visual style lock
- character reference strategy
- location reference strategy
- shot generation order
- scene generation order
- voice/dialogue workflow
- music and sound workflow
- continuity review workflow
- edit assembly workflow
- trailer workflow
- final export workflow

### Scene Generation Plan

For each scene, include:

- source screenplay pages
- story objective
- characters
- location
- wardrobe
- props
- required dialogue
- generated shot prompts
- motion/video prompts
- audio notes
- continuity risks
- approval gate

### Acceptance Criteria

- Movie generation instructions must be detailed enough for a human producer or AI pipeline to execute.
- No video prompt may alter locked canon without a change request.
- Every generated scene must map back to approved screenplay source.

## Feature 11: Technical Edit Pass

### Objective

After requirements, story, chapter, screenplay, image, or movie outputs are generated, the system must perform a technical edit pass.

### Technical Edit Checklist

The technical edit must check for:

- missing acceptance criteria
- missing approval gates
- file path inconsistencies
- unclear state transitions
- canon drift risks
- visual drift risks
- duplicated pipeline steps
- missing audit outputs
- missing generated artifact ledger entries
- missing rollback/versioning behavior
- missing export requirements
- missing safety/legal/IP considerations
- vague implementation language
- untestable requirements

### Required Technical Edit Output

- issue summary
- recommended changes
- severity
- affected requirement
- corrected wording
- final readiness status

## Feature 12: GitHub-Backed Author Approval Workflow

### Objective

Use GitHub as the source of truth for canon, requirements, approvals, and change history.

### Requirements

- Every major generation batch must happen on a branch.
- Every canon promotion must happen through pull request review or explicit approval record.
- Pull requests must include continuity reports.
- Pull requests must include visual consistency reports when images are involved.
- Pull requests must include screenplay audit reports when screenplay files change.
- Merged PRs become the approved project state.
- Unmerged branches remain proposed work.

### Suggested Branch Naming

```text
idea/{project-slug}
canon/{project-slug}-{change}
manuscript/{project-slug}-chapter-{nn}
storyboard/{project-slug}-chapter-{nn}
visuals/{project-slug}-chapter-{nn}
screenplay/{project-slug}-{draft}
movie-plan/{project-slug}-{draft}
```

### Suggested Pull Request Template

Each PR must include:

- summary
- author intent preserved
- canon changes proposed
- files changed
- generated artifacts
- continuity audit result
- visual audit result, if applicable
- author approval needed
- rollback notes

## Feature 13: Export Package Builder

### Objective

Produce complete packages for author review, publisher/pitch use, or production use.

### Export Packages

- author review package
- manuscript package
- screenplay package
- visual bible package
- pitch package
- trailer package
- AI movie generation package
- full franchise package

### Required Export Formats

- Markdown
- PDF-ready Markdown
- Fountain for screenplay
- JSON manifests
- CSV/Markdown ledgers
- ZIP package, future implementation

## Feature 14: Quality Gates

### Required Gates

- canon audit gate
- visual consistency gate
- chapter completeness gate
- screenplay source mapping gate
- image prompt completeness gate
- movie plan completeness gate
- author approval gate

### Gate Behavior

- `pass` — artifact can be promoted.
- `warn` — artifact can be reviewed but not auto-promoted.
- `fail` — artifact is blocked until fixed.

## Implementation Sprints

### Sprint 1 — Phase 2 Foundation

- Add reusable project template.
- Add canon manifest schema.
- Add author approval model.
- Add canon change request format.
- Add PR template for generated story work.

### Sprint 2 — Idea Intake and Story Architecture

- Build idea intake prompt/template.
- Generate premise, logline, synopsis, treatment, and beat sheet.
- Add story architecture approval gate.

### Sprint 3 — Character and Visual Consistency System

- Add character profile schema.
- Add physical character schema.
- Add visual prompt builder.
- Add visual drift audit.

### Sprint 4 — Chapter Pipeline

- Add chapter brief template.
- Add chapter draft workflow.
- Add chapter status tracker.
- Add continuity audit enhancements.

### Sprint 5 — Ten Images Per Chapter and Storyboards

- Add chapter image prompt generator.
- Add generated image ledger.
- Add chapter storyboard generator.
- Add shot list exports.

### Sprint 6 — Screenplay Conversion

- Add chapter-to-scene mapper.
- Add screenplay scaffold generator.
- Add Fountain exporter requirements.
- Add screenplay audit report.

### Sprint 7 — AI Movie Generation Workflow

- Add movie generation plan template.
- Add scene generation plan.
- Add AI video prompt format.
- Add edit decision list template.

### Sprint 8 — Export Packages and Repo Automation

- Add package builder.
- Add validation scripts.
- Add GitHub PR workflow documentation.
- Add final Phase 2 demo using Lantern Protocol.

## Non-Functional Requirements

### Traceability

Every generated artifact must trace back to source canon, author input, and approval state.

### Reversibility

Generated changes must be reversible through Git history and explicit supersession records.

### Reusability

Lantern Protocol must be treated as the first project implementation, not as hard-coded logic.

### Human Approval

The author must remain the final authority for canon, theme, character changes, major plot changes, and final exports.

### Consistency

The system must prefer reuse of approved facts over reinvention.

### Modularity

Each stage must be independently executable: idea, canon, chapter, storyboard, image prompt, screenplay, movie plan, export.

## Open Design Decisions

- Which AI image provider will be the first supported target?
- Should image generation be stored as prompts only first, or should binary outputs be committed through releases/artifacts?
- Should author approval be GitHub-only, app UI-based, or both?
- Should the first UI be CLI, web dashboard, or VS Code/Codex workflow?
- Should the platform support collaborative authors with role-based approvals?

## Technical Edit Result

### Findings

- Added explicit canon lock states to prevent uncontrolled drift.
- Added change request workflow because Git history alone does not explain author intent.
- Added physical character schemas because image consistency requires more than prose character profiles.
- Added generated image ledger because image prompts and image outputs need traceability.
- Added chapter-to-screenplay source mapping because adaptation compression can otherwise hide story changes.
- Added movie generation plan artifacts so the platform supports production, not just writing.
- Added quality gates and PR requirements so GitHub becomes the approval rail.

### Final Readiness Status

This requirements document is ready for Phase 2 planning and issue decomposition. It should be treated as the parent specification for implementation issues, sprint tickets, and Codex-ready development tasks.
