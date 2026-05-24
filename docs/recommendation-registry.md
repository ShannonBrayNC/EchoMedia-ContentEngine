# Recommendation Registry

The recommendation registry is the Content Engine handoff contract for Christina, SignalForge, and Lantern operating loops.

The goal is to expose actionable work without scraping prose-only reports or creating duplicate GitHub issues.

## Record shape

```json
{
  "id": "content-engine-rec-001",
  "title": "Add ElevenLabs webhook receiver",
  "type": "software-change",
  "source": "technical-review",
  "priority": "high",
  "status": "open",
  "ownerRepo": "ShannonBrayNC/EchoMedia-ContentEngine",
  "targetSprint": "Sprint 9",
  "duplicateKey": "content-engine:webhooks:elevenlabs-receiver",
  "linkedIssues": [103],
  "relatedArtifacts": ["docs/webhooks.md"],
  "approvalRequired": true,
  "notes": "Provider callbacks must be idempotent, redacted, and no-provider safe."
}
```

## Required fields

| Field | Purpose |
|---|---|
| `id` | Stable registry ID. |
| `title` | Human-readable recommendation. |
| `type` | `software-change`, `process-change`, `content-workflow-change`, `documentation-change`, `investigation`, or `campaign-opportunity`. |
| `source` | Review, issue, artifact, user request, provider finding, or operating-loop source. |
| `priority` | `urgent`, `high`, `medium`, or `low`. |
| `status` | `open`, `planned`, `in-progress`, `blocked`, `done`, or `deferred`. |
| `ownerRepo` | Owning repository. |
| `targetSprint` | Sprint bucket or RC lane. |
| `duplicateKey` | Deterministic dedupe key. |
| `linkedIssues` | Existing GitHub issues or PRs. |
| `approvalRequired` | Whether publishing, sending, release, or live provider execution needs human approval. |

## Duplicate key convention

Use this format:

```text
<repo-scope>:<domain>:<stable-slug>
```

Examples:

```text
content-engine:webhooks:elevenlabs-receiver
content-engine:rc:readiness-report
content-engine:lantern:reusable-asset-pipeline
```

## Current high-value recommendations

| Recommendation | Type | Priority | Sprint | Tracking |
|---|---|---:|---|---|
| Add ElevenLabs webhook receiver and provider event contract | software-change | high | Sprint 9 | #103 |
| Add webhook security, replay protection, and diagnostics | software-change | high | Sprint 9 | #104 |
| Add RC readiness report and machine-readable recommendation export | process-change | high | Sprint 10 | #105 |
| Expose open recommendations to Christina/Lantern | software-change | high | Sprint 10 | #102 |
| Keep provider calls dry-run by default in CI | process-change | high | RC Hardening | CI workflow |

## Operating-loop rules

- Do not create a new GitHub issue if the duplicate key already maps to an open issue.
- Publishing and sending actions must remain approval-gated.
- Live provider calls must remain opt-in and outside normal CI.
- Recommendations should point to source artifacts and linked issues whenever possible.
- Closed recommendations should retain their duplicate key for future dedupe.
