# EchoMedia Content Engine Lantern Adapter

## Purpose

Content Engine is Lantern's content transformation vertical. It turns verified source context from ETS, OpsHelm, EchoLiving, EchoAlpha, SignalForge, and Christina into reusable, traceable content assets instead of one-off text.

## Lantern Inputs

The adapter accepts Lantern-safe source artifacts from:

- ticket findings,
- customer pain points,
- guest questions,
- listing and property details,
- market research notes,
- business strategy memos,
- approved production or canon notes.

Inputs must include a stable `artifactId`, `sourceVertical`, `title`, `summary`, `audience`, `tone`, and reuse-rights state. Private source files, provider keys, raw PII, unreleased personal data, and blocked-rights material must not be converted into reusable assets.

## Reusable Outputs

`services/lantern_content_assets.py` can turn one source artifact into:

- LinkedIn posts,
- short-form scripts,
- email sequences,
- newsletters,
- knowledge base articles,
- sales collateral,
- campaign briefs.

Every asset carries metadata for source vertical, audience, tone, approval state, reuse rights, target channel, status, brand voice profile, source context references, and optional ETS proof reference.

## Event Mapping

Lantern `opportunity.detected` events create content backlog items. The source artifact remains the traceability anchor, while each generated asset receives a stable `assetId`, target channel, draft preview, source hash, and approval-gated status.

```json
{
  "eventType": "opportunity.detected",
  "sourceArtifactId": "lantern-opportunity-001",
  "sourceVertical": "echoliving",
  "assets": ["linkedin-post", "short-form-script", "email-sequence"],
  "approvalState": "required"
}
```

## Approval Flow

Generated assets start as drafts with `approvalState=required` and `status=draft`. `format_for_channel` can produce a channel preview, but `publishAllowed` remains false until `approve_content_asset` records a human approval. Publishing, sending, provider execution, and public reuse stay blocked for rejected, blocked, or unapproved assets.

## Brand Voice And Feedback

Assets include `brandVoiceProfile` so Christina or a later campaign builder can preserve the intended voice across channels. Performance feedback is scaffolded as a `not-connected` object so analytics can be attached later without changing asset identity.

## Validation

The no-provider validation path is:

```text
python -m pytest tests/e2e/test_lantern_content_assets.py
python scripts/validate_repo_baseline.py
```
