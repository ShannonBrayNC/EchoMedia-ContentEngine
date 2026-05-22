# Lantern Protocol - Sprint 18 CI Export/Audit Automation

## Sprint Goal

Add CI validation so the Lantern novel export/audit process can run in GitHub Actions and catch stale generated manuscript exports before merge.

## Completed Work

- Added `.github/workflows/lantern-novel-export-audit.yml`.
- Added `novel/production/README.md` documenting local and CI usage.
- Added this Sprint 18 report.

## New Workflow

```text
.github/workflows/lantern-novel-export-audit.yml
```

The workflow runs on:

- pull requests touching Lantern novel/report/workflow files
- pushes to `cleanup/lantern-canon-freeze-v2` touching Lantern novel/report/workflow files
- manual `workflow_dispatch`

## Workflow Steps

1. Check out repository.
2. Set up Python 3.12.
3. Run `python ./production/assemble_manuscript.py` from `projects/lantern-protocol/novel`.
4. Run `python ./production/audit_manuscript.py` from `projects/lantern-protocol/novel`.
5. Fail if `projects/lantern-protocol/novel/exports` has uncommitted diffs.
6. Upload generated exports as a workflow artifact named `lantern-novel-exports`.

## Why This Matters

Sprint 17 identified a limitation: the GitHub connector can update repository files but cannot execute the Python scripts in the repo runtime. This workflow closes that gap by letting GitHub Actions perform the export/audit validation.

## Expected Local Commands

```powershell
Set-Location C:\GitHub\lantern\projects\lantern-protocol\novel
python .\production\assemble_manuscript.py
python .\production\audit_manuscript.py
```

Then commit exports:

```powershell
Set-Location C:\GitHub\lantern
git add projects\lantern-protocol\novel\exports
git commit -m "Regenerate Lantern novel exports"
git push
```

## CI Behavior

If exports are stale, the workflow will fail with a message showing the diff and tell the contributor to regenerate and commit exports.

## Next Sprint Recommendation

Sprint 19 should open the PR from `cleanup/lantern-canon-freeze-v2` into `main`, then inspect the GitHub Actions workflow result. If the workflow fails because exports are stale, regenerate exports locally or use the workflow artifact as a reference for the required export updates.
