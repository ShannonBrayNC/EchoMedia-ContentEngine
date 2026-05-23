# Project Registry Service

## Purpose

Manage multiple simultaneous cinematic and narrative projects.

## Responsibilities

- list projects
- select active project
- persist active project
- provide project metadata
- isolate project paths
- support franchise grouping

## Registry File

```text
config/project-registry.json
```

## Required Features

- active project selection
- project filtering
- project lifecycle states
- franchise grouping
- per-project memory isolation
- Christina project awareness

## Planned API Routes

```text
GET /projects
POST /projects/select
GET /projects/active
```
