function slugFragment(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 48) || 'job';
}

function createJobId({ projectSlug, artifactType, action, timestamp = new Date().toISOString() }) {
  const compactTimestamp = timestamp.replace(/[^0-9]/g, '').slice(0, 14);
  return `${slugFragment(projectSlug)}-${slugFragment(artifactType)}-${slugFragment(action)}-${compactTimestamp}`;
}

export function createSceneCardGenerationJob({
  project,
  creativeDirection,
  sourceNotes,
  contextValidation,
  destinationPath
}) {
  const createdAt = new Date().toISOString();
  const jobId = createJobId({
    projectSlug: project?.slug,
    artifactType: 'scene-card',
    action: 'generate-draft',
    timestamp: createdAt
  });

  return {
    job_id: jobId,
    version: '0.1.0',
    project_slug: project?.slug || '',
    artifact_type: 'scene-card',
    action: 'generate-draft',
    state: 'generating',
    request: {
      creative_direction: creativeDirection.trim(),
      source_notes: sourceNotes.trim(),
      destination_path: destinationPath,
      requested_at: createdAt
    },
    source_context: {
      project_title: project?.title || '',
      project_root_path: project?.root_path || '',
      active_canon_files: project?.active_canon_files || [],
      artifact_paths: project?.artifact_paths || {},
      context_validation: contextValidation || null
    },
    outputs: [],
    warnings: contextValidation?.warnings || [],
    errors: [],
    created_at: createdAt,
    updated_at: createdAt
  };
}

export function completeGenerationJob(job, draftArtifact) {
  const updatedAt = new Date().toISOString();

  return {
    ...job,
    state: 'generated',
    outputs: [
      {
        artifact_id: draftArtifact.artifact_id,
        artifact_type: draftArtifact.artifact_type,
        title: draftArtifact.title,
        status: draftArtifact.status,
        preview_only: true,
        created_at: draftArtifact.created_at
      }
    ],
    updated_at: updatedAt
  };
}

export function failGenerationJob(job, error) {
  const updatedAt = new Date().toISOString();
  const message = error instanceof Error ? error.message : String(error);

  return {
    ...job,
    state: 'failed',
    errors: [
      ...(job.errors || []),
      {
        message,
        occurred_at: updatedAt
      }
    ],
    updated_at: updatedAt
  };
}
