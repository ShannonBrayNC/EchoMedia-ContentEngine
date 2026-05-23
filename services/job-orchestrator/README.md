# Job Orchestrator

## Purpose

Provide asynchronous workflow execution for long-running cinematic pipeline operations.

## Current Capabilities

- queued jobs
- retry support
- workflow execution tracking
- job persistence
- cancellation requests
- priority ordering
- release workflow orchestration

## Current Workflows

- assemble-screenplay
- build-export-package
- create-release

## Commands

### Run Worker

```text
python services/job-orchestrator/run_job_worker.py
```

## Job States

```text
queued
running
completed
failed
retrying
cancelled
```

## Storage

Jobs are persisted under:

```text
jobs/
```

## Future Expansion

- Redis queues
- Celery integration
- Azure Service Bus
- distributed workers
- dashboard live updates
- GPU rendering orchestration
