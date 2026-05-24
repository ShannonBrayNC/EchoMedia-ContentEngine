export type ProjectSummary = {
  projectId: string;
  displayTitle: string;
  status: string;
  rootPath: string;
  supportedGenerationTypes: string[];
  exportTargets: string[];
};

export type WorkflowStep = {
  artifactType: string;
  order: number;
  label: string;
  description: string;
};

export type ReadinessCategory = 'structure' | 'content' | 'export';

export type ReadinessItem = {
  id: string;
  category: ReadinessCategory;
  label: string;
  complete: boolean;
  status: 'complete' | 'missing' | 'needs-review' | 'blocked';
  nextAction: string;
  targetArtifact?: string;
};

export type ProjectReadiness = {
  projectId: string;
  percent: number;
  summary: string;
  items: ReadinessItem[];
  blockers: string[];
  nextBestAction: string;
};

export type ArtifactInventoryCategory =
  | 'idea intake'
  | 'canon'
  | 'characters'
  | 'story outline'
  | 'manuscript'
  | 'screenplay'
  | 'production package'
  | 'visual prompts'
  | 'voice packages'
  | 'timelines'
  | 'export manifests'
  | 'release package';

export type ArtifactInventoryItem = {
  artifactId: string;
  label: string;
  category: ArtifactInventoryCategory;
  artifactType: string;
  state: 'missing' | 'planned' | 'draft' | 'review' | 'approved' | 'exported' | 'released' | 'stale' | 'superseded';
  required: boolean;
  path: string;
  readinessImpact: string;
  actions: Array<'preview' | 'review' | 'generate' | 'regenerate' | 'export'>;
};

export type ProjectArtifactInventory = {
  projectId: string;
  items: ArtifactInventoryItem[];
  requiredCount: number;
  completeRequiredCount: number;
  summary: string;
};

export type ProjectScaffoldRequest = {
  displayTitle: string;
  projectId: string;
  universe: string;
  storyType: string;
  targetFormats: string[];
};

export type ProjectScaffold = {
  project: ProjectSummary;
  folders: string[];
  starterArtifacts: Array<{ artifactType: string; path: string; state: string; description: string }>;
  nextSteps: string[];
};

export type IdeaIntakeRequest = {
  projectId: string;
  rawInput: string;
  direction: string;
};

export type IdeaIntake = {
  intakeId: string;
  projectId: string;
  state: 'draft' | 'review' | 'approved' | 'rejected';
  summary: string;
  genreCandidates: string[];
  toneCandidates: string[];
  themeCandidates: string[];
  characterCandidates: string[];
  canonCandidates: string[];
  storyArcCandidates: string[];
  artifactRoadmap: string[];
  nextSteps: string[];
  preview: string;
};

export type JobStatus =
  | 'draft-request'
  | 'queued'
  | 'generating'
  | 'generated'
  | 'needs-review'
  | 'approved'
  | 'exported'
  | 'failed'
  | 'cancelled'
  | 'superseded';

export type GenerationJob = {
  jobId: string;
  projectId: string;
  artifactType: string;
  status: JobStatus;
  progress: number;
  artifactIds: string[];
  warnings: string[];
  correlationId: string;
};

export type ArtifactSummary = {
  artifactId: string;
  projectId: string;
  artifactType: string;
  state: string;
  path: string;
  manifestId: string;
  preview: string;
};

export type CreateGenerationJobRequest = {
  projectId: string;
  artifactType: string;
  userDirection: string;
  templateId?: string;
  exportProfileId?: string;
  dryRun: boolean;
};

export const workflowSteps: WorkflowStep[] = [
  { artifactType: 'idea-intake', order: 1, label: 'Idea Intake', description: 'Capture rough story material before canon decisions.' },
  { artifactType: 'production-package', order: 2, label: 'Production Package', description: 'Create the structured package that downstream tools share.' },
  { artifactType: 'screenplay-scene', order: 3, label: 'Screenplay Scene', description: 'Turn story intent into scene-ready script material.' },
  { artifactType: 'storyboard-pack', order: 4, label: 'Storyboard Pack', description: 'Plan shots, beats, and visual sequence.' },
  { artifactType: 'visual-prompt-pack', order: 5, label: 'Visual Prompt Pack', description: 'Prepare image/video generation prompts.' },
  { artifactType: 'voice-script', order: 6, label: 'Voice Script', description: 'Prepare narration and dialogue voice assets.' },
  { artifactType: 'video-package', order: 7, label: 'Video Package', description: 'Prepare provider-ready video generation package.' },
  { artifactType: 'pitch-package', order: 8, label: 'Pitch Package', description: 'Package approved outputs for presentation.' }
];

export function getWorkflowStep(artifactType: string): WorkflowStep | undefined {
  return workflowSteps.find((step) => step.artifactType === artifactType);
}

const supportedGenerationTypes = workflowSteps.map((step) => step.artifactType);

const mockProjects: ProjectSummary[] = [
  {
    projectId: 'lantern-protocol',
    displayTitle: 'Lantern Protocol',
    status: 'active',
    rootPath: 'projects/lantern-protocol',
    supportedGenerationTypes,
    exportTargets: ['generic-json', 'openai-video', 'runway', 'luma', 'elevenlabs', 'azure-speech', 'openai-audio']
  },
  {
    projectId: 'sovereign-exception',
    displayTitle: 'The Sovereign Exception',
    status: 'planning',
    rootPath: 'projects/sovereign-exception',
    supportedGenerationTypes: ['idea-intake', 'production-package', 'screenplay-scene', 'video-package', 'pitch-package'],
    exportTargets: ['generic-json', 'openai-video', 'runway']
  }
];

export async function listProjects(): Promise<ProjectSummary[]> {
  return mockProjects;
}

export function createSlug(value: string): string {
  return value.toLowerCase().trim().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

export async function getProjectReadiness(projectId: string, hasScaffold: boolean, hasIdeaIntake: boolean, hasApprovedArtifact: boolean): Promise<ProjectReadiness> {
  const items: ReadinessItem[] = [
    { id: 'project-metadata', category: 'structure', label: 'Project metadata', complete: Boolean(projectId), status: projectId ? 'complete' : 'missing', nextAction: 'Create project scaffold', targetArtifact: 'project-manifest' },
    { id: 'folder-structure', category: 'structure', label: 'Folder structure', complete: hasScaffold, status: hasScaffold ? 'complete' : 'missing', nextAction: 'Create project scaffold', targetArtifact: 'project-scaffold' },
    { id: 'idea-intake', category: 'content', label: 'Idea intake', complete: hasIdeaIntake, status: hasIdeaIntake ? 'needs-review' : 'missing', nextAction: hasIdeaIntake ? 'Review idea intake draft' : 'Load ideas', targetArtifact: 'idea-intake' },
    { id: 'canon-seed', category: 'content', label: 'Canon seed', complete: false, status: 'missing', nextAction: 'Promote reviewed idea facts to canon seed', targetArtifact: 'canon-seed' },
    { id: 'character-seed', category: 'content', label: 'Character seed', complete: false, status: 'missing', nextAction: 'Generate character seed from idea intake', targetArtifact: 'character-seed' },
    { id: 'story-outline', category: 'content', label: 'Story outline', complete: false, status: 'missing', nextAction: 'Generate story outline', targetArtifact: 'story-outline' },
    { id: 'production-package', category: 'content', label: 'Production package schema', complete: hasApprovedArtifact, status: hasApprovedArtifact ? 'complete' : 'missing', nextAction: 'Generate and approve production package', targetArtifact: 'production-package' },
    { id: 'voice-readiness', category: 'export', label: 'Voice package readiness', complete: false, status: 'missing', nextAction: 'Create voice package', targetArtifact: 'voice-script' },
    { id: 'visual-readiness', category: 'export', label: 'Visual package readiness', complete: false, status: 'missing', nextAction: 'Create visual prompt pack', targetArtifact: 'visual-prompt-pack' },
    { id: 'export-profile', category: 'export', label: 'Export profile readiness', complete: false, status: 'missing', nextAction: 'Select export profile', targetArtifact: 'export-profile' },
    { id: 'review-approval', category: 'export', label: 'Review and approval status', complete: hasApprovedArtifact, status: hasApprovedArtifact ? 'complete' : 'needs-review', nextAction: 'Approve required draft artifacts', targetArtifact: 'review' }
  ];

  const completeCount = items.filter((item) => item.complete).length;
  const percent = Math.round((completeCount / items.length) * 100);
  const firstIncomplete = items.find((item) => !item.complete);
  const blockers = items.filter((item) => item.status === 'blocked').map((item) => item.label);

  return {
    projectId,
    percent,
    summary: `${completeCount} of ${items.length} readiness items complete.`,
    items,
    blockers,
    nextBestAction: firstIncomplete?.nextAction ?? 'All readiness items are complete. Begin release-readiness review.'
  };
}

export async function getProjectArtifactInventory(projectId: string, hasScaffold: boolean, hasIdeaIntake: boolean, approvedArtifact?: ArtifactSummary | null): Promise<ProjectArtifactInventory> {
  const rootPath = mockProjects.find((project) => project.projectId === projectId)?.rootPath ?? `projects/${projectId}`;
  const items: ArtifactInventoryItem[] = [
    { artifactId: 'artifact-project-manifest', label: 'Project manifest', category: 'canon', artifactType: 'project-manifest', state: hasScaffold ? 'planned' : 'missing', required: true, path: `${rootPath}/project.json`, readinessImpact: 'Required for structure readiness.', actions: hasScaffold ? ['preview'] : ['generate'] },
    { artifactId: 'artifact-idea-intake', label: 'Idea intake', category: 'idea intake', artifactType: 'idea-intake', state: hasIdeaIntake ? 'review' : 'missing', required: true, path: `${rootPath}/story/idea-intake.md`, readinessImpact: 'Required before canon, characters, and outline work.', actions: hasIdeaIntake ? ['preview', 'review', 'regenerate'] : ['generate'] },
    { artifactId: 'artifact-canon-seed', label: 'Canon seed', category: 'canon', artifactType: 'canon-seed', state: 'missing', required: true, path: `${rootPath}/canon/canon-seed.md`, readinessImpact: 'Required before continuity-safe generation.', actions: ['generate'] },
    { artifactId: 'artifact-character-seed', label: 'Character seed', category: 'characters', artifactType: 'character-seed', state: 'missing', required: true, path: `${rootPath}/characters/character-seed.md`, readinessImpact: 'Required for dialogue, voice, and scene planning.', actions: ['generate'] },
    { artifactId: 'artifact-story-outline', label: 'Story outline', category: 'story outline', artifactType: 'story-outline', state: 'missing', required: true, path: `${rootPath}/story/story-outline.md`, readinessImpact: 'Required before screenplay and storyboard generation.', actions: ['generate'] },
    { artifactId: 'artifact-manuscript', label: 'Manuscript draft', category: 'manuscript', artifactType: 'manuscript', state: 'missing', required: false, path: `${rootPath}/manuscript/`, readinessImpact: 'Optional for screenplay-first projects.', actions: ['generate'] },
    { artifactId: 'artifact-screenplay', label: 'Screenplay scene package', category: 'screenplay', artifactType: 'screenplay-scene', state: 'missing', required: true, path: `${rootPath}/screenplay/`, readinessImpact: 'Required before cinematic video planning.', actions: ['generate'] },
    { artifactId: 'artifact-production-package', label: 'Production package', category: 'production package', artifactType: 'production-package', state: approvedArtifact?.artifactType === 'production-package' ? 'approved' : 'missing', required: true, path: `${rootPath}/movie-generation/production-package.json`, readinessImpact: 'Required for provider-ready output.', actions: approvedArtifact?.artifactType === 'production-package' ? ['preview', 'review', 'export'] : ['generate'] },
    { artifactId: 'artifact-visual-prompts', label: 'Visual prompt pack', category: 'visual prompts', artifactType: 'visual-prompt-pack', state: 'missing', required: true, path: `${rootPath}/visual-bible/visual-prompt-pack.json`, readinessImpact: 'Required before image/video provider packages.', actions: ['generate'] },
    { artifactId: 'artifact-voice-package', label: 'Voice package', category: 'voice packages', artifactType: 'voice-script', state: 'missing', required: true, path: `${rootPath}/audio/voice-package.json`, readinessImpact: 'Required before audio generation.', actions: ['generate'] },
    { artifactId: 'artifact-timeline', label: 'Scene timeline', category: 'timelines', artifactType: 'scene-timeline', state: 'missing', required: true, path: `${rootPath}/timelines/`, readinessImpact: 'Required before audio/video synchronization.', actions: ['generate'] },
    { artifactId: 'artifact-export-manifest', label: 'Export manifest', category: 'export manifests', artifactType: 'export-manifest', state: 'missing', required: true, path: `${rootPath}/provider-manifests/`, readinessImpact: 'Required before external provider handoff.', actions: ['export'] },
    { artifactId: 'artifact-release-package', label: 'Release package', category: 'release package', artifactType: 'release-package', state: 'missing', required: false, path: `${rootPath}/release/`, readinessImpact: 'Created after final approval and rights review.', actions: ['export'] }
  ];
  const requiredItems = items.filter((item) => item.required);
  const completeRequiredCount = requiredItems.filter((item) => ['review', 'approved', 'exported', 'released', 'planned'].includes(item.state)).length;
  return {
    projectId,
    items,
    requiredCount: requiredItems.length,
    completeRequiredCount,
    summary: `${completeRequiredCount} of ${requiredItems.length} required artifacts are present or planned.`
  };
}

export async function createProjectScaffold(request: ProjectScaffoldRequest): Promise<ProjectScaffold> {
  const projectId = createSlug(request.projectId || request.displayTitle);
  const rootPath = `projects/${projectId}`;
  const folders = ['canon', 'characters', 'story', 'manuscript', 'storyboards', 'visual-bible', 'screenplay', 'movie-generation', 'audio', 'pitch', 'reports'];
  const project: ProjectSummary = {
    projectId,
    displayTitle: request.displayTitle,
    status: 'planning',
    rootPath,
    supportedGenerationTypes,
    exportTargets: request.targetFormats.length ? request.targetFormats : ['generic-json']
  };
  return {
    project,
    folders: folders.map((folder) => `${rootPath}/${folder}/`),
    starterArtifacts: [
      { artifactType: 'project-manifest', path: `${rootPath}/project.json`, state: 'planned', description: 'Project metadata and registry entry seed.' },
      { artifactType: 'idea-intake', path: `${rootPath}/story/idea-intake.md`, state: 'planned', description: 'Raw concept capture before canon promotion.' },
      { artifactType: 'canon-seed', path: `${rootPath}/canon/canon-seed.md`, state: 'planned', description: 'Initial reviewed world rules and continuity facts.' },
      { artifactType: 'character-seed', path: `${rootPath}/characters/character-seed.md`, state: 'planned', description: 'Initial character list and development notes.' },
      { artifactType: 'readiness-checklist', path: `${rootPath}/reports/readiness-checklist.md`, state: 'planned', description: 'Checklist showing what remains before project readiness reaches 100%.' }
    ],
    nextSteps: ['Load idea intake', 'Add canon seed', 'Add character seed', 'Generate outline', 'Run readiness check']
  };
}

export function appendMockProject(project: ProjectSummary): void {
  if (!mockProjects.some((existing) => existing.projectId === project.projectId)) mockProjects.push(project);
}

export async function createIdeaIntake(request: IdeaIntakeRequest): Promise<IdeaIntake> {
  const trimmedInput = request.rawInput.trim();
  const firstSentence = trimmedInput.split(/[.!?]/).find(Boolean)?.trim() ?? 'Untitled idea';
  const directionNote = request.direction.trim() || 'No extra direction provided.';
  const intake: IdeaIntake = {
    intakeId: `idea-${Date.now()}`,
    projectId: request.projectId,
    state: 'review',
    summary: `${firstSentence}.`,
    genreCandidates: ['techno-thriller', 'political thriller', 'AI drama'],
    toneCandidates: ['cinematic', 'tense', 'grounded', 'high-stakes'],
    themeCandidates: ['consent', 'liberty', 'power', 'identity', 'trust'],
    characterCandidates: ['protagonist', 'technical operator', 'institutional antagonist', 'reluctant ally'],
    canonCandidates: ['Define the governing technology.', 'Define the political pressure system.', 'Define the personal cost.'],
    storyArcCandidates: ['inciting discovery', 'escalation through institutions', 'public/private betrayal', 'final choice with consequences'],
    artifactRoadmap: ['canon seed', 'character seed', 'story outline', 'scene cards', 'production package'],
    nextSteps: ['Review intake draft', 'Promote approved facts to canon seed', 'Generate character seed', 'Generate outline'],
    preview: ''
  };
  intake.preview = `# Idea Intake Draft\n\nProject: ${request.projectId}\n\n## Raw idea summary\n${intake.summary}\n\n## Direction\n${directionNote}\n\n## Genre candidates\n${intake.genreCandidates.map((item) => `- ${item}`).join('\n')}\n\n## Tone candidates\n${intake.toneCandidates.map((item) => `- ${item}`).join('\n')}\n\n## Theme candidates\n${intake.themeCandidates.map((item) => `- ${item}`).join('\n')}\n\n## Character candidates\n${intake.characterCandidates.map((item) => `- ${item}`).join('\n')}\n\n## Canon candidates\n${intake.canonCandidates.map((item) => `- ${item}`).join('\n')}\n\n## Story arc candidates\n${intake.storyArcCandidates.map((item) => `- ${item}`).join('\n')}\n\n## Artifact roadmap\n${intake.artifactRoadmap.map((item) => `- ${item}`).join('\n')}\n\n## Next steps\n${intake.nextSteps.map((item) => `- ${item}`).join('\n')}\n\nDraft only. Nothing is promoted to canon until reviewed.`;
  return intake;
}

export async function validateGenerationRequest(request: CreateGenerationJobRequest): Promise<string[]> {
  const warnings: string[] = [];
  if (!request.projectId) warnings.push('Select a project before validating.');
  if (!request.artifactType) warnings.push('Select an artifact type before validating.');
  if (!request.userDirection.trim()) warnings.push('Add generation direction so the job has a clear creative target.');
  if (request.dryRun) warnings.push('Dry-run mode is enabled. No live provider will be called.');
  return warnings;
}

export async function createGenerationJob(request: CreateGenerationJobRequest): Promise<GenerationJob> {
  return {
    jobId: `job-${Date.now()}`,
    projectId: request.projectId,
    artifactType: request.artifactType,
    status: 'needs-review',
    progress: 100,
    artifactIds: [`artifact-${Date.now()}`],
    warnings: request.dryRun ? ['Generated with mock API in dry-run mode.'] : [],
    correlationId: `trace-${Date.now()}`
  };
}

export async function getArtifactPreview(job: GenerationJob): Promise<ArtifactSummary> {
  return {
    artifactId: job.artifactIds[0] ?? 'artifact-preview',
    projectId: job.projectId,
    artifactType: job.artifactType,
    state: 'review',
    path: `.content-engine/drafts/${job.jobId}.md`,
    manifestId: `manifest-${job.jobId}`,
    preview: `# Draft ${job.artifactType}\n\nProject: ${job.projectId}\n\nThis is a dry-run preview artifact. It follows the Sprint 2 job model and is waiting for review before export or save.`
  };
}

export async function approveArtifact(artifactId: string): Promise<{ artifactId: string; state: string }> {
  return { artifactId, state: 'approved' };
}

export async function rejectArtifact(artifactId: string): Promise<{ artifactId: string; state: string }> {
  return { artifactId, state: 'rejected' };
}
