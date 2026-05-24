# Implementation Sprint 1 - Scene-Card Workspace UI Completion

## Status

Complete for issue #91.

## Added and updated files

- Added `ui/src/components/SceneCardWorkspace.jsx`
- Updated `ui/src/components/GenerationWorkspace.jsx`

## What this completes

This slice adds the first real scene-card workspace UI.

The workspace now supports:

- selecting `scene-card` as the first supported artifact workflow
- entering creative direction
- entering optional source/context notes
- previewing the destination path
- validating context separately from draft generation
- updating status rail state based on project, direction, validation, and blockers

## Action separation

The UI now presents two distinct actions:

1. `Validate generation context`
2. `Generate scene-card draft`

Validation checks whether the scene-card workflow has enough local context for the first vertical slice. Draft generation is intentionally stubbed for issue #92.

## Context validation behavior

The first validation pass checks and reports warnings for:

- missing active canon files
- missing optional source/context notes
- very brief creative direction

Warnings do not block the first vertical slice. Missing project or missing scene-card support blocks progress.

## Status rail behavior

The rail now updates across these states:

- `select-project`
- `creative-direction`
- `validate-context`
- `generate-draft`
- `select-artifact` when scene-card is unsupported

## Deferred to #92

Issue #92 should implement actual draft scene-card generation and preview output.

## Related implementation issues

- #90 - Registry-driven project picker
- #91 - Scene-card workspace UI
- #92 - Draft scene-card generation and preview
- #96 - Compact status rail integration
