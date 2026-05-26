# CI and Release Plan

This document defines the Sprint 2 CI and release baseline.

## Goals

- Validate repository structure before implementation grows.
- Keep default CI free of paid provider calls.
- Parse schema and OpenAPI contract files.
- Provide a future lane for package and release checks.

## Default CI behavior

Default CI runs in safe mode:

```text
CONTENT_ENGINE_NO_PROVIDER_MODE=true
CONTENT_ENGINE_ENABLE_LIVE_PROVIDERS=false
CONTENT_ENGINE_DRY_RUN_PROVIDERS=true
```

## Baseline workflow

The baseline workflow is:

```text
.github/workflows/content-engine-baseline.yml
```

It checks out the repo, sets up Python, and runs:

```bash
python scripts/validate_repo_baseline.py
```

## Current validator scope

The baseline validator checks:

- required Sprint 0 and Sprint 1 documents exist
- required Sprint 1 and Sprint 2 schemas exist
- JSON schemas parse and include required top-level metadata
- OpenAPI file contains expected core API sections

## Future CI expansion

Later sprints should add:

- JSON schema validation against fixtures
- OpenAPI linting
- API unit tests
- UI type-check/build
- provider adapter contract tests with mocks
- worker fake-job tests
- release package manifest validation
- optional manual live-provider smoke workflow

## Release packaging baseline

A release package should eventually include:

- production package manifest
- generated asset manifest
- source references
- prompt/template references
- provider request/result manifests
- review and release metadata
- rights/safety metadata

## Related issues

- #62
- #63
- #61
- #60
