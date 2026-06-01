# EMAS Production RC Hardening

This document tracks the implementation lane for the following release blockers:

- EMAS-001: real production adapters are needed.
- EMAS-003: source-registry consent verification is still needed.
- EMAS-006: publish is still a stub.
- EMAS-008: append-only production audit logging is still open.

## Implementation Location

```text
services/emas/
```

## EMAS-008: Append-only Production Audit Logging

Implemented in:

```text
services/emas/audit.py
```

Capabilities:

- JSONL append-only event log.
- Event hash chaining with `previousHash` and `eventHash`.
- Tamper verification.
- Path traversal rejection for audit log paths.
- Event schema covering actor, action, project, ad, target, result, reason, metadata, and timestamps.

Fast structural PowerShell verifier:

```text
tools/Test-EmasAudit.ps1
```

Python verification remains the source of truth because it recomputes canonical hashes.

## EMAS-003: Source Registry Consent Verification

Implemented in:

```text
services/emas/source_registry.py
```

Capabilities:

- JSON source-registry adapter.
- Consent verification for generate, approve, publish, and export actions.
- Blocks missing, pending, rejected, expired, revoked, unauthorized use, restricted use, and unauthorized platform.
- Writes audit events for consent checks when an audit logger is provided.

Seed registry:

```text
projects/Vanessa/source-registry.json
```

The seed is intentionally `pending` until signed/verified consent is attached.

## EMAS-006: Publish Stub Replacement

Implemented in:

```text
services/emas/publishing.py
```

RC definition of publish:

- Verify output metadata exists.
- Require state `approved` or `publish_ready`.
- Require disclosure metadata.
- Verify source-registry consent for the requested use and platform.
- Require at least one approved asset.
- Copy assets into the export package folder.
- Write optional caption file.
- Write `publish-manifest.json`.
- Update output metadata to `published`.
- Write append-only audit events for blocked or completed publishing.

Direct Instagram auto-posting is intentionally out of scope for the RC.

## EMAS-001: Production Adapters

Implemented in:

```text
services/emas/adapters.py
config/emas-adapters.json
```

Capabilities:

- Adapter registry.
- Local filesystem storage adapter.
- Safe no-provider image generation adapter for CI and local development.
- Config-driven adapter intent for storage, generation, publish, and audit.

Future adapters should implement the same contracts without changing workflow logic.

## Tests

Added tests:

```text
tests/emas/test_audit.py
tests/emas/test_source_registry.py
tests/emas/test_publishing.py
```

Recommended local command:

```powershell
python -m pytest tests/emas
```

## Remaining Integration Work

These modules are production-RC service primitives. The next integration pass should wire them into the actual API/dashboard route layer once that app scaffold lands.

Required wiring points:

- Generation preflight must call `SourceRegistryService.verify_consent`.
- Approval workflows should append audit events.
- Export and publish endpoints should call `ExportPackagePublishAdapter.publish`.
- UI should expose blocked reasons from consent/publish results.
- CI should run `python -m pytest tests/emas`.
