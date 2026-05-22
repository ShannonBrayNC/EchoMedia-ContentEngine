# Lantern Protocol - Sprint 22 Final Proofread Batch A

## Sprint Goal

Proofread Batch A, Chapters 1-4, on the `lantern-final-proofread` branch. This sprint sharpens the opening blade without adding new plot or expanding the locked 24-chapter structure.

## Branch

```text
lantern-final-proofread
```

## Scope

| Chapter | Focus |
|---:|---|
| 1 | Opening polish, eight-second anomaly, no overexplaining |
| 2 | Decide bridge vs. slight expansion |
| 3 | Hearing-room pacing |
| 4 | Live-query turn and ethical-authority question |

## Guardrails

- Do not draft Chapters 25-32.
- Do not add new plot architecture.
- Preserve Lantern as faceless and system-bound.
- Preserve no-Lantern-interior-POV discipline.
- Prefer precise proofread edits over expansion.
- Record any structural concern in the revision backlog instead of solving it by widening the manuscript.

## Validation Commands

```powershell
Set-Location C:\GitHub\lantern\projects\lantern-protocol\novel
python .\production\assemble_manuscript.py
python .\production\audit_manuscript.py
```

## Acceptance Criteria

```text
[ ] Chapters 1-4 proofread
[ ] Chapter 1 opening and eight-second anomaly are clear without overexplaining
[ ] Chapter 2 bridge decision is documented or applied
[ ] Chapter 3 hearing-room pacing is tightened
[ ] Chapter 4 live-query and ethical-authority beats land cleanly
[ ] No Chapters 25-32 drafting introduced
[ ] Generated exports refreshed after edits
[ ] Manuscript audit reviewed
```

