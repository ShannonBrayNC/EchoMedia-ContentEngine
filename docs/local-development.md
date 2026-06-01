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

Local tooling assumes:

- Python 3.12+ for the no-provider API service, service scripts, validators, and E2E tests.
- Node.js 22 for the UI/dashboard build.
- GitHub Actions for baseline validation, no-provider E2E, and dashboard build checks.
- Optional Ubuntu worker for local media jobs in a later sprint.

## Sprint 4 backend API

The no-provider backend is implemented with the Python standard library:

```bash
python services/content_engine_api.py
```

Default endpoint:

```text
http://127.0.0.1:8080
```

The backend persists local state here unless overridden:

```text
.content-engine/state/content-engine-state.json
```

The backend supports the Sprint 4 workflow rails:

- create project scaffold
- create idea intake
- create generation job
- fetch preview
- fetch traceability
- approve/reject/request revision/supersede
- export approved artifact package
- fetch readiness
- fetch artifact inventory

## EMAS Ad Studio API

EchoMedia Ad Studio has a standalone no-provider API host for the Vanessa ad production workflow:

```bash
python services/emas_http_api.py
```

Default endpoint:

```text
http://127.0.0.1:8081
```

Optional root override:

```powershell
$env:EMAS_ROOT = "C:\GitHub\EchoMedia-ContentEngine"
python services/emas_http_api.py
```

Dashboard/frontend clients should use:

```bash
VITE_EMAS_API_BASE_URL=http://127.0.0.1:8081
```

The EMAS API supports:

- create ad project
- upload and tag Vanessa references
- list references
- submit storyboard frames
- approve/reject storyboard frames
- generation preflight
- publish-ready export package creation
- dashboard status payloads

See the full endpoint contract:

```text
docs/emas-api-dashboard-contract.md
```

## Dashboard with backend API

The dashboard still supports mock fallback. To point it at the local backend, set:

```bash
VITE_CONTENT_ENGINE_API_BASE_URL=http://127.0.0.1:8080
VITE_EMAS_API_BASE_URL=http://127.0.0.1:8081
```

Then run:

```bash
cd ui/content-engine-dashboard
npm install
npm run dev
```

If `VITE_CONTENT_ENGINE_API_BASE_URL` is not set, the dashboard uses the built-in mock client.

## Safe first checks

Run these checks before changing provider behavior:

```bash
python scripts/validate_repo_baseline.py
python tests/e2e/test_no_provider_manuscript_to_export.py
python -m pytest tests/emas

cd ui/content-engine-dashboard
npm install
npm run build
```

The E2E test proves the no-provider workflow:

```text
manuscript idea -> project scaffold -> idea intake -> generation job -> preview -> traceability -> review gate -> approved export -> inventory/readiness
```

The EMAS test suite proves the ad-studio workflow:

```text
ad project scaffold -> reference upload/tag -> storyboard frame review -> consent-gated preflight -> publish-ready export package
```

## Provider use policy

Provider adapters must never call paid services by default. Live provider calls require all of the following:

1. `CONTENT_ENGINE_ENABLE_LIVE_PROVIDERS=true`
2. Provider-specific credentials in local environment only.
3. Dry-run disabled where appropriate.
4. Cost estimate or unknown-cost warning.
5. Manual approval for expensive jobs.

## Launch provider placeholders

`.env.example` includes placeholders for:

- OpenAI
- Azure OpenAI
- Azure Speech
- ElevenLabs
- Runway
- Luma
- local worker
- local TTS
- ComfyUI

Real keys belong in local `.env.local`, GitHub Actions secrets, or deployment secret stores. They must not be committed.

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

Expected local paths:

```text
.content-engine/drafts/
.content-engine/artifacts/
.content-engine/exports/
.content-engine/diagnostics/
.content-engine/state/
```

These paths should be treated as generated runtime output, not canonical source files.

## Troubleshooting rules

- If provider config is missing, the system should fail with a validation message, not a stack trace.
- If no-provider mode is enabled, provider adapters should return dry-run manifests or mocked responses.
- If local worker is offline, jobs should fail cleanly with worker status diagnostics.
- Logs must redact secrets.

## Related issues

- #79 OpenAPI parity
- #80 Backend persistence
- #81 API-driven E2E
- #87 Dashboard build/typecheck CI
- #82 Provider-neutral deliverable package contract
- #83 Provider adapters and dry-run fakes
- #84 Video package export adapters
- #85 Local Ubuntu worker contract
- #86 Branch reconciliation
