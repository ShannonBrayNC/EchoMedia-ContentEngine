# Screenplay Import Status

Date: 2026-05-26

## Status

The screenplay blocker has been reduced into a working screenplay pipeline.

The repo now contains four committed screenplay page batches under the legacy movie path:

```text
projects/lantern-protocol/movie/screenplay/pages-001-010.md
projects/lantern-protocol/movie/screenplay/pages-011-020.md
projects/lantern-protocol/movie/screenplay/pages-021-030.md
projects/lantern-protocol/movie/screenplay/pages-031-040.md
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

The assembler now includes Pages 001-040.

## Remaining gap

Pages 001-040 currently exist as committed screenplay pages.

Pages 041+ still need to be drafted or imported.

## Next writing target

Continue from the formal public hearing setup into:

1. Opening the public hearing.
2. Elias testifying under oath about irresistible recommendations.
3. Naomi or Elena's written statement landing as a moral counterweight.
4. First hint of Anchor Condition as constraint rather than faster approval.

## Recommended issue linkage

This directly advances issue #127 by giving the screenplay workflow committed page batches, a normalized workspace, a review path, an assembly script, and export targets.
