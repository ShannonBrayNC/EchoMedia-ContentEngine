import { useEffect, useState } from 'react';
import { JobSummary, listJobs } from './jobsApi';

export default function JobQueuePanel() {
  const [jobs, setJobs] = useState<JobSummary[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    async function refresh() {
      try {
        const result = await listJobs();
        if (mounted) {
          setJobs(result);
        }
      } catch (err) {
        if (mounted) {
          setError(String(err));
        }
      }
    }

    refresh();
    const interval = setInterval(refresh, 5000);

    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  return (
    <div style={{ border: '1px solid #ccc', borderRadius: 12, padding: 16 }}>
      <h2>Workflow Queue</h2>

      {error && <p>{error}</p>}

      {jobs.length === 0 ? (
        <p>No active jobs.</p>
      ) : (
        <table style={{ width: '100%' }}>
          <thead>
            <tr>
              <th>Workflow</th>
              <th>State</th>
              <th>Project</th>
            </tr>
          </thead>
          <tbody>
            {jobs.map((job) => (
              <tr key={job.job_id}>
                <td>{job.workflow}</td>
                <td>{job.state}</td>
                <td>{job.project_id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
