export type ProjectSummary = {
  projectId: string;
  displayTitle: string;
  status: string;
  rootPath: string;
  supportedGenerationTypes: string[];
  exportTargets: string[];
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

const mockProjects: ProjectSummary[] = [
  {
    projectId: 'lantern-protocol',
    displayTitle: 'Lantern Protocol',
    status: 'active',
    rootPath: 'projects/lantern-protocol',
    supportedGenerationTypes: [
      'production-package',
      'screenplay-scene',
      'storyboard-pack',
      'visual-prompt-pack',
      'voice-script',
      'video-package',
      'pitch-package'
    ],
    exportTargets: ['generic-json', 'openai-video', 'runway', 'luma', 'elevenlabs', 'azure-speech', 'openai-audio']
  },
  {
    projectId: 'sovereign-exception',
    displayTitle: 'The Sovereign Exception',
    status: 'planning',
    rootPath: 'projects/sovereign-exception',
    supportedGenerationTypes: ['production-package', 'screenplay-scene', 'video-package', 'pitch-package'],
    exportTargets: ['generic-json', 'openai-video', 'runway']
  }
];

export async function listProjects(): Promise<ProjectSummary[]> {
  return mockProjects;
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
