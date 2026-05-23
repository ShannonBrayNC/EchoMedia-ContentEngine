# Platform Review and Priority Roadmap

## Purpose

This document captures the current platform review after the Sprint 6 automation, API, UI, Christina, and governance additions.

The Content Engine is now evolving from a manuscript tool into a multi-project cinematic operating platform.

## Current Strengths

### Governance

- canon validation
- continuity scoring
- semantic continuity comparison
- GitHub validation workflows
- release states
- audit logging

### Production Pipeline

- chapter packet generation
- screenplay assembly
- Fountain export
- scene segmentation
- runtime estimation
- trailer suitability scoring
- export package creation

### Operations Layer

- FastAPI orchestration shell
- dashboard scaffold
- Christina operator workspace
- role-based access control
- API audit logging

## Highest Priority Gaps

### 1. Multi-Project Persistence

The platform must support many simultaneous projects.

Examples:

- Lantern Protocol Book I
- Lantern Protocol Book II
- unrelated novel series
- TV adaptation
- movie package
- commercial campaign

The system must not assume a single active project.

### 2. Project Selection

Every UI, API, and Christina workflow must operate against an explicit selected project.

### 3. Christina Conversational Control

Christina must be able to:

- list projects
- select a project
- summarize project status
- launch workflows
- explain continuity drift
- package releases

### 4. Async Workflow Orchestration

Long-running operations must move to background jobs.

Examples:

- screenplay assembly
- image generation
- movie package generation
- release packaging
- semantic indexing

### 5. Vector Memory Isolation

Semantic memory must be scoped by project and franchise.

Book I memory must not contaminate Book II unless a relationship is approved.

### 6. TV and Commercial Adaptation Pipelines

The platform must support adaptation targets beyond novels and feature screenplays:

- TV episodes
- streaming seasons
- trailers
- commercials
- social media clips

## Required Product Conversion Paths

### Manuscript to Screenplay

```text
manuscript -> chapter packets -> screenplay scenes -> Fountain export
```

### Manuscript to Movie Package

```text
manuscript -> screenplay -> scene cards -> runtime report -> trailer suitability -> production package
```

### Manuscript to TV Series

```text
manuscript -> season arc -> episode map -> episode scripts -> runtime balance -> release package
```

### Manuscript to Commercials

```text
story package -> hook extraction -> commercial script -> voiceover script -> social cutdowns
```

## Immediate Implementation Order

1. Multi-project registry and project switching
2. Christina project-aware workflow control
3. End-to-end test harness
4. Async job orchestration
5. Vector memory integration
6. TV adaptation engine
7. Commercial generation engine

## Completion Definition

The platform is ready for first integrated product testing when:

- multiple projects can be registered and selected
- Christina can operate on the selected project
- API routes are project-aware
- UI can switch active projects
- an end-to-end test converts one project from manuscript to screenplay/export package
