# EMAS API and Dashboard Contract

This document defines the API/dashboard wiring contract for EchoMedia Ad Studio.

The current implementation is intentionally standard-library and no-provider safe. It does not call paid AI providers and it does not auto-post to Instagram.

## Runtime

Start the standalone EMAS API host:

```powershell
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

Health check:

```http
GET /health
```

## Route Family

All EMAS dashboard routes live under:

```text
/api/ad-studio/projects/{projectName}/ads/{adName}
```

The current route handler is framework-neutral:

```text
services/emas/api.py
```

A future FastAPI or Azure Functions host should call `route_emas()` or the underlying services rather than duplicating workflow logic.

## Create Ad Project

```http
POST /api/ad-studio/projects/{projectName}/ads
```

Example body:

```json
{
  "adName": "Vanessa-Christina-Outfit-Update-Ad",
  "actor": "ShannonBrayNC",
  "force": false
}
```

Returns:

```json
{
  "created": true,
  "adPath": "projects/Vanessa/ads/Vanessa-Christina-Outfit-Update-Ad",
  "warnings": []
}
```

## Dashboard Summary

```http
GET /api/ad-studio/projects/{projectName}/ads/{adName}/dashboard
```

Returns UI-ready status:

```json
{
  "project": "Vanessa",
  "ad": "Vanessa-Christina-Outfit-Update-Ad",
  "status": "Storyboard Draft",
  "format": "Instagram Reel / Story / Feed",
  "durationSeconds": 32,
  "tabs": [
    "Production Brief",
    "Script",
    "Storyboard",
    "References",
    "Website Mockups",
    "Audio",
    "Logo Assets",
    "Approvals",
    "Exports"
  ],
  "counts": {
    "references": 0,
    "approvedReferences": 0,
    "scenes": 8,
    "frames": 0,
    "approvedFrames": 0,
    "approvedAudio": 0,
    "exports": 0
  },
  "missingAssets": [
    "Vanessa reference uploads",
    "pink outfit reference",
    "approved storyboard frames",
    "approved website mockups",
    "EchoMedia/Lantern logo lockup"
  ],
  "nextBestAction": "Upload Vanessa reference images."
}
```

## Upload and Tag Vanessa References

Current RC upload route expects a server-local `sourcePath`. This is suitable for local operators, Codex/Christina workflows, and worker-side uploads. Browser multipart upload should be added in a later UI sprint.

```http
POST /api/ad-studio/projects/{projectName}/ads/{adName}/references
```

Example body:

```json
{
  "sourcePath": "C:/temp/vanessa-pink-reference.jpg",
  "actor": "ShannonBrayNC",
  "tags": ["pink-updated-outfit", "smiling", "soft-light"],
  "outfit": "pink-updated-outfit",
  "expression": "smiling",
  "pose": "looking-at-screen",
  "sceneCandidates": ["scene-06", "scene-07"],
  "qualityScore": 0.94,
  "notes": "Candidate for final review scene."
}
```

List references:

```http
GET /api/ad-studio/projects/{projectName}/ads/{adName}/references
```

Tag an existing reference:

```http
POST /api/ad-studio/projects/{projectName}/ads/{adName}/references/{assetId}/tag
```

Example body:

```json
{
  "actor": "ShannonBrayNC",
  "tags": ["hero-shot"],
  "approved": true
}
```

## Storyboard Frames

Submit frame:

```http
POST /api/ad-studio/projects/{projectName}/ads/{adName}/storyboard/frames
```

Example body:

```json
{
  "sourcePath": "C:/temp/scene-01-frame.png",
  "sceneId": "scene-01",
  "actor": "ShannonBrayNC",
  "notes": "Opening shot candidate."
}
```

List frames:

```http
GET /api/ad-studio/projects/{projectName}/ads/{adName}/storyboard/frames
```

Approve frame:

```http
POST /api/ad-studio/projects/{projectName}/ads/{adName}/storyboard/frames/{frameId}/approve
```

Reject frame:

```http
POST /api/ad-studio/projects/{projectName}/ads/{adName}/storyboard/frames/{frameId}/reject
```

## Generation Preflight

Preflight must run before any provider call.

```http
POST /api/ad-studio/projects/{projectName}/ads/{adName}/generate/preflight
```

Example body:

```json
{
  "actor": "ShannonBrayNC",
  "subjectId": "Vanessa",
  "intendedUse": "social_media",
  "platform": "instagram",
  "prompt": "Create the Christina outfit update scene.",
  "referencePaths": [],
  "outputCount": 4
}
```

If consent is pending, revoked, expired, missing, or out of scope, this returns `409` with reasons. This is expected until `projects/Vanessa/source-registry.json` is changed from `pending` to `approved` with a verified consent record.

## Publish Export Package

For RC, publish means creating an export package and manifest. It does not post to Instagram.

```http
POST /api/ad-studio/projects/{projectName}/ads/{adName}/outputs/{outputId}/publish
```

Example body:

```json
{
  "actor": "ShannonBrayNC",
  "platform": "instagram",
  "format": "reels-9x16",
  "intendedUse": "social_media",
  "outputMetadataPath": "projects/Vanessa/ads/Vanessa-Christina-Outfit-Update-Ad/outputs/draft/output-1.json"
}
```

The output metadata must include:

```json
{
  "state": "approved",
  "disclosure": "AI-generated authorized likeness image.",
  "assets": [
    "path/to/final-video.mp4"
  ],
  "caption": "EchoMedia.ai | Powered by Lantern Protocol"
}
```

## Dashboard Client Guidance

Recommended frontend environment variable:

```text
VITE_EMAS_API_BASE_URL=http://127.0.0.1:8081
```

Recommended dashboard actions:

1. Load dashboard summary.
2. Show `missingAssets` and `nextBestAction` prominently.
3. Upload/tag references through the References tab.
4. Submit/approve/reject frames through the Storyboard tab.
5. Run preflight before generation buttons are enabled.
6. Disable publish until the output is approved and preflight/source-registry checks pass.
7. Surface blocked reasons directly to the user.

## Tests

Run:

```powershell
python -m pytest tests/emas
```

The API/dashboard contract is covered by:

```text
tests/emas/test_assets_frames_dashboard_api.py
```
