# Sprint 3 - Generation Job State History Completion

## Status

Complete for issue #88.

## Files

- Added `ui/src/lib/generationJobHistory.js`
- Added `ui/src/components/GenerationJobHistoryPanel.jsx`
- Updated `ui/src/components/GenerationWorkspace.jsx`

## Completed behavior

This sprint adds a reusable generation job state/history model for long-running content work.

The first implementation is wired into the scene-card vertical slice so generation is tracked separately from validation and review UI state.

## Job states

The shared state model supports:

- draft-request
- queued
- generating
- generated
- needs-review
- approved
- exported
- failed
- superseded
- cancelled

## State transitions

The model defines allowed transitions so future async/background execution can reuse the same lifecycle without redesigning the UI.

Examples:

- generating -> generated
- generated -> needs-review
- needs-review -> approved
- approved -> exported
- failed -> queued
- generated/approved/exported -> superseded

## Job history behavior

The scene-card workflow now records a per-project job history with:

- job id
- project slug
- artifact type
- action
- attempt number
- output count
- errors
- state events
- updated timestamp
- retry/supersede placeholders

## UI behavior

A new `GenerationJobHistoryPanel` shows generation jobs beneath the workspace. The panel shows active, failed, exported, and total counts, plus expandable state-event breadcrumbs per job.

## Design guardrails

- The job model remains provider-neutral.
- No live provider calls are introduced.
- Failed jobs do not write project artifacts.
- Save/export remains local manifest behavior until a persistence/export service is added.
- Future backend async orchestration can adopt the same state model.

## Why this matters

This separates generation work from button validation and review UI state. The Content Engine now has a visible job timeline for generated outputs, which is required before movie-ready packages, provider exports, and async workers can be added safely.