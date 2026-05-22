# Lantern Protocol - Sprint 19 PR Validation

## Sprint Goal

Open the pull request from `cleanup/lantern-canon-freeze-v2` into `main`, trigger the Lantern novel export/audit workflow, and document merge-readiness checks.

## Current Branch State

```text
Source: cleanup/lantern-canon-freeze-v2
Target: main
Purpose: merge locked 24-chapter Lantern Protocol novel draft, reports, export/audit tooling, and CI validation workflow
```

## PR Scope

The PR includes:

- 24 active manuscript chapters under `novel/manuscript/chapters/`.
- Chapter status, POV map, continuity map, and manuscript README.
- Manuscript export and audit tooling.
- Generated manuscript exports.
- Sprint 1-19 reports.
- 24-chapter structure decision and revision backlog.
- GitHub Actions workflow for export/audit validation.

## Required CI Check

```text
Lantern Novel Export and Audit / Export and audit Lantern novel
```

Workflow file:

```text
.github/workflows/lantern-novel-export-audit.yml
```

The workflow runs:

```bash
python ./production/assemble_manuscript.py
python ./production/audit_manuscript.py
```

from:

```text
projects/lantern-protocol/novel
```

Then it fails if generated exports are stale.

## Merge Readiness Checklist

```text
[ ] PR opened from cleanup/lantern-canon-freeze-v2 into main
[ ] GitHub Actions workflow started
[ ] Export/audit workflow passed
[ ] If workflow fails, inspect whether exports are stale
[ ] Regenerate exports locally if needed
[ ] Confirm branch remains 0 behind main
[ ] Review final changed-file summary
[ ] Merge PR after CI is green
```

## If CI Fails Because Exports Are Stale

Run locally:

```powershell
Set-Location C:\GitHub\lantern

git fetch origin
git switch cleanup/lantern-canon-freeze-v2
git pull origin cleanup/lantern-canon-freeze-v2

Set-Location C:\GitHub\lantern\projects\lantern-protocol\novel
python .\production\assemble_manuscript.py
python .\production\audit_manuscript.py

Set-Location C:\GitHub\lantern
git add projects\lantern-protocol\novel\exports
git commit -m "Regenerate Lantern novel exports for PR validation"
git push
```

## PR Body Draft

```markdown
## Summary

Locks Lantern Protocol as a 24-chapter first complete novel draft and completes line-edit passes across the manuscript.

## Major changes

- Adds active Chapters 1-24 under `projects/lantern-protocol/novel/manuscript/chapters/`.
- Locks Chapters 25-32 as deferred expansion/reservoir slots.
- Adds manuscript assembly and audit tooling.
- Adds chapter-status, POV, and continuity notes.
- Adds Sprint 1-19 completion/review reports.
- Adds generated novel exports.
- Adds GitHub Actions export/audit validation workflow.

## Structure decision

The manuscript is now treated as a 24-chapter first complete draft. Chapters 25-32 should not be drafted unless a later revision pass decides to redistribute the final act.

## Validation

CI workflow added:

- `.github/workflows/lantern-novel-export-audit.yml`

Expected local validation commands:

```powershell
Set-Location projects/lantern-protocol/novel
python .\production\assemble_manuscript.py
python .\production\audit_manuscript.py
```
```

## Next Step After Merge

Start a new branch for final proofread and copyedit:

```powershell
git switch main
git pull origin main
git switch -c edit/lantern-final-proofread
```
