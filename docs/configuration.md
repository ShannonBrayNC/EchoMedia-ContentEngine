# Configuration and Secrets Contract

This document defines the Sprint 0 configuration rules for EchoMedia Content Engine.

## Goals

- Keep provider secrets out of source code.
- Keep UI code away from raw secrets.
- Allow CI and local tests to run without paid provider calls.
- Support local worker and cloud provider configuration through one predictable pattern.
- Redact sensitive values from logs, manifests, errors, and diagnostics.

## Configuration layers

Configuration should resolve in this order:

1. Repository defaults and schema-defined defaults.
2. Project registry and project-level config.
3. Provider profile config.
4. Environment variables.
5. Local development override file such as `.env.local`.
6. CI secrets, only for explicitly gated live-provider smoke tests.

No implementation should read random process environment variables directly from UI components or provider business logic. Provider adapters should receive validated configuration from a shared config service/module.

## Safe defaults

Default behavior must be safe:

```bash
CONTENT_ENGINE_NO_PROVIDER_MODE=true
CONTENT_ENGINE_ENABLE_LIVE_PROVIDERS=false
CONTENT_ENGINE_DRY_RUN_PROVIDERS=true
CONTENT_ENGINE_REQUIRE_APPROVAL_FOR_PAID_JOBS=true
CONTENT_ENGINE_REDACT_SECRETS=true
```

## Provider categories

### Text/audio/video cloud providers

- OpenAI
- Azure Speech
- ElevenLabs
- Runway
- Luma / Dream Machine
- Kling, Pika, and other future providers

### Local providers and workers

- Local TTS engines
- Ubuntu media worker
- ComfyUI
- Local transcoding/alignment tools

## Secret handling rules

- Never commit real secrets.
- Never expose provider keys to the browser.
- Never write full provider request headers into logs.
- Never include bearer tokens in manifests.
- Redact environment values matching `KEY`, `TOKEN`, `SECRET`, `PASSWORD`, or provider-specific secret fields.
- Provider errors should be normalized before surfacing in the UI.

## Provider enablement rules

Provider adapters must check:

1. Is live provider mode enabled?
2. Is the provider configured?
3. Is dry-run mode enabled?
4. Is the project allowed to use this provider?
5. Does the request exceed budget limits?
6. Does the request require manual approval?
7. Does the provider support the requested artifact type?

## Local worker configuration

The local worker should be treated as a service boundary, not a pile of shell calls.

Expected settings:

```bash
LOCAL_WORKER_ENABLED=false
LOCAL_WORKER_BASE_URL=http://127.0.0.1:8090
LOCAL_WORKER_SHARED_INPUT_ROOT=./.content-engine/worker-input
LOCAL_WORKER_SHARED_OUTPUT_ROOT=./.content-engine/worker-output
LOCAL_WORKER_TIMEOUT_SECONDS=3600
```

The worker should expose future capability/status endpoints such as:

```text
GET /health
GET /capabilities
POST /jobs
GET /jobs/{id}
```

## No-provider and dry-run behavior

In no-provider mode, generation should produce one of the following:

- A validated request manifest.
- A mocked provider response.
- A dry-run artifact package.
- A clear validation error describing what would be required for live execution.

It should not silently call live services.

## Config examples

Use `.env.example` as the canonical example file. Real developer overrides belong in `.env.local`, which should remain untracked.

## Required follow-up implementation

- Shared config loader.
- Config validation schema.
- Secret redaction utility.
- Provider capability discovery without credentials where possible.
- Provider-specific config adapters.

## Related issues

- #59 Environment, secrets, and provider configuration
- #64 Cost estimation and budget guardrails
- #65 Observability and redaction
