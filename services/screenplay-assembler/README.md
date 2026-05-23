# Screenplay Assembler

## Purpose

Assemble approved chapter packets into screenplay-oriented draft artifacts.

## Current Features

- collect chapter files
- sort chapters by chapter number
- generate screenplay markdown draft
- generate Fountain screenplay export
- generate assembly report

## Command

```text
python services/screenplay-assembler/assemble_screenplay.py projects/example
```

## Outputs

```text
screenplay/exports/screenplay-draft.md
screenplay/exports/screenplay-draft.fountain
screenplay/exports/screenplay-assembly-report.json
```

## Fountain Support

The assembler now creates a basic Fountain-compatible screenplay export for interoperability with screenplay tooling.

## Future Expansion

- scene-card generation
- screenplay pacing report
- chapter-to-scene traceability
- adaptation audit
- screenplay continuity scoring
