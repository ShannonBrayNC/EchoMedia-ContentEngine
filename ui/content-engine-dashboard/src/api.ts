const API_BASE = import.meta.env.VITE_CONTENT_ENGINE_API_URL || 'http://localhost:8000';

export type ApiResult = {
  ok?: boolean;
  returncode?: number;
  stdout?: string;
  stderr?: string;
  [key: string]: unknown;
};

export type SessionContext = {
  role: string;
  user: string;
  projectScope?: string;
  bearerToken?: string;
};

let sessionContext: SessionContext = {
  role: 'christina',
  user: 'Christina',
};

export function setSessionContext(context: SessionContext) {
  sessionContext = context;
}

function buildHeaders(): HeadersInit {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };

  if (sessionContext.bearerToken) {
    headers.Authorization = `Bearer ${sessionContext.bearerToken}`;
  } else {
    headers['X-Content-Engine-Role'] = sessionContext.role;
    headers['X-Content-Engine-User'] = sessionContext.user;

    if (sessionContext.projectScope) {
      headers['X-Content-Engine-Project'] = sessionContext.projectScope;
    }
  }

  return headers;
}

async function post<T extends object>(path: string, body: T): Promise<ApiResult> {
  const response = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: buildHeaders(),
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}

export async function health(): Promise<ApiResult> {
  const response = await fetch(`${API_BASE}/health`);
  return response.json();
}

export async function whoAmI(): Promise<ApiResult> {
  const response = await fetch(`${API_BASE}/auth/me`, {
    headers: buildHeaders(),
  });
  return response.json();
}

export const ContentEngineApi = {
  validateCanon: (manifestPath: string) =>
    post('/projects/validate-canon', { manifest_path: manifestPath }),

  auditContinuity: (targetPath: string, failUnder = 70) =>
    post('/projects/audit-continuity', { target_path: targetPath, fail_under: failUnder }),

  buildChapterPacket: (projectRoot: string, chapterNumber: number, chapterTitle: string) =>
    post('/projects/build-chapter-packet', {
      project_root: projectRoot,
      chapter_number: chapterNumber,
      chapter_title: chapterTitle,
    }),

  assembleScreenplay: (projectRoot: string) =>
    post('/projects/assemble-screenplay', { project_root: projectRoot }),

  buildExportPackage: (projectRoot: string, packageType = 'author-review') =>
    post('/projects/build-export-package', { project_root: projectRoot, package_type: packageType }),

  createRelease: (projectRoot: string, version: string, releaseState = 'candidate') =>
    post('/projects/create-release', {
      project_root: projectRoot,
      version,
      release_state: releaseState,
    }),
};
