import React from 'react';
import { renderSceneCardDraftMarkdown } from '../lib/sceneCardDraft.js';

const SCENE_CARD_ARTIFACT_TYPE = 'scene-card';

function buildSceneCardDestination(project) {
  if (!project) {
    return '';
  }

  const basePath = project.artifact_paths?.story || project.artifact_paths?.movie_generation || project.root_path;
  return `${basePath}/scene-cards/draft-scene-card.md`;
}

export default function SceneCardWorkspace({
  project,
  creativeDirection,
  sourceNotes,
  onCreativeDirectionChange,
  onSourceNotesChange,
  onValidateContext,
  onGenerateDraft,
  contextValidation,
  draftArtifact
}) {
  const supportsSceneCard = project?.supported_generation_types?.includes(SCENE_CARD_ARTIFACT_TYPE);
  const destinationPath = buildSceneCardDestination(project);
  const hasDirection = creativeDirection.trim().length > 0;
  const canValidate = Boolean(project && supportsSceneCard && hasDirection);
  const canGenerate = Boolean(canValidate && contextValidation?.status === 'passed');
  const draftMarkdown = draftArtifact ? renderSceneCardDraftMarkdown(draftArtifact) : '';

  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-950/70 p-4 shadow-lg">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-cyan-300">Workspace</p>
          <h2 className="mt-1 text-lg font-semibold text-white">Scene-card generation</h2>
          <p className="mt-1 text-sm text-slate-400">
            First vertical slice for creating a previewable scene card draft from registry project context.
          </p>
        </div>
        <span className="rounded-full bg-cyan-500/15 px-3 py-1 text-xs font-medium text-cyan-300">
          {SCENE_CARD_ARTIFACT_TYPE}
        </span>
      </div>

      {!project ? (
        <p className="mt-4 rounded-xl border border-slate-800 bg-slate-900 p-3 text-sm text-slate-400">
          Select a project to start the scene-card workflow.
        </p>
      ) : null}

      {project && !supportsSceneCard ? (
        <p className="mt-4 rounded-xl border border-amber-500/30 bg-amber-500/10 p-3 text-sm text-amber-200">
          This project does not advertise scene-card support in the registry.
        </p>
      ) : null}

      <div className="mt-5 grid gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-300" htmlFor="artifact-type">
            Artifact type
          </label>
          <select
            id="artifact-type"
            className="mt-2 w-full rounded-xl border border-slate-700 bg-slate-900 px-3 py-2 text-white outline-none focus:border-cyan-400"
            value={SCENE_CARD_ARTIFACT_TYPE}
            disabled
          >
            <option value={SCENE_CARD_ARTIFACT_TYPE}>Scene card</option>
          </select>
          <p className="mt-1 text-xs text-slate-500">Only scene-card is enabled for this first implementation slice.</p>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-300" htmlFor="creative-direction">
            Creative direction
          </label>
          <textarea
            id="creative-direction"
            className="mt-2 min-h-32 w-full rounded-xl border border-slate-700 bg-slate-900 px-3 py-2 text-white outline-none placeholder:text-slate-600 focus:border-cyan-400"
            placeholder="Example: Create a tense scene card for a surveillance discovery sequence that can later become an AI video package."
            value={creativeDirection}
            onChange={(event) => onCreativeDirectionChange?.(event.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-300" htmlFor="source-notes">
            Source/context notes
          </label>
          <textarea
            id="source-notes"
            className="mt-2 min-h-24 w-full rounded-xl border border-slate-700 bg-slate-900 px-3 py-2 text-white outline-none placeholder:text-slate-600 focus:border-cyan-400"
            placeholder="Optional: chapter, sequence, canon, character, visual bible, or mood references to use for this scene card."
            value={sourceNotes}
            onChange={(event) => onSourceNotesChange?.(event.target.value)}
          />
        </div>

        <div>
          <p className="text-sm font-medium text-slate-300">Destination preview</p>
          <p className="mt-2 rounded-xl bg-slate-900 p-3 font-mono text-sm text-slate-300">
            {destinationPath || 'Select a project to preview destination path'}
          </p>
          <p className="mt-1 text-xs text-slate-500">Draft generation only previews output. Review/save arrives in later implementation slices.</p>
        </div>

        {contextValidation ? (
          <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-3">
            <div className="flex flex-wrap items-center gap-2">
              <span className="rounded-full bg-emerald-500/15 px-2 py-1 text-xs font-medium text-emerald-300">
                context {contextValidation.status}
              </span>
              <span className="text-sm text-slate-400">{contextValidation.message}</span>
            </div>
            {contextValidation.warnings?.length ? (
              <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-amber-200">
                {contextValidation.warnings.map((warning) => (
                  <li key={warning}>{warning}</li>
                ))}
              </ul>
            ) : null}
          </div>
        ) : null}

        <div className="flex flex-wrap gap-3 border-t border-slate-800 pt-4">
          <button
            type="button"
            className="rounded-xl border border-cyan-400 px-4 py-2 text-sm font-semibold text-cyan-200 disabled:cursor-not-allowed disabled:border-slate-700 disabled:text-slate-500"
            disabled={!canValidate}
            onClick={onValidateContext}
          >
            Validate generation context
          </button>
          <button
            type="button"
            className="rounded-xl bg-cyan-400 px-4 py-2 text-sm font-semibold text-slate-950 disabled:cursor-not-allowed disabled:bg-slate-700 disabled:text-slate-400"
            disabled={!canGenerate}
            onClick={onGenerateDraft}
          >
            Generate scene-card draft
          </button>
        </div>

        {draftArtifact ? (
          <div className="rounded-2xl border border-emerald-500/30 bg-emerald-500/5 p-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-emerald-300">Draft preview</p>
                <h3 className="mt-1 text-lg font-semibold text-white">{draftArtifact.title}</h3>
              </div>
              <span className="rounded-full bg-emerald-500/15 px-3 py-1 text-xs font-medium text-emerald-300">
                preview only
              </span>
            </div>

            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <div className="rounded-xl bg-slate-950/80 p-3">
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Scene ID</p>
                <p className="mt-1 break-words font-mono text-sm text-slate-300">{draftArtifact.scene_id}</p>
              </div>
              <div className="rounded-xl bg-slate-950/80 p-3">
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Source refs</p>
                <p className="mt-1 text-sm text-slate-300">{draftArtifact.source_refs.length}</p>
              </div>
              <div className="rounded-xl bg-slate-950/80 p-3">
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Shots</p>
                <p className="mt-1 text-sm text-slate-300">{draftArtifact.shots.length}</p>
              </div>
              <div className="rounded-xl bg-slate-950/80 p-3">
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Status</p>
                <p className="mt-1 text-sm text-slate-300">{draftArtifact.status}</p>
              </div>
            </div>

            <div className="mt-4">
              <p className="text-sm font-medium text-slate-300">Markdown preview</p>
              <pre className="mt-2 max-h-96 overflow-auto rounded-xl bg-slate-950 p-4 text-xs leading-6 text-slate-300">
                {draftMarkdown}
              </pre>
            </div>
          </div>
        ) : null}
      </div>
    </section>
  );
}

export { buildSceneCardDestination };
