# Sprint 6 - Export Profiles and Tool Adapters

## Status

Complete.

## Related issue

- #33 - Add export profiles for major AI video and audio tools

## Sprint goal

Define the export-profile contract and add an initial catalog of export profiles so a single canonical production package can be transformed into tool-specific packages without rewriting the source content.

This sprint creates the adapter bay: canonical package in, tool-shaped output out.

---

## Completed deliverables

### 1. Export profile schema

Added:

`schemas/exports/export-profile.schema.json`

The schema defines how a canonical production package maps into target tools or output formats.

It includes:

- Profile identity
- Target tool
- Target category
- Supported input package types
- Required fields
- Optional fields
- Practical limits
- Rendering rules
- Output format
- Validation rules

### 2. Initial export profile catalog

Added:

`exports/profiles/export-profiles.catalog.json`

Initial profiles:

| Profile | Category | Purpose |
|---|---|---|
| `generic-json` | Generic JSON | Preserve canonical package structure for future adapters. |
| `runway` | AI video | Shot-based prompt package for Runway-style workflows. |
| `pika` | AI video | Concise motion-focused video prompt package. |
| `luma-dream-machine` | AI video | Cinematic shot package with camera and lighting emphasis. |
| `kling` | AI video | Motion/action and character-continuity prompt package. |
| `sora-style` | AI video | High-context scene package for Sora-style video models. |
| `elevenlabs` | AI audio | Narration/dialogue/voice package for audiobook and dialogue generation. |
| `storyboard-deck` | Storyboard | Deck/panel package for storyboard and pitch support. |

---

## Export profile rules

### Rule 1 - Export profiles transform, they do not author canon

Export profiles should not change the canonical production package.

They transform canonical fields into target-shaped outputs.

### Rule 2 - Profiles must declare required fields

Every profile must define required fields using JSONPath-like source paths.

Missing required fields should produce validation errors before export.

### Rule 3 - Profiles should declare optional fields with warning behavior

Optional fields can improve output quality. Missing optional fields should usually warn, not block.

Examples:

- Reference assets
- Negative prompts
- Voice notes
- Continuity notes
- Visual style notes

### Rule 4 - Profiles should define output format and naming pattern

Every export should have predictable output naming.

Examples:

```text
{project_slug}-{package_id}-runway.md
{project_slug}-{package_id}-elevenlabs.md
{project_slug}-{package_id}-generic.json
```

### Rule 5 - Tool profiles should stay data-driven

Adding a new tool should mean adding a new profile entry, not rewriting the production package schema.

---

## Export readiness states

The production package already tracks export target readiness. Export profiles should drive readiness checks.

Recommended states:

| State | Meaning |
|---|---|
| `not-ready` | Required fields are missing. |
| `ready` | Required fields are present. |
| `exported` | Export package was generated. |
| `failed` | Export failed and requires inspection. |

---

## Minimum future implementation slice

The first implementation PR should support this narrow path:

1. Load a canonical production package.
2. Load `exports/profiles/export-profiles.catalog.json`.
3. Select the `generic-json` and `runway` profiles.
4. Validate required fields against the package.
5. Generate export output files using the profile naming pattern.
6. Update export readiness state.
7. Surface any missing fields in the status rail.

Do not attempt all profiles in the first implementation PR.

---

## Integration with previous sprints

| Sprint | Integration |
|---|---|
| Sprint 1 | Export targets are referenced by project registry metadata. |
| Sprint 2 | Export is a distinct action from Generate, Validate, Assemble, and Save/Commit. |
| Sprint 3 | Export profiles transform production packages. |
| Sprint 4 | Exports require review/approval rules before persistence. |
| Sprint 5 | Export readiness appears in the compact status rail. |

---

## Definition of done

- [x] Export profile schema added.
- [x] Initial export profile catalog added.
- [x] Major target categories represented.
- [x] Required/optional field model defined.
- [x] Output format and naming rules defined.
- [x] Export readiness rules documented.
- [x] Minimum future implementation slice identified.

## Backlog after Sprint 6

Recommended next issues/PRs:

1. Implement project registry inventory and validation.
2. Build the first generation workspace UI vertical slice.
3. Implement generation-job creation for one `scene-card` workflow.
4. Implement review gate creation for generated drafts.
5. Implement export validation for `generic-json` and `runway`.
6. Render the compact status rail from local/mock state, then backend state.
