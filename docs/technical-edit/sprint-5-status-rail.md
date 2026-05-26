# Sprint 5 - Compact Workflow Status Rail

## Status

Complete.

## Related issue

- #34 - Replace redundant order display with compact workflow/status rail

## Sprint goal

Replace the redundant order display concept with a compact workflow/status rail that shows where the user is in the Content Engine workflow, what is blocked, what is ready, and what the next action should be.

The rail should be a cockpit instrument, not a cargo manifest pasted to the windshield.

---

## Completed deliverables

### 1. Status rail schema

Added:

`schemas/workflows/status-rail.schema.json`

This schema defines the compact UI data contract for showing:

- Project summary
- Artifact summary
- Current workflow stage
- Generation job state
- Review state
- Traceability state
- Export readiness
- Warnings/errors
- Next action
- Link to full details

---

## Why the old order display should be replaced

The current order display concept risks showing too much duplicated metadata in too much space. It also frames the workflow like a passive list instead of an active production path.

The status rail should answer only five questions:

1. What project am I in?
2. What artifact am I working on?
3. What stage am I in?
4. What is blocking me?
5. What should I do next?

Everything else belongs in an expandable detail panel.

---

## Required rail modes

### Collapsed mode

Use collapsed mode by default.

Required display fields:

- Project title or slug
- Artifact type/title
- Current stage
- Stage status
- Blocking warning count
- Next action

Recommended shape:

```text
[Lantern Protocol] [Scene Card] [Preview / Review: warning] [2 blockers] [Approve Draft]
```

### Expanded mode

Expanded mode appears on click/tap or details affordance.

Show:

- Project status
- Canon state
- Artifact destination path
- Job id/state/action
- Review checks passed/failed
- Traceability summary
- Export readiness by profile
- Full warning/error list

---

## Workflow stages

The rail should support these stages:

| Stage | Meaning |
|---|---|
| `select-project` | User must choose a project from the registry. |
| `select-artifact` | User must choose what artifact to work on. |
| `load-context` | Engine loads source/canon/project context. |
| `creative-direction` | User provides generation instructions. |
| `validate-context` | Engine checks whether generation has enough context. |
| `generate-draft` | Engine creates draft output. |
| `preview-review` | User reviews generated draft. |
| `validate-draft` | Engine validates generated draft. |
| `approve` | User approves or rejects draft. |
| `export` | Engine exports approved artifact to a target profile. |
| `save-commit` | Engine saves or commits approved output. |

---

## Stage statuses

| Status | Meaning |
|---|---|
| `not-started` | Stage has not begun. |
| `active` | Stage is current. |
| `blocked` | Stage cannot continue until a required issue is resolved. |
| `warning` | Stage can continue but needs user awareness. |
| `complete` | Stage is complete. |
| `failed` | Stage failed and needs retry or intervention. |

---

## Next action rules

The rail should always recommend one next action.

Examples:

| Situation | Next action |
|---|---|
| No project selected | Select project |
| Project selected but no artifact type | Select artifact type |
| Missing context | Validate source context |
| Context valid | Generate draft |
| Draft generated | Review draft |
| Draft reviewed with failed checks | Resolve failed checks |
| Draft approved | Export package or Save approved artifact |
| Export profile missing fields | Fix export readiness |
| Save target would overwrite | Review overwrite |

The next action can be disabled, but must explain why.

---

## Warning and blocker rules

### Warning

A warning means the workflow can continue, but user awareness is required.

Examples:

- Export profile missing optional fields.
- Visual continuity check not yet run.
- Traceability has downstream artifacts but no canon impact.

### Blocker

A blocker means the workflow must not continue.

Examples:

- No project selected.
- Destination path missing.
- Required schema validation failed.
- Review approval missing before save.
- Locked canon touched without change request.

---

## Data sources

The status rail summarizes state from prior sprint contracts:

| Source | Data used |
|---|---|
| Project registry | Project title, status, canon state |
| Generation job | Job state, action, attempt, outputs |
| Review gate | Review state, checks passed/failed, persistence permission |
| Traceability | Source count, downstream count, canon impact |
| Export profiles | Ready/blocked target profiles |

The rail should never become its own source of truth. It is a compact projection of workflow state.

---

## UI layout guidance

Recommended placement:

- Sticky top bar inside the Content Engine workspace, or
- Slim side rail if the app layout already uses a persistent top nav.

Recommended behavior:

- Collapsed by default.
- Expandable details.
- One primary next-action button.
- Warnings summarized by count with expandable details.
- Critical blockers visually obvious.
- Avoid dense tables in the rail.

---

## Anti-patterns

Do not:

- Recreate the full order display inside the rail.
- Show every source reference in collapsed mode.
- Show every validation detail in collapsed mode.
- Use generic button labels like Run, Process, Build, Start.
- Allow Save/Commit as the next action before review approval.
- Make validation look like generation.

---

## Minimum future implementation slice

The first implementation PR should support this path:

1. User selects a project.
2. User selects `scene-card` artifact type.
3. Rail shows current stage as `creative-direction`.
4. User validates context.
5. Rail updates to `generate-draft`.
6. User generates draft.
7. Rail updates to `preview-review` with job state.
8. User approves draft.
9. Rail updates to `save-commit` or `export`.

This should use mock or local state first if the backend is not ready.

---

## Definition of done

- [x] Status rail schema added.
- [x] Collapsed mode defined.
- [x] Expanded mode defined.
- [x] Workflow stages defined.
- [x] Stage statuses defined.
- [x] Next action rules defined.
- [x] Warning and blocker rules defined.
- [x] Data source mapping documented.
- [x] Minimum future implementation slice identified.

## Next sprint

Sprint 6 should address:

- #33 - Add export profiles for major AI video and audio tools
