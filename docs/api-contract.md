# Content Engine API Contract

This document defines the Sprint 2 API surface for EchoMedia Content Engine.

## Goals

- Give the UI one stable backend contract.
- Keep provider actions behind validated API calls.
- Support no-provider mode and dry-run responses.
- Track generation jobs consistently.
- Keep drafts separate from approved artifacts.
- Make future provider adapters swappable.

## API groups

### Health and configuration

- `GET /health`
- `GET /config/runtime`

### Projects

- `GET /projects`
- `GET /projects/{projectId}`
- `GET /projects/{projectId}/artifacts`

### Schemas and profiles

- `GET /schemas`
- `GET /export-profiles`
- `GET /providers/capabilities`

### Generation jobs

- `POST /generation/jobs`
- `GET /generation/jobs/{jobId}`
- `POST /generation/jobs/{jobId}/cancel`
- `POST /generation/jobs/{jobId}/retry`

### Review and approval

- `POST /reviews/{artifactId}/approve`
- `POST /reviews/{artifactId}/reject`
- `POST /reviews/{artifactId}/request-revision`

### Artifacts and manifests

- `GET /artifacts/{artifactId}`
- `GET /manifests/{manifestId}`
- `POST /exports/packages`

### Worker status

- `GET /workers/capabilities`
- `GET /workers/jobs/{workerJobId}`

## Error model

All errors should follow one shape:

```json
{
  "error": {
    "code": "CONFIG_MISSING",
    "message": "Provider configuration is missing.",
    "details": {},
    "correlationId": "trace-123"
  }
}
```

## Provider safety

The API must not call live paid providers unless live provider mode is enabled, dry-run mode is disabled, configuration is valid, and the request passes approval/cost checks.

## Related issues

- #61 API/OpenAPI contract
- #39 Generation job/state model
- #38 Preview/review gate
- #59 Configuration contract
- #64 Cost controls
- #65 Observability
