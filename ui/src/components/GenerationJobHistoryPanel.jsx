import React from 'react';
import { summarizeGenerationJobHistory } from '../lib/generationJobHistory.js';

function formatDate(value) {
  if (!value) {
    return 'unknown';
  }

  try {
    return new Date(value).toLocaleString();
  } catch {
    return value;
  }
}

export default function GenerationJobHistoryPanel({ jobs }) {
  const summary = summarizeGenerationJobHistory(jobs);

  if (!jobs?.length) {
    return (
      <section className="rounded-2xl border border-slate-700 bg-slate-950/70 p-4 shadow-lg">
        <p className="text-xs font-semibold uppercase tracking-wide text-blue-300">Generation jobs</p>
        <h2 className="mt-1 text-lg font-semibold text-white">Job history</h2>
        <p className="mt-2 text-sm text-slate-400">No generation jobs have been created in this workspace yet.</p>
      </section>
    );
  }

  return (
    <section className="rounded-2xl border border-blue-500/30 bg-blue-500/5 p-4 shadow-lg">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-blue-300">Generation jobs</p>
          <h2 className="mt-1 text-lg font-semibold text-white">Job history</h2>
          <p className="mt-1 text-sm text-slate-400">Per-project generation state, retry context, and event breadcrumbs.</p>
        </div>
        <div className="flex flex-wrap gap-2 text-xs">
          <span className="rounded-full bg-slate-900 px-2 py-1 text-slate-300">{summary.total} total</span>
          <span className="rounded-full bg-slate-900 px-2 py-1 text-slate-300">{summary.active} active</span>
          <span className="rounded-full bg-slate-900 px-2 py-1 text-slate-300">{summary.failed} failed</span>
          <span className="rounded-full bg-slate-900 px-2 py-1 text-slate-300">{summary.exported} exported</span>
        </div>
      </div>

      <div className="mt-4 grid gap-3">
        {jobs.map((job) => (
          <article key={job.job_id} className="rounded-xl bg-slate-950/80 p-3">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p className="break-words font-mono text-sm text-slate-300">{job.job_id}</p>
                <p className="mt-1 text-xs text-slate-500">
                  {job.project_slug} · {job.artifact_type} · attempt {job.attempt || 1}
                </p>
              </div>
              <span className="rounded-full bg-blue-500/15 px-3 py-1 text-xs font-medium text-blue-300">{job.state}</span>
            </div>

            <div className="mt-3 grid gap-2 md:grid-cols-3">
              <div className="rounded-lg bg-slate-900 p-2">
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Action</p>
                <p className="mt-1 text-sm text-slate-300">{job.action}</p>
              </div>
              <div className="rounded-lg bg-slate-900 p-2">
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Outputs</p>
                <p className="mt-1 text-sm text-slate-300">{job.outputs?.length || 0}</p>
              </div>
              <div className="rounded-lg bg-slate-900 p-2">
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Updated</p>
                <p className="mt-1 text-sm text-slate-300">{formatDate(job.updated_at)}</p>
              </div>
            </div>

            {job.request?.creative_direction ? (
              <p className="mt-3 rounded-lg bg-slate-900 p-2 text-sm text-slate-300">{job.request.creative_direction}</p>
            ) : null}

            {job.errors?.length ? (
              <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-red-200">
                {job.errors.map((error) => (
                  <li key={`${job.job_id}-${error.message}-${error.occurred_at}`}>{error.message}</li>
                ))}
              </ul>
            ) : null}

            {job.events?.length ? (
              <details className="mt-3 rounded-lg bg-slate-900 p-2 text-sm text-slate-300">
                <summary className="cursor-pointer text-slate-400">State events</summary>
                <ol className="mt-2 list-decimal space-y-2 pl-5">
                  {job.events.map((event, index) => (
                    <li key={`${job.job_id}-${event.to_state}-${event.occurred_at}-${index}`}>
                      <span className="font-mono text-xs text-blue-300">{event.from_state || 'start'} → {event.to_state}</span>
                      <span className="text-slate-500"> · {formatDate(event.occurred_at)}</span>
                      <p className="mt-1 text-xs text-slate-400">{event.reason}</p>
                    </li>
                  ))}
                </ol>
              </details>
            ) : null}
          </article>
        ))}
      </div>
    </section>
  );
}
