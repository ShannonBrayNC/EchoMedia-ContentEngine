# Trailer Suitability Workflow

## Purpose

The screenplay assembler now evaluates scenes for trailer suitability and cinematic marketing potential.

## Current Scoring Factors

The current model evaluates:

- high-impact narrative terms
- scene density
- runtime suitability
- emotional trigger indicators

## Status States

```text
strong
candidate
low
```

## Outputs

The assembler generates:

```text
screenplay/exports/trailer-suitability-report.json
```

## Scene Metadata

Each scene card now contains:

- trailer suitability score
- trailer suitability status
- matched cinematic trigger terms

## Example Command

```text
python services/screenplay-assembler/assemble_screenplay.py projects/example
```

## Future Expansion

Future versions should support:

- emotional pacing analysis
- teaser sequencing
- soundtrack timing support
- social clip extraction
- cinematic hook analysis
- audience-retention modeling
