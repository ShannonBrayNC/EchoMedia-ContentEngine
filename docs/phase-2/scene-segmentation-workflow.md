# Scene Segmentation Workflow

## Purpose

The screenplay assembler now generates scene-level artifacts from chapter-derived screenplay drafts.

## Scene Outputs

The assembler creates:

```text
screenplay/scenes/
```

including:

```text
scene-index.json
scn-001.json
scn-002.json
```

## Scene Metadata

Each scene card contains:

- scene ID
- source chapter
- title
- estimated word count
- story objective
- emotional objective
- continuity notes
- adaptation notes
- status

## Example Command

```text
python services/screenplay-assembler/assemble_screenplay.py projects/example
```

## Future Expansion

Future versions should support:

- runtime estimation
- trailer suitability scoring
- production scheduling
- scene-level continuity scoring
- shot extraction
- cinematic pacing analysis
