# Production Schema and Traceability Contract

This document defines the Sprint 1 canonical production package model for EchoMedia Content Engine.

## Purpose

The Content Engine must generate structured production artifacts that can move from manuscript to screenplay to audio and video packages without losing source, canon, or approval context.

## Canonical flow

```text
Project
  -> Canon and context package
  -> Prompt template
  -> Generation job
  -> Draft artifact
  -> Review/approval
  -> Production package
  -> Provider request manifests
  -> Generated media manifests
  -> Release package
```

## Core identifiers

Every traceable object should include stable IDs:

- `projectId`
- `packageId`
- `sceneId`
- `shotId`
- `assetId`
- `sourceRefId`
- `contextManifestId`
- `promptTemplateId`
- `generationJobId`

IDs should be deterministic where possible and should not depend on provider-specific job IDs.

## Source references

A source reference links generated artifacts back to authoritative material.

Required fields:

- `sourceType`: canon, manuscript, screenplay, character, visual-bible, voice-package, timeline, prior-artifact
- `path`
- `hash`
- `anchor`: optional chapter/scene/line/paragraph identifier
- `notes`: optional human-readable note

## Production package

A production package contains:

- project metadata
- package metadata
- source references
- scenes
- shots
- characters
- voice references
- audio references
- subtitle/timing references
- export profile references
- provider request manifests
- generated asset manifests
- review state
- release state

## Scene model

A scene should carry:

- `sceneId`
- title
- source references
- screenplay reference
- summary
- location reference
- character references
- shot references
- timeline references
- export profile references
- continuity notes

## Shot model

A shot should carry:

- `shotId`
- `sceneId`
- source references
- visual prompt
- negative prompt
- camera direction
- lighting direction
- visual style reference
- location reference
- character references
- input image references
- input video reference
- duration
- aspect ratio/size/fps/seed
- voice references
- audio references
- dialogue timing reference
- subtitle references
- sound cue references
- export profile references

## Traceability requirements

Generated artifacts must record:

- source references used
- context manifest used
- prompt template/version used
- generation job ID
- provider/export profile used
- output asset manifest ID
- review/approval state

## Canon change impact

A future validator should be able to answer:

- Which scenes depend on this canon entry?
- Which audio files were generated from this dialogue line?
- Which video jobs used this shot prompt?
- Which exports are stale after a canon change?
- Which final packages need regeneration or review?

## Draft versus approved artifacts

Draft artifacts are not canonical. Approved artifacts can become part of a production package. Final release artifacts require rights and release-readiness review.

## Related issues

- #32 Production package schema
- #36 Artifact traceability
- #57 Audio/video timeline bridge
- #60 Asset storage and manifest policy
- #66 Release-readiness review
