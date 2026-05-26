# UI Workflow Redesign

This document defines the Sprint 3 UI workflow for EchoMedia Content Engine.

## Purpose

The UI must be a production workspace, not a row of validation buttons. Users need to choose a project, select an artifact type, generate a draft, review it, approve or reject it, and export it through the appropriate package/profile flow.

## Core workspace regions

1. Project selector
2. Artifact type selector
3. Generation instructions
4. Action bar
5. Job/status rail
6. Draft preview panel
7. Review controls
8. Export readiness panel

## Primary flow

```text
Select project
  -> Select artifact type
  -> Enter generation direction
  -> Generate draft
  -> Watch job status
  -> Preview generated artifact
  -> Approve, reject, or request revision
  -> Export approved package
```

## Action semantics

Validation and generation are separate actions.

- Validate: checks readiness and schema requirements.
- Generate: creates a draft job.
- Review: inspects generated output.
- Approve: promotes draft output to approved state.
- Export: creates provider/tool package output.

## Accessibility requirements

- All primary actions must be reachable by keyboard.
- Status messages must not rely on color alone.
- Buttons must have clear labels.
- Form fields must have visible labels.
- Draft preview and status rail must have readable focus order.
- Critical actions must not be drag-only.

## No-provider mode

The Sprint 3 dashboard uses mock API data by default. It should follow the OpenAPI shape without requiring a running backend or paid provider credentials.

## Related issues

- #30
- #34
- #35
- #38
- #39
- #61
- #72
