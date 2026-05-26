# Lantern Asset Manifest Schema

## Purpose

The Lantern Asset Manifest is the handoff contract for canon, story, audio, visual, video, and marketing assets produced by EchoMedia Content Engine.

It prevents creative output from becoming production-ready unless canon, rights, approval, consent, and verification state travel with the asset.

## Minimum manifest fields

| Field | Required | Description |
| --- | --- | --- |
| `artifactId` | Yes | Stable Content Engine artifact ID. |
| `canonId` | Yes | Canon registry entry that anchors the asset. |
| `projectId` | Yes | Source project or story-world ID. |
| `assetType` | Yes | `manuscript`, `audio-package`, `visual-bible`, `video-package`, `marketing-package`, or other controlled type. |
| `provider` | Yes | Target provider or `provider-neutral`. |
| `promptTemplateVersion` | Yes | Prompt/template version used to create the asset. |
| `rightsStatus` | Yes | `unknown`, `review-required`, `cleared`, or `blocked`. |
| `approvalState` | Yes | `not-required`, `required`, `pending`, `approved`, or `rejected`. |
| `consentState` | Yes | Lantern consent state. |
| `evidenceHash` | Yes | SHA-256 hash of the manifest-safe evidence payload. |
| `etsProofRef` | No | ETS proof reference or explicit local/mock marker. |
| `sourceFiles` | Yes | Manifest-safe source references. No secrets or private provider keys. |
| `reviewOwner` | Yes | Human owner responsible for approval/release. |
| `releaseGateStatus` | Yes | `draft`, `blocked`, `ready-for-review`, or `released`. |

## Release gate rules

A manifest may not be marked `released` unless:

1. `rightsStatus` is `cleared`.
2. `approvalState` is `approved`.
3. `consentState` is `granted` or `not-required`.
4. `evidenceHash` is present and valid.
5. `etsProofRef` is present or the package is explicitly marked local/mock.
6. Source files exclude private drafts, provider keys, raw credentials, private likeness releases, or unreleased personal data.

## SignalForge handoff shape

```json
{
  "eventType": "artifact.created",
  "sourceRepo": "ShannonBrayNC/EchoMedia-ContentEngine",
  "sourceSystem": "content-engine",
  "targetSystem": "signalforge",
  "actionType": "publication",
  "approvalState": "required",
  "consentState": "requested",
  "payload": {
    "artifactId": "asset-001",
    "canonId": "lantern-origin-001",
    "assetType": "audio-package",
    "releaseGateStatus": "ready-for-review"
  }
}
```

## No-provider implementation

`services/lantern_verified_assets.py` implements the release gate described by this schema.

It can:

- build a manifest-safe Lantern asset manifest,
- hash manifest evidence,
- keep draft assets out of production-ready status,
- block assets with missing or blocked rights,
- require human approval, consent, and ETS proof before release,
- emit a SignalForge `LanternArtifact` handoff only for released manifests.

## Validation checklist

- Draft assets cannot be exported as released packages.
- Blocked rights status blocks release.
- Missing approval blocks release.
- Missing consent blocks external provider execution or publishing.
- Missing proof blocks verified SignalForge routing.
- Provider webhook payloads must include replay-protection metadata before they affect release state.
