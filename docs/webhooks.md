# Provider Webhooks

This document defines the inbound provider webhook pattern for Content Engine.

## Current endpoint convention

```text
POST /api/webhooks/elevenlabs
```

Production URL example:

```text
https://api.echomedia.ai/api/webhooks/elevenlabs
```

Local tunnel example:

```text
https://<dev-tunnel-host>/api/webhooks/elevenlabs
```

## ElevenLabs events

Initial supported events:

- `transcription_completed`
- `voice_removal_notice`

The webhook receiver normalizes each callback into a provider-neutral event record with:

- provider
- provider event type
- delivery key
- received timestamp
- correlation metadata
- redacted headers
- redacted payload snapshot
- raw payload hash
- warnings

## Correlation metadata

When creating provider jobs, include metadata fields that can flow back through the webhook payload:

```json
{
  "projectId": "lantern-protocol",
  "jobId": "job-audio-001",
  "artifactId": "artifact-audio-001",
  "chapterId": "chapter-01",
  "sceneId": "scene-01",
  "audioAssetId": "audio-001"
}
```

The receiver accepts either camelCase or snake_case keys. Missing metadata is not fatal, but it is recorded as `missing-correlation-metadata` so diagnostics can surface orphaned events.

## Security model

The receiver must never treat provider callbacks as trusted final state by default. Webhooks are event inputs, not release gates.

Required controls:

- Validate payload shape and size.
- Redact sensitive headers and payload fields.
- Store event hashes for audit and duplicate detection.
- Use idempotency keys from provider event IDs, delivery IDs, or payload hashes.
- Support replay protection through delivery keys.
- Support a project-owned HMAC fallback using `CONTENT_ENGINE_WEBHOOK_SECRET` and `X-Content-Engine-Signature`.
- Do not log provider credentials or signed payload material.

## CI behavior

CI uses deterministic webhook fixtures only. It must not call live ElevenLabs endpoints and must not require provider credentials.

Current fixture test:

```text
tests/e2e/test_elevenlabs_webhook_event.py
```

## RC requirement

Webhook readiness is not complete until:

- duplicate callbacks are idempotent;
- invalid callbacks fail safely;
- correlation warnings are visible;
- event diagnostics are available;
- production endpoint hosting is documented;
- provider secrets stay out of logs and manifests.
