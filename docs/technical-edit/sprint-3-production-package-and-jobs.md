# Sprint 3 - Production Package and Generation Job Model

## Status

Complete.

## Related issues

- #32 - Define pre-movie production package schema for AI video tools
- #39 - Create generation job/state model for long-running content work

## Sprint goal

Define the structured data models required for movie-ready production packages and long-running generation work.

Sprint 1 gave the engine a project map. Sprint 2 gave it a cockpit. Sprint 3 gives it the cargo manifest and flight recorder.

---

## Completed deliverables

### 1. Production package schema

Added:

`schemas/production/production-package.schema.json`

This schema defines a canonical pre-movie production package that can support:

- Scene packages
- Sequence packages
- Trailer packages
- Feature packages
- Pitch packages
- Audio packages
- Tool export packages

The schema captures:

- Project metadata
- Source references
- Canon references
- Visual references
- Character references
- Scene definitions
- Shot definitions
- Camera direction
- Lighting and motion notes
- Visual prompts
- Negative prompts
- Audio/dialogue/narration guidance
- Export target readiness

### 2. Generation job schema

Added:

`schemas/workflows/generation-job.schema.json`

This schema defines how long-running or reviewable generation work is tracked.

It supports:

- Job identity
- Project slug
- Artifact type
- Action type
- Job state
- Generation request
- Source context
- Outputs
- Warnings
- Errors
- Review state
- Retry state
- Supersession tracking

---

## Generation job state machine

Allowed job states:

| State | Meaning |
|---|---|
| `draft-request` | User is composing or editing the request before running it. |
| `queued` | Request is accepted and waiting to run. |
| `generating` | The engine is producing draft output. |
| `generated` | Draft output exists but has not been reviewed. |
| `needs-review` | Draft output requires user or workflow review. |
| `approved` | Draft output is approved for save/export. |
| `exported` | Output has been transformed into one or more export packages. |
| `failed` | Job failed and requires retry or inspection. |
| `superseded` | A newer job replaces this one. |
| `cancelled` | User or workflow cancelled the job. |

Recommended happy path:

```text
draft-request
  -> queued
    -> generating
      -> generated
        -> needs-review
          -> approved
            -> exported or saved
```

Recommended failure path:

```text
queued
  -> generating
    -> failed
      -> queued or superseded
```

---

## Production package rules

### Rule 1 - Packages are canonical until exported

A production package should be tool-neutral. It should not be written only for Runway, Pika, Luma, Kling, ElevenLabs, or any single tool.

Tool-specific details belong in export profiles and export packages.

### Rule 2 - Every scene must include source references

Scene packages must be traceable back to source material.

Minimum references should include at least one of:

- manuscript section
- screenplay scene
- story outline
- canon item
- visual bible item

### Rule 3 - Every scene must include at least one shot

A scene without a shot list is not ready for AI video production.

### Rule 4 - Exports must report readiness

Each export target tracks:

- profile
- status
- output path
- validation notes

This prevents pretending a package is ready for a tool when it is missing required fields.

### Rule 5 - Generated packages should reference their generation job

The `generation_job_id` field links the production package back to the request, source context, warnings, and review state that produced it.

---

## Review and persistence rules

Generated packages should not be saved into final project locations until reviewed.

Expected lifecycle:

1. User creates a generation request.
2. Generation job enters `queued` or `generating`.
3. Draft production package is created.
4. Draft is previewed.
5. Draft is validated.
6. Draft moves to `needs-review`.
7. User approves or rejects.
8. Approved package can be saved or exported.

---

## Minimum future implementation slice

The first implementation PR should support a narrow vertical slice:

1. Create a `generation-job` for a `scene-card` or `production-package` request.
2. Generate a draft JSON package using the production package schema.
3. Store the draft as preview output only.
4. Validate that the draft has project metadata, source refs, at least one scene, and at least one shot.
5. Mark the draft as `needs-review`.
6. Allow approval to move it to `approved`.

Do not attempt every export tool in the first implementation.

---

## Relationship to Sprint 4

Sprint 4 should use these schemas to define:

- Preview/review gate behavior
- Artifact traceability model
- Draft approval flow
- Canon-change downstream impact rules

Sprint 3 intentionally stops before implementing review UX.

---

## Definition of done

- [x] Production package schema added.
- [x] Generation job schema added.
- [x] Job state machine documented.
- [x] Production package rules documented.
- [x] Review/persistence expectations documented.
- [x] Minimum future implementation slice identified.

## Next sprint

Sprint 4 should address:

- #38 - Add preview/review gate before generated artifacts are saved
- #36 - Add artifact traceability from manuscript to screenplay to video package
