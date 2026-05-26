# Implementation Sprint 1 - Project Registry Inventory and Validator Completion

## Status

Complete for issue #89.

## Added files

- `config/project-registry.json`
- `scripts/validate-project-registry.mjs`

## What this completes

This slice creates the first concrete project registry inventory and validator for the Content Engine implementation sprint.

The registry now includes:

- `lantern-protocol`
- `the-sovereign-exception`

Each project entry includes:

- slug
- title
- root path
- status
- visibility
- series
- universe
- canon state
- legacy aliases
- standard artifact paths
- supported generation types
- export targets

## Validator behavior

Run from the repo root:

```bash
node scripts/validate-project-registry.mjs
```

Optional custom registry path:

```bash
node scripts/validate-project-registry.mjs config/project-registry.json
```

The validator checks:

- Registry JSON can be parsed.
- Root object includes `version` and `projects`.
- Required project fields exist.
- Slugs are lowercase kebab-case.
- Duplicate slugs are rejected.
- Project status is supported.
- Visibility is supported.
- Root paths are checked.
- Required artifact path keys exist.
- Artifact paths are checked.
- Supported generation types are known.
- Export targets are arrays when present.

## Error and warning policy

Errors block completion and return exit code `1`.

Warnings are reported but do not fail the run. This is intentional because the repo still contains legacy/imported project structures and should not crash before migration cleanup.

## Known follow-up

The registry intentionally preserves legacy-path awareness. Future issues should decide whether projects are normalized into `projects/<slug>/...` or kept with aliases until a migration PR is reviewed.

## Related implementation issues

- #89 - Project registry inventory and validator
- #90 - Registry-driven project picker
