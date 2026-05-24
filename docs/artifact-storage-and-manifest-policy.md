# Artifact Storage and Manifest Policy

This document defines the Sprint 1 storage and manifest policy for generated Content Engine artifacts.

## Goals

- Keep draft, review, approved, exported, and released artifacts distinct.
- Keep large generated media out of Git unless explicitly approved.
- Preserve traceability from source to output.
- Support local workers and cloud providers with the same manifest pattern.
- Make cleanup and retention rules explicit.

## Artifact states

Artifacts can be in one of these states:

- `draft`: generated but not reviewed
- `review`: ready for review
- `approved`: accepted into the project package
- `exported`: transformed for a target provider/tool
- `released`: part of a final deliverable
- `failed`: job failed or partial output is unusable
- `superseded`: replaced by a newer artifact

## Runtime output roots

Runtime output should use generated folders outside canonical source content by default:

```text
.content-engine/drafts/
.content-engine/artifacts/
.content-engine/exports/
.content-engine/diagnostics/
.content-engine/worker-input/
.content-engine/worker-output/
```

These should not be treated as canon. Approved artifacts may later be copied or promoted into project folders through review gates.

## Project artifact folders

Project-owned artifacts may be stored under:

```text
projects/<project-slug>/exports/
projects/<project-slug>/provider-manifests/
projects/<project-slug>/timelines/
projects/<project-slug>/release/
```

Large binary media should use a storage policy before being committed to Git.

## Manifest requirements

Every generated artifact should have a manifest record containing:

- artifact ID
- project ID
- package ID or generation job ID
- artifact type
- path or external URI
- hash
- state
- provider/export profile
- source references
- context manifest ID
- prompt template ID/version
- request hash
- created timestamp
- review state
- rights/commercial metadata where applicable

## File naming convention

Use predictable, lowercase, hyphenated names:

```text
<project>-<scene>-<shot>-<artifact-type>-<short-hash>.<ext>
```

Examples:

```text
lantern-protocol-scene-004-shot-002-video-request-a1b2c3.json
lantern-protocol-scene-004-dialogue-audio-91de22.wav
lantern-protocol-scene-004-subtitles-en-us-77aa10.srt
```

## Retention policy

Suggested defaults:

- Failed artifacts: keep manifest and logs, delete large media after review window.
- Rejected drafts: keep lightweight manifest, delete generated media unless explicitly pinned.
- Approved artifacts: keep manifest and artifact until superseded.
- Released artifacts: immutable unless a release correction is created.
- Superseded artifacts: keep manifest and source links for audit.

## External storage

If generated media becomes too large for Git, manifests should reference external/local object paths with hashes and metadata.

Supported future URI patterns:

```text
file://...
azblob://...
s3://...
gcs://...
worker://...
provider://...
```

## Local worker outputs

Worker outputs must be copied into the artifact store or referenced by manifest. Loose files in worker output folders are not considered production artifacts until indexed.

## Related issues

- #38 Preview/review gate
- #39 Generation job model
- #49 Local worker
- #56 Async job orchestration
- #60 Artifact storage and retention
- #65 Observability
- #66 Release-readiness review
