# Semantic Continuity Workflow

## Purpose

The semantic continuity workflow compares narrative artifacts for conceptual alignment and drift risk.

## Example Command

```text
python services/continuity-engine/compare_semantic_continuity.py source.md candidate.md
```

## Current Comparison Model

The current engine:

- tokenizes narrative text
- removes common stop words
- calculates semantic overlap
- generates drift classifications
- produces machine-readable reports

## Status States

### aligned

High semantic overlap.

### review

Moderate overlap. Human review recommended.

### drift-risk

Low overlap. Potential continuity drift detected.

## Report Outputs

The workflow generates:

```text
reports/semantic-continuity-report.json
```

including:

- semantic score
- shared terms
- missing terms
- added terms
- drift classification

## Future Expansion

Future versions should support:

- embedding-based similarity
- entity-aware comparison
- relationship-state comparison
- screenplay pacing comparison
- visual continuity embeddings
