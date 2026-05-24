import React, { useMemo, useState } from 'react';
import ProjectPicker from './ProjectPicker.jsx';
import SceneCardWorkspace, { buildSceneCardDestination } from './SceneCardWorkspace.jsx';
import WorkflowStatusRail from './WorkflowStatusRail.jsx';
import { buildSceneCardDraft } from '../lib/sceneCardDraft.js';
import { completeGenerationJob, createSceneCardGenerationJob, failGenerationJob } from '../lib/generationJob.js';
import {
  approveReviewGate,
  buildSceneCardSaveManifest,
  createSceneCardReviewGate,
  markReviewGateSaved,
  rejectReviewGate,
  reviewGateHasBlockingFailures
} from '../lib/reviewGate.js';
import { getDefaultProject, getProjectBySlug, getVisibleProjects } from '../lib/projectRegistry.js';

function buildRail(selectedProject, creativeDirection, contextValidation, draftArtifact, generationJob, reviewGate) {
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
  const reviewBlocksSave = reviewGateHasBlockingFailures(reviewGate);

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
  } else if (generationJob?.state === 'failed') {
    currentStage = 'generate-draft';
    stageStatus = 'failed';
    nextAction = {
      label: 'Fix generation error',
      action_key: 'generate',
      enabled: false,
      disabled_reason: generationJob.errors?.[0]?.message || 'Generation failed.'
    };
  } else if (reviewGate?.state === 'saved') {
    currentStage = 'save-commit';
    stageStatus = 'complete';
    nextAction = {
      label: 'Saved locally',
      action_key: 'saved',
      enabled: false,
      disabled_reason: 'The approved draft has a local save manifest.'
    };
  } else if (reviewGate?.state === 'approved') {
    currentStage = 'save-commit';
    stageStatus = reviewBlocksSave ? 'blocked' : 'active';
    nextAction = {
      label: 'Save approved draft',
      action_key: 'save',
      enabled: !reviewBlocksSave,
      disabled_reason: reviewBlocksSave ? 'Blocking review checks must pass before save.' : undefined
    };
  } else if (reviewGate?.state === 'rejected') {
    currentStage = 'preview-review';
    stageStatus = 'blocked';
    nextAction = {
      label: 'Regenerate draft',
      action_key: 'generate',
      enabled: true
    };
  } else if (draftArtifact) {
    currentStage = 'preview-review';
    nextAction = {
      label: 'Review draft preview',
      action_key: 'review',
      enabled: true
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
      artifact_id: draftArtifact?.artifact_id,
      title: draftArtifact?.title,
      destination_path: destinationPath
    },
    job: generationJob
      ? {
          job_id: generationJob.job_id,
          state: generationJob.state,
          action: generationJob.action,
          attempt: 1
        }
      : undefined,
    review: reviewGate
      ? {
          review_id: reviewGate.review_id,
          state: reviewGate.state,
          required_checks_total: reviewGate.checks?.filter((check) => check.required).length || 0,
          required_checks_passed:
            reviewGate.checks?.filter((check) => check.required && check.status === 'passed').length || 0,
          blocking_failures: reviewGate.checks?.filter((check) => check.required && check.status === 'failed').length || 0
        }
      : undefined,
    workflow: {
      current_stage: currentStage,
      stage_status: stageStatus,
      completed_stages: draftArtifact ? ['select-project', 'validate-context', 'generate-draft'] : ['select-project']
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
  const [draftArtifact, setDraftArtifact] = useState(null);
  const [generationJob, setGenerationJob] = useState(null);
  const [reviewGate, setReviewGate] = useState(null);
  const [overwriteConfirmed, setOverwriteConfirmed] = useState(false);
  const selectedProject = getProjectBySlug(selectedSlug);
  const rail = buildRail(selectedProject, creativeDirection, contextValidation, draftArtifact, generationJob, reviewGate);

  function resetDraftState() {
    setContextValidation(null);
    setDraftArtifact(null);
    setGenerationJob(null);
    setReviewGate(null);
    setOverwriteConfirmed(false);
  }

  function handleSelectProject(slug) {
    setSelectedSlug(slug);
    resetDraftState();
  }

  function handleCreativeDirectionChange(value) {
    setCreativeDirection(value);
    resetDraftState();
  }

  function handleSourceNotesChange(value) {
    setSourceNotes(value);
    resetDraftState();
  }

  function handleValidateContext() {
    if (!selectedProject) {
      return;
    }

    setContextValidation(validateSceneCardContext(selectedProject, creativeDirection, sourceNotes));
    setDraftArtifact(null);
    setGenerationJob(null);
    setReviewGate(null);
    setOverwriteConfirmed(false);
  }

  function handleGenerateDraft() {
    if (!selectedProject || contextValidation?.status !== 'passed') {
      return;
    }

    const destinationPath = buildSceneCardDestination(selectedProject);
    const initialJob = createSceneCardGenerationJob({
      project: selectedProject,
      creativeDirection,
      sourceNotes,
      contextValidation,
      destinationPath
    });

    try {
      const draft = buildSceneCardDraft({
        project: selectedProject,
        creativeDirection,
        sourceNotes,
        generationJobId: initialJob.job_id
      });

      const completedJob = completeGenerationJob(initialJob, draft);
      const pendingReviewGate = createSceneCardReviewGate({
        project: selectedProject,
        draftArtifact: draft,
        generationJob: completedJob,
        destinationPath
      });

      setGenerationJob(completedJob);
      setDraftArtifact(draft);
      setReviewGate(pendingReviewGate);
      setOverwriteConfirmed(false);
    } catch (error) {
      setGenerationJob(failGenerationJob(initialJob, error));
      setDraftArtifact(null);
      setReviewGate(null);
      setOverwriteConfirmed(false);
    }
  }

  function handleApproveDraft() {
    if (!reviewGate) {
      return;
    }

    setReviewGate(approveReviewGate(reviewGate, 'Approved in first vertical slice review gate.'));
  }

  function handleRejectDraft() {
    if (!reviewGate) {
      return;
    }

    setReviewGate(rejectReviewGate(reviewGate, 'Rejected in first vertical slice review gate.'));
  }

  function handleOverwriteConfirmedChange(confirmed) {
    setOverwriteConfirmed(confirmed);
  }

  function handleSaveApprovedDraft() {
    if (!selectedProject || !draftArtifact || !reviewGate || reviewGate.state !== 'approved') {
      return;
    }

    const destinationPath = buildSceneCardDestination(selectedProject);
    const saveManifest = buildSceneCardSaveManifest({
      project: selectedProject,
      draftArtifact,
      reviewGate,
      destinationPath,
      overwriteConfirmed
    });

    setReviewGate(markReviewGateSaved(reviewGate, saveManifest));
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
            draftArtifact={draftArtifact}
            generationJob={generationJob}
            reviewGate={reviewGate}
            overwriteConfirmed={overwriteConfirmed}
            onCreativeDirectionChange={handleCreativeDirectionChange}
            onSourceNotesChange={handleSourceNotesChange}
            onValidateContext={handleValidateContext}
            onGenerateDraft={handleGenerateDraft}
            onApproveDraft={handleApproveDraft}
            onRejectDraft={handleRejectDraft}
            onOverwriteConfirmedChange={handleOverwriteConfirmedChange}
            onSaveApprovedDraft={handleSaveApprovedDraft}
          />
        </div>
      </div>
    </main>
  );
}
