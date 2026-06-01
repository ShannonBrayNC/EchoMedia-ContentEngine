export type EmasDashboard = {
  project: string;
  ad: string;
  status: string;
  format: string;
  durationSeconds: number;
  tabs: string[];
  counts: {
    references: number;
    approvedReferences: number;
    scenes: number;
    frames: number;
    approvedFrames: number;
    approvedAudio: number;
    exports: number;
  };
  missingAssets: string[];
  nextBestAction: string;
  paths: Record<string, string>;
};

export type EmasAsset = {
  asset_id: string;
  filename: string;
  original_filename: string;
  source_path: string;
  approved: boolean;
  approval_state: string;
  tags: string[];
  outfit?: string | null;
  expression?: string | null;
  pose?: string | null;
  scene_candidates: string[];
  quality_score?: number | null;
  notes?: string;
  uploaded_at?: string;
  updated_at?: string;
};

export type EmasFrame = {
  frame_id: string;
  scene_id: string;
  filename: string;
  path: string;
  state: 'pending' | 'approved' | 'rejected' | string;
  submitted_by: string;
  submitted_at: string;
  reviewed_by?: string | null;
  reviewed_at?: string | null;
  notes?: string;
};

export type EmasPreflightResult = {
  allowed: boolean;
  reasons: string[];
  normalizedPrompt: string;
  sourceRegistryVerified: boolean;
};

export type EmasPublishResult = {
  published: boolean;
  outputId: string;
  state: string;
  packagePath: string;
  manifestPath: string;
  captionPath?: string | null;
  auditEventId: string;
};

const env = (import.meta as ImportMeta & { env?: Record<string, string> }).env ?? {};
export const EMAS_API_BASE_URL = env.VITE_EMAS_API_BASE_URL || 'http://127.0.0.1:8081';

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${EMAS_API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'content-type': 'application/json',
      ...(options.headers ?? {})
    }
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = data?.error?.message || `EMAS request failed with ${response.status}`;
    throw new Error(message);
  }
  return data as T;
}

function adPath(projectName: string, adName: string) {
  return `/api/ad-studio/projects/${encodeURIComponent(projectName)}/ads/${encodeURIComponent(adName)}`;
}

export async function createEmasAdProject(input: { projectName: string; adName: string; actor: string; force?: boolean }) {
  return request<{ created: boolean; adPath: string; warnings: string[] }>(`/api/ad-studio/projects/${encodeURIComponent(input.projectName)}/ads`, {
    method: 'POST',
    body: JSON.stringify({ adName: input.adName, actor: input.actor, force: Boolean(input.force) })
  });
}

export async function getEmasDashboard(projectName: string, adName: string) {
  return request<EmasDashboard>(`${adPath(projectName, adName)}/dashboard`);
}

export async function listEmasReferences(projectName: string, adName: string) {
  return request<{ project: string; ad: string; assets: EmasAsset[]; count: number }>(`${adPath(projectName, adName)}/references`);
}

export async function uploadEmasReference(input: {
  projectName: string;
  adName: string;
  sourcePath: string;
  actor: string;
  tags: string[];
  outfit?: string;
  expression?: string;
  pose?: string;
  sceneCandidates?: string[];
  qualityScore?: number;
  notes?: string;
}) {
  return request<{ asset: EmasAsset }>(`${adPath(input.projectName, input.adName)}/references`, {
    method: 'POST',
    body: JSON.stringify({
      sourcePath: input.sourcePath,
      actor: input.actor,
      tags: input.tags,
      outfit: input.outfit,
      expression: input.expression,
      pose: input.pose,
      sceneCandidates: input.sceneCandidates ?? [],
      qualityScore: input.qualityScore,
      notes: input.notes ?? ''
    })
  });
}

export async function tagEmasReference(input: {
  projectName: string;
  adName: string;
  assetId: string;
  actor: string;
  tags: string[];
  approved?: boolean;
  outfit?: string;
  expression?: string;
  pose?: string;
  notes?: string;
}) {
  return request<{ asset: EmasAsset }>(`${adPath(input.projectName, input.adName)}/references/${encodeURIComponent(input.assetId)}/tag`, {
    method: 'POST',
    body: JSON.stringify({
      actor: input.actor,
      tags: input.tags,
      approved: input.approved,
      outfit: input.outfit,
      expression: input.expression,
      pose: input.pose,
      notes: input.notes
    })
  });
}

export async function listEmasFrames(projectName: string, adName: string) {
  return request<{ project: string; ad: string; frames: EmasFrame[]; count: number }>(`${adPath(projectName, adName)}/storyboard/frames`);
}

export async function submitEmasFrame(input: { projectName: string; adName: string; sourcePath: string; sceneId: string; actor: string; notes?: string }) {
  return request<{ frame: EmasFrame }>(`${adPath(input.projectName, input.adName)}/storyboard/frames`, {
    method: 'POST',
    body: JSON.stringify({ sourcePath: input.sourcePath, sceneId: input.sceneId, actor: input.actor, notes: input.notes ?? '' })
  });
}

export async function reviewEmasFrame(input: { projectName: string; adName: string; frameId: string; actor: string; approved: boolean; notes?: string }) {
  return request<{ frame: EmasFrame }>(`${adPath(input.projectName, input.adName)}/storyboard/frames/${encodeURIComponent(input.frameId)}/${input.approved ? 'approve' : 'reject'}`, {
    method: 'POST',
    body: JSON.stringify({ actor: input.actor, notes: input.notes ?? '' })
  });
}

export async function runEmasPreflight(input: {
  projectName: string;
  adName: string;
  actor: string;
  subjectId: string;
  intendedUse: string;
  platform: string;
  prompt: string;
  referencePaths: string[];
  outputCount: number;
}) {
  return request<EmasPreflightResult>(`${adPath(input.projectName, input.adName)}/generate/preflight`, {
    method: 'POST',
    body: JSON.stringify({
      actor: input.actor,
      subjectId: input.subjectId,
      intendedUse: input.intendedUse,
      platform: input.platform,
      prompt: input.prompt,
      referencePaths: input.referencePaths,
      outputCount: input.outputCount
    })
  });
}

export async function publishEmasOutput(input: {
  projectName: string;
  adName: string;
  outputId: string;
  actor: string;
  platform: string;
  format: string;
  intendedUse: string;
  outputMetadataPath: string;
}) {
  return request<EmasPublishResult>(`${adPath(input.projectName, input.adName)}/outputs/${encodeURIComponent(input.outputId)}/publish`, {
    method: 'POST',
    body: JSON.stringify({
      actor: input.actor,
      platform: input.platform,
      format: input.format,
      intendedUse: input.intendedUse,
      outputMetadataPath: input.outputMetadataPath
    })
  });
}
