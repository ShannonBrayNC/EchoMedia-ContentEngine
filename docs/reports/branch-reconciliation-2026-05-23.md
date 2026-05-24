# Branch Reconciliation Report

Date: 2026-05-23
Repository: `ShannonBrayNC/EchoMedia-ContentEngine`
Base branch: `main`

## Executive Summary

The repo contains several useful but divergent branches. None of the active divergent branches should be merged blindly into `main`. The safest reconciliation approach is targeted cherry-pick/import by functional category:

1. Platform/API/UI/CI work from `sprint6-automation`.
2. Lantern trilogy/movie/manuscript assets from `chatgpt/lantern-trilogy-expansion-pass` and `chatgpt/lantern-sync-main-clean-local`.
3. Lantern art generation assets from `codex/review-main-branch-for-completeness`.
4. Phase 2 docs/templates from the phase branches.
5. Artifact generator script/test from the best Codex artifact-generator variant.
6. Archive stale/behind-only branches after useful content is imported or confirmed duplicated.

## Branch Matrix

| Branch | Compare to `main` | Key contents | Recommendation |
|---|---:|---|---|
| `chatgpt/lantern-sync-main-clean` | 0 ahead / 24 behind | No unique files reported | Archive/delete candidate after confirmation. No merge needed. |
| `chatgpt/lantern-sync-main-clean-local` | 91 ahead / 21 behind | Lantern movie package, trilogy outlines/treatments, manuscript edits, shared-universe docs, Sovereign starter movie files | Content cherry-pick candidate. Do not merge wholesale. Review manuscript modifications carefully against current canon. |
| `chatgpt/lantern-trilogy-expansion-pass` | 96 ahead / 164 behind | Overlaps with `lantern-sync-main-clean-local`; adds Sovereign alignment pass, Book II scaffolding, `lantern-ii.project.json`, trilogy/movie materials | Content cherry-pick candidate. Prefer this branch for trilogy/Book II/Sovereign alignment artifacts after deduping with `lantern-sync-main-clean-local`. |
| `codex/add-lantern-protocol-artifact-generator` | 1 ahead / 210 behind | `.gitignore`, `scripts/generate_content_artifacts.py` | Superseded by tested variant. Archive after checking diff against `-9eimbn`. |
| `codex/add-lantern-protocol-artifact-generator-9eimbn` | 1 ahead / 210 behind | Artifact generator script plus `tests/test_generate_content_artifacts.py` | Best artifact-generator variant. Cherry-pick/adapt into new prompt/artifact pipeline after #69/#70 decisions. |
| `codex/add-lantern-protocol-artifact-generator-eae1t8` | 1 ahead / 210 behind | Artifact generator script only | Duplicate/superseded by `-9eimbn`. Archive after confirmation. |
| `codex/add-lantern-protocol-artifact-generator-qcceir` | 1 ahead / 210 behind | Artifact generator script only | Duplicate/superseded by `-9eimbn`. Archive after confirmation. |
| `codex/review-main-branch-for-completeness` | 5 ahead / 164 behind | Lantern art package: prompts, asset manifest, image jobs, validation script, art runbook/reports | Content/artifact cherry-pick candidate. Import through new asset storage and prompt-governance rules. Do not merge wholesale. |
| `lantern-final-proofread` | 16 ahead / 164 behind | Final proofread reports, art generation Codex task, chapter status update, workflow tweak | Cherry-pick reports/task notes only after canon review. Workflow change must be evaluated against current CI design. |
| `phase-2/sprint-1-foundation` | 4 ahead / 277 behind | PR template, canon schemas, foundation implementation doc | Cherry-pick useful docs/schemas if not duplicated by current backlog. Review schema compatibility with #32/#71. |
| `phase2-sprint2-story-architecture` | 4 ahead / 277 behind | Story architecture doc, beat sheet/chapter map/idea intake templates | Cherry-pick templates into governed prompt/template structure after #69. |
| `phase2-sprint3-character-engine` | 4 ahead / 68 behind | Character engine doc, character/dialogue/physical templates | Cherry-pick templates after #42 voice/character schema review. |
| `phase2-sprint4-chapter-storyboards` | 4 ahead / 66 behind | Chapter image prompt guidelines, storyboard/chapter brief templates | Cherry-pick templates after #32/#69/#70. |
| `phase2-sprint5-screenplay-movie` | 4 ahead / 63 behind | Screenplay/movie workflow docs, scene orchestration and screenplay templates | Cherry-pick into video/export workflow docs after #33/#51. |
| `requirements/phase-2-idea-to-blockbuster` | 1 ahead / 277 behind | Large Phase 2 requirements doc | Import as historical requirements/reference doc. Do not treat as current implementation contract without review. |
| `sprint6-automation` | 80 ahead / 53 behind | API, UI, job orchestrator, project registry, CI workflows, canon/continuity services, embedding memory, release manager, tests | Highest-value platform cherry-pick candidate. Must be split into PRs by subsystem; do not merge wholesale. |

## Recommended PR Sequence

### PR 1: Repo Governance and Developer Front Door
Source branches:
- `phase-2/sprint-1-foundation`
- `sprint6-automation`

Candidate imports:
- `.github/pull_request_template.md`
- selected governance docs
- root README/runbook alignment from new backlog issue #67

Related issues:
- #58, #67, #68

### PR 2: Project Registry and Canon Validation
Source branch:
- `sprint6-automation`

Candidate imports:
- `config/project-registry.json`
- `projects/project-registry.json`
- `services/project-registry/*`
- `services/canon-validator/*`
- canon validation workflow, after CI review

Related issues:
- #31, #37, #58, #59, #63, #71

### PR 3: Schema, Context, Continuity, and Memory Services
Source branches:
- `sprint6-automation`
- phase-2 branches

Candidate imports:
- `services/continuity-engine/*`
- `services/embedding-memory/*`
- `services/embedding-continuity/*`
- `docs/phase-2/semantic-continuity-workflow.md`
- templates only after governance rules are set

Related issues:
- #36, #62, #69, #70, #71

### PR 4: API, Job Orchestrator, and Release Manager
Source branch:
- `sprint6-automation`

Candidate imports:
- `services/content-engine-api/*`
- `services/job-orchestrator/*`
- `services/release-manager/*`
- `services/export-packager/*`
- `tests/integration/test_cinematic_pipeline.py`

Related issues:
- #39, #56, #60, #61, #62, #63, #65

### PR 5: UI Dashboard Scaffold
Source branch:
- `sprint6-automation`

Candidate imports:
- `ui/content-engine-dashboard/*`

Caveat:
- Must be reconciled with #30, #34, #35, #38, and #72. Do not import as final UI without addressing generation/review/accessibility requirements.

Related issues:
- #30, #34, #35, #38, #39, #61, #72

### PR 6: Phase 2 Templates and Prompt Governance
Source branches:
- `phase2-sprint2-story-architecture`
- `phase2-sprint3-character-engine`
- `phase2-sprint4-chapter-storyboards`
- `phase2-sprint5-screenplay-movie`
- `codex/add-lantern-protocol-artifact-generator-9eimbn`

Candidate imports:
- story templates
- character templates
- storyboard templates
- screenplay/movie templates
- artifact generator script/test, adapted to the governed template system

Related issues:
- #32, #33, #42, #62, #69, #70

### PR 7: Lantern Art Package Import
Source branch:
- `codex/review-main-branch-for-completeness`

Candidate imports:
- `projects/lantern-protocol/art/*`
- art asset manifest
- art generation runbook
- art prompt packs
- validation script

Caveat:
- Import through #60 asset storage policy and #69 prompt governance. Validate against current Lantern canon before marking approved.

Related issues:
- #36, #60, #66, #69, #70, #71

### PR 8: Lantern Trilogy / Movie / Sovereign Content Import
Source branches:
- `chatgpt/lantern-trilogy-expansion-pass`
- `chatgpt/lantern-sync-main-clean-local`
- `lantern-final-proofread`
- `requirements/phase-2-idea-to-blockbuster`

Candidate imports:
- trilogy bible/outlines/treatments
- Book II scaffolding
- Lantern movie package docs
- Sovereign alignment and starter movie files
- final proofread reports
- large Phase 2 requirement doc as historical/reference material

Caveat:
- Must be reviewed under #71 migration and #70 canon context rules. Manuscript modifications should not be applied without a canon/proofread decision.

Related issues:
- #1, #2, #3, #5, #31, #36, #66, #70, #71

## Branches Recommended for Archive After Import/Verification

- `chatgpt/lantern-sync-main-clean`
- `codex/add-lantern-protocol-artifact-generator`
- `codex/add-lantern-protocol-artifact-generator-eae1t8`
- `codex/add-lantern-protocol-artifact-generator-qcceir`

Archive the remaining divergent branches only after the corresponding import PRs are merged or explicitly rejected.

## Non-Negotiable Rules

- Do not merge any divergent branch wholesale.
- Do not import manuscript changes without canon/proofread review.
- Do not import generated art/video/audio assets until storage and manifest rules are accepted.
- Do not import provider/API code until config/secrets rules are accepted.
- Do not import UI code as final until generation/review/accessibility issues are addressed.

## Status

Branch reconciliation audit is complete. Execution requires follow-up import PRs using the sequence above.