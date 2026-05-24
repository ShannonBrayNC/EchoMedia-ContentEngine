# New Project Creation Workflow

This document defines the project creation workflow for Content Engine.

## Purpose

Users need a clear way to start a brand-new story project without manually creating folders or editing the project registry.

## Required inputs

A new project needs:

- Project title
- Project slug
- Universe or series name
- Initial story type
- Target formats
- Project status

## Scaffolded folders

The default scaffold follows the project registry and folder contract:

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

## Starter artifacts

The creation flow should prepare starter artifact records for:

- Project manifest
- Idea intake file
- Canon seed file
- Character seed file
- Readiness checklist

## UI behavior

The dashboard should offer a `Create New Project` workflow. In no-provider mode, the UI creates a mock scaffold summary and adds the new project to the project selector. Later backend work should persist the scaffold and registry update.

## Post-create next steps

After creation, users should be shown:

1. Load idea intake.
2. Add canon seed.
3. Add characters.
4. Generate outline.
5. Review readiness checklist.

## Related issue

- #73
