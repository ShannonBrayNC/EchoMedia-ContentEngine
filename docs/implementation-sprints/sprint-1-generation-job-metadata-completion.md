# Implementation Sprint 1 - Generation Job Metadata Completion

## Status

Complete for issue #93.

## Added and updated files

- Added `ui/src/lib/generationJob.js`
- Updated `ui/src/lib/sceneCardDraft.js`
- Updated `ui/src/components/SceneCardWorkspace.jsx`
- Updated `ui/src/components/GenerationWorkspace.jsx`

## What this completes

This slice adds first-pass generation job metadata for scene-card drafts.

Each generated scene-card draft now receives a job record that captures:

- job id
- version
- project slug
- artifact type
- action
- state
- request payload
- source context
- output reference
- warnings
- errors
- created/updated timestamps

## Job lifecycle

The current local lifecycle is:

```text
createSceneCardGenerationJob
  -> state: generating
buildSceneCardDraft
  -> attach generation_job_id to draft
completeGenerationJob
  -> state: generated
```

If draft creation throws, the job is transitioned through:

```text
failGenerationJob
  -> state: failed
```

## UI behavior

The scene-card workspace now displays a generation job card with:

- job id
- state
- action
- warning count
- error count
- error messages when present

The draft preview now displays the attached generation job id.

## Status rail behavior

The rail receives a `job` summary when a job exists:

- `job_id`
- `state`
- `action`
- `attempt`

When draft generation fails, the rail enters a failed generate-draft state with a readable disabled reason.

## Deferred to later issues

- #94 adds review gate approval and save flow.
- #95 adds formal traceability metadata.
- #96 expands status rail integration across review and trace state.
