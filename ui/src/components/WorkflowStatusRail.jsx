import React from 'react';

export default function WorkflowStatusRail({ rail }) {
  const projectLabel = rail?.project?.title || 'No project selected';
  const artifactLabel = rail?.artifact?.artifact_type || 'No artifact selected';
  const stageLabel = rail?.workflow?.current_stage || 'select-project';
  const stageStatus = rail?.workflow?.stage_status || 'active';
  const warnings = rail?.warnings || [];
  const nextAction = rail?.next_action || {
    label: 'Select project',
    enabled: false,
    disabled_reason: 'Choose a project to begin.'
  };

  return (
    <aside className="sticky top-0 z-10 rounded-2xl border border-slate-700 bg-slate-950/90 p-3 shadow-lg backdrop-blur">
      <div className="flex flex-wrap items-center gap-2 text-sm">
        <span className="rounded-full bg-slate-800 px-3 py-1 font-medium text-white">{projectLabel}</span>
        <span className="rounded-full bg-slate-800 px-3 py-1 text-slate-300">{artifactLabel}</span>
        <span className="rounded-full bg-cyan-500/15 px-3 py-1 text-cyan-300">{stageLabel}</span>
        <span className="rounded-full bg-slate-800 px-3 py-1 text-slate-300">{stageStatus}</span>
        {warnings.length > 0 ? (
          <span className="rounded-full bg-amber-500/15 px-3 py-1 text-amber-300">
            {warnings.length} warning{warnings.length === 1 ? '' : 's'}
          </span>
        ) : null}
        <button
          type="button"
          className="ml-auto rounded-xl bg-cyan-400 px-4 py-2 text-sm font-semibold text-slate-950 disabled:cursor-not-allowed disabled:bg-slate-700 disabled:text-slate-400"
          disabled={!nextAction.enabled}
          title={nextAction.disabled_reason || ''}
        >
          {nextAction.label}
        </button>
      </div>
    </aside>
  );
}
