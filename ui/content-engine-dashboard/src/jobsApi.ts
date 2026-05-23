const API_BASE = import.meta.env.VITE_CONTENT_ENGINE_API_URL || 'http://localhost:8000';

export type JobSummary = {
  job_id: string;
  workflow: string;
  state: string;
  project_id?: string;
  priority?: number;
  created_at?: string;
  updated_at?: string;
};

export async function listJobs(state?: string): Promise<JobSummary[]> {
  const url = new URL(`${API_BASE}/jobs`);
  if (state) {
    url.searchParams.set('state', state);
  }

  const response = await fetch(url.toString(), {
    headers: {
      'X-Content-Engine-Role': 'christina',
      'X-Content-Engine-User': 'Christina',
    },
  });

  if (!response.ok) {
    throw new Error(`Job request failed: ${response.status}`);
  }

  return response.json();
}
