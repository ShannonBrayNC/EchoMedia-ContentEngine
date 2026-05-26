# Implementation Sprint 1 - Scene-Card Draft Generation and Preview Completion

## Status

Complete for issue #92.

## Added and updated files

- Added `ui/src/lib/sceneCardDraft.js`
- Updated `ui/src/components/SceneCardWorkspace.jsx`
- Updated `ui/src/components/GenerationWorkspace.jsx`

## What this completes

This slice turns the `Generate scene-card draft` action into a real local draft creator with preview output.

The draft is not saved into final project folders. It remains a preview-only artifact until later review-gate and save-flow issues are completed.

## Draft fields created

The draft builder creates:

- `artifact_type`
- `artifact_id`
- `status`
- `created_at`
- project metadata
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

## Required acceptance behavior

Completed behavior:

- Draft output is previewed before saving.
- Draft has at least one source reference.
- Draft has at least one shot with a visual prompt.
- Draft is not written directly into final project folders.
- Draft creation requires context validation to pass first.

## Preview behavior

The UI now shows:

- draft title
- scene id
- source reference count
- shot count
- draft status
- generated Markdown preview

## Status rail behavior

After draft generation, the rail moves to:

`preview-review`

The next action is intentionally disabled and labeled for review because #94 will implement the review gate and save flow.

## Deferred to later issues

- #93 creates formal generation job metadata.
- #94 adds review gate approval/save flow.
- #95 adds traceability metadata.
- #96 expands status rail integration across the full slice.
