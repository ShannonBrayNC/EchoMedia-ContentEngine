# Continuity Engine

## Purpose

Audit story artifacts for continuity drift.

## Current Validation Areas

- timeline continuity
- character continuity
- relationship continuity
- screenplay continuity
- chapter continuity
- visual continuity

## Inputs

- canon manifest
- chapter files
- screenplay files
- storyboard files

## Outputs

```text
reports/continuity-audit-report.json
```

## Continuity Scoring

The engine now generates:

- continuity score
- pass/warn/fail status
- weighted penalties
- machine-readable findings

## Example Command

```text
python services/continuity-engine/audit_continuity.py manuscript/chapters/chapter-01.md
```

## Exit Codes

- `0` means score passed threshold
- `1` means score failed threshold

## Future Expansion

- semantic continuity comparison
- relationship-state scoring
- screenplay pacing scoring
- cross-book continuity analysis
- visual continuity scoring
