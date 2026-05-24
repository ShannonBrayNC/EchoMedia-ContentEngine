# Sprint 4 - Provider-Neutral Deliverable Contract Completion

## Status

Complete for issue #82.

## Files

- Added `schemas/deliverables/provider-neutral-deliverable.schema.json`
- Added `docs/provider-contracts/provider-neutral-deliverable-package.md`
- Added `fixtures/deliverables/lantern-protocol-scene-provider-neutral-deliverable.example.json`

## Completed behavior

This sprint defines the provider-neutral deliverable package contract that sits between reviewed Content Engine artifacts and provider-specific export adapters.

The contract identifies the canonical artifact set required before a package can be handed to video/audio providers, storyboard tools, or a local worker.

## Required canonical artifacts

The schema and documentation now require references to:

- production package
- scene timeline
- screenplay or scene cards
- visual prompt pack
- voice package
- subtitle/caption timing
- asset manifest
- provider export manifest

## Provider views

The contract distinguishes canonical artifacts from provider-specific views.

Initial provider views include:

- generic-json
- openai-video
- runway
- luma
- elevenlabs
- azure-speech
- openai-audio
- local-worker
- comfyui

## Review and readiness gates

The package schema includes structured gates for:

- human review approval
- required checks
- source rights
- voice rights
- likeness rights
- provider terms
- release disclosure
- quality gates
- traceability

## Folder and naming conventions

The contract documents the recommended deliverable layout:

```text
<project-root>/deliverables/<package-id>/
  canonical/
  provider-exports/
  review/
  package-manifest.json
```

The recommended naming pattern is:

```text
<project-slug>_<package-type>_<scene-or-sequence-id>_<version>_<provider-or-canonical>.<ext>
```

## Fixture

A Lantern Protocol scene fixture was added so future E2E tests have a concrete export-ready package shape to validate.

## Design guardrails

- This sprint does not call live providers.
- Provider adapters remain out of scope.
- Canonical artifacts must not be mutated by provider views.
- Draft or missing artifacts should block export-ready state.
- Rights/safety/review metadata must be visible before production handoff.

## Why this matters

The Content Engine now has a stable studio handoff contract. Video, audio, storyboard, local worker, and future provider adapters can build against this package shape without rewiring the project, review, traceability, or job-history layers.