# Sprint 2 - Generation Workspace and Action Semantics

## Status

Complete.

## Related issues

- #30 - Define the real Content Engine generation workspace in the UI
- #35 - Separate validation actions from generation actions in the UI and API

## Sprint goal

Define the actual working surface of the Content Engine so the product stops feeling like a folder validator and starts behaving like a content production system.

Sprint 2 does not implement the UI components yet. It defines the interaction contract that future UI/backend work should follow.

---

## Problem statement

The current interaction model risks confusing users because buttons can appear to validate whether something exists instead of generating new production artifacts.

A content engine needs a primary workspace where the user can:

1. Select a project.
2. Choose an artifact type.
3. Provide creative direction.
4. Generate draft output.
5. Preview and review the draft.
6. Validate it against canon and folder rules.
7. Export it to target formats.
8. Save or commit approved output.

---

## Required UI regions

### 1. Project context bar

Shows the active project and context loaded from the project registry.

Required fields:

- Project title
- Project slug
- Status
- Canon state
- Supported generation types
- Active artifact destination
- Active export target, when applicable

Primary purpose:

- Make it clear what project the user is working in.
- Prevent generated artifacts from being saved into the wrong project.

---

### 2. Artifact selector

Allows the user to choose what kind of content they want to create.

Initial artifact types:

- Canon update
- Character profile
- Story outline
- Manuscript section
- Screenplay scene
- Scene card
- Storyboard panel set
- Visual prompt pack
- Production package
- Pitch artifact
- Audio script
- Tool-specific export

Each artifact type should resolve to:

- Required source context
- Output format
- Default destination folder
- Validation rules
- Available export targets

---

### 3. Creative direction panel

The core work area where the user tells the engine what to make.

Required inputs:

- User instruction
- Tone/style notes
- Source references
- Constraints
- Intended target format
- Optional tool/export target

Recommended optional inputs:

- Scene/chapter range
- Character focus
- Visual style focus
- Runtime/duration target
- Dialogue/narration preference
- Negative constraints

---

### 4. Source context panel

Shows what the engine will use as context before generation.

Required source groups:

- Project registry entry
- Active canon files
- Relevant manuscript/story files
- Relevant screenplay files
- Character references
- Visual bible references
- Prior related generated artifacts

The user should be able to see when context is missing before generation starts.

---

### 5. Generation output preview

Generated content must appear as a draft preview before it can be saved.

Preview requirements:

- Render Markdown and structured JSON clearly.
- Show destination path before save.
- Show generation warnings.
- Show source references used.
- Allow copy, regenerate, edit, reject, approve, validate, export.

---

### 6. Validation and warning panel

Validation belongs near the output, not as the whole product experience.

Validation categories:

- Project/folder validation
- Required field validation
- Canon continuity validation
- Visual continuity validation
- Export profile validation
- Destination overwrite warnings
- Missing source context warnings

---

### 7. Export panel

Shows tool-specific export options after a draft is approved or ready for export.

Initial targets:

- Generic JSON
- Runway
- Pika
- Luma / Dream Machine
- Kling
- Sora-style prompt package
- ElevenLabs
- Storyboard / pitch deck package

---

## Action taxonomy

The UI and API should use five top-level action groups.

### Validate

Purpose:

Inspect existing inputs, project structure, source context, or generated draft output.

Must not:

- Create new creative content.
- Save draft artifacts.
- Export packages.
- Commit files.

Example labels:

- Validate project
- Validate source context
- Validate draft
- Validate export readiness

---

### Generate

Purpose:

Create new draft content from project context and user direction.

Must:

- Produce previewable draft output.
- Capture generation metadata.
- Avoid overwriting approved project files.

Example labels:

- Generate scene card
- Generate screenplay scene
- Generate storyboard prompts
- Generate production package

---

### Assemble

Purpose:

Combine existing artifacts into a larger artifact without inventing new creative content by default.

Examples:

- Assemble screenplay draft
- Assemble pitch packet
- Assemble scene package
- Assemble chapter bundle

---

### Export

Purpose:

Transform canonical or approved artifacts into a target tool format.

Must:

- Use export profiles.
- Report missing required fields.
- Keep canonical source content unchanged.

Examples:

- Export for Runway
- Export for ElevenLabs
- Export generic JSON package

---

### Save / Commit

Purpose:

Persist approved output into repo paths.

Must:

- Require review/approval state.
- Show target path.
- Warn on overwrite.
- Include generation metadata.

Examples:

- Save approved draft
- Commit generated artifact
- Save export package

---

## Suggested workspace flow

```text
Select Project
  -> Select Artifact Type
    -> Load Source Context
      -> Enter Creative Direction
        -> Validate Context
          -> Generate Draft
            -> Preview / Edit / Regenerate
              -> Validate Draft
                -> Approve
                  -> Export or Save
```

---

## Button naming rules

Buttons must say exactly what they do.

Avoid vague labels:

- Run
- Process
- Build
- Check
- Start

Preferred labels:

- Validate project folders
- Validate generation context
- Generate screenplay scene
- Generate visual prompt pack
- Assemble pitch packet
- Export Runway package
- Save approved artifact

---

## Persistence rules

Generated output should follow this lifecycle:

1. Draft output appears only in preview state.
2. User may edit, reject, or regenerate.
3. User approves the output.
4. Approved output can be saved or exported.
5. Save/commit writes to the destination path.

Generated drafts must not overwrite existing files automatically.

---

## API contract draft

Future backend endpoints/actions should map to the action taxonomy.

Suggested action names:

```text
validateProject(projectSlug)
validateGenerationContext(projectSlug, artifactType, sourceRefs)
generateArtifact(projectSlug, artifactType, generationRequest)
assembleArtifact(projectSlug, assemblyType, sourceRefs)
validateDraft(projectSlug, draftId)
exportArtifact(projectSlug, artifactId, exportProfile)
saveApprovedArtifact(projectSlug, artifactId, destinationPath)
```

---

## Minimum viable Sprint 2 implementation target for future PRs

The first UI implementation should support one vertical slice:

1. Select project from registry.
2. Select `scene-card` as artifact type.
3. Enter creative direction.
4. Validate context.
5. Generate a draft scene card.
6. Preview draft.
7. Save approved draft to the project `movie_generation` or `story` path.

This avoids trying to implement every artifact type at once.

---

## Definition of done

- [x] Generation workspace regions defined.
- [x] Action taxonomy defined.
- [x] Button naming rules defined.
- [x] Persistence lifecycle defined.
- [x] API action contract drafted.
- [x] Minimum future UI vertical slice identified.

## Next sprint

Sprint 3 should address:

- #32 - pre-movie production package schema
- #39 - generation job/state model

Sprint 3 should turn this interaction model into structured package and job schemas.
