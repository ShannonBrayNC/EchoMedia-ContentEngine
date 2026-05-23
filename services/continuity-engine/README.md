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
- semantic continuity comparison

## Inputs

- canon manifest
- chapter files
- screenplay files
- storyboard files

## Outputs

```text
reports/continuity-audit-report.json
reports/semantic-continuity-report.json
```

## Continuity Scoring

The engine generates:

- continuity score
- pass/warn/fail status
- weighted penalties
- semantic overlap scoring
- machine-readable findings

## Example Commands

### Continuity Audit

```text
python services/continuity-engine/audit_continuity.py manuscript/chapters/chapter-01.md
```

### Semantic Comparison

```text
python services/continuity-engine/compare_semantic_continuity.py source.md candidate.md
```

## Semantic Status States

```text
aligned
review
drift-risk
```

## Exit Codes

- `0` means score passed threshold
- `1` means score failed threshold

## Future Expansion

- embedding-based comparison
- relationship-state scoring
- screenplay pacing scoring
- cross-book continuity analysis
- visual continuity scoring
