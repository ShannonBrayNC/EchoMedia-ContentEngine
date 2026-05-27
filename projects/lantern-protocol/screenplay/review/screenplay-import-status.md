# Screenplay Import Status

Date: 2026-05-26

## Status

The screenplay blocker is no longer a missing-source mystery.

The repo already contains the first committed screenplay sample under the legacy movie path:

```text
projects/lantern-protocol/movie/screenplay/pages-001-010.md
```

The normalized screenplay workspace now exists here:

```text
projects/lantern-protocol/screenplay/
```

## Imported / referenced source

| Source | Status | Notes |
|---|---|---|
| `projects/lantern-protocol/movie/screenplay/pages-001-010.md` | Available | First screenplay sample pass. Region Six flood response, Mercy General, Mara, Naomi, Elias, eight-second gap. |
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

## Remaining gap

Only Pages 001-010 currently exist as committed screenplay pages.

Pages 011+ still need to be drafted or imported.

## Next writing target

Continue from the current sample into:

1. After-action review.
2. Senator Adrienne Cross's first inquiry pressure.
3. Caleb Rusk's first public framing.
4. The empty chair as the visual symbol of unowned authority.

## Recommended issue linkage

This directly advances issue #127 by giving the screenplay workflow a committed normalized workspace, review path, assembly script, and export targets.
