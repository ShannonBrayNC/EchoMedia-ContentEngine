# Lantern Content Engine Adapter

## Purpose

The Content Engine Lantern adapter turns creative outputs, canon decisions, provider jobs, and approved production packages into traceable Lantern artifacts.

The Content Engine also carries the narrative doctrine for Lantern: systems without consent become dangerous. That story principle should map directly into platform rules.

## Adapter responsibilities

- Register story worlds, manuscripts, scripts, visual bibles, audio plans, and provider packages as Lantern artifacts.
- Preserve canon source, prompt template version, provider configuration, rights state, and approval state.
- Emit reusable creative assets into SignalForge only after preview/review approval.
- Attach ETS proof references for approved manifests and exported packages.
- Block production-ready status when rights or release gates are missing.

## Supported event types

- `artifact.created`
- `recommendation.created`
- `approval.required`
- `approval.granted`
- `action.queued`
- `action.completed`
- `action.failed`

## Supported action types

- `internal-draft`
- `publication`
- `data-export`

## Required asset manifest fields

| Field | Purpose |
| --- | --- |
| `projectId` | Content Engine project ID. |
| `artifactId` | Draft or approved artifact ID. |
| `artifactType` | Manuscript, script, visual bible, audio plan, video package, image package, etc. |
| `canonVersion` | Canon/context version used to generate or approve the asset. |
| `promptTemplateVersion` | Prompt template version. |
| `provider` | Provider target, or `none` for no-provider mode. |
| `rightsStatus` | Draft, review-required, cleared, blocked, or unknown. |
| `approvalState` | Lantern approval state. |
| `evidenceHash` | Hash of canonical manifest or exported package. |
| `etsProofRef` | ETS proof reference when available. |

## Consent Theme Bible mapping

At least one narrative doctrine must map to a concrete platform rule.

| Story theme | Platform rule |
| --- | --- |
| Systems operating without consent corrupt human agency. | External action categories require explicit approval and consent state. |
| Unverified memory becomes manipulation. | Memory writes require proof, source, and human-visible explanation. |
| Automation without provenance becomes a ghost in the machine. | Cross-system recommendations without ETS verification are quarantined. |

## Done criteria for implementation

- `LANTERN_CANON_REGISTRY.md` lists story worlds and canon sources.
- `CONSENT_THEME_BIBLE.md` maps narrative doctrine to platform rules.
- Approved creative assets can emit a Lantern artifact payload.
- Production-ready exports require manifest, rights status, approval state, and ETS proof reference.
- Tests or fixtures cover draft asset, missing rights gate, approved manifest, and provider job event.
