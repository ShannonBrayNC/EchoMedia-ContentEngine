# Sprint 2 - Artifact Preview and Review Workspace Completion

## Status

Complete for issue #97.

## Files

- Added `ui/src/components/ArtifactPreviewReviewWorkspace.jsx`
- Updated `ui/src/components/SceneCardWorkspace.jsx`
- Updated `ui/src/components/GenerationWorkspace.jsx`
- Updated `ui/src/lib/reviewGate.js`

## Completed behavior

This sprint adds a reusable preview and review workspace for generated artifacts.

The first implementation is wired into the scene-card vertical slice and supports generated drafts before live provider integrations are available.

## Preview modes

The preview workspace supports:

- Markdown preview
- JSON preview
- traceability metadata preview
- save manifest preview
- draft versus approved/saved comparison

## Review actions

The preview workspace supports:

- approve
- reject
- request revision
- save approved

The review gate now supports a `revision-requested` state.

## Metadata shown

The workspace shows:

- artifact id
- artifact state
- generation job id
- review gate id
- trace id
- source reference count
- readiness impact
- preview mode availability
- reviewer notes

## Design guardrails

- Preview is read-only in this slice.
- Editing remains out of scope until an explicit edit mode is added.
- Provider integrations are not required.
- Save remains represented by local manifest behavior until a persistence service is added.

## Why this matters

This creates the dedicated review surface that turns generated draft artifacts into inspectable, approvable, and traceable production candidates.