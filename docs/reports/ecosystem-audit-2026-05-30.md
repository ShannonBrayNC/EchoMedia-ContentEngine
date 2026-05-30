# Ecosystem Audit - 2026-05-30

Scope: local Git repositories under `C:\GitHub`.

## Inventory

| Repo | Remote group | Branch | Last commit | Dirty | Capabilities |
| --- | --- | --- | --- | ---: | --- |
| christina-assistant | christina-assistant | codex/christina-wire-runner-entrypoint | 2026-05-27 | 33 | assistant/review automation, code assessment workflow, content production pipeline, frontend or node automation, lantern domain assets, operations orchestration |
| EchoChamber | echochamber | feature/p1-foundation-scaffold | 2026-03-20 | 1 | frontend or node automation, operations orchestration |
| echocode | echocode | main | 2026-05-20 | 0 | code assessment workflow |
| echocode-pipeline-christina-19 | echocode-pipeline | codex/chr-0002-register-christina | 2026-05-21 | 0 | assistant/review automation, code assessment workflow, operations orchestration, python service or automation |
| echocode-pipeline-starter | echocode-pipeline | master | 2026-05-20 | 14 | assistant/review automation, code assessment workflow, operations orchestration, python service or automation |
| echocode-platform | echocode-platform | echocodex/live-pr-write-automation-verify | 2026-05-29 | 2 | assistant/review automation, code assessment workflow, content production pipeline, frontend or node automation, lantern domain assets, operations orchestration, python service or automation |
| echocode-platform-codex-lantern | echocode-platform | codex/echocode-christina-onboarding | 2026-05-26 | 0 | assistant/review automation, code assessment workflow, lantern domain assets, operations orchestration, python service or automation |
| echoliving | echoliving | codex/echoliving-lantern-adapter-doc | 2026-05-26 | 1 | assistant/review automation, code assessment workflow, content production pipeline, frontend or node automation, operations orchestration, python service or automation, recommendation/adaptation workflow |
| EchoLiving-lantern-test | echoliving | (detached) | 2026-05-25 | 1 | code assessment workflow, content production pipeline, frontend or node automation, lantern domain assets, operations orchestration, python service or automation, recommendation/adaptation workflow |
| EchoMedia-ContentEngine | echomedia-contentengine | main | 2026-05-29 | 12 | assistant/review automation, code assessment workflow, content production pipeline, frontend or node automation, lantern domain assets, operations orchestration, recommendation/adaptation workflow |
| EchoMedia-ContentEngine-codex-lantern | echomedia-contentengine | codex/content-engine-lantern-assets | 2026-05-26 | 0 | assistant/review automation, content production pipeline, frontend or node automation, lantern domain assets, operations orchestration, recommendation/adaptation workflow |
| EchoMedia-ContentEngine-pr112 | echomedia-contentengine | codex/book-ii-canon-scaffold-local | 2026-05-26 | 0 | assistant/review automation, content production pipeline, frontend or node automation, lantern domain assets, operations orchestration, recommendation/adaptation workflow |
| echomedia-website | echomedia-website | master | 2026-05-20 | 23 | assistant/review automation, code assessment workflow, content production pipeline, frontend or node automation, lantern domain assets, operations orchestration, public web presence |
| EmMigrationToolKit | em.migration.toolkit | main | 2026-03-25 | 6 | migration toolkit |
| ETS | ets | codex/lantern-stack-sweep-20260526 | 2026-05-26 | 1 | assistant/review automation, code assessment workflow, containerized service, content production pipeline, frontend or node automation, lantern domain assets, operations orchestration, python service or automation, recommendation/adaptation workflow |
| ETS-pr15 | ets | (detached) | 2026-05-24 | 0 | code assessment workflow, containerized service, frontend or node automation, operations orchestration, python service or automation |
| lantern | echomedia-contentengine | chatgpt/lantern-sync-main-clean-local | 2026-05-23 | 3 | content production pipeline, lantern domain assets, operations orchestration |
| Lantern-Civic | lantern-civic | main | 2026-05-26 | 0 | assistant/review automation, code assessment workflow, lantern domain assets, operations orchestration, python service or automation |
| linkedin-integration | linkedin-integration | master | 2026-05-20 | 0 | code assessment workflow, linkedin integration, python service or automation |
| OpsHelm | opshelm | feature/opshelm-47-graph-ticket-container-compat | 2026-05-29 | 1 | assistant/review automation, code assessment workflow, content production pipeline, frontend or node automation, lantern domain assets, operations orchestration, python service or automation, recommendation/adaptation workflow |
| OpsHelm-codex-christina | opshelm | codex/opshelm-christina-onboarding | 2026-05-26 | 0 | assistant/review automation, code assessment workflow, content production pipeline, frontend or node automation, operations orchestration, python service or automation, recommendation/adaptation workflow |
| OpsHelm-lantern-test | opshelm | (detached) | 2026-05-25 | 1 | assistant/review automation, code assessment workflow, frontend or node automation, lantern domain assets, operations orchestration, python service or automation, recommendation/adaptation workflow |

## Dependency Graph

- `api runtime` -> ETS, ETS-pr15, EchoLiving-lantern-test, echoliving
- `browser runtime` -> ETS, ETS-pr15, EchoLiving-lantern-test, EchoMedia-ContentEngine, EchoMedia-ContentEngine-codex-lantern, EchoMedia-ContentEngine-pr112, echoliving
- `docker` -> ETS, ETS-pr15
- `node/npm` -> ETS, ETS-pr15, EchoChamber, EchoLiving-lantern-test, EchoMedia-ContentEngine, EchoMedia-ContentEngine-codex-lantern, EchoMedia-ContentEngine-pr112, OpsHelm, OpsHelm-codex-christina, OpsHelm-lantern-test, christina-assistant, echocode-platform, echoliving, echomedia-website
- `python` -> ETS, ETS-pr15, EchoLiving-lantern-test, Lantern-Civic, OpsHelm, OpsHelm-codex-christina, OpsHelm-lantern-test, echocode-pipeline-christina-19, echocode-pipeline-starter, echocode-platform, echocode-platform-codex-lantern, echoliving, linkedin-integration

## Capability Map

- assistant/review automation: ETS, EchoMedia-ContentEngine, EchoMedia-ContentEngine-codex-lantern, EchoMedia-ContentEngine-pr112, Lantern-Civic, OpsHelm, OpsHelm-codex-christina, OpsHelm-lantern-test, christina-assistant, echocode-pipeline-christina-19, echocode-pipeline-starter, echocode-platform, echocode-platform-codex-lantern, echoliving, echomedia-website
- code assessment workflow: ETS, ETS-pr15, EchoLiving-lantern-test, EchoMedia-ContentEngine, Lantern-Civic, OpsHelm, OpsHelm-codex-christina, OpsHelm-lantern-test, christina-assistant, echocode, echocode-pipeline-christina-19, echocode-pipeline-starter, echocode-platform, echocode-platform-codex-lantern, echoliving, echomedia-website, linkedin-integration
- containerized service: ETS, ETS-pr15
- content production pipeline: ETS, EchoLiving-lantern-test, EchoMedia-ContentEngine, EchoMedia-ContentEngine-codex-lantern, EchoMedia-ContentEngine-pr112, OpsHelm, OpsHelm-codex-christina, christina-assistant, echocode-platform, echoliving, echomedia-website, lantern
- frontend or node automation: ETS, ETS-pr15, EchoChamber, EchoLiving-lantern-test, EchoMedia-ContentEngine, EchoMedia-ContentEngine-codex-lantern, EchoMedia-ContentEngine-pr112, OpsHelm, OpsHelm-codex-christina, OpsHelm-lantern-test, christina-assistant, echocode-platform, echoliving, echomedia-website
- lantern domain assets: ETS, EchoLiving-lantern-test, EchoMedia-ContentEngine, EchoMedia-ContentEngine-codex-lantern, EchoMedia-ContentEngine-pr112, Lantern-Civic, OpsHelm, OpsHelm-lantern-test, christina-assistant, echocode-platform, echocode-platform-codex-lantern, echomedia-website, lantern
- linkedin integration: linkedin-integration
- migration toolkit: EmMigrationToolKit
- operations orchestration: ETS, ETS-pr15, EchoChamber, EchoLiving-lantern-test, EchoMedia-ContentEngine, EchoMedia-ContentEngine-codex-lantern, EchoMedia-ContentEngine-pr112, Lantern-Civic, OpsHelm, OpsHelm-codex-christina, OpsHelm-lantern-test, christina-assistant, echocode-pipeline-christina-19, echocode-pipeline-starter, echocode-platform, echocode-platform-codex-lantern, echoliving, echomedia-website, lantern
- public web presence: echomedia-website
- python service or automation: ETS, ETS-pr15, EchoLiving-lantern-test, Lantern-Civic, OpsHelm, OpsHelm-codex-christina, OpsHelm-lantern-test, echocode-pipeline-christina-19, echocode-pipeline-starter, echocode-platform, echocode-platform-codex-lantern, echoliving, linkedin-integration
- recommendation/adaptation workflow: ETS, EchoLiving-lantern-test, EchoMedia-ContentEngine, EchoMedia-ContentEngine-codex-lantern, EchoMedia-ContentEngine-pr112, OpsHelm, OpsHelm-codex-christina, OpsHelm-lantern-test, echoliving

## Overlap And Duplicate Services

- `echocode-pipeline` has 2 local checkouts: echocode-pipeline-christina-19, echocode-pipeline-starter
- `echocode-platform` has 2 local checkouts: echocode-platform, echocode-platform-codex-lantern
- `echoliving` has 2 local checkouts: echoliving, EchoLiving-lantern-test
- `echomedia-contentengine` has 4 local checkouts: EchoMedia-ContentEngine, EchoMedia-ContentEngine-codex-lantern, EchoMedia-ContentEngine-pr112, lantern
- `ets` has 2 local checkouts: ETS, ETS-pr15
- `opshelm` has 3 local checkouts: OpsHelm, OpsHelm-codex-christina, OpsHelm-lantern-test
- Capability overlap `assistant/review automation`: ETS, EchoMedia-ContentEngine, EchoMedia-ContentEngine-codex-lantern, EchoMedia-ContentEngine-pr112, Lantern-Civic, OpsHelm, OpsHelm-codex-christina, OpsHelm-lantern-test, christina-assistant, echocode-pipeline-christina-19, echocode-pipeline-starter, echocode-platform, echocode-platform-codex-lantern, echoliving, echomedia-website
- Capability overlap `code assessment workflow`: ETS, ETS-pr15, EchoLiving-lantern-test, EchoMedia-ContentEngine, Lantern-Civic, OpsHelm, OpsHelm-codex-christina, OpsHelm-lantern-test, christina-assistant, echocode, echocode-pipeline-christina-19, echocode-pipeline-starter, echocode-platform, echocode-platform-codex-lantern, echoliving, echomedia-website, linkedin-integration
- Capability overlap `containerized service`: ETS, ETS-pr15
- Capability overlap `content production pipeline`: ETS, EchoLiving-lantern-test, EchoMedia-ContentEngine, EchoMedia-ContentEngine-codex-lantern, EchoMedia-ContentEngine-pr112, OpsHelm, OpsHelm-codex-christina, christina-assistant, echocode-platform, echoliving, echomedia-website, lantern
- Capability overlap `frontend or node automation`: ETS, ETS-pr15, EchoChamber, EchoLiving-lantern-test, EchoMedia-ContentEngine, EchoMedia-ContentEngine-codex-lantern, EchoMedia-ContentEngine-pr112, OpsHelm, OpsHelm-codex-christina, OpsHelm-lantern-test, christina-assistant, echocode-platform, echoliving, echomedia-website
- Capability overlap `lantern domain assets`: ETS, EchoLiving-lantern-test, EchoMedia-ContentEngine, EchoMedia-ContentEngine-codex-lantern, EchoMedia-ContentEngine-pr112, Lantern-Civic, OpsHelm, OpsHelm-lantern-test, christina-assistant, echocode-platform, echocode-platform-codex-lantern, echomedia-website, lantern
- Capability overlap `operations orchestration`: ETS, ETS-pr15, EchoChamber, EchoLiving-lantern-test, EchoMedia-ContentEngine, EchoMedia-ContentEngine-codex-lantern, EchoMedia-ContentEngine-pr112, Lantern-Civic, OpsHelm, OpsHelm-codex-christina, OpsHelm-lantern-test, christina-assistant, echocode-pipeline-christina-19, echocode-pipeline-starter, echocode-platform, echocode-platform-codex-lantern, echoliving, echomedia-website, lantern
- Capability overlap `python service or automation`: ETS, ETS-pr15, EchoLiving-lantern-test, Lantern-Civic, OpsHelm, OpsHelm-codex-christina, OpsHelm-lantern-test, echocode-pipeline-christina-19, echocode-pipeline-starter, echocode-platform, echocode-platform-codex-lantern, echoliving, linkedin-integration
- Capability overlap `recommendation/adaptation workflow`: ETS, EchoLiving-lantern-test, EchoMedia-ContentEngine, EchoMedia-ContentEngine-codex-lantern, EchoMedia-ContentEngine-pr112, OpsHelm, OpsHelm-codex-christina, OpsHelm-lantern-test, echoliving

## Abandoned Or At-Risk Initiatives

- EchoChamber: last commit 2026-03-20; branch `feature/p1-foundation-scaffold`
- EmMigrationToolKit: last commit 2026-03-25; branch `main`

## Generated Issues

1. [P0] Consolidate duplicate local clones and PR worktrees: 6 remote groups have multiple local checkouts; choose canonical working copies before cross-repo implementation.
2. [P0] Resolve dirty worktrees before ecosystem-wide changes: 13 repos have uncommitted files. Capture, commit, or intentionally park them before automated changes.
3. [P1] Archive or merge temporary Codex/test clones: 9 repos look like task-specific clones. Fold useful changes into canonical repos and remove stale checkouts.
4. [P1] Review stale initiatives for ownership: 2 repos have not had a commit in more than 60 days.
5. [P2] Assign clear system ownership for overlapping capabilities: 9 capabilities appear in multiple repos. Document source-of-truth boundaries and adapter contracts.

## Implementation Order

1. P0: choose canonical checkout per duplicate remote group and resolve dirty worktrees.
2. P0: keep this audit script in CI or a scheduled local run so ecosystem drift becomes visible.
3. P1: merge or archive temporary Codex/test clones after useful deltas are harvested.
4. P1: assign owner and disposition for stale repos.
5. P2: document capability boundaries and adapter contracts for overlapping services.

## Highest Priority Sprint

Sprint launched: ecosystem audit automation in `EchoMedia-ContentEngine`.

Acceptance criteria:
- `python scripts/ecosystem_audit.py --root C:\GitHub --output docs/reports/ecosystem-audit-2026-05-30.md --json-output docs/reports/ecosystem-audit-2026-05-30.json` regenerates this report.
- Unit tests cover duplicate detection, stale detection, dependency inference, and issue prioritization.
- The report identifies P0/P1/P2 work before any cross-repo code changes.

## Re-Evaluation Loop

Repeat this audit after each consolidation PR, then reprioritize the generated issues from the new report.
