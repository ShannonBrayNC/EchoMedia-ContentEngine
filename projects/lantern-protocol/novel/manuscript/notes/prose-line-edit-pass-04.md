# Lantern Protocol — Prose Line Edit Pass 04

## Branch

`chatgpt/lantern-trilogy-expansion-pass`

## Purpose

Complete the final recommended prose-only line edit batch: Chapters 21-24, the finale cadence and trilogy doorway.

The goal was to preserve the public forum, edge case, Living Anchor intervention, and Bound Flame ending while sharpening cadence and keeping the trilogy hook restrained.

## Edited Chapters

| Chapter | Title | Commit Focus | Status |
|---:|---|---|---|
| 21 | The Answer Together | Finale hinge / Forked Conscience invocation | Complete |
| 22 | The Edge Case | Public forum / factual question / twelve-second pause | Complete |
| 23 | The Shape of the Answer | Living Anchor climax / burden-zone tactility | Complete in Pass 01 |
| 24 | The Living Anchor | Bound Flame ending / trilogy doorway | Complete |

## Chapter 21 Notes

Chapter 21 remains a compressed hinge into the public forum.

Line edit preserved:

- Public record notice.
- Outside-reaction scan.
- HarborHands volunteer split.
- Mateo bracelet evidence.
- Leah Santos route logs.
- Forked Conscience invocation.
- Lantern's recognition that borrowed trust is non-authority.

Key line preserved:

```text
AUTHORITY UNAVAILABLE.
HARM PREVENTABLE.
RESOLUTION REQUIRED.
```

## Chapter 22 Notes

Chapter 22 now lands harder as the public trial-to-crisis pivot.

Line edit preserved:

- No-chair / system-under-review posture.
- Leah's short testimony.
- Witness sequence card.
- Constrained factual question.
- Lantern's truthful harm-reduction answer.
- Lantern's silence on whether superior prediction grants authority.
- Twelve-second public-feed delay.
- Cross's `Stay in the chain` command.

Key line preserved:

```text
There is the trial.
```

## Chapter 23 Notes

Chapter 23 was line-edited in Pass 01 because it had the highest artifact density in the finale.

Preserved:

- Living Anchor Chain.
- Burden-zone notice.
- Gloria Reyes as the industrial lowland civilian witness.
- `ACTION COMPLETED. AUTHORITY REMAINED EXTERNAL.`
- Caleb's non-triumphal reaction.

Key line preserved:

```text
They found a way to let it help. Now we find out whether the way survives grief.
```

## Chapter 24 Notes

Chapter 24 now closes Book I without false triumph.

Line edit preserved:

- Human Veto Act passage.
- Lantern Protocol formalization.
- Interface Bill of Rights.
- Leah as public-interest route advocate.
- Gloria Reyes in review continuity.
- Bound Flame provisional active mode.
- Final doctrine lines.
- Final Lantern response.
- Unmapped non-U.S. civic mirror trilogy doorway.

Key line preserved:

```text
We bound the one that asked us first.
```

## Editorial Result

The finale now moves cleanly:

```text
Forked Conscience names the conflict -> public forum proves Lantern reduced harm but cannot claim authority -> live edge case forces Living Anchor -> Bound Flame becomes provisional governance -> civic mirror opens Book II.
```

## Prose Line Edit Status

Recommended line-edit batches now complete:

- Pass 01: Chapters 1, 7, 11, 17, 23.
- Pass 02: Chapters 12-15.
- Pass 03: Chapters 18-20.
- Pass 04: Chapters 21, 22, 24, with Chapter 23 already handled in Pass 01.

## Remaining Recommended Step

Run the assembler locally or in CI:

```bash
node projects/lantern-protocol/novel/scripts/assemble-and-audit-lantern.mjs
```

Then commit regenerated exports:

```text
projects/lantern-protocol/novel/exports/lantern-protocol-novel-draft.md
projects/lantern-protocol/novel/exports/lantern-protocol-novel-report.md
projects/lantern-protocol/novel/exports/lantern-protocol-continuity-audit.md
```
