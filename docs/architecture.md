# Architecture Overview

EchoMedia Content Engine is organized as a production pipeline for story-world development and AI media pre-production.

## Architectural principles

1. Canon first.
2. Generated artifacts must be traceable.
3. Provider integrations must be swappable.
4. Paid providers must be opt-in.
5. Draft generation must not overwrite approved content.
6. UI actions must distinguish validation, generation, assembly, export, and save.
7. Local workers are service boundaries, not random shell calls.
8. Prompts, schemas, manifests, and context packs are source artifacts.

## Core domains

### Project registry

The registry defines known projects and their artifact folders, supported generation types, export targets, and status.

### Canon and context assembly

Generation must use deterministic context packs assembled from canon, characters, story state, visual bible, voice packages, timeline records, and prior approved artifacts.

### Prompt templates

Prompt templates should be versioned, validated, and linked to generated artifacts.

### Generation jobs

A generation job records:

- project
- artifact type
- context manifest
- prompt template/version
- user direction
- provider/export target
- draft output
- status
- warnings/errors
- approval state

### Review gate

Generated content should land as draft/review output before it becomes canonical project content.

### Artifact storage

Generated outputs must have manifests that capture source references, request hashes, provider metadata, output paths, approval state, and rights/release metadata.

### Provider adapters

Audio and video providers should use provider-neutral contracts.

Audio target providers:

- ElevenLabs
- Azure Speech
- OpenAI audio/TTS
- Local TTS

Video target providers:

- Runway
- OpenAI video / Sora-style APIs
- Luma / Dream Machine
- Kling
- Pika
- Local ComfyUI/open video workflows

### Local worker

The Ubuntu/local worker lane should expose capabilities through an API or queue. The main app should submit jobs and collect structured outputs.

### CI and release

CI should validate registry, schemas, tests, export profiles, manifests, and secrets policy. CI should not call paid providers by default.

## Pipeline view

```text
Project registry
  -> Canon/context assembly
  -> Prompt template/version
  -> Generation job
  -> Draft artifact
  -> Preview/review
  -> Approved artifact manifest
  -> Provider request or export package
  -> Async job tracking
  -> Output manifest
  -> Release-readiness review
```

## Provider request flow

```text
UI generation request
  -> API validates project and artifact type
  -> context pack assembled
  -> prompt template rendered
  -> cost/readiness checks
  -> provider adapter dry-run or live call
  -> async job state stored
  -> outputs attached to manifest
  -> review gate
```

## Related issues

- #30 UI generation workspace
- #32 Production package schema
- #33 Export profiles
- #38 Preview/review gate
- #39 Generation jobs
- #45 Voice abstraction
- #51 Video abstraction
- #56 Async job orchestration
- #57 Audio/video timeline bridge
- #60 Artifact storage
- #61 API/OpenAPI
- #64 Cost controls
- #65 Observability
- #66 Rights/release gate
