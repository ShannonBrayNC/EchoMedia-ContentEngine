# EMAS Dashboard UI Sprint

This sprint wires the EchoMedia Ad Studio API into the React/Vite dashboard without disrupting the existing Content Engine generation workspace.

## Implemented Files

```text
ui/content-engine-dashboard/src/emasApi.ts
ui/content-engine-dashboard/src/EmasAdStudio.tsx
ui/content-engine-dashboard/src/main.tsx
ui/content-engine-dashboard/src/styles.css
ui/content-engine-dashboard/src/vite-env.d.ts
```

## Runtime Setup

Start the EMAS API:

```powershell
python services/emas_http_api.py
```

Default EMAS API endpoint:

```text
http://127.0.0.1:8081
```

Start the Content Engine API if the main workspace also needs live API mode:

```powershell
python services/content_engine_api.py
```

Default Content Engine API endpoint:

```text
http://127.0.0.1:8080
```

Set dashboard environment variables:

```powershell
$env:VITE_CONTENT_ENGINE_API_BASE_URL = "http://127.0.0.1:8080"
$env:VITE_EMAS_API_BASE_URL = "http://127.0.0.1:8081"
```

Run the dashboard:

```powershell
cd ui/content-engine-dashboard
npm install
npm run dev
```

## Dashboard Behavior

The new EMAS panel is mounted beside the existing dashboard workspace through:

```text
ui/content-engine-dashboard/src/main.tsx
```

It provides UI controls for:

- Creating the Vanessa / Christina ad project.
- Refreshing the dashboard status payload.
- Uploading and tagging Vanessa reference images from a server-local path.
- Approving Vanessa references.
- Submitting storyboard frames from a server-local path.
- Approving or rejecting storyboard frames.
- Running generation preflight before provider calls.
- Publishing a verified export package from approved output metadata.

## Safety and RC Boundaries

The dashboard does not upload binary files directly from the browser yet. It sends `sourcePath` values to the local EMAS API host, which copies and audits server-local files.

This sprint intentionally preserves the RC safety rules:

- No paid provider calls.
- No Instagram auto-posting.
- Generation preflight must pass before publish controls activate.
- Publish means export-package creation, not platform posting.
- Blocked reasons from the API are surfaced in the UI.

## Operator Flow

1. Start `services/emas_http_api.py`.
2. Open the dashboard.
3. Use **Create ad project** if the ad folder does not exist.
4. Upload Vanessa references using local file paths.
5. Approve the best references.
6. Submit storyboard frames for `scene-01` through `scene-08`.
7. Approve frames.
8. Run preflight.
9. Once preflight passes and output metadata exists, publish the export package.

## Current Known Limitation

`projects/Vanessa/source-registry.json` is intentionally pending until verified consent is attached and marked approved. Because of that, preflight will block by design until the source registry is updated.

## Validation

Run backend tests:

```powershell
python -m pytest tests/emas
```

Run dashboard build:

```powershell
cd ui/content-engine-dashboard
npm run build
```
