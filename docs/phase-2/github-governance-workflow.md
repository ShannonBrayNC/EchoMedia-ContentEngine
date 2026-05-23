# GitHub Governance Workflow

## Purpose

The GitHub governance workflow enforces narrative quality controls before pull requests can merge.

## Active Enforcement Workflows

### Canon Validation

The canon validation workflow:

- locates canon manifests
- validates required fields
- validates canon states
- generates machine-readable reports
- fails the workflow if validation fails

### Continuity Audit

The continuity audit workflow:

- scans narrative markdown files
- generates continuity findings
- generates continuity scores
- applies fail-under thresholds
- fails the workflow if score thresholds are not met

## Current Thresholds

```text
continuity fail-under: 70
```

## Machine-Readable Reports

The workflows generate:

```text
reports/*.json
```

for future PR annotations and release validation.

## Future Expansion

Future governance workflows should support:

- PR annotations
- merge blocking policies
- release quality scoring
- semantic continuity comparison
- adaptation scoring
- branch protection integration
