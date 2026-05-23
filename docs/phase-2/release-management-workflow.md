# Release Management Workflow

## Purpose

The release management workflow governs promotion and packaging of screenplay, manuscript, storyboard, and production artifacts.

## Release States

```text
draft
candidate
approved
released
superseded
archived
```

## Example Command

```text
python services/release-manager/create_release_manifest.py projects/example 0.1.0 candidate
```

## Outputs

The release manager creates:

```text
releases/{version}/release-manifest.json
releases/{version}/release-notes.md
```

## Governance Requirements

Release manifests track:

- canon validation requirements
- continuity validation requirements
- semantic validation requirements
- included artifacts
- release timestamps

## Future Expansion

Future versions should support:

- GitHub release integration
- artifact snapshots
- changelog generation
- rollback support
- package integrity verification
- production milestone promotion
