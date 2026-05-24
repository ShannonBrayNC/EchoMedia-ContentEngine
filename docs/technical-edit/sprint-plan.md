# Content Engine Technical Edit Sprint Plan

## Purpose

This plan breaks the technical edit issues into small implementation sprints. The goal is to bring the Content Engine back to its intended product shape: a project-driven system that generates pre-movie production files for advanced AI video, audio, storyboard, screenplay, and pitch workflows.

The first principle is separation of concerns:

- Project consistency first.
- Generation workflow second.
- Review and traceability third.
- Export adapters last.

That keeps the project from turning into a button garden where every button claims to do everything and secretly only checks whether a folder exists.

---

## Sprint 1 - Project registry and folder consistency foundation

**Primary issues**

- #31 - Restore project registry consistency for Lantern Protocol and all book projects
- #37 - Standardize folder structure across all story projects

**Goal**

Create a single project registry contract and folder-structure standard so every book/story project can be discovered, validated, and addressed consistently by later UI and generation workflows.

**Deliverables**

- Project registry schema.
- Standard project folder contract.
- Sprint 1 completion report.
- Rules for project visibility, required folders, optional folders, and legacy aliases.

**Definition of done**

- The repo has a documented project registry model.
- The repo has a documented folder contract for all projects.
- The next sprint can build UI/project selection against this contract.

---

## Sprint 2 - Real generation workspace and action semantics

**Primary issues**

- #30 - Define the real Content Engine generation workspace in the UI
- #35 - Separate validation actions from generation actions in the UI and API

**Goal**

Redesign the interaction model so the user has a clear place to generate content, not just press validation buttons.

**Deliverables**

- UI workflow spec for the generation workspace.
- Action taxonomy for Validate, Generate, Assemble, Export, and Save/Commit.
- Button-label and placement rules.
- Draft wireframe/spec for the workspace.

**Definition of done**

- Validation and generation are visibly different actions.
- The UI has a primary generation surface.
- Each action has a predictable input, output, and persistence rule.

---

## Sprint 3 - Production package and generation job model

**Primary issues**

- #32 - Define pre-movie production package schema for AI video tools
- #39 - Create generation job/state model for long-running content work

**Goal**

Define the data structures that represent movie-ready generation requests, scene packages, and long-running generation work.

**Deliverables**

- Production package schema.
- Scene package schema.
- Generation job schema.
- State machine for draft request, queued, generating, generated, needs review, approved, exported, failed, and superseded.

**Definition of done**

- The engine can represent a production package as structured data.
- The UI/backend can track generation as a job instead of a single button click.
- Failed generation cannot corrupt approved project artifacts.

---

## Sprint 4 - Preview/review gate and traceability

**Primary issues**

- #38 - Add preview/review gate before generated artifacts are saved
- #36 - Add artifact traceability from manuscript to screenplay to video package

**Goal**

Ensure generated artifacts are reviewable, auditable, and linked back to source material before they become project assets.

**Deliverables**

- Draft artifact lifecycle model.
- Preview/review/approve/reject flow.
- Traceability model from manuscript to screenplay to scene card to storyboard to visual/video export.
- Canon-impact regeneration rules.

**Definition of done**

- Generated artifacts do not overwrite approved files without review.
- Artifacts can be traced back to their source chapter, scene, canon, and visual bible references.
- Canon changes can identify downstream affected artifacts.

---

## Sprint 5 - Compact workflow/status rail

**Primary issue**

- #34 - Replace redundant order display with compact workflow/status rail

**Goal**

Replace the redundant order display with a compact status rail that supports generation, review, validation, export, and save/commit stages.

**Deliverables**

- Compact rail specification.
- Required status fields.
- Expanded-detail rules.
- Error/warning visibility rules.

**Definition of done**

- The workflow/status display uses less space.
- It supports current project, artifact type, stage, status, warnings, and next action.
- It works for generation, not just validation.

---

## Sprint 6 - Export profiles and tool adapters

**Primary issue**

- #33 - Add export profiles for major AI video and audio tools

**Goal**

Create reusable export profiles that transform canonical production packages into tool-specific packages.

**Initial target profiles**

- Runway scene prompt package.
- Pika prompt package.
- Luma / Dream Machine shot package.
- Kling video prompt package.
- Sora-style scene package.
- ElevenLabs audiobook/dialogue package.
- Generic storyboard / pitch deck package.
- Generic JSON package for future adapters.

**Definition of done**

- Export profiles are data-driven.
- One scene can export to at least two target formats from the same canonical source.
- Missing required fields produce useful validation messages.

---

## Recommended sequence

1. Complete Sprint 1 before touching the UI.
2. Complete Sprint 2 before adding more buttons.
3. Complete Sprint 3 before wiring advanced generation.
4. Complete Sprint 4 before saving generated output directly into project folders.
5. Complete Sprint 5 after action semantics are clear.
6. Complete Sprint 6 once the canonical production package is stable.
