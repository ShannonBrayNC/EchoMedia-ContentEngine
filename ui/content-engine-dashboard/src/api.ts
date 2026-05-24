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
