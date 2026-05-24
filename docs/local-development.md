# Local Development Runbook

This runbook defines the safe local-development path for EchoMedia Content Engine.

## Default mode: no-provider mode

Local development should start in no-provider mode. This allows developers and Codex agents to validate schemas, run tests, inspect projects, and build UI/API scaffolding without calling paid providers.

Use these environment defaults:

```bash
CONTENT_ENGINE_NO_PROVIDER_MODE=true
CONTENT_ENGINE_ENABLE_LIVE_PROVIDERS=false
CONTENT_ENGINE_DRY_RUN_PROVIDERS=true
CONTENT_ENGINE_REQUIRE_APPROVAL_FOR_PAID_JOBS=true
```

Copy the example environment file before local runs:

```bash
cp .env.example .env.local
```

Do not put real secrets in files committed to the repo.

## Expected runtime tooling

The exact implementation stack is still being reconciled from active branches, but local tooling should assume:

- Python 3.12+ for service scripts and validators.
- Node.js 20+ or 22+ for UI/dashboard and JavaScript tooling.
- GitHub Actions for CI once workflows are accepted.
- Optional Ubuntu worker for local media jobs.

## Safe first checks

After Sprint 0, the repo should support checks in this order:

```bash
# inspect project and configuration docs
ls
ls docs

# no-provider validation placeholder
# exact commands will be added by Sprint 2 API/testing work

# expected future checks
python -m pytest
npm test
npm run build
```

Until the test harness is finalized, do not invent one-off validation commands in random folders. Add them through the testing and CI issues.

## Provider use policy

Provider adapters must never call paid services by default. Live provider calls require all of the following:

1. `CONTENT_ENGINE_ENABLE_LIVE_PROVIDERS=true`
2. Provider-specific credentials in local environment only.
3. Dry-run disabled where appropriate.
4. Cost estimate or unknown-cost warning.
5. Manual approval for expensive jobs.

## Local worker use policy

The Ubuntu/local worker lane is optional and disabled by default:

```bash
LOCAL_WORKER_ENABLED=false
LOCAL_WORKER_BASE_URL=http://127.0.0.1:8090
```

The main app should submit jobs through a worker API or queue, not direct machine-specific shell commands.

## Branch workflow

Use the branch reconciliation report before importing old work:

```text
docs/reports/branch-reconciliation-2026-05-23.md
```

Do not merge divergent branches wholesale. Split imports into small PRs by subsystem.

## Generated artifacts

Generated outputs should not land directly in final project folders. Use draft/review/approved states once the storage policy is implemented.

Expected future local paths:

```text
.content-engine/drafts/
.content-engine/artifacts/
.content-engine/exports/
.content-engine/diagnostics/
```

These paths should be treated as generated runtime output, not canonical source files.

## Troubleshooting rules

- If provider config is missing, the system should fail with a validation message, not a stack trace.
- If no-provider mode is enabled, provider adapters should return dry-run manifests or mocked responses.
- If local worker is offline, jobs should fail cleanly with worker status diagnostics.
- Logs must redact secrets.

## Related issues

- #58 Branch reconciliation
- #59 Provider configuration
- #60 Artifact storage and retention
- #61 API/OpenAPI contract
- #62 Testing strategy
- #63 CI/CD
- #67 Developer front door
