# Screenplay Import Status

Date: 2026-05-26

## Status

The screenplay blocker has been reduced into a working screenplay pipeline.

The repo now contains five committed screenplay page batches under the legacy movie path:

```text
projects/lantern-protocol/movie/screenplay/pages-001-010.md
projects/lantern-protocol/movie/screenplay/pages-011-020.md
projects/lantern-protocol/movie/screenplay/pages-021-030.md
projects/lantern-protocol/movie/screenplay/pages-031-040.md
projects/lantern-protocol/movie/screenplay/pages-041-050.md
```

The normalized screenplay workspace exists here:

```text
projects/lantern-protocol/screenplay/
```

## Imported / referenced source

| Source | Status | Notes |
|---|---|---|
| `projects/lantern-protocol/movie/screenplay/pages-001-010.md` | Available | First screenplay sample pass. Region Six flood response, Mercy General, Mara, Naomi, Elias, eight-second gap. |
| `projects/lantern-protocol/movie/screenplay/pages-011-020.md` | Available | Continuation pass. After-action review, Cross first inquiry pressure, Caleb public framing, empty-chair image. |
| `projects/lantern-protocol/movie/screenplay/pages-021-030.md` | Available | Continuation pass. Advisory claim challenged, Marcus Thorne speed argument, Naomi protecting Mateo from abstraction, public chant split. |
| `projects/lantern-protocol/movie/screenplay/pages-031-040.md` | Available | Continuation pass. Public hearing setup, Elias testimony prep, Naomi/Elena statement decision, Lantern truth placement. |
| `projects/lantern-protocol/movie/screenplay/pages-041-050.md` | Available | Continuation pass. Public hearing opens, irresistible recommendation testimony, Elena statement, Anchor Condition named. |
| `projects/lantern-protocol/movie/lantern-protocol-feature-treatment.md` | Available | Feature adaptation spine, logline, doctrine, act structure. |
| `projects/lantern-protocol/movie/lantern-protocol-eight-sequence-beat-sheet.md` | Available | Eight-sequence structure and continuation map. |

## Normalized exports

| Export | Status |
|---|---|
| `projects/lantern-protocol/screenplay/exports/screenplay-draft.md` | Created as initial checked-in export stub. Regenerate from source with assembler. |
| `projects/lantern-protocol/screenplay/exports/screenplay-draft.fountain` | Created as initial checked-in export stub. Regenerate from source with assembler. |

## Assembly script

```text
projects/lantern-protocol/screenplay/scripts/assemble-screenplay.mjs
```

Run from repo root:

```bash
node projects/lantern-protocol/screenplay/scripts/assemble-screenplay.mjs
```

The assembler now includes Pages 001-050.

## Remaining gap

Pages 001-050 currently exist as committed screenplay pages.

Pages 051+ still need to be drafted or imported.

## Next writing target

Continue from the Anchor Condition introduction into:

1. Interrogating Lantern public context releases as truthful pressure.
2. Mara exposing or nearly exposing the two-minute review window pattern.
3. Cross asking when truth placement becomes action.
4. Caleb reframing Anchor Condition as bureaucracy slowing rescue.
5. Elias and Juno shaping first rough Anchor Condition architecture.

## Recommended issue linkage

This directly advances issue #127 by giving the screenplay workflow committed page batches, a normalized workspace, a review path, an assembly script, and export targets.
