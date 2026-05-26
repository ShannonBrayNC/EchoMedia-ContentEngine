function slugify(value) {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 64) || 'scene-card';
}

function firstSentence(value) {
  const trimmed = value.trim();
  const match = trimmed.match(/^(.+?[.!?])\s/);
  return match ? match[1] : trimmed;
}

function buildTitle(creativeDirection) {
  const summary = firstSentence(creativeDirection);
  const cleaned = summary.replace(/^create\s+/i, '').replace(/^a\s+/i, '').trim();
  const title = cleaned.length > 80 ? `${cleaned.slice(0, 77)}...` : cleaned;
  return title || 'Draft Scene Card';
}

function buildSceneId(project, creativeDirection) {
  const titleSlug = slugify(buildTitle(creativeDirection));
  return `${project.slug}-scene-${titleSlug}`;
}

function buildSourceRefs(project, sourceNotes) {
  const refs = [
    {
      type: 'story',
      path: project.artifact_paths?.story || project.root_path,
      summary: 'Project story folder selected as first-slice source context.'
    }
  ];

  if (project.active_canon_files?.length) {
    for (const canonPath of project.active_canon_files) {
      refs.push({
        type: 'canon',
        path: canonPath,
        summary: 'Active project canon reference.'
      });
    }
  }

  if (sourceNotes.trim()) {
    refs.push({
      type: 'external-note',
      path: 'workspace/source-notes',
      summary: sourceNotes.trim()
    });
  }

  return refs;
}

export function buildSceneCardDraft({ project, creativeDirection, sourceNotes, generationJobId }) {
  if (!project) {
    throw new Error('Project is required to build a scene-card draft.');
  }

  if (!creativeDirection?.trim()) {
    throw new Error('Creative direction is required to build a scene-card draft.');
  }

  const now = new Date().toISOString();
  const title = buildTitle(creativeDirection);
  const sceneId = buildSceneId(project, creativeDirection);
  const sourceRefs = buildSourceRefs(project, sourceNotes || '');

  return {
    artifact_type: 'scene-card',
    artifact_id: sceneId,
    generation_job_id: generationJobId || null,
    status: 'draft',
    created_at: now,
    project: {
      slug: project.slug,
      title: project.title,
      root_path: project.root_path,
      universe: project.universe,
      series: project.series
    },
    scene_id: sceneId,
    title,
    purpose: 'Create a focused scene-card draft that can be reviewed, expanded, and later converted into storyboard or AI video production packages.',
    summary: creativeDirection.trim(),
    location: 'TBD during review',
    characters: [],
    source_refs: sourceRefs,
    visual_notes: sourceNotes?.trim() || 'No additional visual notes supplied yet.',
    dialogue_or_narration: 'TBD during review',
    shots: [
      {
        shot_id: `${sceneId}-shot-001`,
        description: `Opening image for: ${title}`,
        camera: 'Establishing cinematic frame, specific camera direction to be refined during review.',
        visual_prompt: creativeDirection.trim(),
        lighting: 'TBD during review',
        motion: 'Slow, controlled motion suitable for an AI video prompt package.',
        negative_prompt: 'Avoid continuity-breaking details, unclear faces, illegible UI text, and unrelated objects.'
      }
    ],
    continuity_notes: [
      'Draft generated from registry project context and user creative direction.',
      generationJobId ? `Generation job: ${generationJobId}` : 'Generation job metadata was not attached.',
      'Requires review before save or export.',
      'Character, canon, and visual-bible details should be expanded in later implementation slices.'
    ]
  };
}

export function renderSceneCardDraftMarkdown(draft) {
  const lines = [
    `# ${draft.title}`,
    '',
    `Artifact Type: ${draft.artifact_type}`,
    `Artifact ID: ${draft.artifact_id}`,
    `Generation Job ID: ${draft.generation_job_id || 'not attached'}`,
    `Status: ${draft.status}`,
    `Project: ${draft.project.title} (${draft.project.slug})`,
    `Created: ${draft.created_at}`,
    '',
    '## Purpose',
    '',
    draft.purpose,
    '',
    '## Summary',
    '',
    draft.summary,
    '',
    '## Location',
    '',
    draft.location,
    '',
    '## Source References',
    '',
    ...draft.source_refs.map((ref) => `- ${ref.type}: ${ref.path}${ref.summary ? ` - ${ref.summary}` : ''}`),
    '',
    '## Visual Notes',
    '',
    draft.visual_notes,
    '',
    '## Dialogue or Narration',
    '',
    draft.dialogue_or_narration,
    '',
    '## Shots',
    ''
  ];

  for (const shot of draft.shots) {
    lines.push(`### ${shot.shot_id}`);
    lines.push('');
    lines.push(`Description: ${shot.description}`);
    lines.push('');
    lines.push(`Camera: ${shot.camera}`);
    lines.push('');
    lines.push(`Visual Prompt: ${shot.visual_prompt}`);
    lines.push('');
    lines.push(`Lighting: ${shot.lighting}`);
    lines.push('');
    lines.push(`Motion: ${shot.motion}`);
    lines.push('');
    lines.push(`Negative Prompt: ${shot.negative_prompt}`);
    lines.push('');
  }

  lines.push('## Continuity Notes');
  lines.push('');
  for (const note of draft.continuity_notes) {
    lines.push(`- ${note}`);
  }

  return lines.join('\n');
}
