# Legacy Artifact Migration Plan

This document defines the Sprint 1 migration plan for existing project artifacts.

## Purpose

Existing Lantern Protocol, Sovereign Exception, and phase branch files must be mapped into the new project registry, folder contract, schemas, and artifact manifest policy before large imports or moves occur.

## Migration principles

- Do not move files until a migration report is reviewed.
- Do not overwrite canon files without approval.
- Do not import branch content wholesale.
- Do not treat generated files as approved until reviewed.
- Preserve useful history through archive folders or manifests.

## Classification types

Each discovered file should be classified as one of:

- canonical source
- approved artifact
- draft artifact
- generated asset
- report
- template
- schema candidate
- legacy duplicate
- archive candidate
- delete candidate after review

## Migration matrix fields

A migration report should include:

- current path
- proposed canonical path
- project ID
- artifact type
- source or generated status
- hash
- branch source if imported
- action: keep, move, alias, archive, skip, delete candidate
- reviewer notes

## Branch sources

The branch reconciliation report identifies candidate sources:

- `sprint6-automation`
- `chatgpt/lantern-trilogy-expansion-pass`
- `chatgpt/lantern-sync-main-clean-local`
- `codex/review-main-branch-for-completeness`
- `lantern-final-proofread`
- phase 2 template branches

## Validation checks

Before a migration PR is accepted, check:

- target path follows folder contract
- project registry entry exists
- schema validation passes where applicable
- manifest records source references
- duplicate canon conflicts are flagged
- large media storage policy is followed
- generated content has review state

## Migration order

1. Inventory current `main` project files.
2. Inventory candidate branch files.
3. Create migration matrix.
4. Import templates and schemas first.
5. Import reports and docs next.
6. Import generated/art package manifests after storage policy acceptance.
7. Import manuscript/canon changes only after review.

## Related issues

- #31
- #37
- #58
- #60
- #70
- #71
