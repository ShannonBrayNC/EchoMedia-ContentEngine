# Runtime Estimation Workflow

## Purpose

The screenplay assembler now estimates scene and screenplay runtime from chapter-derived screenplay artifacts.

## Runtime Model

Current estimation assumptions:

```text
130 words ≈ 1 screenplay minute
minimum scene runtime = 30 seconds
```

## Outputs

The assembler generates:

```text
screenplay/exports/runtime-report.json
```

## Scene Metadata

Each generated scene card now includes:

- estimated runtime seconds
- estimated runtime display value
- estimated word count

## Runtime Report

The runtime report includes:

- total runtime
- average scene runtime
- scene count
- scene-level runtime estimates

## Example Command

```text
python services/screenplay-assembler/assemble_screenplay.py projects/example
```

## Future Expansion

Future versions should support:

- dialogue-aware runtime estimation
- action-sequence scaling
- pacing analysis
- trailer runtime extraction
- production scheduling estimates
- budget estimation support
