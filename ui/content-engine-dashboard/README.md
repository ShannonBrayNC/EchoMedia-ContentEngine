# Content Engine Dashboard

This is the Sprint 3 UI scaffold for EchoMedia Content Engine.

## Purpose

The dashboard provides a safe no-provider workflow for:

1. Selecting a project.
2. Selecting an artifact type.
3. Entering generation direction.
4. Validating readiness.
5. Generating a draft artifact through a mock API.
6. Reviewing the generated preview.
7. Approving or rejecting the artifact.
8. Preparing approved artifacts for export packaging.

## Local run

```bash
cd ui/content-engine-dashboard
npm install
npm run dev
```

## Build

```bash
cd ui/content-engine-dashboard
npm install
npm run build
```

## Current mode

Sprint 3 uses mock data and does not require a backend or provider credentials.

The UI follows the API shapes defined in:

```text
openapi/content-engine.openapi.yaml
```

## Accessibility notes

- Primary actions are buttons with visible labels.
- Form controls have labels.
- Focus states are visible.
- Status messages use text and not only color.
- The draft preview is keyboard-focusable.
- Critical operations do not require drag and drop.

## Future work

Later sprints should replace the mock API client with a real typed API wrapper once the backend service is implemented.
