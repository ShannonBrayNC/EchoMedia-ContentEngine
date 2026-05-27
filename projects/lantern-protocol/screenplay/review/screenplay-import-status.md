# Screenplay Import Status

Date: 2026-05-26

## Status

The screenplay blocker has been reduced into a working screenplay pipeline.

The repo now contains two committed screenplay page batches under the legacy movie path:

```text
projects/lantern-protocol/movie/screenplay/pages-001-010.md
projects/lantern-protocol/movie/screenplay/pages-011-020.md
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

The assembler now includes both page batches.

## Remaining gap

Pages 001-020 currently exist as committed screenplay pages.

Pages 021+ still need to be drafted or imported.

## Next writing target

Continue from the preliminary inquiry into:

1. Agency claims that Lantern remained advisory.
2. Director Marcus Thorne presenting the honest speed argument.
3. Naomi refusing to let Mateo become only a symbol.
4. Public chants splitting into `LET IT SAVE US` and `NAME THE HAND`.

## Recommended issue linkage

This directly advances issue #127 by giving the screenplay workflow committed page batches, a normalized workspace, a review path, an assembly script, and export targets.
