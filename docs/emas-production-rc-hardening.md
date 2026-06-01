# EMAS Production RC Hardening

This document tracks the implementation lane for the following release blockers and the follow-up integration sprint:

- EMAS-001: real production adapters are needed.
- EMAS-003: source-registry consent verification is still needed.
- EMAS-006: publish is still a stub.
- EMAS-008: append-only production audit logging is still open.
- EMAS-S2: project/ad scaffolding, generation preflight, CLI wrappers, and CI.

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

## EMAS-S2: Integration Sprint

Implemented in:

```text
services/emas/project_scaffold.py
services/emas/preflight.py
scripts/emas_create_ad_project.py
scripts/emas_generation_preflight.py
tools/New-EmasAdProject.ps1
tools/Test-EmasGenerationPreflight.ps1
.github/workflows/emas-tests.yml
```

Capabilities:

- Creates a repeatable Vanessa ad project scaffold under `projects/{ProjectName}/ads/{AdName}`.
- Seeds production brief, scripts, captions, storyboard, shot list, scene prompts, and metadata indexes.
- Writes audit events when ad projects are created.
- Runs generation preflight before provider calls.
- Normalizes risky prompt wording into authorized synthetic likeness language.
- Blocks pending/rejected references.
- Blocks invalid output counts.
- Requires source-registry consent before generation.
- Provides PowerShell 7+ wrappers for local operators and Codex/Christina workflows.
- Adds GitHub Actions CI for EMAS tests.

Example scaffold command:

```powershell
pwsh ./tools/New-EmasAdProject.ps1 `
  -ProjectName Vanessa `
  -AdName Vanessa-Christina-Outfit-Update-Ad `
  -Actor ShannonBrayNC
```

Example preflight command:

```powershell
pwsh ./tools/Test-EmasGenerationPreflight.ps1 `
  -ProjectName Vanessa `
  -AdName Vanessa-Christina-Outfit-Update-Ad `
  -IntendedUse social_media `
  -Platform instagram `
  -Prompt "Create the Christina outfit update scene."
```

## Tests

Added tests:

```text
tests/emas/test_audit.py
tests/emas/test_source_registry.py
tests/emas/test_publishing.py
tests/emas/test_project_scaffold.py
tests/emas/test_preflight.py
```

Recommended local command:

```powershell
python -m pytest tests/emas
```

CI workflow:

```text
.github/workflows/emas-tests.yml
```

## Remaining Integration Work

These modules are production-RC service primitives and workflow utilities. The next integration pass should wire them into the actual API/dashboard route layer once that app scaffold lands.

Required wiring points:

- API route layer should call `AdProjectScaffoldService.create_ad_project`.
- Generation endpoints must call `GenerationPreflightService.validate` before provider calls.
- Approval workflows should append audit events.
- Export and publish endpoints should call `ExportPackagePublishAdapter.publish`.
- UI should expose blocked reasons from consent/preflight/publish results.
- CI should run `python -m pytest tests/emas`.
