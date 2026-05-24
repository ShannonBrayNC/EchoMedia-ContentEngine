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
