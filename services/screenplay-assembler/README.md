# Screenplay Assembler

## Purpose

Assemble approved chapter packets into screenplay-oriented draft artifacts.

## Planned Features

- collect chapter files
- sort chapters by chapter number
- generate screenplay markdown draft
- generate assembly report
- prepare future Fountain export support

## Command

```text
python services/screenplay-assembler/assemble_screenplay.py projects/example
```

## Outputs

```text
screenplay/exports/screenplay-draft.md
screenplay/exports/screenplay-assembly-report.json
```

## Future Expansion

- Fountain export
- scene-card generation
- screenplay pacing report
- chapter-to-scene traceability
- adaptation audit
