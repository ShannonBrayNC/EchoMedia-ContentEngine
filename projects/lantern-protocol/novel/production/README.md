# Lantern Novel Production

This folder contains the local and CI tooling for assembling and auditing the locked 24-chapter Lantern Protocol novel draft.

## Scripts

| Script | Purpose |
|---|---|
| `assemble_manuscript.py` | Builds `novel/exports/lantern-protocol-novel-draft.md` and `novel/exports/lantern-protocol-novel-report.md` from `novel/manuscript/front-matter/` and `novel/manuscript/chapters/`. Supports `--profile markdown`, `--profile elevenlabs-docx`, and `--profile all`. |
| `audit_manuscript.py` | Builds `novel/exports/lantern-protocol-novel-audit.md` and checks chapter sequence, metadata sections, required beat markers, configured body word ranges, legacy-name leakage, Lantern POV leakage, and Lantern embodiment risk phrases. |
| `export_elevenlabs_docx.py` | Builds a single ElevenLabs-ready audiobook DOCX from title/front matter/chapter manuscript bodies while excluding internal planning metadata. |

## Local Run

From PowerShell 7+:

```powershell
Set-Location C:\GitHub\EchoMedia-ContentEngine\projects\lantern-protocol\novel
python .\production\assemble_manuscript.py
python .\production\audit_manuscript.py
```

To generate the ElevenLabs audiobook DOCX export:

```powershell
Set-Location C:\GitHub\EchoMedia-ContentEngine\projects\lantern-protocol\novel
python -m pip install python-docx
python .\production\assemble_manuscript.py --profile elevenlabs-docx
```

To regenerate every supported export profile:

```powershell
Set-Location C:\GitHub\EchoMedia-ContentEngine\projects\lantern-protocol\novel
python -m pip install python-docx
python .\production\assemble_manuscript.py --profile all
python .\production\audit_manuscript.py
```

Then commit generated exports:

```powershell
Set-Location C:\GitHub\EchoMedia-ContentEngine
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
- pushes to `main` that touch Lantern novel/report/workflow files
- manual `workflow_dispatch`

The workflow:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs `python-docx`.
4. Runs `assemble_manuscript.py --profile all`.
5. Runs `audit_manuscript.py`.
6. Fails if generated exports are stale compared with the committed files.
7. Uploads the generated exports as a workflow artifact named `lantern-novel-exports`.

## Expected Exports

```text
novel/exports/lantern-protocol-novel-draft.md
novel/exports/lantern-protocol-novel-report.md
novel/exports/lantern-protocol-novel-audit.md
novel/exports/Lantern_Protocol_Book_One_ElevenLabs.docx
novel/exports/lantern-protocol-elevenlabs-audiobook-report.md
```

## ElevenLabs Audiobook Export Contract

The ElevenLabs export is intended for a single Studio upload in dynamic narration / audiobook workflows.

It must:

- include the book title, front matter, reader-facing manifest/protocol excerpts, and all active chapters;
- bold the book title;
- bold every chapter heading;
- preserve in-world alerts, logs, system outputs, and manifest/protocol inserts that belong in the narration;
- remove planning-only sections such as `Canon Sources`, `POV Strategy`, `Chapter Purpose`, `Continuity Requirements`, `Continuity Notes`, and `Revision Notes`;
- remove source comments and assembly metadata;
- normalize Markdown code fences into styled insert paragraphs that are safe for narration review.

## Current Manuscript Contract

```text
Lantern Protocol Novel Draft v0.1
24 active chapters
Chapters 25-32 deferred as expansion/reservoir slots
Status: locked for export, audit, and merge-readiness review
```
