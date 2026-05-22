# Lantern Novel Production

This folder contains the local and CI tooling for assembling and auditing the locked 24-chapter Lantern Protocol novel draft.

## Scripts

| Script | Purpose |
|---|---|
| `assemble_manuscript.py` | Builds `novel/exports/lantern-protocol-novel-draft.md` and `novel/exports/lantern-protocol-novel-report.md` from `novel/manuscript/chapters/`. |
| `audit_manuscript.py` | Builds `novel/exports/lantern-protocol-novel-audit.md` and checks chapter sequence, metadata sections, required beat markers, configured body word ranges, legacy-name leakage, Lantern POV leakage, and Lantern embodiment risk phrases. |

## Local Run

From PowerShell 7+:

```powershell
Set-Location C:\GitHub\lantern\projects\lantern-protocol\novel
python .\production\assemble_manuscript.py
python .\production\audit_manuscript.py
```

Then commit generated exports:

```powershell
Set-Location C:\GitHub\lantern
git add projects\lantern-protocol\novel\exports
git commit -m "Regenerate Lantern novel exports"
git push
```

## CI Workflow

The workflow lives at:

```text
.github/workflows/lantern-novel-export-audit.yml
```

It runs on:

- pull requests that touch Lantern novel/report/workflow files
- pushes to `cleanup/lantern-canon-freeze-v2` that touch Lantern novel/report/workflow files
- manual `workflow_dispatch`

The workflow:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Runs `assemble_manuscript.py`.
4. Runs `audit_manuscript.py`.
5. Fails if generated exports are stale compared with the committed files.
6. Uploads the generated exports as a workflow artifact named `lantern-novel-exports`.

## Expected Exports

```text
novel/exports/lantern-protocol-novel-draft.md
novel/exports/lantern-protocol-novel-report.md
novel/exports/lantern-protocol-novel-audit.md
```

## Current Manuscript Contract

```text
Lantern Protocol Novel Draft v0.1
24 active chapters
Chapters 25-32 deferred as expansion/reservoir slots
Status: locked for export, audit, and merge-readiness review
```
