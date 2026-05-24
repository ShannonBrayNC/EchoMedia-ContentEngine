import { useEffect, useMemo, useState } from 'react';
import {
  ArtifactSummary,
  GenerationJob,
  IdeaIntake,
  ProjectScaffold,
  ProjectSummary,
  appendMockProject,
  approveArtifact,
  createIdeaIntake,
  createProjectScaffold,
  createSlug,
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
  const [newProjectTitle, setNewProjectTitle] = useState('');
  const [newProjectSlug, setNewProjectSlug] = useState('');
  const [newProjectUniverse, setNewProjectUniverse] = useState('');
  const [newProjectStoryType, setNewProjectStoryType] = useState('novel-to-film');
  const [newProjectTargets, setNewProjectTargets] = useState('generic-json, openai-video, runway');
  const [scaffold, setScaffold] = useState<ProjectScaffold | null>(null);
  const [rawIdea, setRawIdea] = useState('');
  const [ideaDirection, setIdeaDirection] = useState('Extract the strongest story engine, canon candidates, character seeds, and production roadmap.');
  const [ideaIntake, setIdeaIntake] = useState<IdeaIntake | null>(null);

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

  async function handleCreateProject() {
    const displayTitle = newProjectTitle.trim();
    const projectId = createSlug(newProjectSlug || displayTitle);
    if (!displayTitle || !projectId) {
      setValidationMessages(['Add a project title and valid slug before creating a scaffold.']);
      return;
    }

    const createdScaffold = await createProjectScaffold({
      displayTitle,
      projectId,
      universe: newProjectUniverse.trim(),
      storyType: newProjectStoryType,
      targetFormats: newProjectTargets
        .split(',')
        .map((target) => target.trim())
        .filter(Boolean)
    });

    appendMockProject(createdScaffold.project);
    const updatedProjects = await listProjects();
    setProjects([...updatedProjects]);
    setSelectedProjectId(createdScaffold.project.projectId);
    setArtifactType(createdScaffold.project.supportedGenerationTypes[0]);
    setScaffold(createdScaffold);
    setValidationMessages(['New project scaffold created in mock mode. Backend persistence will be added later.']);
    setJob(null);
    setArtifact(null);
    setIdeaIntake(null);
    setReviewMessage('New project created. Start with idea intake, then run readiness checks.');
  }

  async function handleCreateIdeaIntake() {
    if (!selectedProjectId) {
      setValidationMessages(['Select or create a project before loading idea intake.']);
      return;
    }
    if (!rawIdea.trim()) {
      setValidationMessages(['Paste raw idea notes before creating idea intake.']);
      return;
    }

    const intake = await createIdeaIntake({
      projectId: selectedProjectId,
      rawInput: rawIdea,
      direction: ideaDirection
    });

    setIdeaIntake(intake);
    setArtifact({
      artifactId: intake.intakeId,
      projectId: intake.projectId,
      artifactType: 'idea-intake',
      state: intake.state,
      path: `${selectedProject?.rootPath ?? `projects/${selectedProjectId}`}/story/idea-intake.md`,
      manifestId: `manifest-${intake.intakeId}`,
      preview: intake.preview
    });
    setArtifactType('idea-intake');
    setReviewMessage('Idea intake draft created. Review it before promoting anything to canon.');
    setValidationMessages(['Idea intake created in mock mode. It remains draft/review context, not canon.']);
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
            Create a project, load ideas, generate a draft artifact, review it, then approve it for export. Sprint 3 runs in mock API mode.
          </p>
        </div>
        <div className="mode-card" aria-label="Runtime mode">
          <span className="status-dot" aria-hidden="true" />
          <strong>No-provider mode</strong>
          <small>Safe dry-run workflow</small>
        </div>
      </header>

      <section className="project-create-grid" aria-label="New project creation">
        <section className="panel create-panel" aria-labelledby="create-heading">
          <h2 id="create-heading">Create New Project</h2>
          <p className="panel-copy">Create the initial scaffold before structure verification. This mock flow shows the folders and starter artifacts that will be generated.</p>

          <label htmlFor="new-project-title">Project title</label>
          <input
            id="new-project-title"
            value={newProjectTitle}
            onChange={(event) => {
              setNewProjectTitle(event.target.value);
              if (!newProjectSlug) setNewProjectSlug(createSlug(event.target.value));
            }}
            placeholder="Example: The Clockwork Gospel"
          />

          <label htmlFor="new-project-slug">Project slug</label>
          <input
            id="new-project-slug"
            value={newProjectSlug}
            onChange={(event) => setNewProjectSlug(createSlug(event.target.value))}
            placeholder="the-clockwork-gospel"
          />

          <label htmlFor="new-project-universe">Universe or series</label>
          <input
            id="new-project-universe"
            value={newProjectUniverse}
            onChange={(event) => setNewProjectUniverse(event.target.value)}
            placeholder="Lantern / Sovereign"
          />

          <label htmlFor="new-project-story-type">Initial story type</label>
          <select id="new-project-story-type" value={newProjectStoryType} onChange={(event) => setNewProjectStoryType(event.target.value)}>
            <option value="novel-to-film">Novel to film</option>
            <option value="screenplay-first">Screenplay first</option>
            <option value="series-bible">Series bible</option>
            <option value="short-form-campaign">Short-form campaign</option>
          </select>

          <label htmlFor="new-project-targets">Target formats</label>
          <input
            id="new-project-targets"
            value={newProjectTargets}
            onChange={(event) => setNewProjectTargets(event.target.value)}
          />

          <button type="button" className="primary" onClick={handleCreateProject}>
            Create project scaffold
          </button>
        </section>

        <section className="panel scaffold-panel" aria-labelledby="scaffold-heading">
          <h2 id="scaffold-heading">Scaffold preview</h2>
          {scaffold ? (
            <div className="scaffold-summary">
              <strong>{scaffold.project.displayTitle}</strong>
              <span>{scaffold.project.rootPath}</span>
              <h3>Folders</h3>
              <ul>
                {scaffold.folders.map((folder) => (
                  <li key={folder}>{folder}</li>
                ))}
              </ul>
              <h3>Starter artifacts</h3>
              <ul>
                {scaffold.starterArtifacts.map((starter) => (
                  <li key={starter.path}>
                    <strong>{starter.artifactType}</strong>: {starter.path} ({starter.state})
                  </li>
                ))}
              </ul>
              <h3>Next steps</h3>
              <ol>
                {scaffold.nextSteps.map((step) => (
                  <li key={step}>{step}</li>
                ))}
              </ol>
            </div>
          ) : (
            <p className="empty-state">Create a project to see the scaffold summary, starter files, and next steps.</p>
          )}
        </section>
      </section>

      <section className="idea-grid" aria-label="Idea intake workflow">
        <section className="panel idea-panel" aria-labelledby="idea-heading">
          <h2 id="idea-heading">Load Ideas</h2>
          <p className="panel-copy">Paste rough notes, fragments, or a seed concept. The intake draft stays out of canon until reviewed.</p>

          <label htmlFor="raw-idea">Raw idea notes</label>
          <textarea
            id="raw-idea"
            value={rawIdea}
            onChange={(event) => setRawIdea(event.target.value)}
            rows={8}
            placeholder="Paste the messy spark here: premise, characters, scenes, themes, politics, technology, emotional stakes..."
          />

          <label htmlFor="idea-direction">AI structuring direction</label>
          <textarea
            id="idea-direction"
            value={ideaDirection}
            onChange={(event) => setIdeaDirection(event.target.value)}
            rows={3}
          />

          <button type="button" className="primary" onClick={handleCreateIdeaIntake}>
            Create idea intake draft
          </button>
        </section>

        <section className="panel idea-output-panel" aria-labelledby="idea-output-heading">
          <h2 id="idea-output-heading">Idea intake output</h2>
          {ideaIntake ? (
            <div className="scaffold-summary">
              <strong>{ideaIntake.intakeId}</strong>
              <span>State: {ideaIntake.state}</span>
              <h3>Summary</h3>
              <p>{ideaIntake.summary}</p>
              <h3>Artifact roadmap</h3>
              <ol>
                {ideaIntake.artifactRoadmap.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ol>
              <h3>Next steps</h3>
              <ol>
                {ideaIntake.nextSteps.map((step) => (
                  <li key={step}>{step}</li>
                ))}
              </ol>
            </div>
          ) : (
            <p className="empty-state">Load an idea to see structured story candidates and next steps.</p>
          )}
        </section>
      </section>

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
