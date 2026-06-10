# EchoCodex Approved Change Note

- Repository: ShannonBrayNC/EchoMedia-ContentEngine
- Branch: echocodex/echomedia-contentengine-217-contentengine-sprint-profile-driven-image-genera
- Issue: ShannonBrayNC/EchoMedia-ContentEngine#217 ContentEngine Sprint: Profile-driven image generation
- Source issue URL: https://github.com/ShannonBrayNC/EchoMedia-ContentEngine/issues/217
- Generated at: 2026-06-10T02:01:45.544Z
- EchoCodex report: C:\workspace\GitHub\christina-sprint-runs\process-open-sprints-20260609-220058/20260610020145-shannonbraync-echomedia-contentengine-217

## Objective

ContentEngine Sprint: Profile-driven image generation

## Request body

## Objective

Generate images from durable profiles rather than one-off prompts.

## Requirements

- Resolve subject profile by name or ID.
- Resolve brand profile.
- Resolve production/scene profile.
- Build prompt from profile data.
- Include approved reference images.
- Save output metadata:
  - outputId
  - profileIds
  - profileVersions
  - references used
  - prompt
  - negativePrompt
  - approvalStatus
- Support image backend adapter interface.

## Acceptance Criteria

- User can request: Generate Vanessa presenting Lantern to investors.
- ContentEngine uses Vanessa profile, Lantern brand profile, and investor-pitch production profile.
- Output records profile versions used.

## Execution notes

This file was written only after EchoCodex policy returned allow and explicit human approval was provided.
The file is intentionally placed under docs/echocodex/sprints so it stays auditable and does not alter application runtime behavior.

## Validation notes

Review the paired EchoCodex report folder for validation preview and policy metadata before committing or opening a pull request.

## Rollback notes

Remove this file from the feature branch if the sprint is rejected or superseded.
