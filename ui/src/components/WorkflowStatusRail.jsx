import React, { useState } from 'react';

function countBySeverity(items = []) {
  return items.reduce(
    (counts, item) => {
      if (item.severity === 'error') {
        return { ...counts, blockers: counts.blockers + 1 };
      }

      return { ...counts, warnings: counts.warnings + 1 };
    },
    { warnings: 0, blockers: 0 }
  );
}

function compactLabel(value, fallback) {
  return value || fallback;
}

function stageProgress(rail) {
  const completed = rail?.workflow?.completed_stages?.length || 0;
  const current = rail?.workflow?.current_stage ? 1 : 0;
  return completed + current;
}

export default function WorkflowStatusRail({ rail }) {
  const [expanded, setExpanded] = useState(false);
  const projectLabel = compactLabel(rail?.project?.title, 'No project selected');
  const artifactLabel = compactLabel(rail?.artifact?.artifact_type, 'No artifact selected');
  const stageLabel = compactLabel(rail?.workflow?.current_stage, 'select-project');
  const stageStatus = compactLabel(rail?.workflow?.stage_status, 'active');
  const warnings = rail?.warnings || [];
  const warningCounts = countBySeverity(warnings);
  const nextAction = rail?.next_action || {
    label: 'Select project',
    enabled: false,
    disabled_reason: 'Choose a project to begin.'
  };
  const progress = stageProgress(rail);
  const destinationPath = rail?.artifact?.destination_path;

  return (
    <aside className="sticky top-0 z-10 rounded-2xl border border-slate-700 bg-slate-950/90 p-3 shadow-lg backdrop-blur">
      <div className="flex flex-wrap items-center gap-2 text-sm">
        <span className="rounded-full bg-slate-800 px-3 py-1 font-medium text-white" title={rail?.project?.slug || ''}>
          {projectLabel}
        </span>
        <span className="rounded-full bg-slate-800 px-3 py-1 text-slate-300">{artifactLabel}</span>
        <span className="rounded-full bg-cyan-500/15 px-3 py-1 text-cyan-300">{stageLabel}</span>
        <span className="rounded-full bg-slate-800 px-3 py-1 text-slate-300">{stageStatus}</span>
        <span className="rounded-full bg-slate-800 px-3 py-1 text-slate-300">{progress} stage{progress === 1 ? '' : 's'}</span>

        {rail?.job ? (
          <span className="rounded-full bg-blue-500/15 px-3 py-1 text-blue-300">job {rail.job.state}</span>
        ) : null}

        {rail?.review ? (
          <span className="rounded-full bg-violet-500/15 px-3 py-1 text-violet-300">review {rail.review.state}</span>
        ) : null}

        {rail?.traceability ? (
          <span className="rounded-full bg-fuchsia-500/15 px-3 py-1 text-fuchsia-300">trace {rail.traceability.status}</span>
        ) : null}

        {warningCounts.blockers > 0 ? (
          <span className="rounded-full bg-red-500/15 px-3 py-1 text-red-300">
            {warningCounts.blockers} blocker{warningCounts.blockers === 1 ? '' : 's'}
          </span>
        ) : null}

        {warningCounts.warnings > 0 ? (
          <span className="rounded-full bg-amber-500/15 px-3 py-1 text-amber-300">
            {warningCounts.warnings} warning{warningCounts.warnings === 1 ? '' : 's'}
          </span>
        ) : null}

        <button
          type="button"
          className="ml-auto rounded-xl border border-slate-700 px-3 py-2 text-sm font-semibold text-slate-200 hover:border-slate-500"
          onClick={() => setExpanded((value) => !value)}
        >
          {expanded ? 'Hide details' : 'Details'}
        </button>

        <button
          type="button"
          className="rounded-xl bg-cyan-400 px-4 py-2 text-sm font-semibold text-slate-950 disabled:cursor-not-allowed disabled:bg-slate-700 disabled:text-slate-400"
          disabled={!nextAction.enabled}
          title={nextAction.disabled_reason || ''}
        >
          {nextAction.label}
        </button>
      </div>

      {expanded ? (
        <div className="mt-3 grid gap-3 border-t border-slate-800 pt-3 text-sm md:grid-cols-2 xl:grid-cols-4">
          <div className="rounded-xl bg-slate-900 p-3">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Project</p>
            <p className="mt-1 text-slate-200">{projectLabel}</p>
            <p className="mt-1 font-mono text-xs text-slate-500">{rail?.project?.slug || 'no-slug'}</p>
          </div>

          <div className="rounded-xl bg-slate-900 p-3">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Artifact</p>
            <p className="mt-1 text-slate-200">{artifactLabel}</p>
            <p className="mt-1 break-words font-mono text-xs text-slate-500">{rail?.artifact?.artifact_id || 'draft not generated'}</p>
          </div>

          <div className="rounded-xl bg-slate-900 p-3">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Workflow</p>
            <p className="mt-1 text-slate-200">{stageLabel}</p>
            <p className="mt-1 text-xs text-slate-500">{rail?.workflow?.completed_stages?.join(' → ') || 'No completed stages yet'}</p>
          </div>

          <div className="rounded-xl bg-slate-900 p-3">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Next action</p>
            <p className="mt-1 text-slate-200">{nextAction.label}</p>
            {!nextAction.enabled && nextAction.disabled_reason ? (
              <p className="mt-1 text-xs text-slate-500">{nextAction.disabled_reason}</p>
            ) : null}
          </div>

          {rail?.job ? (
            <div className="rounded-xl bg-slate-900 p-3">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Job</p>
              <p className="mt-1 text-slate-200">{rail.job.state}</p>
              <p className="mt-1 break-words font-mono text-xs text-slate-500">{rail.job.job_id}</p>
            </div>
          ) : null}

          {rail?.review ? (
            <div className="rounded-xl bg-slate-900 p-3">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Review</p>
              <p className="mt-1 text-slate-200">{rail.review.state}</p>
              <p className="mt-1 text-xs text-slate-500">
                {rail.review.required_checks_passed}/{rail.review.required_checks_total} required checks passed
              </p>
            </div>
          ) : null}

          {rail?.traceability ? (
            <div className="rounded-xl bg-slate-900 p-3">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Traceability</p>
              <p className="mt-1 text-slate-200">{rail.traceability.status}</p>
              <p className="mt-1 text-xs text-slate-500">
                {rail.traceability.warnings} warnings · {rail.traceability.blockers} blockers
              </p>
            </div>
          ) : null}

          {destinationPath ? (
            <div className="rounded-xl bg-slate-900 p-3 md:col-span-2">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Destination</p>
              <p className="mt-1 break-words font-mono text-xs text-slate-300">{destinationPath}</p>
            </div>
          ) : null}

          {warnings.length > 0 ? (
            <div className="rounded-xl bg-slate-900 p-3 md:col-span-2 xl:col-span-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Warnings and blockers</p>
              <ul className="mt-2 grid gap-2">
                {warnings.map((warning, index) => (
                  <li key={`${warning.source}-${warning.message}-${index}`} className="rounded-lg bg-slate-950 p-2 text-xs text-slate-300">
                    <span className={warning.severity === 'error' ? 'text-red-300' : 'text-amber-300'}>
                      {warning.severity || 'warning'}
                    </span>
                    <span className="text-slate-600"> · </span>
                    <span className="text-slate-400">{warning.source || 'workflow'}</span>
                    <span className="text-slate-600"> · </span>
                    {warning.message}
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
        </div>
      ) : null}
    </aside>
  );
}
