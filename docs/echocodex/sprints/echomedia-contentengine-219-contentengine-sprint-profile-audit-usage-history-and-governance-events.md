# EchoCodex Approved Change Note

- Repository: ShannonBrayNC/EchoMedia-ContentEngine
- Branch: echocodex/echomedia-contentengine-219-contentengine-sprint-profile-audit-usage-history
- Issue: ShannonBrayNC/EchoMedia-ContentEngine#219 ContentEngine Sprint: Profile audit, usage history, and governance events
- Source issue URL: https://github.com/ShannonBrayNC/EchoMedia-ContentEngine/issues/219
- Generated at: 2026-06-10T02:04:27.747Z
- EchoCodex report: C:\workspace\GitHub\christina-sprint-runs\process-open-sprints-20260609-220333/20260610020427-shannonbraync-echomedia-contentengine-219

## Objective

ContentEngine Sprint: Profile audit, usage history, and governance events

## Request body

## Objective

Add audit tracking for profile actions and profile usage.

## Requirements

Audit events for:

- profile.created
- profile.updated
- profile.archived
- profile.deleted
- profile.reference.added
- profile.reference.removed
- profile.used
- output.generated
- output.approved
- output.rejected

Audit must answer:

- Who created this profile?
- Which references were used?
- Which output used which profile version?
- Was approval required?
- Was approval granted?
- Who archived/deleted a profile?

## Acceptance Criteria

- Every profile change emits an audit event.
- Every generated output records profile usage.
- Deleted profiles leave a tombstone unless hard-delete is explicitly approved.

## Execution notes

This file was written only after EchoCodex policy returned allow and explicit human approval was provided.
The file is intentionally placed under docs/echocodex/sprints so it stays auditable and does not alter application runtime behavior.

## Validation notes

Review the paired EchoCodex report folder for validation preview and policy metadata before committing or opening a pull request.

## Rollback notes

Remove this file from the feature branch if the sprint is rejected or superseded.
