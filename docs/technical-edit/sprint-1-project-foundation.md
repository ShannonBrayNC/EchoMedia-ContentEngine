# Sprint 1 - Project Registry and Folder Consistency Foundation

## Status

Complete.

## Related issues

- #31 - Restore project registry consistency for Lantern Protocol and all book projects
- #37 - Standardize folder structure across all story projects

## Sprint goal

Create a stable foundation for project discovery, validation, and future generation workflows.

Before the UI can generate content, it needs to know what projects exist, where their artifacts live, what generation types they support, and which folders are required. Sprint 1 provides that contract.

---

## Completed deliverables

### 1. Sprint plan

Added `docs/technical-edit/sprint-plan.md`.

This breaks the technical edit backlog into six implementation sprints:

1. Project registry and folder consistency foundation.
2. Real generation workspace and action semantics.
3. Production package and generation job model.
4. Preview/review gate and traceability.
5. Compact workflow/status rail.
6. Export profiles and tool adapters.

### 2. Project registry schema

Added `schemas/projects/project-registry.schema.json`.

The schema defines the single source of truth for project visibility and project metadata.

Required project fields include:

- `slug`
- `title`
- `root_path`
- `status`
- `artifact_paths`
- `supported_generation_types`

The registry also supports:

- `series`
- `universe`
- `visibility`
- `canon_state`
- `active_canon_files`
- `legacy_aliases`
- `export_targets`

### 3. Folder contract

This document defines the standard folder structure expected by the project registry.

Required logical artifact folders:

| Logical key | Purpose |
|---|---|
| `canon` | Canon rules, doctrine, continuity, locked facts |
| `characters` | Character profiles, continuity sheets, casting/voice notes |
| `story` | Outlines, treatments, beats, sequence plans |
| `manuscript` | Novel/book manuscript files |
| `storyboards` | Storyboard plans, panels, beat boards, teaser boards |
| `visual_bible` | Visual rules, style references, location/character looks |
| `screenplay` | Screenplay drafts, assembled scripts, scene pages |
| `movie_generation` | AI video/audio production packages and tool-ready outputs |
| `pitch` | Producer pitch, decks, one-pagers, franchise packets |
| `reports` | Audits, technical edits, validation reports, drift reports |

---

## Project registry rules

### Rule 1 - Every real project must have one registry entry

If a story/book folder exists and should be available to the engine, it must appear in the project registry.

Examples:

- `fiction/lantern-protocol`
- `The-Sovereign-Exception`

### Rule 2 - Every registry entry must resolve to a repo path

A registry entry cannot point to a missing folder unless the project status is `archived` or explicitly marked as a future placeholder.

### Rule 3 - UI project lists must use the registry

The UI should not hard-code project names. The project picker should be generated from the registry and filtered by `visibility` and `status`.

### Rule 4 - Generators must use artifact paths from the registry

Generation workflows should not guess folder names. They should resolve paths through `artifact_paths`.

### Rule 5 - Legacy aliases are temporary migration tools

If existing folders use inconsistent names, `legacy_aliases` can preserve compatibility during migration. Aliases should not become the long-term contract.

---

## Folder migration rules

No file movement should happen automatically during Sprint 1.

Before moving or renaming folders:

1. Inventory the current project folders.
2. Compare each project to the folder contract.
3. Build a gap matrix.
4. Decide whether each mismatch should be migrated, aliased, or left as legacy.
5. Open a reviewed migration PR.

---

## Validation requirements for future work

A future validator should report:

- Project folders missing from the registry.
- Registry projects with missing root paths.
- Missing required artifact folders.
- Empty critical folders for active projects.
- Unsupported generation types.
- Export targets with no matching export profile.
- Legacy aliases still being used after migration.

---

## Example registry entry

```json
{
  "slug": "lantern-protocol",
  "title": "Lantern Protocol",
  "series": "Lantern Protocol Trilogy",
  "universe": "Lantern / Sovereign Shared Universe",
  "root_path": "fiction/lantern-protocol",
  "status": "active",
  "visibility": "visible",
  "canon_state": "candidate",
  "active_canon_files": [
    "fiction/lantern-protocol/canon"
  ],
  "artifact_paths": {
    "canon": "fiction/lantern-protocol/canon",
    "characters": "fiction/lantern-protocol/characters",
    "story": "fiction/lantern-protocol/story",
    "manuscript": "fiction/lantern-protocol/manuscript",
    "storyboards": "fiction/lantern-protocol/storyboards",
    "visual_bible": "fiction/lantern-protocol/visual-bible",
    "screenplay": "fiction/lantern-protocol/screenplay",
    "movie_generation": "fiction/lantern-protocol/movie-generation",
    "pitch": "fiction/lantern-protocol/pitch",
    "reports": "fiction/lantern-protocol/reports"
  },
  "legacy_aliases": [],
  "supported_generation_types": [
    "canon",
    "character",
    "story-outline",
    "manuscript",
    "screenplay",
    "scene-card",
    "storyboard",
    "visual-prompt",
    "production-package",
    "pitch",
    "audio-script",
    "tool-export"
  ],
  "export_targets": [
    "generic-json",
    "runway",
    "pika",
    "luma-dream-machine",
    "kling",
    "sora-style",
    "elevenlabs"
  ]
}
```

---

## Sprint 1 definition of done

- [x] Technical edit issues broken into sprints.
- [x] Project registry schema added.
- [x] Folder contract documented.
- [x] Registry rules documented.
- [x] Migration rules documented.
- [x] Future validation requirements documented.

## Next sprint

Sprint 2 should address:

- #30 - real generation workspace
- #35 - validation/generation/action separation

Sprint 2 should not add more validators until the UI has a proper generation workspace and clear action semantics.
