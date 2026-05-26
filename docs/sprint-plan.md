# Functional Sprint Plan

This document records the execution order for EchoMedia Content Engine.

## Sprint 0: Repo Stabilization

Goal: establish the developer front door, branch reconciliation report, provider configuration contract, and project registry/folder rules.

Artifacts completed in this sprint:

- Root README
- Environment example
- Local development runbook
- Configuration and secrets contract
- Architecture overview
- Project registry and folder contract
- Branch reconciliation report

## Sprint 1: Schema, Storage, Context, and Migration

Goal: define production package schemas, artifact storage, context assembly, prompt governance, traceability, and migration rules for legacy project content.

## Sprint 2: API, Testing, and CI

Goal: define the backend API contract, job model, test strategy, CI workflow, and release packaging checks.

## Sprint 3: UI Workflow

Goal: create the generation workspace, status rail, review gate, action semantics, and accessible keyboard-friendly UI flow.

## Sprint 4: Provider Abstractions

Goal: define provider-neutral audio/video contracts, export profiles, cost controls, job orchestration, logging, and diagnostics.

## Sprint 5: Audio Providers

Goal: implement voice generation support for approved cloud and local TTS providers with quality and rights gates.

## Sprint 6: Video Providers

Goal: implement video generation adapters and package exports for approved AI video providers.

## Sprint 7: Local Worker

Goal: make the Ubuntu media workstation a controlled worker for local processing, ComfyUI workflows, local TTS, and media preparation.

## Sprint 8: Content Expansion

Goal: apply the engine consistently to Lantern Protocol, The Sovereign Exception, and future story projects.

## Sprint 9: External Event Ingestion and Webhook Hardening

Goal: add inbound provider event handling, starting with ElevenLabs webhooks for transcription completion and voice lifecycle notices.

Key tracking issues:

- #103 ElevenLabs webhook receiver and inbound provider event contract
- #104 Webhook security, replay protection, and provider event diagnostics

Required outcomes:

- Public HTTPS webhook route convention documented for local tunnel, Azure-hosted, and production deployments.
- Provider events normalized into a canonical event model.
- Webhook payloads correlated to projects, jobs, artifacts, chapters, scenes, or audio assets.
- Duplicate and replayed callbacks handled idempotently.
- Webhook diagnostics added without logging secrets.
- CI remains no-provider and uses deterministic fixtures.

## Sprint 10: RC Readiness, Recommendation Registry, and Operating-Loop Integration

Goal: expose recommendations and sprint candidates in a machine-readable way and produce a release-candidate readiness report for Content Engine.

Key tracking issues:

- #102 Open recommendations and sprint candidates for Christina operating loop
- #105 Recommendation registry and RC readiness report

Required outcomes:

- Recommendation registry format documented.
- Open recommendations mapped to GitHub issues where possible.
- Duplicate-detection keys prevent repeated issue creation.
- RC status report covers repo hygiene, CI, UI workflow, API workflow, provider safety, webhook readiness, artifact traceability, rights/release gates, docs, and deployment.
- Export pattern supports SignalForge and Christina/Lantern review loops.

## RC Hardening Lane

Goal: convert the engine from feature-complete candidate to release candidate.

Required gates:

- Baseline validation and no-provider E2E pass in CI.
- Dashboard build passes in CI.
- Provider calls remain disabled by default in CI and local safe mode.
- Every generated artifact has source traceability and review status.
- Export packages enforce approval and rights/release gates.
- Webhooks are secure, idempotent, and diagnosable.
- Open PRs and legacy branch content are reconciled before large content import.
- A current RC readiness report exists under `docs/reports/`.

## Execution rule

Later sprints depend on the Sprint 0 and Sprint 1 foundations. Build the contracts before importing large branches or implementing provider-specific behavior. Provider integrations, webhooks, and worker jobs must default to deterministic dry-run behavior until explicitly enabled for live use.