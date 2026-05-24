# Provider-Neutral Deliverable Package Contract

## Purpose

The provider-neutral deliverable package is the canonical handoff contract between EchoMedia Content Engine and downstream AI video, audio, storyboard, image, and local worker tools.

It is not a provider payload. It is the studio package that says, "this scene, sequence, trailer, audiobook segment, or production bundle is ready to be adapted into provider-specific formats."

## Contract boundary

The canonical package answers:

- What project does this deliverable belong to?
- What reviewed artifacts make up the deliverable?
- What provider-specific export views can be produced?
- What rights, safety, review, and quality gates passed?
- Where should package files live?
- Which generation jobs and source artifacts created it?

Provider adapters answer a different question:

- How does this canonical package map to OpenAI video, Runway, Luma, ElevenLabs, Azure Speech, OpenAI audio, a local worker, or ComfyUI?

Keep those layers separate. The canonical contract is the sturdy studio table; provider adapters are the camera mounts bolted to the edges.

## Schema

Canonical schema:

```text
schemas/deliverables/provider-neutral-deliverable.schema.json
```

## Required canonical artifacts

A polished video/audio deliverable package must reference these canonical artifacts:

| Artifact | Purpose | Required state before export |
| --- | --- | --- |
| Production package | Canonical production brief, scene metadata, target format, creative direction | approved or export-ready |
| Scene timeline | Beat/shot/timing structure used for video and audio sync | approved or export-ready |
| Screenplay or scene cards | Human-readable narrative/scene source | approved or export-ready |
| Visual prompt pack | Shot-level visual prompts, style, camera, lighting, and negative prompt guidance | approved or export-ready |
| Voice package | Narrator/character voice plan and provider-neutral voice metadata | approved or export-ready |
| Subtitle/caption timing | Subtitle, caption, alignment, or dialogue timing metadata | approved or export-ready |
| Asset manifest | Input/output asset references, hashes, locations, generated asset metadata | approved or export-ready |
| Provider export manifest | Provider view list and export validation metadata | approved or export-ready |

## Provider views

Provider views are export targets derived from the same canonical package.

Initial provider view targets:

| Provider view | Target | Notes |
| --- | --- | --- |
| generic-json | manifest | Deterministic test/export target for CI and fixtures |
| openai-video | video | Sora-style video package view; exact adapter maps later |
| runway | video | Runway package view for text/image-to-video flows |
| luma | video | Luma/Dream Machine package view |
| elevenlabs | audio | Audiobook, narrator, dialogue, alignment, and sound effects lane |
| azure-speech | audio | Enterprise narration and SSML-friendly lane |
| openai-audio | audio | OpenAI audio/TTS package lane |
| local-worker | local-worker | Local Ubuntu worker handoff package |
| comfyui | image/local-worker | Local image/video prep workflow package |

Provider views must include:

- provider id
- profile id
- target type
- state
- required input list
- output path
- validation status/messages

## Minimum review gates

A package cannot be marked `export-ready` until these checks are represented:

| Check | Required | Notes |
| --- | --- | --- |
| Canonical artifacts present | yes | All required artifacts must be referenced |
| Required artifacts approved | yes | Draft-only artifacts cannot be exported |
| Human review approval | yes | Review gate must record human approval |
| Rights/safety review | yes | Source, likeness, voice, provider terms, disclosure notes |
| Traceability present | yes | Package must link source refs and generation job ids |
| Provider view validation | yes | Each requested provider view must pass or block with messages |
| Asset manifest present | yes | Loose files are not sufficient |

## Rights and safety metadata

The contract requires explicit metadata for:

- source rights checked
- voice rights checked
- likeness rights checked
- provider terms checked
- release disclosure required
- blockers
- review notes

This does not replace legal review. It creates a structured audit trail so generated media cannot drift into release without a visible gate.

## Folder conventions

Recommended package folder layout:

```text
<project-root>/deliverables/<package-id>/
  canonical/
    production-package.json
    scene-timeline.json
    scene-cards.md
    visual-prompt-pack.json
    voice-package.json
    subtitle-caption-timing.json
    asset-manifest.json
    provider-export-manifest.json
  provider-exports/
    generic-json/
    openai-video/
    runway/
    luma/
    elevenlabs/
    azure-speech/
    openai-audio/
    local-worker/
    comfyui/
  review/
    review-gate.json
    rights-safety.json
  package-manifest.json
```

Recommended naming pattern:

```text
<project-slug>_<package-type>_<scene-or-sequence-id>_<version>_<provider-or-canonical>.<ext>
```

Example:

```text
lantern-protocol_scene_scene-001_v0.1.0_canonical.json
lantern-protocol_scene_scene-001_v0.1.0_runway.json
lantern-protocol_scene_scene-001_v0.1.0_elevenlabs.json
```

## State model

Package states:

- draft
- needs-review
- approved
- export-ready
- exported
- blocked
- superseded

Provider view states:

- planned
- ready
- blocked
- exported

Artifact reference states:

- draft
- needs-review
- approved
- export-ready
- exported
- blocked
- missing

## E2E test expectations

Future E2E tests should assert that:

1. A canonical package contains all required canonical artifact refs.
2. Draft or missing artifacts block export-ready state.
3. Human review approval is required.
4. Rights/safety blockers prevent export-ready state.
5. At least one provider view validates before export.
6. Provider views do not mutate canonical artifacts.
7. Generated provider output paths are predictable.
8. Traceability includes source refs and generation job ids.

## Out of scope

This contract does not implement live provider calls.

Out of scope for this sprint:

- OpenAI video adapter implementation
- Runway adapter implementation
- Luma adapter implementation
- ElevenLabs adapter implementation
- Azure Speech adapter implementation
- local worker execution
- ComfyUI workflow execution
- live API authentication

## Implementation notes

Use this contract before adding provider adapters. Adapters should consume a validated canonical package and produce provider-specific export files/manifests without rewriting source artifacts.