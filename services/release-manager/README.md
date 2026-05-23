# Release Manager

## Purpose

Manage governed release versions for story, screenplay, visual, and production packages.

## Release States

- draft
- candidate
- approved
- released
- superseded
- archived

## Command

```text
python services/release-manager/create_release_manifest.py projects/example 0.1.0 candidate
```

## Outputs

```text
releases/{version}/release-manifest.json
releases/{version}/release-notes.md
```

## Future Expansion

- GitHub release publishing
- package checksums
- artifact snapshots
- release promotion gates
- changelog generation
