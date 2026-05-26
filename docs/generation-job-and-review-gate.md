# Generation Job and Review Gate Contract

This document defines the Sprint 2 job state model and review gate rules.

## Purpose

Generation is not an instant button action. It is a tracked job that may create drafts, fail validation, require review, export to providers, or become superseded.

## Job states

Allowed job states:

- `draft-request`: request has been assembled but not submitted
- `queued`: accepted for processing
- `generating`: active work is running
- `generated`: output was produced
- `needs-review`: output is waiting for human review
- `approved`: output was accepted
- `exported`: output was converted into a target package
- `failed`: work failed
- `cancelled`: user or system cancelled the job
- `superseded`: newer work replaced this output

## Required job metadata

A job should record:

- job ID
- project ID
- artifact type
- source references
- context manifest ID
- template ID/version
- user direction
- export profile ID
- provider target when applicable
- dry-run/live mode
- status
- warnings
- errors
- artifact IDs
- manifest IDs
- correlation ID
- timestamps

## Review gate rules

Generated artifacts first land in draft or review state. They should not overwrite approved project content.

Review actions:

- approve
- reject
- request revision
- supersede

Approval should record:

- reviewer
- timestamp
- notes
- artifact IDs
- manifest IDs

## Save behavior

Saving approved content should be explicit. Existing files require overwrite confirmation. Rejected drafts should not become canonical artifacts.

## Retry behavior

Retries should keep the original job record and create a linked retry attempt or child job. The system should not erase the failed attempt.

## Related issues

- #38
- #39
- #56
- #60
- #61
