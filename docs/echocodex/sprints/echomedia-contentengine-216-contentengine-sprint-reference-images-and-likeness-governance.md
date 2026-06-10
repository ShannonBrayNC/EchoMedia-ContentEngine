# EchoCodex Approved Change Note

- Repository: ShannonBrayNC/EchoMedia-ContentEngine
- Branch: echocodex/echomedia-contentengine-216-contentengine-sprint-reference-images-and-likene
- Issue: ShannonBrayNC/EchoMedia-ContentEngine#216 ContentEngine Sprint: Reference images and likeness governance
- Source issue URL: https://github.com/ShannonBrayNC/EchoMedia-ContentEngine/issues/216
- Generated at: 2026-06-10T02:00:33.585Z
- EchoCodex report: C:\workspace\GitHub\christina-sprint-runs\process-open-sprints-20260609-215945/20260610020033-shannonbraync-echomedia-contentengine-216

## Objective

ContentEngine Sprint: Reference images and likeness governance

## Request body

## Objective

Add governed reference image handling for subject profiles.

## Requirements

- Store reference images under profile directories.
- Classify references:
  - identity
  - wardrobe
  - pose
  - scene
  - mood
  - expression
  - full_body
- Track approval status per reference image.
- Track whether profile represents a real person, fictional character, or generated composite.
- Add likeness consent flags.
- Add commercial-use and public-use restrictions.
- Prevent accidental identity blending by keeping reference types explicit.

## Acceptance Criteria

- Vanessa can have approved identity references.
- A wardrobe-only reference does not become identity reference.
- Outputs record which reference images were used.

## Execution notes

This file was written only after EchoCodex policy returned allow and explicit human approval was provided.
The file is intentionally placed under docs/echocodex/sprints so it stays auditable and does not alter application runtime behavior.

## Validation notes

Review the paired EchoCodex report folder for validation preview and policy metadata before committing or opening a pull request.

## Rollback notes

Remove this file from the feature branch if the sprint is rejected or superseded.
