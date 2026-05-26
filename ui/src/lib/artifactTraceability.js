function compactTimestamp(value = new Date().toISOString()) {
  return value.replace(/[^0-9]/g, '').slice(0, 14);
}

function safeSlug(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 64) || 'trace';
}

export function createSceneCardTraceability({
  project,
  draftArtifact,
  generationJob,
  reviewGate,
  destinationPath,
  sourceNotes
}) {
  const createdAt = new Date().toISOString();
  const traceId = `${safeSlug(project?.slug)}-${safeSlug(draftArtifact?.artifact_id)}-trace-${compactTimestamp(createdAt)}`;

  return {
    trace_id: traceId,
    version: '0.1.0',
    artifact: {
      artifact_id: draftArtifact?.artifact_id || '',
      artifact_type: draftArtifact?.artifact_type || 'scene-card',
      title: draftArtifact?.title || '',
      status: draftArtifact?.status || 'draft',
      destination_path: destinationPath || ''
    },
    project: {
      slug: project?.slug || '',
      title: project?.title || '',
      root_path: project?.root_path || '',
      series: project?.series || '',
      universe: project?.universe || ''
    },
    source_context: {
      source_refs: draftArtifact?.source_refs || [],
      active_canon_files: project?.active_canon_files || [],
      source_notes: sourceNotes?.trim() || '',
      artifact_paths: project?.artifact_paths || {}
    },
    generation: {
      job_id: generationJob?.job_id || draftArtifact?.generation_job_id || '',
      action: generationJob?.action || 'generate-draft',
      state: generationJob?.state || 'unknown',
      created_at: generationJob?.created_at || null,
      updated_at: generationJob?.updated_at || null
    },
    review: {
      review_id: reviewGate?.review_id || '',
      state: reviewGate?.state || 'pending-review',
      source_job_id: reviewGate?.source_job_id || generationJob?.job_id || '',
      reviewed_at: reviewGate?.reviewed_at || null
    },
    downstream_ready: {
      storyboard: Boolean(draftArtifact?.shots?.length),
      video_prompt: Boolean(draftArtifact?.shots?.some((shot) => shot.visual_prompt)),
      audio_script: Boolean(draftArtifact?.dialogue_or_narration)
    },
    warnings: [],
    blockers: [],
    created_at: createdAt,
    updated_at: createdAt
  };
}

export function validateSceneCardTraceability(traceability) {
  const warnings = [];
  const blockers = [];

  if (!traceability?.project?.slug) {
    blockers.push('Traceability is missing project slug.');
  }

  if (!traceability?.artifact?.artifact_id) {
    blockers.push('Traceability is missing artifact id.');
  }

  if (!traceability?.generation?.job_id) {
    blockers.push('Traceability is missing generation job id.');
  }

  if (!traceability?.review?.review_id) {
    blockers.push('Traceability is missing review gate id.');
  }

  if (!traceability?.source_context?.source_refs?.length) {
    warnings.push('Traceability has no explicit source references.');
  }

  if (!traceability?.source_context?.active_canon_files?.length) {
    warnings.push('Traceability has no active canon files yet.');
  }

  if (!traceability?.artifact?.destination_path) {
    blockers.push('Traceability is missing destination path.');
  }

  return {
    status: blockers.length ? 'blocked' : warnings.length ? 'warning' : 'passed',
    warnings,
    blockers
  };
}

export function attachTraceabilityValidation(traceability) {
  const validation = validateSceneCardTraceability(traceability);
  const updatedAt = new Date().toISOString();

  return {
    ...traceability,
    warnings: validation.warnings,
    blockers: validation.blockers,
    validation_status: validation.status,
    updated_at: updatedAt
  };
}

export function refreshTraceabilityReview(traceability, reviewGate) {
  if (!traceability) {
    return null;
  }

  return attachTraceabilityValidation({
    ...traceability,
    review: {
      ...traceability.review,
      review_id: reviewGate?.review_id || traceability.review?.review_id || '',
      state: reviewGate?.state || traceability.review?.state || 'unknown',
      source_job_id: reviewGate?.source_job_id || traceability.review?.source_job_id || '',
      reviewed_at: reviewGate?.reviewed_at || traceability.review?.reviewed_at || null
    },
    updated_at: new Date().toISOString()
  });
}

export function attachSaveManifestToTraceability(traceability, saveManifest) {
  if (!traceability) {
    return null;
  }

  return attachTraceabilityValidation({
    ...traceability,
    save: saveManifest
      ? {
          save_id: saveManifest.save_id,
          destination_path: saveManifest.destination_path,
          saved_at: saveManifest.saved_at,
          persistence_mode: saveManifest.persistence_mode
        }
      : null,
    updated_at: new Date().toISOString()
  });
}

export function traceabilityHasBlockers(traceability) {
  return Boolean(traceability?.blockers?.length);
}
