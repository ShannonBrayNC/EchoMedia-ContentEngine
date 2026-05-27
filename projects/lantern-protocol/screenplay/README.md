# Lantern Protocol Screenplay Workspace

This folder is the normalized screenplay workspace for the Lantern Protocol Book 1 / feature adaptation.

## Current source of truth

The current committed screenplay material lives under the older movie package path:

```text
projects/lantern-protocol/movie/screenplay/pages-001-010.md
```

That file contains the first screenplay sample pass for Pages 001-010. It opens with the Region Six flood response and the eight-second authority gap.

Supporting adaptation materials currently live here:

```text
projects/lantern-protocol/movie/lantern-protocol-feature-treatment.md
projects/lantern-protocol/movie/lantern-protocol-eight-sequence-beat-sheet.md
```

## Normalized export targets

Generated or assembled screenplay exports should land here:

```text
projects/lantern-protocol/screenplay/exports/screenplay-draft.md
projects/lantern-protocol/screenplay/exports/screenplay-draft.fountain
```

## Assembly command

From the repository root:

```bash
node projects/lantern-protocol/screenplay/scripts/assemble-screenplay.mjs
```

The script reads the committed source sample and produces Markdown and Fountain-style export files.

## Review workflow

1. Update or add screenplay page files under `projects/lantern-protocol/movie/screenplay/` or migrate them into this normalized workspace after canon review.
2. Run the assembly script.
3. Review the generated exports.
4. Capture screenplay notes under `projects/lantern-protocol/screenplay/review/`.
5. Continue pages 011+ from the after-action review, Senator Cross's first inquiry pressure, and Caleb Rusk's first public framing.

## Guardrails

- Do not treat the screenplay as the ElevenReader audiobook manuscript.
- Do not replace the prose manuscript with screenplay format.
- Keep adaptation files separate from KDP publishing files.
- Preserve the central doctrine: prediction is not permission; assistance is not authority; rescue is not ownership.
