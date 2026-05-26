export const GENERATION_JOB_STATES = Object.freeze({
  DRAFT_REQUEST: 'draft-request',
  QUEUED: 'queued',
  GENERATING: 'generating',
  GENERATED: 'generated',
  NEEDS_REVIEW: 'needs-review',
  APPROVED: 'approved',
  EXPORTED: 'exported',
  FAILED: 'failed',
  SUPERSEDED: 'superseded',
  CANCELLED: 'cancelled'
});

export const TERMINAL_JOB_STATES = Object.freeze([
  GENERATION_JOB_STATES.APPROVED,
  GENERATION_JOB_STATES.EXPORTED,
  GENERATION_JOB_STATES.FAILED,
  GENERATION_JOB_STATES.SUPERSEDED,
  GENERATION_JOB_STATES.CANCELLED
]);

export const GENERATION_JOB_TRANSITIONS = Object.freeze({
  [GENERATION_JOB_STATES.DRAFT_REQUEST]: [GENERATION_JOB_STATES.QUEUED, GENERATION_JOB_STATES.CANCELLED],
  [GENERATION_JOB_STATES.QUEUED]: [GENERATION_JOB_STATES.GENERATING, GENERATION_JOB_STATES.CANCELLED, GENERATION_JOB_STATES.FAILED],
  [GENERATION_JOB_STATES.GENERATING]: [GENERATION_JOB_STATES.GENERATED, GENERATION_JOB_STATES.FAILED, GENERATION_JOB_STATES.CANCELLED],
  [GENERATION_JOB_STATES.GENERATED]: [GENERATION_JOB_STATES.NEEDS_REVIEW, GENERATION_JOB_STATES.SUPERSEDED],
  [GENERATION_JOB_STATES.NEEDS_REVIEW]: [
    GENERATION_JOB_STATES.APPROVED,
    GENERATION_JOB_STATES.SUPERSEDED,
    GENERATION_JOB_STATES.FAILED
  ],
  [GENERATION_JOB_STATES.APPROVED]: [GENERATION_JOB_STATES.EXPORTED, GENERATION_JOB_STATES.SUPERSEDED],
  [GENERATION_JOB_STATES.EXPORTED]: [GENERATION_JOB_STATES.SUPERSEDED],
  [GENERATION_JOB_STATES.FAILED]: [GENERATION_JOB_STATES.QUEUED, GENERATION_JOB_STATES.SUPERSEDED],
  [GENERATION_JOB_STATES.SUPERSEDED]: [],
  [GENERATION_JOB_STATES.CANCELLED]: [GENERATION_JOB_STATES.QUEUED, GENERATION_JOB_STATES.SUPERSEDED]
});

function nowIso() {
  return new Date().toISOString();
}

function normalizeReason(reason) {
  return reason || 'State changed by generation workflow.';
}

export function canTransitionGenerationJob(fromState, toState) {
  return Boolean(GENERATION_JOB_TRANSITIONS[fromState]?.includes(toState));
}

export function createGenerationJobEvent({ fromState, toState, reason, metadata }) {
  return {
    from_state: fromState || null,
    to_state: toState,
    reason: normalizeReason(reason),
    metadata: metadata || {},
    occurred_at: nowIso()
  };
}

export function withGenerationJobEvent(job, event) {
  return {
    ...job,
    state: event.to_state,
    events: [...(job.events || []), event],
    updated_at: event.occurred_at
  };
}

export function transitionGenerationJob(job, toState, reason, metadata) {
  if (!job) {
    throw new Error('Cannot transition a missing generation job.');
  }

  if (!canTransitionGenerationJob(job.state, toState)) {
    throw new Error(`Invalid generation job transition from ${job.state} to ${toState}.`);
  }

  return withGenerationJobEvent(
    job,
    createGenerationJobEvent({
      fromState: job.state,
      toState,
      reason,
      metadata
    })
  );
}

export function initializeGenerationJobHistory(job) {
  if (!job) {
    return [];
  }

  const createdEvent = createGenerationJobEvent({
    fromState: null,
    toState: job.state,
    reason: 'Generation job created.',
    metadata: {
      action: job.action,
      artifact_type: job.artifact_type,
      project_slug: job.project_slug
    }
  });

  return [
    {
      ...job,
      events: job.events?.length ? job.events : [createdEvent],
      attempt: job.attempt || 1,
      parent_job_id: job.parent_job_id || null,
      retry_of_job_id: job.retry_of_job_id || null,
      supersedes_job_id: job.supersedes_job_id || null
    }
  ];
}

export function upsertGenerationJob(history, job) {
  const existing = history || [];
  const index = existing.findIndex((item) => item.job_id === job.job_id);

  if (index === -1) {
    return [job, ...existing];
  }

  return existing.map((item, itemIndex) => (itemIndex === index ? job : item));
}

export function appendGenerationJob(history, job) {
  return [job, ...(history || [])];
}

export function markGenerationJobNeedsReview(job, reviewGate) {
  if (!job || job.state !== GENERATION_JOB_STATES.GENERATED) {
    return job;
  }

  return transitionGenerationJob(job, GENERATION_JOB_STATES.NEEDS_REVIEW, 'Generated artifact is ready for review.', {
    review_id: reviewGate?.review_id || null
  });
}

export function markGenerationJobApproved(job, reviewGate) {
  if (!job || job.state !== GENERATION_JOB_STATES.NEEDS_REVIEW) {
    return job;
  }

  return transitionGenerationJob(job, GENERATION_JOB_STATES.APPROVED, 'Review gate approved generated artifact.', {
    review_id: reviewGate?.review_id || null
  });
}

export function markGenerationJobExported(job, saveManifest) {
  if (!job || job.state !== GENERATION_JOB_STATES.APPROVED) {
    return job;
  }

  return transitionGenerationJob(job, GENERATION_JOB_STATES.EXPORTED, 'Approved artifact save/export manifest created.', {
    save_id: saveManifest?.save_id || null,
    destination_path: saveManifest?.destination_path || null
  });
}

export function markGenerationJobSuperseded(job, supersededByJobId) {
  if (!job || TERMINAL_JOB_STATES.includes(job.state) && job.state === GENERATION_JOB_STATES.SUPERSEDED) {
    return job;
  }

  const allowed = canTransitionGenerationJob(job.state, GENERATION_JOB_STATES.SUPERSEDED);
  if (!allowed) {
    return {
      ...job,
      state: GENERATION_JOB_STATES.SUPERSEDED,
      superseded_by_job_id: supersededByJobId,
      events: [
        ...(job.events || []),
        createGenerationJobEvent({
          fromState: job.state,
          toState: GENERATION_JOB_STATES.SUPERSEDED,
          reason: 'Job superseded by a newer generation request.',
          metadata: { superseded_by_job_id: supersededByJobId }
        })
      ],
      updated_at: nowIso()
    };
  }

  return {
    ...transitionGenerationJob(job, GENERATION_JOB_STATES.SUPERSEDED, 'Job superseded by a newer generation request.', {
      superseded_by_job_id: supersededByJobId
    }),
    superseded_by_job_id: supersededByJobId
  };
}

export function createRetryGenerationJob(failedJob, nextJob) {
  if (!failedJob || !nextJob) {
    return nextJob;
  }

  return {
    ...nextJob,
    retry_of_job_id: failedJob.job_id,
    attempt: (failedJob.attempt || 1) + 1,
    events: [
      ...(nextJob.events || []),
      createGenerationJobEvent({
        fromState: null,
        toState: nextJob.state,
        reason: 'Retry generation job created.',
        metadata: {
          retry_of_job_id: failedJob.job_id,
          attempt: (failedJob.attempt || 1) + 1
        }
      })
    ]
  };
}

export function getActiveGenerationJob(history) {
  return (history || []).find((job) => !TERMINAL_JOB_STATES.includes(job.state)) || null;
}

export function getGenerationJobsForProject(history, projectSlug) {
  return (history || []).filter((job) => job.project_slug === projectSlug);
}

export function summarizeGenerationJobHistory(history) {
  const jobs = history || [];

  return {
    total: jobs.length,
    active: jobs.filter((job) => !TERMINAL_JOB_STATES.includes(job.state)).length,
    failed: jobs.filter((job) => job.state === GENERATION_JOB_STATES.FAILED).length,
    approved: jobs.filter((job) => job.state === GENERATION_JOB_STATES.APPROVED).length,
    exported: jobs.filter((job) => job.state === GENERATION_JOB_STATES.EXPORTED).length,
    superseded: jobs.filter((job) => job.state === GENERATION_JOB_STATES.SUPERSEDED).length
  };
}
