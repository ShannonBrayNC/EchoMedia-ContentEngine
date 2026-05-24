import React, { useMemo, useState } from 'react';
import ProjectPicker from './ProjectPicker.jsx';
import SceneCardWorkspace, { buildSceneCardDestination } from './SceneCardWorkspace.jsx';
import WorkflowStatusRail from './WorkflowStatusRail.jsx';
import { getDefaultProject, getProjectBySlug, getVisibleProjects } from '../lib/projectRegistry.js';

function buildRail(selectedProject, creativeDirection, contextValidation) {
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
  const hasDirection = creativeDirection.trim().length > 0;
  const destinationPath = buildSceneCardDestination(selectedProject);
  const contextPassed = contextValidation?.status === 'passed';

  let currentStage = 'creative-direction';
  let stageStatus = 'active';
  let nextAction = {
    label: 'Enter creative direction',
    action_key: 'creative-direction',
    enabled: false,
    disabled_reason: 'Creative direction is required before validation.'
  };

  if (!supportsSceneCard) {
    currentStage = 'select-artifact';
    stageStatus = 'blocked';
    nextAction = {
      label: 'Choose supported artifact',
      action_key: 'select-artifact',
      enabled: false,
      disabled_reason: 'Scene-card is not listed in supported_generation_types.'
    };
  } else if (hasDirection && !contextPassed) {
    currentStage = 'validate-context';
    nextAction = {
      label: 'Validate generation context',
      action_key: 'validate',
      enabled: true
    };
  } else if (contextPassed) {
    currentStage = 'generate-draft';
    nextAction = {
      label: 'Generate scene-card draft',
      action_key: 'generate',
      enabled: true
    };
  }

  const warnings = [];

  if (!supportsSceneCard) {
    warnings.push({
      severity: 'error',
      source: 'project-registry',
      message: 'Selected project does not advertise scene-card generation support.'
    });
  }

  if (contextValidation?.warnings?.length) {
    for (const warning of contextValidation.warnings) {
      warnings.push({
        severity: 'warning',
        source: 'context-validation',
        message: warning
      });
    }
  }

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
      destination_path: destinationPath
    },
    workflow: {
      current_stage: currentStage,
      stage_status: stageStatus,
      completed_stages: ['select-project']
    },
    warnings,
    next_action: nextAction,
    updated_at: new Date().toISOString()
  };
}

function validateSceneCardContext(project, creativeDirection, sourceNotes) {
  const warnings = [];

  if (!project?.active_canon_files?.length) {
    warnings.push('No active canon files are listed for this project yet.');
  }

  if (!sourceNotes.trim()) {
    warnings.push('No optional source/context notes were provided.');
  }

  if (creativeDirection.trim().length < 40) {
    warnings.push('Creative direction is brief; richer scene intent will improve the draft.');
  }

  return {
    status: 'passed',
    message: 'Required scene-card context is present for this first vertical slice.',
    warnings
  };
}

export default function GenerationWorkspace() {
  const projects = useMemo(() => getVisibleProjects(), []);
  const defaultProject = useMemo(() => getDefaultProject(), []);
  const [selectedSlug, setSelectedSlug] = useState(defaultProject?.slug || '');
  const [creativeDirection, setCreativeDirection] = useState('');
  const [sourceNotes, setSourceNotes] = useState('');
  const [contextValidation, setContextValidation] = useState(null);
  const selectedProject = getProjectBySlug(selectedSlug);
  const rail = buildRail(selectedProject, creativeDirection, contextValidation);

  function handleSelectProject(slug) {
    setSelectedSlug(slug);
    setContextValidation(null);
  }

  function handleCreativeDirectionChange(value) {
    setCreativeDirection(value);
    setContextValidation(null);
  }

  function handleSourceNotesChange(value) {
    setSourceNotes(value);
    setContextValidation(null);
  }

  function handleValidateContext() {
    if (!selectedProject) {
      return;
    }

    setContextValidation(validateSceneCardContext(selectedProject, creativeDirection, sourceNotes));
  }

  function handleGenerateDraft() {
    // Issue #92 will implement draft scene-card generation and preview.
  }

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
          <ProjectPicker projects={projects} selectedSlug={selectedSlug} onSelectProject={handleSelectProject} />

          <SceneCardWorkspace
            project={selectedProject}
            creativeDirection={creativeDirection}
            sourceNotes={sourceNotes}
            contextValidation={contextValidation}
            onCreativeDirectionChange={handleCreativeDirectionChange}
            onSourceNotesChange={handleSourceNotesChange}
            onValidateContext={handleValidateContext}
            onGenerateDraft={handleGenerateDraft}
          />
        </div>
      </div>
    </main>
  );
}
