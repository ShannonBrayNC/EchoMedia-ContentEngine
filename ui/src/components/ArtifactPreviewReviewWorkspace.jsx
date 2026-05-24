import React, { useMemo, useState } from 'react';

function previewJson(value) {
  return JSON.stringify(value || {}, null, 2);
}

function hasValue(value) {
  return value !== undefined && value !== null && value !== '';
}

function getArtifactState({ artifact, reviewGate }) {
  if (reviewGate?.state === 'saved') {
    return 'saved';
  }

  if (reviewGate?.state === 'approved') {
    return 'approved';
  }

  if (reviewGate?.state === 'rejected') {
    return 'rejected';
  }

  if (reviewGate?.state === 'revision-requested') {
    return 'revision-requested';
  }

  return artifact?.status || 'draft';
}

function PreviewModeButton({ mode, selectedMode, onSelect }) {
  return (
    <button
      type="button"
      className={`rounded-xl px-3 py-2 text-xs font-semibold ${
        selectedMode === mode ? 'bg-cyan-400 text-slate-950' : 'border border-slate-700 text-slate-300 hover:border-slate-500'
      }`}
      onClick={() => onSelect(mode)}
    >
      {mode}
    </button>
  );
}

export default function ArtifactPreviewReviewWorkspace({
  artifact,
  artifactMarkdown,
  generationJob,
  reviewGate,
  traceability,
  overwriteConfirmed,
  onApprove,
  onReject,
  onRequestRevision,
  onOverwriteConfirmedChange,
  onSaveApproved,
  canApprove,
  canReject,
  canRequestRevision,
  canSave
}) {
  const [previewMode, setPreviewMode] = useState('markdown');
  const artifactState = getArtifactState({ artifact, reviewGate });
  const approvedSnapshot = reviewGate?.save_manifest || null;
  const metadataPreview = useMemo(
    () =>
      previewJson({
        artifact,
        generationJob,
        reviewGate,
        traceability
      }),
    [artifact, generationJob, reviewGate, traceability]
  );

  if (!artifact) {
    return null;
  }

  return (
    <section className="rounded-2xl border border-emerald-500/30 bg-emerald-500/5 p-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-emerald-300">Preview and review</p>
          <h3 className="mt-1 text-lg font-semibold text-white">{artifact.title || artifact.artifact_id}</h3>
          <p className="mt-1 text-sm text-slate-400">
            Read-only artifact review surface with metadata, traceability, and gate actions.
          </p>
        </div>
        <span className="rounded-full bg-emerald-500/15 px-3 py-1 text-xs font-medium text-emerald-300">
          {artifactState}
        </span>
      </div>

      <div className="mt-4 grid gap-3 md:grid-cols-4">
        <div className="rounded-xl bg-slate-950/80 p-3">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Artifact</p>
          <p className="mt-1 break-words font-mono text-sm text-slate-300">{artifact.artifact_id}</p>
        </div>
        <div className="rounded-xl bg-slate-950/80 p-3">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Generation job</p>
          <p className="mt-1 break-words font-mono text-sm text-slate-300">{artifact.generation_job_id || generationJob?.job_id || 'missing'}</p>
        </div>
        <div className="rounded-xl bg-slate-950/80 p-3">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Review gate</p>
          <p className="mt-1 break-words font-mono text-sm text-slate-300">{reviewGate?.review_id || 'missing'}</p>
        </div>
        <div className="rounded-xl bg-slate-950/80 p-3">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Trace</p>
          <p className="mt-1 break-words font-mono text-sm text-slate-300">{traceability?.trace_id || 'missing'}</p>
        </div>
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        {['markdown', 'json', 'trace', 'manifest', 'compare'].map((mode) => (
          <PreviewModeButton key={mode} mode={mode} selectedMode={previewMode} onSelect={setPreviewMode} />
        ))}
      </div>

      <div className="mt-4 rounded-xl bg-slate-950 p-4">
        {previewMode === 'markdown' ? (
          <pre className="max-h-96 overflow-auto text-xs leading-6 text-slate-300">{artifactMarkdown || 'No Markdown preview available.'}</pre>
        ) : null}

        {previewMode === 'json' ? (
          <pre className="max-h-96 overflow-auto text-xs leading-6 text-slate-300">{previewJson(artifact)}</pre>
        ) : null}

        {previewMode === 'trace' ? (
          <pre className="max-h-96 overflow-auto text-xs leading-6 text-slate-300">{previewJson(traceability || {})}</pre>
        ) : null}

        {previewMode === 'manifest' ? (
          <pre className="max-h-96 overflow-auto text-xs leading-6 text-slate-300">{previewJson(reviewGate?.save_manifest || {})}</pre>
        ) : null}

        {previewMode === 'compare' ? (
          <div className="grid gap-3 lg:grid-cols-2">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Draft</p>
              <pre className="mt-2 max-h-80 overflow-auto rounded-xl bg-slate-900 p-3 text-xs leading-6 text-slate-300">
                {artifactMarkdown || previewJson(artifact)}
              </pre>
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Approved or saved snapshot</p>
              <pre className="mt-2 max-h-80 overflow-auto rounded-xl bg-slate-900 p-3 text-xs leading-6 text-slate-300">
                {approvedSnapshot ? previewJson(approvedSnapshot) : 'No approved or saved snapshot yet.'}
              </pre>
            </div>
          </div>
        ) : null}
      </div>

      <div className="mt-4 grid gap-3 md:grid-cols-3">
        <div className="rounded-xl bg-slate-950/80 p-3">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Source refs</p>
          <p className="mt-1 text-sm text-slate-300">{artifact.source_refs?.length || 0}</p>
        </div>
        <div className="rounded-xl bg-slate-950/80 p-3">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Readiness impact</p>
          <p className="mt-1 text-sm text-slate-300">
            {traceability?.blockers?.length ? 'Blocked' : traceability?.warnings?.length ? 'Warning' : 'Ready for review'}
          </p>
        </div>
        <div className="rounded-xl bg-slate-950/80 p-3">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Preview modes</p>
          <p className="mt-1 text-sm text-slate-300">Markdown, JSON, trace, manifest, compare</p>
        </div>
      </div>

      <label className="mt-4 flex items-center gap-2 text-sm text-slate-300">
        <input
          type="checkbox"
          checked={Boolean(overwriteConfirmed)}
          onChange={(event) => onOverwriteConfirmedChange?.(event.target.checked)}
        />
        I reviewed the destination path and overwrite risk.
      </label>

      <div className="mt-4 flex flex-wrap gap-3">
        <button
          type="button"
          className="rounded-xl border border-emerald-400 px-4 py-2 text-sm font-semibold text-emerald-200 disabled:cursor-not-allowed disabled:border-slate-700 disabled:text-slate-500"
          disabled={!canApprove}
          onClick={onApprove}
        >
          Approve
        </button>
        <button
          type="button"
          className="rounded-xl border border-amber-400 px-4 py-2 text-sm font-semibold text-amber-200 disabled:cursor-not-allowed disabled:border-slate-700 disabled:text-slate-500"
          disabled={!canRequestRevision}
          onClick={onRequestRevision}
        >
          Request revision
        </button>
        <button
          type="button"
          className="rounded-xl border border-red-400 px-4 py-2 text-sm font-semibold text-red-200 disabled:cursor-not-allowed disabled:border-slate-700 disabled:text-slate-500"
          disabled={!canReject}
          onClick={onReject}
        >
          Reject
        </button>
        <button
          type="button"
          className="rounded-xl bg-emerald-400 px-4 py-2 text-sm font-semibold text-slate-950 disabled:cursor-not-allowed disabled:bg-slate-700 disabled:text-slate-400"
          disabled={!canSave}
          onClick={onSaveApproved}
        >
          Save approved
        </button>
      </div>

      {reviewGate?.state === 'approved' && !overwriteConfirmed ? (
        <p className="mt-3 text-sm text-amber-200">Approval is complete. Confirm destination/overwrite review to enable save.</p>
      ) : null}

      {hasValue(reviewGate?.reviewer_notes) ? (
        <p className="mt-3 rounded-xl bg-slate-950/80 p-3 text-sm text-slate-300">{reviewGate.reviewer_notes}</p>
      ) : null}
    </section>
  );
}
