# Book Factory Design

**Sprint:** PUB-002  
**Status:** Active architecture  
**Owner:** Lantern Publishing / EchoMedia Content Engine

## Purpose
The Book Factory is the repeatable creation and management system for books, series, trilogies, anthologies, and case files. Its purpose is to make the creation of hundreds of books predictable, auditable, and governed.

## Core Capability
A new book should be creatable from a template with:

- canonical folder structure
- metadata file
- chapter workspace
- outline workspace
- canon references
- Producer Review workspace
- publishing package workspace
- audiobook workspace
- marketing workspace

## Factory Inputs
- Universe ID
- Series ID
- Book ID
- Title
- Book number
- Series type
- Genre
- Status
- Canon status
- Producer Review status
- Rights status

## Factory Outputs

```text
projects/<universe>/series/<series>/books/<book>/
├── README.md
├── metadata.yaml
├── manuscript/
├── chapters/
├── outlines/
├── characters/
├── locations/
├── research/
├── continuity/
├── producer-review/
├── publishing-package/
├── audiobook/
└── marketing/
```

## Registries
The factory must be registry-driven. Future automation should read:

- universe registry
- series registry
- book metadata
- character registry
- timeline registry
- release calendar
- Producer Review status

## Validation Gates
A book is not eligible for release packaging until:

1. Required folders exist.
2. `metadata.yaml` validates against schema.
3. Series metadata exists.
4. Canon dependencies are declared.
5. Producer Review status is approved or explicitly waived.
6. Publishing package manifest exists.

## Automation Hooks
Future scripts should support:

```text
create-universe
create-series
create-book
validate-book
validate-series
compile-manuscript
run-continuity-check
create-publishing-package
create-audiobook-package
```

## Scale Requirements
The system must support:

- 100-500 books
- multiple universes
- multiple series per universe
- multiple production states
- parallel AI/human editing
- safe partial completion
- retryable workflows
- searchable metadata

## Agent Rules
Codex, Christina, and future Lantern agents must not invent arbitrary folders. They must use the Book Folder Contract and Series Folder Contract.

## Success Criteria
The Book Factory succeeds when a new book can be created, validated, reviewed, packaged, and indexed without manual structure decisions.
