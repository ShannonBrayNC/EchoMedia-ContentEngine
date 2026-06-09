# EchoMedia Content Engine Repo Boundary

EchoMedia Content Engine owns creative and media production workflows. It is not the global Lantern Protocol platform, deployment, trust, or operations control plane. Christina and Codex should route work here only when the requested change belongs to content production, creative packaging, provider-neutral media generation, or rights/release metadata for creative artifacts.

## Belongs Here

- Manuscripts, canon, scripts, story bibles, media packages.
- Prompt templates and creative generation manifests.
- Audio, video, and image production packaging.
- Provider request abstractions for media generation.
- Rights and release gate metadata for creative artifacts.
- Project registry, scene cards, continuity packets, artifact manifests, and export profiles for EchoMedia creative work.

## Does Not Belong Here

- Global Azure deployment control plane.
- ETS trust protocol internals.
- Christina sprint-runner internals.
- OpsHelm ticket, log, or customer operations logic.
- EchoLiving/Casakey short-term rental property operations.
- EchoSpectrum passive RF simulation internals.
- Public website-only marketing changes unless exported as content assets.

## Adjacent Repo Relationships

### EchoChamber

EchoChamber owns translation, audio, voice, and localization workflows when the primary concern is multilingual delivery, speech packaging, or voice pipeline execution. Content Engine may export approved scripts, casting notes, pronunciations, and audio package manifests to EchoChamber, but it should not absorb EchoChamber runtime or service logic.

### SignalForge

SignalForge owns shared deployment, platform contracts, orchestration boundaries, and cross-repo operational control. Content Engine may emit approved creative asset handoff payloads for SignalForge routing, but global Azure infrastructure, worker control planes, and shared Lantern deployment policy belong in SignalForge.

### ETS

ETS owns provenance, evidence, rights verification, and trust protocol internals. Content Engine stores rights/release gate metadata and ETS proof references for creative artifacts, but the proof engine, trust rules, and verification protocol belong in ETS.

### echomedia-website

`echomedia-website` owns public marketing pages, service positioning, landing pages, lead magnets, and site-only presentation. Content Engine may create source content assets, case-study source packets, copy drafts, or media packages for export, but website implementation and public page layout belong in `echomedia-website`.

## Christina And Codex Routing Rules

Route work to Content Engine when the request asks for:

- Story, canon, manuscript, screenplay, chapter, scene, trailer, storyboard, or visual bible work.
- Creative generation templates, prompts, manifests, review gates, export profiles, or provider-neutral deliverable packages.
- Audio/video/image production package preparation.
- Rights/release metadata attached to creative artifacts.
- Project registry, content workflow, and artifact traceability improvements.

Route work away from Content Engine when the request asks for:

- Christina runner behavior, scheduled review loops, approval UI, or personal assistant policy.
- SignalForge deployment, shared contracts, or cross-repo operational routing.
- ETS proof verification, trust protocol internals, or evidence ledger design.
- OpsHelm operational ticket/log analysis.
- EchoLiving/Casakey property operations.
- EchoSpectrum RF simulation or civic resilience internals.
- Public website implementation with no reusable content asset output.

When a request crosses boundaries, Christina should create or update the owning repo issue first, then reference Content Engine only for the creative asset packet or manifest that the owning repo needs.

## Branch And Import Rules

Do not merge divergent branches wholesale into `main`. Use targeted import PRs by subsystem and keep imports reviewable.

Safe imports:

- One project, workflow, schema, or template family per PR.
- Branch artifacts mapped through the project registry and folder contract.
- Creative assets accompanied by manifest, rights/release status, and review notes.
- Workflow or CI changes only after current policy and branch state are reviewed.

Unsafe imports:

- Full branch merges from old content or phase branches.
- Mixed PRs that combine manuscripts, schemas, UI, provider workers, and CI.
- Generated media assets promoted directly into final folders without preview/review approval.
- Imports that bypass canon, proofread, rights, or release gates.

Use `docs/reports/branch-reconciliation-2026-05-23.md` and `docs/legacy-artifact-migration-plan.md` before importing legacy or divergent branch content.
