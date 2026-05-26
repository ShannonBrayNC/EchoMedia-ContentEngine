# Testing Strategy

This document defines the Sprint 2 testing strategy for EchoMedia Content Engine.

## Goals

- Run default tests without paid provider calls.
- Validate schemas and contract files early.
- Support mocked provider adapter tests later.
- Support full pipeline tests using fixtures.
- Keep UI, API, worker, and provider behavior testable in isolation.

## Test layers

### 1. Schema tests

Validate JSON schemas and fixture files for:

- production packages
- generated asset manifests
- voice packages
- scene timelines
- template records
- generation jobs

### 2. Contract tests

Future provider adapters should be tested with mocked request/response fixtures. Contract tests should not call live providers.

### 3. API tests

API tests should verify endpoint request/response shape against the OpenAPI contract.

### 4. Job lifecycle tests

Job lifecycle tests should cover:

- draft request
- queued
- generating
- generated
- needs review
- approved
- failed
- cancelled
- superseded

### 5. Review gate tests

Review tests should prove generated artifacts do not overwrite approved artifacts without explicit approval.

### 6. Worker tests

Worker tests should use fake worker capabilities and fake jobs.

### 7. UI tests

UI tests should verify core generation workflow, status display, preview/review actions, and accessible controls.

## No-provider mode

The default test mode is no-provider mode:

```bash
CONTENT_ENGINE_NO_PROVIDER_MODE=true
CONTENT_ENGINE_ENABLE_LIVE_PROVIDERS=false
CONTENT_ENGINE_DRY_RUN_PROVIDERS=true
```

Live-provider smoke tests must be manually triggered and require secrets.

## Fixture strategy

Use a small synthetic project for deterministic tests and Lantern Protocol samples for realistic workflow tests.

Recommended folders:

```text
tests/fixtures/projects/minimal-project/
tests/fixtures/manifests/
tests/fixtures/jobs/
tests/fixtures/provider-responses/
```

## CI expectations

Default CI should:

- check required repo files exist
- parse JSON schemas
- parse OpenAPI YAML
- block obvious secret filenames or values
- avoid live provider calls

## Related issues

- #62
- #63
- #61
- #39
- #38
