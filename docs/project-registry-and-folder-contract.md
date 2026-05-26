# Project Registry and Folder Contract

This document defines the Sprint 0 project registry and folder expectations for EchoMedia Content Engine.

## Purpose

The Content Engine must treat projects as first-class entities. Story folders, canon files, manuscripts, audio packages, video packages, and generated assets should not float around as orphaned files.

A project registry is the single source of truth for:

- project slug
- display title
- universe or series
- project status
- folder paths
- supported artifact types
- canon entry points
- export targets
- provider permissions
- generation readiness

## Registry goals

The project registry should allow the UI, validators, generators, provider adapters, and export workflows to agree on what a project is.

Required behavior:

- Every project folder should appear in the registry.
- Every registry entry should resolve to an existing project folder.
- The UI project list should come from the registry.
- Validators should report orphaned folders and missing registry entries.
- Project-specific paths should not be hard-coded in provider adapters or UI components.

## Proposed registry shape

```json
{
  "projects": [
    {
      "slug": "lantern-protocol",
      "displayTitle": "Lantern Protocol",
      "universe": "Lantern / Sovereign",
      "status": "active",
      "rootPath": "projects/lantern-protocol",
      "artifactFolders": {
        "canon": "canon",
        "characters": "characters",
        "story": "story",
        "manuscript": "manuscript",
        "storyboards": "storyboards",
        "visualBible": "visual-bible",
        "screenplay": "screenplay",
        "movieGeneration": "movie-generation",
        "audio": "audio",
        "pitch": "pitch",
        "reports": "reports"
      },
      "supportedGenerationTypes": [
        "manuscript",
        "screenplay",
        "scene-card",
        "storyboard",
        "visual-prompt",
        "voice-script",
        "audio-package",
        "video-package",
        "pitch-package"
      ],
      "exportTargets": [
        "generic-json",
        "elevenlabs",
        "azure-speech",
        "openai-audio",
        "openai-video",
        "runway",
        "luma"
      ]
    }
  ]
}
```

## Standard project folder contract

Each active story project should eventually normalize around this structure:

```text
projects/<project-slug>/
  canon/
  characters/
  story/
  manuscript/
  storyboards/
  visual-bible/
  screenplay/
  movie-generation/
  audio/
  pitch/
  reports/
```

Optional future folders:

```text
  art/
  exports/
  timelines/
  provider-manifests/
  release/
```

## Legacy folder policy

Existing folders must not be moved destructively until the migration plan is accepted.

Legacy content should be classified as:

- keep as canonical
- move to canonical folder
- alias to canonical folder
- archive
- delete candidate after review

Every move should produce a before/after migration report.

## Validation requirements

Future validators should check:

- registry entry exists for each project folder
- project root exists for each registry entry
- required folders exist or are explicitly marked optional
- canon entry points exist
- unsupported artifact folders are reported, not silently ignored
- duplicate project slugs are rejected
- export targets map to known export profiles

## Relationship to branch reconciliation

Several branches contain registry/config candidates, especially `sprint6-automation`. Those files should be reviewed and imported through the branch reconciliation plan rather than merged wholesale.

## Related issues

- #31 Restore project registry consistency
- #37 Standardize folder structure
- #58 Branch reconciliation
- #71 Schema migration and legacy artifact normalization
