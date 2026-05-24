import React, { useMemo, useState } from 'react';
import ProjectPicker from './ProjectPicker.jsx';
import WorkflowStatusRail from './WorkflowStatusRail.jsx';
import { getDefaultProject, getProjectBySlug, getVisibleProjects } from '../lib/projectRegistry.js';

function buildRail(selectedProject) {
  if (!selectedProject) {
    return {
      rail_id: 'workspace-project-selection',
      version: '0.1.0',
      project: {
        slug: '',
        title: 'No project selected',
        status: 'not-started'
      },
      artifact: {
        artifact_type: 'scene-card'
      },
      workflow: {
        current_stage: 'select-project',
        stage_status: 'active',
        completed_stages: []
      },
      warnings: [],
      next_action: {
        label: 'Select project',
        action_key: 'select-project',
        enabled: false,
        disabled_reason: 'Choose a registry project before continuing.'
      },
      updated_at: new Date().toISOString()
    };
  }

  const supportsSceneCard = selectedProject.supported_generation_types?.includes('scene-card');

  return {
    rail_id: `${selectedProject.slug}-scene-card-workspace`,
    version: '0.1.0',
    project: {
      slug: selectedProject.slug,
      title: selectedProject.title,
      status: selectedProject.status,
      canon_state: selectedProject.canon_state
    },
    artifact: {
      artifact_type: 'scene-card',
      destination_path: selectedProject.artifact_paths?.story || selectedProject.artifact_paths?.movie_generation
    },
    workflow: {
      current_stage: supportsSceneCard ? 'creative-direction' : 'select-artifact',
      stage_status: supportsSceneCard ? 'active' : 'blocked',
      completed_stages: ['select-project']
    },
    warnings: supportsSceneCard
      ? []
      : [
          {
            severity: 'error',
            source: 'project-registry',
            message: 'Selected project does not advertise scene-card generation support.'
          }
        ],
    next_action: {
      label: supportsSceneCard ? 'Enter creative direction' : 'Choose supported artifact',
      action_key: supportsSceneCard ? 'creative-direction' : 'select-artifact',
      enabled: supportsSceneCard,
      disabled_reason: supportsSceneCard ? undefined : 'Scene-card is not listed in supported_generation_types.'
    },
    updated_at: new Date().toISOString()
  };
}

export default function GenerationWorkspace() {
  const projects = useMemo(() => getVisibleProjects(), []);
  const defaultProject = useMemo(() => getDefaultProject(), []);
  const [selectedSlug, setSelectedSlug] = useState(defaultProject?.slug || '');
  const selectedProject = getProjectBySlug(selectedSlug);
  const rail = buildRail(selectedProject);

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-white">
      <div className="mx-auto flex max-w-6xl flex-col gap-5">
        <WorkflowStatusRail rail={rail} />

        <header>
          <p className="text-sm font-semibold uppercase tracking-wide text-cyan-300">EchoMedia Content Engine</p>
          <h1 className="mt-2 text-3xl font-bold">Generation workspace</h1>
          <p className="mt-2 max-w-3xl text-slate-400">
            Registry-driven project selection for the first scene-card vertical slice.
          </p>
        </header>

        <div className="grid gap-5 lg:grid-cols-[minmax(280px,360px)_1fr]">
          <ProjectPicker projects={projects} selectedSlug={selectedSlug} onSelectProject={setSelectedSlug} />

          <section className="rounded-2xl border border-slate-700 bg-slate-950/70 p-4 shadow-lg">
            <p className="text-xs font-semibold uppercase tracking-wide text-cyan-300">Workspace</p>
            <h2 className="mt-1 text-lg font-semibold">Scene-card vertical slice</h2>

            {selectedProject ? (
              <div className="mt-4 space-y-4">
                <div>
                  <p className="text-sm font-medium text-slate-300">Selected project</p>
                  <p className="mt-1 text-xl font-semibold text-white">{selectedProject.title}</p>
                </div>

                <div>
                  <p className="text-sm font-medium text-slate-300">Destination preview</p>
                  <p className="mt-1 rounded-xl bg-slate-900 p-3 font-mono text-sm text-slate-300">
                    {selectedProject.artifact_paths?.story || selectedProject.artifact_paths?.movie_generation || 'No destination path available'}
                  </p>
                </div>

                <div>
                  <p className="text-sm font-medium text-slate-300">Next implementation issue</p>
                  <p className="mt-1 text-sm text-slate-400">
                    Issue #91 adds the scene-card workspace input controls and separates validation from draft creation.
                  </p>
                </div>
              </div>
            ) : (
              <p className="mt-4 text-slate-400">Select a project to continue.</p>
            )}
          </section>
        </div>
      </div>
    </main>
  );
}
