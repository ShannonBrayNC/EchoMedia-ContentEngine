import { useEffect, useMemo, useState } from 'react';
import {
  ArtifactSummary,
  GenerationJob,
  ProjectSummary,
  approveArtifact,
  createGenerationJob,
  getArtifactPreview,
  listProjects,
  rejectArtifact,
  validateGenerationRequest
} from './api';
import './styles.css';

const defaultDirection = 'Create a structured, pre-production-ready package with traceability, review notes, and export readiness.';

function App() {
  const [projects, setProjects] = useState<ProjectSummary[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState('');
  const [artifactType, setArtifactType] = useState('');
  const [direction, setDirection] = useState(defaultDirection);
  const [dryRun, setDryRun] = useState(true);
  const [validationMessages, setValidationMessages] = useState<string[]>([]);
  const [job, setJob] = useState<GenerationJob | null>(null);
  const [artifact, setArtifact] = useState<ArtifactSummary | null>(null);
  const [reviewMessage, setReviewMessage] = useState('No artifact has been reviewed yet.');

  useEffect(() => {
    listProjects().then((items) => {
      setProjects(items);
      if (items[0]) {
        setSelectedProjectId(items[0].projectId);
        setArtifactType(items[0].supportedGenerationTypes[0]);
      }
    });
  }, []);

  const selectedProject = useMemo(
    () => projects.find((project) => project.projectId === selectedProjectId),
    [projects, selectedProjectId]
  );

  async function handleValidate() {
    const messages = await validateGenerationRequest({
      projectId: selectedProjectId,
      artifactType,
      userDirection: direction,
      dryRun
    });
    setValidationMessages(messages.length ? messages : ['Validation passed. Ready to generate a draft.']);
  }

  async function handleGenerate() {
    const messages = await validateGenerationRequest({
      projectId: selectedProjectId,
      artifactType,
      userDirection: direction,
      dryRun
    });
    setValidationMessages(messages);
    if (messages.some((message) => !message.includes('Dry-run'))) return;

    const createdJob = await createGenerationJob({
      projectId: selectedProjectId,
      artifactType,
      userDirection: direction,
      dryRun
    });
    setJob(createdJob);
    setArtifact(await getArtifactPreview(createdJob));
    setReviewMessage('Draft generated. Review before approval or export.');
  }

  async function handleApprove() {
    if (!artifact) return;
    const result = await approveArtifact(artifact.artifactId);
    setArtifact({ ...artifact, state: result.state });
    setReviewMessage('Artifact approved. It can now move to export packaging.');
  }

  async function handleReject() {
    if (!artifact) return;
    const result = await rejectArtifact(artifact.artifactId);
    setArtifact({ ...artifact, state: result.state });
    setReviewMessage('Artifact rejected. Generate a revision before export.');
  }

  return (
    <main className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">EchoMedia Content Engine</p>
          <h1>Generation Workspace</h1>
          <p className="hero-copy">
            Select a project, generate a draft artifact, review it, then approve it for export. Sprint 3 runs in mock API mode.
          </p>
        </div>
        <div className="mode-card" aria-label="Runtime mode">
          <span className="status-dot" aria-hidden="true" />
          <strong>No-provider mode</strong>
          <small>Safe dry-run workflow</small>
        </div>
      </header>

      <section className="workspace-grid" aria-label="Content generation workspace">
        <section className="panel controls-panel" aria-labelledby="controls-heading">
          <h2 id="controls-heading">1. Configure generation</h2>

          <label htmlFor="project-select">Project</label>
          <select
            id="project-select"
            value={selectedProjectId}
            onChange={(event) => {
              const nextProjectId = event.target.value;
              const nextProject = projects.find((project) => project.projectId === nextProjectId);
              setSelectedProjectId(nextProjectId);
              setArtifactType(nextProject?.supportedGenerationTypes[0] ?? '');
              setJob(null);
              setArtifact(null);
            }}
          >
            {projects.map((project) => (
              <option key={project.projectId} value={project.projectId}>
                {project.displayTitle}
              </option>
            ))}
          </select>

          <label htmlFor="artifact-type">Artifact type</label>
          <select id="artifact-type" value={artifactType} onChange={(event) => setArtifactType(event.target.value)}>
            {(selectedProject?.supportedGenerationTypes ?? []).map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>

          <label htmlFor="direction">Generation direction</label>
          <textarea
            id="direction"
            value={direction}
            onChange={(event) => setDirection(event.target.value)}
            rows={7}
          />

          <label className="checkbox-row">
            <input type="checkbox" checked={dryRun} onChange={(event) => setDryRun(event.target.checked)} />
            Dry-run only. Do not call live providers.
          </label>

          <div className="action-row" aria-label="Generation actions">
            <button type="button" onClick={handleValidate}>
              Validate
            </button>
            <button type="button" className="primary" onClick={handleGenerate}>
              Generate draft
            </button>
          </div>
        </section>

        <section className="panel status-panel" aria-labelledby="status-heading">
          <h2 id="status-heading">2. Status rail</h2>
          <ol className="status-list">
            {['configured', 'validated', 'generated', 'needs-review', 'approved', 'export-ready'].map((step) => (
              <li key={step} className={statusClass(step, validationMessages, job, artifact)}>
                <span>{step}</span>
              </li>
            ))}
          </ol>

          <div className="message-box" role="status" aria-live="polite">
            <strong>Validation</strong>
            <ul>
              {(validationMessages.length ? validationMessages : ['No validation has run yet.']).map((message) => (
                <li key={message}>{message}</li>
              ))}
            </ul>
          </div>

          {job && (
            <div className="job-card">
              <strong>Job</strong>
              <span>{job.jobId}</span>
              <span>Status: {job.status}</span>
              <span>Trace: {job.correlationId}</span>
            </div>
          )}
        </section>

        <section className="panel preview-panel" aria-labelledby="preview-heading">
          <h2 id="preview-heading">3. Draft preview and review</h2>
          <div className="preview-box" tabIndex={0} aria-label="Generated artifact preview">
            <pre>{artifact?.preview ?? 'Generate a draft to preview the artifact here.'}</pre>
          </div>

          <div className="review-banner" role="status" aria-live="polite">
            {reviewMessage}
          </div>

          <div className="action-row">
            <button type="button" onClick={handleReject} disabled={!artifact || artifact.state === 'approved'}>
              Reject
            </button>
            <button type="button" className="primary" onClick={handleApprove} disabled={!artifact || artifact.state === 'approved'}>
              Approve
            </button>
            <button type="button" disabled={!artifact || artifact.state !== 'approved'}>
              Export package
            </button>
          </div>
        </section>
      </section>
    </main>
  );
}

function statusClass(step: string, validationMessages: string[], job: GenerationJob | null, artifact: ArtifactSummary | null) {
  const complete =
    step === 'configured' ||
    (step === 'validated' && validationMessages.length > 0) ||
    (step === 'generated' && Boolean(job)) ||
    (step === 'needs-review' && artifact?.state === 'review') ||
    (step === 'approved' && artifact?.state === 'approved') ||
    (step === 'export-ready' && artifact?.state === 'approved');

  return complete ? 'complete' : 'pending';
}

export default App;
