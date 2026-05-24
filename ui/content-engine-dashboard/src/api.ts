export type ProjectSummary = {
  projectId: string;
  displayTitle: string;
  status: string;
  rootPath: string;
  supportedGenerationTypes: string[];
  exportTargets: string[];
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

const supportedGenerationTypes = [
  'idea-intake',
  'production-package',
  'screenplay-scene',
  'storyboard-pack',
  'visual-prompt-pack',
  'voice-script',
  'video-package',
  'pitch-package'
];

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
  return value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

export async function createProjectScaffold(request: ProjectScaffoldRequest): Promise<ProjectScaffold> {
  const projectId = createSlug(request.projectId || request.displayTitle);
  const rootPath = `projects/${projectId}`;
  const folders = [
    'canon',
    'characters',
    'story',
    'manuscript',
    'storyboards',
    'visual-bible',
    'screenplay',
    'movie-generation',
    'audio',
    'pitch',
    'reports'
  ];

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
      {
        artifactType: 'project-manifest',
        path: `${rootPath}/project.json`,
        state: 'planned',
        description: 'Project metadata and registry entry seed.'
      },
      {
        artifactType: 'idea-intake',
        path: `${rootPath}/story/idea-intake.md`,
        state: 'planned',
        description: 'Raw concept capture before canon promotion.'
      },
      {
        artifactType: 'canon-seed',
        path: `${rootPath}/canon/canon-seed.md`,
        state: 'planned',
        description: 'Initial reviewed world rules and continuity facts.'
      },
      {
        artifactType: 'character-seed',
        path: `${rootPath}/characters/character-seed.md`,
        state: 'planned',
        description: 'Initial character list and development notes.'
      },
      {
        artifactType: 'readiness-checklist',
        path: `${rootPath}/reports/readiness-checklist.md`,
        state: 'planned',
        description: 'Checklist showing what remains before project readiness reaches 100%.'
      }
    ],
    nextSteps: ['Load idea intake', 'Add canon seed', 'Add character seed', 'Generate outline', 'Run readiness check']
  };
}

export function appendMockProject(project: ProjectSummary): void {
  if (!mockProjects.some((existing) => existing.projectId === project.projectId)) {
    mockProjects.push(project);
  }
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
