# Screenplay Assembly Workflow

## Purpose

The screenplay assembler converts chapter packets into a screenplay-oriented draft export.

## Example Command

```text
python services/screenplay-assembler/assemble_screenplay.py projects/example
```

## Inputs

The assembler scans:

```text
manuscript/chapters/
```

## Outputs

The assembler creates:

```text
screenplay/exports/screenplay-draft.md
screenplay/exports/screenplay-assembly-report.json
```

## Current Behavior

The current version:

- collects chapter markdown files
- sorts chapters by filename
- assembles a screenplay draft document
- creates a machine-readable assembly report

## Planned Expansion

Future versions should support:

- Fountain export
- scene segmentation
- pacing analysis
- chapter-to-scene mapping
- adaptation reporting
- screenplay continuity audits
