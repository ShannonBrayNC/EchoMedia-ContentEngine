# Lantern Protocol - Sprint 17 Export and Audit Readiness

## Sprint Goal

Prepare the locked 24-chapter manuscript for final export/audit validation after the line-edit passes through Chapters 1-24.

## Current Manuscript State

The active manuscript is locked as:

```text
Lantern Protocol Novel Draft v0.1
24 chapters
First complete manuscript pass
Status: locked for export, audit, and merge-readiness review
```

Sprint 11 through Sprint 16 completed line-edit passes across all active chapters:

| Sprint | Chapters | Focus |
|---:|---|---|
| 11 | 1-4 | opening anomaly, legitimacy thread, early hearing flow |
| 12 | 5-8 | citation cascade, Consent Riots, Black Lantern, choice architecture |
| 13 | 9-12 | False Preference Map, Human Veto Act, drafting room, Anchor Condition trim |
| 14 | 13-16 | pause burden, Case 6B-1147, Mercy Ledger, schism temptations |
| 15 | 17-20 | trust-chain burn, HarborHands, Mateo/Elena, Human Exception comparison |
| 16 | 21-24 | Forked Conscience runway, trial pacing, Living Anchor field process, Bound Flame ending |

## Export Commands

Run locally from PowerShell 7+:

```powershell
Set-Location C:\GitHub\lantern

git fetch origin
git switch cleanup/lantern-canon-freeze-v2
git pull origin cleanup/lantern-canon-freeze-v2

Set-Location C:\GitHub\lantern\projects\lantern-protocol\novel
python .\production\assemble_manuscript.py
python .\production\audit_manuscript.py
```

Expected outputs:

```text
projects/lantern-protocol/novel/exports/lantern-protocol-novel-draft.md
projects/lantern-protocol/novel/exports/lantern-protocol-novel-report.md
projects/lantern-protocol/novel/exports/lantern-protocol-novel-audit.md
```

Then commit the generated exports:

```powershell
Set-Location C:\GitHub\lantern

git status --short
git add projects\lantern-protocol\novel\exports
git commit -m "Regenerate Lantern novel exports after Sprint 17 audit"
git push
```

## Audit Expectations

The configured audit checks:

- Chapter sequence continuity.
- Required chapter metadata sections.
- Body-only chapter word-count ranges for configured chapters.
- Required screenplay/canon beat markers for configured chapters.
- Legacy v0 character leakage.
- Lantern interior POV phrases.
- Lantern embodiment risk phrases.
- Required manuscript note files.
- Final doctrine presence if final/deferred chapters are restored later.

## Known Risk Areas To Inspect After Audit

| Area | Risk | Expected Handling |
|---|---|---|
| Chapter 12 | Trimmed during Sprint 13 | Audit range was updated to reflect the narrower Anchor Condition role. |
| Chapters 21-24 | Final-act density | Accept if audit passes; flag for final prose proofread if pacing feels compressed. |
| Chapter 24 | Resolution tone | Must remain sober/provisional, not triumphant. First review docket was added in Sprint 16. |
| Generated draft export | May be stale until local generation | Regenerate with `assemble_manuscript.py`. |
| Audit export | May be stale until local generation | Regenerate with `audit_manuscript.py`. |

## Merge / PR Readiness Checklist

```text
[ ] Pull latest cleanup branch locally
[ ] Run assemble_manuscript.py
[ ] Run audit_manuscript.py
[ ] Review generated audit report
[ ] Commit regenerated exports
[ ] Confirm branch is still ahead of main and not behind
[ ] Open PR from cleanup/lantern-canon-freeze-v2 to main
[ ] Include Sprint 9-17 summary in PR body
```

## PR Summary Draft

```markdown
## Summary

Locks Lantern Protocol as a 24-chapter first complete novel draft and completes line-edit passes across the manuscript.

## Major changes

- Adds active Chapters 1-24 under `novel/manuscript/chapters/`.
- Locks Chapters 25-32 as deferred expansion/reservoir slots.
- Adds manuscript assembly and audit tooling.
- Adds chapter-status, POV, and continuity notes.
- Adds Sprint 1-17 completion/review reports.
- Adds/updates generated novel exports after local generation.

## Structure decision

The manuscript is now treated as a 24-chapter first complete draft. Chapters 25-32 should not be drafted unless a later revision pass decides to redistribute the final act.

## Validation

- `python .\production\assemble_manuscript.py`
- `python .\production\audit_manuscript.py`
```

## Connector Limitation Note

This report was added through the GitHub connector. The connector can create and update repository files, but it cannot execute the Python export/audit scripts inside the repository runtime. The export generation step above must be run locally or through a CI workflow.
