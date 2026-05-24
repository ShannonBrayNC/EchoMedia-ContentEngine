# Context Assembly Strategy

This document defines how generation work gathers project context.

## Purpose

Generation must use project canon and approved artifacts rather than loose memory.

## Context sources

A context package may include:

- project registry entry
- canon files
- character files
- manuscript sections
- screenplay scenes
- visual bible entries
- voice package records
- timeline records
- approved prior artifacts
- selected user direction

## Rules

Canon is authoritative. Memory indexes and prior generated drafts are secondary.

Each generation job should record a context manifest with:

- context manifest ID
- project ID
- artifact type
- source references
- hashes
- token or size estimate
- assembly timestamp
- notes about omitted or stale context

## Stale context

If canon changes, generated artifacts that depend on that canon should be marked for review or regeneration.

## Bounded context

Large projects should not send everything into every job. Each artifact type needs retrieval rules that select the smallest useful context package.

## Related issues

- #70
- #36
- #32
- #60
