# Implementation Sprint 1 - Registry-Driven Project Picker Completion

## Status

Complete for issue #90.

## Added files

- `ui/src/lib/projectRegistry.js`
- `ui/src/components/ProjectPicker.jsx`
- `ui/src/components/WorkflowStatusRail.jsx`
- `ui/src/components/GenerationWorkspace.jsx`

## What this completes

This slice adds the first registry-driven UI path for project selection.

The project picker now reads from:

`config/project-registry.json`

The UI helper filters out hidden projects and projects outside the normal visible workflow statuses.

## Behavior

The picker supports:

- loading visible projects from the registry
- selecting a registered project
- showing selected project metadata
- showing project status and canon state
- showing supported generation types
- exposing the selected project to the workspace shell
- projecting selected project state into the compact workflow/status rail

## Status rail integration

The workspace creates an initial rail projection with:

- selected project
- `scene-card` artifact type
- current workflow stage
- stage status
- warnings
- next action

This is intentionally a small projection for the first vertical slice. Later issues should connect it to generation job, review gate, traceability, and export state.

## Notes

The repo does not currently expose a complete indexed UI application scaffold, so this slice provides drop-in React components under `ui/src`. Future UI scaffold work can import `GenerationWorkspace` as the first working content-generation surface.

## Related implementation issues

- #90 - Registry-driven project picker
- #91 - Scene-card workspace UI
- #96 - Compact status rail integration
