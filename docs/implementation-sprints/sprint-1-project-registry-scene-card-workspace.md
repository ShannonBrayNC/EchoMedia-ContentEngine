# Implementation Sprint 1 - Project Registry Inventory and Scene Card Generation Workspace

## Status

Opened.

## Sprint goal

Build the first real vertical slice of the Content Engine:

1. Discover registered story projects.
2. Select a project in the UI.
3. Select `scene-card` as the artifact type.
4. Enter creative direction.
5. Validate source context.
6. Generate a draft scene card.
7. Preview the draft.
8. Create a review gate.
9. Save the approved artifact to the correct project path.
10. Show progress in the compact workflow/status rail.

This sprint should prove that the Content Engine can generate content instead of only validating whether files exist.

---

## Source foundation

This sprint implements the first narrow slice from the technical edit foundation:

- `docs/technical-edit/sprint-1-project-foundation.md`
- `docs/technical-edit/sprint-2-generation-workspace.md`
- `docs/technical-edit/sprint-3-production-package-and-jobs.md`
- `docs/technical-edit/sprint-4-review-and-traceability.md`
- `docs/technical-edit/sprint-5-status-rail.md`
- `docs/technical-edit/sprint-6-export-profiles.md`

Relevant schemas:

- `schemas/projects/project-registry.schema.json`
- `schemas/workflows/action-taxonomy.schema.json`
- `schemas/workflows/generation-job.schema.json`
- `schemas/workflows/review-gate.schema.json`
- `schemas/workflows/artifact-traceability.schema.json`
- `schemas/workflows/status-rail.schema.json`
- `schemas/production/production-package.schema.json`

---

## Vertical slice flow

```text
Project Registry
  -> Project Picker
    -> Scene Card Artifact Type
      -> Creative Direction
        -> Context Validation
          -> Draft Scene Card Generation
            -> Preview
              -> Review Gate
                -> Approval
                  -> Save Approved Artifact
                    -> Status Rail Updates
```

---

## Sprint scope

### In scope

- Create or load a project registry file that conforms to `project-registry.schema.json`.
- Inventory existing story projects and include at least:
  - `lantern-protocol`
  - `The-Sovereign-Exception`
- Add a project-selection UI path driven by the registry.
- Add a `scene-card` artifact workflow.
- Add a creative-direction input area.
- Add local/backend action separation for:
  - Validate context
  - Generate draft
  - Review draft
  - Save approved artifact
- Generate a draft scene-card object or Markdown artifact.
- Create generation-job metadata for the draft.
- Create review-gate metadata before saving.
- Create traceability metadata linking the draft to project/source context.
- Display status rail state for the workflow.

### Out of scope

- Full screenplay generation.
- Full video export implementation.
- All export profiles.
- All artifact types.
- Full canon impact analysis.
- Full provider API adapters.
- Long-running external async job execution.

---

## Implementation tasks

### Task 1 - Project registry inventory

Create a registry artifact, likely one of:

- `config/project-registry.json`
- `projects/project-registry.json`
- `content/project-registry.json`

The registry must conform to:

`schemas/projects/project-registry.schema.json`

Acceptance criteria:

- `lantern-protocol` appears in the registry.
- `The-Sovereign-Exception` appears in the registry if the folder exists.
- Every listed project has required artifact paths.
- The registry can drive UI project selection.

---

### Task 2 - Registry validation utility

Add a small validation utility or script that checks:

- Registry JSON parses.
- Required fields exist.
- Required artifact path keys exist.
- Project root paths exist when expected.
- Missing folders are reported as warnings or errors.

Acceptance criteria:

- Running the validator prints a readable report.
- Missing folders do not crash the app.
- Output distinguishes warnings from blockers.

---

### Task 3 - Project picker UI

Add or update the UI so project selection reads from the registry, not hard-coded project names.

Acceptance criteria:

- User can select a registered project.
- Selected project is visible in the workspace.
- Status rail shows selected project.
- Hidden/archived projects are not shown by default.

---

### Task 4 - Scene card generation workspace

Add the first generation workspace flow for `scene-card`.

Required fields:

- Project
- Artifact type: `scene-card`
- User creative direction
- Source/context notes
- Destination path preview

Acceptance criteria:

- User can enter creative direction.
- User can trigger context validation.
- User can trigger draft scene-card generation.
- Validation and generation are separate actions.

---

### Task 5 - Draft scene-card generation

Implement a simple draft generation path.

The first implementation may be local/template-driven if model integration is not ready.

Suggested draft scene-card fields:

- `scene_id`
- `title`
- `purpose`
- `summary`
- `location`
- `characters`
- `source_refs`
- `visual_notes`
- `dialogue_or_narration`
- `shots`
- `continuity_notes`

Acceptance criteria:

- Draft output is previewed before saving.
- Draft has at least one source reference.
- Draft has at least one shot or visual prompt stub.
- Draft is not written directly into final project folders.

---

### Task 6 - Generation job metadata

Create job metadata conforming to the intent of:

`schemas/workflows/generation-job.schema.json`

Acceptance criteria:

- Draft generation creates a job id.
- Job captures project slug, artifact type, action, state, request, source context, outputs, warnings/errors.
- Failed generation does not save artifacts.

---

### Task 7 - Review gate and save flow

Generated scene cards must pass through a review gate before saving.

Acceptance criteria:

- Review gate is created in `pending-review` or equivalent state.
- User can approve or reject draft.
- Save is disabled until approved.
- Destination path is shown before save.
- Existing file overwrite requires explicit confirmation.

---

### Task 8 - Traceability metadata

Create traceability metadata for the generated scene card.

Acceptance criteria:

- Scene card links back to project/source context.
- Scene card links to generation job id.
- Scene card links to review gate id.
- Missing traceability blocks save or produces a clear warning.

---

### Task 9 - Status rail integration

Render the compact status rail through the vertical slice.

Acceptance criteria:

- Rail shows project.
- Rail shows artifact type.
- Rail shows current stage.
- Rail shows warnings/blockers.
- Rail shows next action.
- Rail does not become a full order display.

---

## Suggested branch

```text
impl/sprint-1-registry-scene-card-workspace
```

---

## Suggested issue breakdown

1. Implement project registry inventory and validator.
2. Build registry-driven project picker.
3. Build scene-card generation workspace UI.
4. Add draft scene-card generation and preview.
5. Add generation job metadata.
6. Add review gate approval/save flow.
7. Add scene-card traceability metadata.
8. Wire compact status rail to the vertical slice.

---

## Definition of done

- [ ] Registry exists and includes core story projects.
- [ ] Registry validation can run and report issues.
- [ ] UI project picker reads from registry.
- [ ] User can select `scene-card` workflow.
- [ ] User can enter creative direction.
- [ ] User can validate context separately from generation.
- [ ] User can generate draft scene card.
- [ ] Draft preview appears before save.
- [ ] Review gate blocks save until approval.
- [ ] Traceability metadata is created.
- [ ] Status rail shows stage, blocker/warning, and next action.
- [ ] Approved scene card saves to the correct project artifact path.

---

## Success demo script

1. Open Content Engine UI.
2. Select `Lantern Protocol` from registry-driven project list.
3. Select `scene-card`.
4. Enter: `Create a tense scene card for a surveillance discovery sequence that can later become an AI video package.`
5. Click `Validate generation context`.
6. Confirm context warnings are visible but non-blocking.
7. Click `Generate scene card`.
8. Preview generated draft.
9. Confirm status rail moves to `preview-review`.
10. Approve draft.
11. Confirm status rail moves to `save-commit`.
12. Save approved artifact.
13. Confirm generated scene card includes job/review/trace metadata.
