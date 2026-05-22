# Lantern Protocol - Sprint 21 Final Proofread Plan

## Sprint Goal

Create the final proofread branch from merged `main` and prepare the locked 24-chapter manuscript for copyedit, consistency polish, and publication-readiness review.

## Branch

```text
lantern-final-proofread
```

Created from merge commit:

```text
7cfbf48eacfe6ad2164e3802978e927ed4913ab5
```

## Current Manuscript Contract

```text
Lantern Protocol Novel Draft v0.1
24 active chapters
Chapters 25-32 deferred as expansion/reservoir slots
Status: merged to main and ready for final proofread
```

## Proofread Objectives

The final proofread should not add new plot. It should sharpen what is already there.

### Primary objectives

1. Remove typos, grammar slips, casing inconsistencies, and duplicated phrases.
2. Normalize in-world document blocks and labels.
3. Preserve Lantern as faceless and system-bound.
4. Preserve no-Lantern-interior-POV discipline.
5. Check character voice consistency across all 24 chapters.
6. Confirm recurring artifacts stay consistent:
   - Mateo Vega bracelet
   - Manual Fallback Card
   - Human Oversight Record
   - Mercy Ledger
   - Living Anchor Field Packet
   - Interface Bill of Rights
7. Keep the Bound Flame ending sober, provisional, and accountable.

## Chapter Batch Plan

| Proofread Batch | Chapters | Focus |
|---:|---|---|
| Batch A | 1-4 | opening polish, eight-second anomaly, hearing setup |
| Batch B | 5-8 | citation cascade, Consent Riots, Black Lantern, Iris grammar |
| Batch C | 9-12 | False Preference Map, Human Veto Act, drafting room, Anchor Condition |
| Batch D | 13-16 | oversight burden, Case 6B-1147, Mercy Ledger, schism |
| Batch E | 17-20 | trust-chain burn, HarborHands, Mateo/Elena, Human Exception |
| Batch F | 21-24 | Forked Conscience, trial/forum, Living Anchor, Bound Flame ending |

## Proofread Rules

### Do

- Prefer small, precise prose edits.
- Preserve established chapter structure and section headings.
- Keep document inserts in fenced `text` blocks.
- Preserve line-edit sprint additions unless they create continuity problems.
- Mark any proposed plot-level change in the revision backlog rather than applying it casually.

### Do not

- Draft Chapters 25-32.
- Add new major characters.
- Give Lantern a body, avatar, face, or emotional interiority.
- Reopen the 24-vs-32 chapter decision unless final proofread proves the final act cannot hold.
- Turn doctrine scenes into lectures.

## Validation Commands

Run after each proofread batch or at least before PR:

```powershell
Set-Location C:\GitHub\lantern\projects\lantern-protocol\novel
python .\production\assemble_manuscript.py
python .\production\audit_manuscript.py
```

Commit updated exports after the final batch:

```powershell
Set-Location C:\GitHub\lantern
git add projects\lantern-protocol\novel\exports
git commit -m "Regenerate Lantern exports after final proofread"
git push
```

## Acceptance Criteria

```text
[ ] All 24 chapters proofread
[ ] No new plot drift introduced
[ ] Lantern facelessness preserved
[ ] No Lantern interior POV introduced
[ ] Recurring artifacts consistent
[ ] Generated exports refreshed
[ ] Audit reviewed
[ ] Final proofread PR opened against main
```

## Next Sprint Recommendation

Sprint 22 should proofread Batch A: Chapters 1-4.
