function compactTimestamp(value = new Date().toISOString()) {
  return value.replace(/[^0-9]/g, '').slice(0, 14);
}

function safeSlug(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 64) || 'review';
}

export function createSceneCardReviewGate({ project, draftArtifact, generationJob, destinationPath }) {
  const createdAt = new Date().toISOString();
  const reviewId = `${safeSlug(project?.slug)}-${safeSlug(draftArtifact?.artifact_type)}-review-${compactTimestamp(createdAt)}`;

  return {
    review_id: reviewId,
    version: '0.1.0',
    project_slug: project?.slug || '',
    artifact_id: draftArtifact?.artifact_id || '',
    artifact_type: draftArtifact?.artifact_type || 'scene-card',
    source_job_id: generationJob?.job_id || draftArtifact?.generation_job_id || null,
    state: 'pending-review',
    destination_path: destinationPath,
    checks: [
      {
        key: 'schema-valid',
        label: 'Draft shape present',
        status: draftArtifact ? 'passed' : 'failed',
        required: true
      },
      {
        key: 'source-context-present',
        label: 'Source references present',
        status: draftArtifact?.source_refs?.length ? 'passed' : 'failed',
        required: true
      },
      {
        key: 'generation-job-linked',
        label: 'Generation job linked',
        status: generationJob?.job_id || draftArtifact?.generation_job_id ? 'passed' : 'failed',
        required: true
      },
      {
        key: 'destination-path-valid',
        label: 'Destination path available',
        status: destinationPath ? 'passed' : 'failed',
        required: true
      },
      {
        key: 'overwrite-reviewed',
        label: 'Overwrite reviewed',
        status: 'warning',
        required: false
      }
    ],
    created_at: createdAt,
    updated_at: createdAt,
    reviewed_at: null,
    reviewer_notes: ''
  };
}

export function approveReviewGate(reviewGate, reviewerNotes = '') {
  const updatedAt = new Date().toISOString();

  return {
    ...reviewGate,
    state: 'approved',
    reviewer_notes: reviewerNotes,
    reviewed_at: updatedAt,
    updated_at: updatedAt
  };
}

export function rejectReviewGate(reviewGate, reviewerNotes = '') {
  const updatedAt = new Date().toISOString();

  return {
    ...reviewGate,
    state: 'rejected',
    reviewer_notes: reviewerNotes,
    reviewed_at: updatedAt,
    updated_at: updatedAt
  };
}

export function markReviewGateSaved(reviewGate, saveManifest) {
  const updatedAt = new Date().toISOString();

  return {
    ...reviewGate,
    state: 'saved',
    save_manifest: saveManifest,
    updated_at: updatedAt
  };
}

export function buildSceneCardSaveManifest({ project, draftArtifact, reviewGate, destinationPath, overwriteConfirmed }) {
  const savedAt = new Date().toISOString();

  return {
    save_id: `${safeSlug(project?.slug)}-${safeSlug(draftArtifact?.artifact_id)}-save-${compactTimestamp(savedAt)}`,
    project_slug: project?.slug || '',
    artifact_id: draftArtifact?.artifact_id || '',
    artifact_type: draftArtifact?.artifact_type || 'scene-card',
    review_id: reviewGate?.review_id || '',
    generation_job_id: draftArtifact?.generation_job_id || reviewGate?.source_job_id || null,
    destination_path: destinationPath,
    overwrite_confirmed: Boolean(overwriteConfirmed),
    saved_at: savedAt,
    persistence_mode: 'ui-local-manifest'
  };
}

export function reviewGateHasBlockingFailures(reviewGate) {
  return Boolean(reviewGate?.checks?.some((check) => check.required && check.status === 'failed'));
}
