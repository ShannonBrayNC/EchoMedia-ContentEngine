# EchoMedia Content Engine

EchoMedia Content Engine is the production pipeline for turning story worlds, manuscripts, scripts, canon, visual bibles, audio plans, and video-generation packages into structured pre-production artifacts for advanced AI media tools.

The goal is not to create another folder of loose prompts. The goal is a traceable engine that can generate, preview, validate, approve, export, and package creative assets across text, audio, video, images, local workers, and cloud providers.

## Current operating model

The repo is moving toward this canonical flow:

```text
Project registry
  -> Canon/context assembly
  -> Prompt template and version
  -> Generation job
  -> Draft artifact
  -> Preview/review
  -> Approved manifest
  -> Audio/video provider request
  -> Async job tracking
  -> Output asset manifest
  -> Final package
  -> Rights/release gate
```

## First sprint status

Sprint 0 is the stabilization sprint. It establishes the repo front door, branch reconciliation, provider configuration rules, project registry expectations, and sprint tracking.

Important Sprint 0 artifacts:

- `docs/reports/branch-reconciliation-2026-05-23.md`
- `docs/local-development.md`
- `docs/architecture.md`
- `docs/architecture/repo-boundary.md`
- `docs/configuration.md`
- `docs/project-registry-and-folder-contract.md`
- `docs/sprint-plan.md`
- `.env.example`

## Branch reconciliation

Branch reconciliation has been completed as an audit artifact. The report is here:

```text
docs/reports/branch-reconciliation-2026-05-23.md
```

Do not merge divergent branches wholesale. The recommended path is targeted import PRs by subsystem:

1. Repo governance and developer front door.
2. Project registry and canon validation.
3. Schema, context, continuity, and memory services.
4. API, job orchestrator, and release manager.
5. UI dashboard scaffold.
6. Phase 2 templates and prompt governance.
7. Lantern art package import.
8. Lantern trilogy/movie/Sovereign content import.

## Repository areas

Expected top-level areas:

```text
config/       Shared project/provider configuration once implemented
docs/         Architecture, development, sprint, and operational documents
projects/     Story projects and generated production artifacts
schemas/      Canonical schemas and validation contracts
services/     API, validators, generators, provider adapters, workers
scripts/      Utility scripts and one-shot tooling
templates/    Prompt and artifact templates
ui/           Content Engine dashboard/workspace
tests/        Unit, integration, contract, and fixture tests
```

Some of these folders may still arrive through follow-up import PRs from reconciled branches.

## Local development quickstart

Read the local runbook first:

```text
docs/local-development.md
```

Safe default mode is **no-provider mode**. Local validation and tests should run without paid provider credentials.

## Provider configuration

Never hard-code provider secrets or machine-specific paths. Start with:

```text
.env.example
docs/configuration.md
```

Provider integrations should read settings through the shared configuration contract before connecting to OpenAI, Azure Speech, ElevenLabs, Runway, Luma, local TTS, ComfyUI, or any future provider.

## Current Sprint 0 issues

- #58 Branch reconciliation
- #59 Provider configuration and secrets contract
- #67 Root README and local runbook
- #68 Labels, milestones, and sprint tracking
- #31 Project registry consistency
- #37 Folder structure consistency

## Development rules

- Do not merge old divergent branches directly into `main`.
- Do not commit real provider keys or tokens.
- Do not call paid providers during normal CI.
- Do not write generated artifacts directly into final project folders without preview/review approval.
- Do not treat generated audio/video/image assets as production-ready without manifest and rights metadata.
- Do not import manuscript changes without canon/proofread review.

## Recommended next implementation lane

After Sprint 0, continue with Sprint 1:

1. Canonical production schema.
2. Artifact storage and manifest policy.
3. Prompt template governance.
4. Canon retrieval/context assembly.
5. Legacy artifact migration plan.

That is the roadbed. The cinematic machinery comes after the rails are straight.
