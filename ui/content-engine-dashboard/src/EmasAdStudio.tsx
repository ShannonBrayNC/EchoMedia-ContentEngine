import { useEffect, useMemo, useState } from 'react';
import {
  EMAS_API_BASE_URL,
  EmasAsset,
  EmasDashboard,
  EmasFrame,
  EmasPreflightResult,
  EmasPublishResult,
  createEmasAdProject,
  getEmasDashboard,
  listEmasFrames,
  listEmasReferences,
  publishEmasOutput,
  reviewEmasFrame,
  runEmasPreflight,
  submitEmasFrame,
  tagEmasReference,
  uploadEmasReference
} from './emasApi';

const DEFAULT_PROJECT = 'Vanessa';
const DEFAULT_AD = 'Vanessa-Christina-Outfit-Update-Ad';
const DEFAULT_ACTOR = 'ShannonBrayNC';
const DEFAULT_PROMPT = 'Create the Christina outfit update scene with Vanessa seated at a computer, reviewing the EchoMedia site, then approving the pink outfit update.';

function splitList(value: string) {
  return value.split(',').map((item) => item.trim()).filter(Boolean);
}

export function EmasAdStudio() {
  const [projectName, setProjectName] = useState(DEFAULT_PROJECT);
  const [adName, setAdName] = useState(DEFAULT_AD);
  const [actor, setActor] = useState(DEFAULT_ACTOR);
  const [dashboard, setDashboard] = useState<EmasDashboard | null>(null);
  const [assets, setAssets] = useState<EmasAsset[]>([]);
  const [frames, setFrames] = useState<EmasFrame[]>([]);
  const [message, setMessage] = useState('EMAS dashboard has not loaded yet.');
  const [busy, setBusy] = useState(false);

  const [referencePath, setReferencePath] = useState('');
  const [referenceTags, setReferenceTags] = useState('pink-updated-outfit, smiling, soft-light');
  const [outfit, setOutfit] = useState('pink-updated-outfit');
  const [expression, setExpression] = useState('smiling');
  const [pose, setPose] = useState('looking-at-screen');

  const [framePath, setFramePath] = useState('');
  const [sceneId, setSceneId] = useState('scene-01');

  const [prompt, setPrompt] = useState(DEFAULT_PROMPT);
  const [referencePaths, setReferencePaths] = useState('');
  const [preflight, setPreflight] = useState<EmasPreflightResult | null>(null);

  const [outputId, setOutputId] = useState('output-1');
  const [outputMetadataPath, setOutputMetadataPath] = useState('');
  const [publishResult, setPublishResult] = useState<EmasPublishResult | null>(null);

  const canPublish = Boolean(preflight?.allowed && outputMetadataPath.trim());

  async function refresh() {
    if (!projectName || !adName) return;
    try {
      const [nextDashboard, nextAssets, nextFrames] = await Promise.all([
        getEmasDashboard(projectName, adName),
        listEmasReferences(projectName, adName),
        listEmasFrames(projectName, adName)
      ]);
      setDashboard(nextDashboard);
      setAssets(nextAssets.assets);
      setFrames(nextFrames.frames);
      setMessage('EMAS dashboard refreshed.');
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Unable to refresh EMAS dashboard.');
    }
  }

  useEffect(() => {
    refresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const approvedFrames = useMemo(() => frames.filter((frame) => frame.state === 'approved'), [frames]);
  const pendingFrames = useMemo(() => frames.filter((frame) => frame.state === 'pending'), [frames]);

  async function runAction(action: () => Promise<void>) {
    setBusy(true);
    try {
      await action();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'EMAS action failed.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="panel emas-panel" aria-labelledby="emas-heading">
      <div className="section-heading-row">
        <div>
          <p className="eyebrow">EchoMedia Ad Studio</p>
          <h2 id="emas-heading">Vanessa / Christina Instagram Ad</h2>
          <p className="panel-copy">Wire the storyboard workflow to the local EMAS API: references, frame approvals, preflight, and export package publishing.</p>
        </div>
        <div className="mode-card compact-mode" aria-label="EMAS runtime mode">
          <span className="status-dot" aria-hidden="true" />
          <strong>No-provider EMAS</strong>
          <small>{EMAS_API_BASE_URL}</small>
        </div>
      </div>

      <div className="emas-controls-grid">
        <label htmlFor="emas-project">Project</label>
        <input id="emas-project" value={projectName} onChange={(event) => setProjectName(event.target.value)} />
        <label htmlFor="emas-ad">Ad</label>
        <input id="emas-ad" value={adName} onChange={(event) => setAdName(event.target.value)} />
        <label htmlFor="emas-actor">Actor</label>
        <input id="emas-actor" value={actor} onChange={(event) => setActor(event.target.value)} />
      </div>

      <div className="action-row">
        <button type="button" onClick={() => runAction(async () => { await createEmasAdProject({ projectName, adName, actor, force: false }); await refresh(); })} disabled={busy}>Create ad project</button>
        <button type="button" onClick={() => runAction(refresh)} disabled={busy}>Refresh dashboard</button>
      </div>

      <div className="review-banner" role="status" aria-live="polite">{message}</div>

      {dashboard && <div className="emas-summary-grid">
        <div className="readiness-score"><strong>{dashboard.status}</strong><span>{dashboard.format} · {dashboard.durationSeconds}s target</span></div>
        <div className="message-box"><strong>Next best action</strong><p>{dashboard.nextBestAction}</p></div>
        <div className="message-box warning-box"><strong>Missing assets</strong><ul>{dashboard.missingAssets.map((item) => <li key={item}>{item}</li>)}</ul></div>
      </div>}

      {dashboard && <div className="emas-metric-grid">
        {Object.entries(dashboard.counts).map(([key, value]) => <div key={key} className="traceability-grid-item"><strong>{value}</strong><span>{key}</span></div>)}
      </div>}

      <div className="emas-workflow-grid">
        <section className="subpanel" aria-labelledby="emas-ref-heading">
          <h3 id="emas-ref-heading">References</h3>
          <label htmlFor="emas-reference-path">Server-local image path</label>
          <input id="emas-reference-path" value={referencePath} onChange={(event) => setReferencePath(event.target.value)} placeholder="C:/temp/vanessa-pink-reference.jpg" />
          <label htmlFor="emas-tags">Tags</label>
          <input id="emas-tags" value={referenceTags} onChange={(event) => setReferenceTags(event.target.value)} />
          <div className="three-field-row">
            <input aria-label="Outfit" value={outfit} onChange={(event) => setOutfit(event.target.value)} placeholder="outfit" />
            <input aria-label="Expression" value={expression} onChange={(event) => setExpression(event.target.value)} placeholder="expression" />
            <input aria-label="Pose" value={pose} onChange={(event) => setPose(event.target.value)} placeholder="pose" />
          </div>
          <button type="button" className="primary" onClick={() => runAction(async () => { await uploadEmasReference({ projectName, adName, actor, sourcePath: referencePath, tags: splitList(referenceTags), outfit, expression, pose }); await refresh(); })} disabled={busy || !referencePath.trim()}>Upload/tag reference</button>
          <div className="compact-list">{assets.map((asset) => <article key={asset.asset_id} className="compact-card"><strong>{asset.original_filename}</strong><span>{asset.approval_state} · {asset.tags.join(', ') || 'untagged'}</span><button type="button" onClick={() => runAction(async () => { await tagEmasReference({ projectName, adName, assetId: asset.asset_id, actor, tags: ['approved-reference'], approved: true }); await refresh(); })}>Approve ref</button></article>)}</div>
        </section>

        <section className="subpanel" aria-labelledby="emas-frame-heading">
          <h3 id="emas-frame-heading">Storyboard</h3>
          <label htmlFor="emas-frame-path">Server-local frame path</label>
          <input id="emas-frame-path" value={framePath} onChange={(event) => setFramePath(event.target.value)} placeholder="C:/temp/scene-01-frame.png" />
          <label htmlFor="emas-scene-id">Scene</label>
          <select id="emas-scene-id" value={sceneId} onChange={(event) => setSceneId(event.target.value)}>{Array.from({ length: 8 }, (_, index) => `scene-${String(index + 1).padStart(2, '0')}`).map((scene) => <option key={scene} value={scene}>{scene}</option>)}</select>
          <button type="button" className="primary" onClick={() => runAction(async () => { await submitEmasFrame({ projectName, adName, sourcePath: framePath, sceneId, actor }); await refresh(); })} disabled={busy || !framePath.trim()}>Submit frame</button>
          <div className="compact-list">{frames.map((frame) => <article key={frame.frame_id} className={`compact-card ${frame.state}`}><strong>{frame.scene_id}</strong><span>{frame.state} · {frame.filename}</span>{frame.state === 'pending' && <div className="action-row"><button type="button" onClick={() => runAction(async () => { await reviewEmasFrame({ projectName, adName, frameId: frame.frame_id, actor, approved: true }); await refresh(); })}>Approve</button><button type="button" onClick={() => runAction(async () => { await reviewEmasFrame({ projectName, adName, frameId: frame.frame_id, actor, approved: false }); await refresh(); })}>Reject</button></div>}</article>)}</div>
        </section>

        <section className="subpanel" aria-labelledby="emas-preflight-heading">
          <h3 id="emas-preflight-heading">Preflight</h3>
          <label htmlFor="emas-prompt">Prompt</label>
          <textarea id="emas-prompt" value={prompt} onChange={(event) => setPrompt(event.target.value)} rows={5} />
          <label htmlFor="emas-reference-paths">Reference paths</label>
          <textarea id="emas-reference-paths" value={referencePaths} onChange={(event) => setReferencePaths(event.target.value)} rows={3} placeholder="One or more approved reference paths, comma separated" />
          <button type="button" className="primary" onClick={() => runAction(async () => { const result = await runEmasPreflight({ projectName, adName, actor, subjectId: projectName, intendedUse: 'social_media', platform: 'instagram', prompt, referencePaths: splitList(referencePaths), outputCount: 4 }); setPreflight(result); setMessage(result.allowed ? 'Preflight passed. Ready for provider-safe generation.' : `Preflight blocked: ${result.reasons.join('; ')}`); })} disabled={busy}>Run preflight</button>
          {preflight && <div className={`message-box ${preflight.allowed ? '' : 'warning-box'}`}><strong>{preflight.allowed ? 'Allowed' : 'Blocked'}</strong><p>{preflight.normalizedPrompt}</p><ul>{preflight.reasons.map((reason) => <li key={reason}>{reason}</li>)}</ul></div>}
        </section>

        <section className="subpanel" aria-labelledby="emas-export-heading">
          <h3 id="emas-export-heading">Exports</h3>
          <label htmlFor="emas-output-id">Output ID</label>
          <input id="emas-output-id" value={outputId} onChange={(event) => setOutputId(event.target.value)} />
          <label htmlFor="emas-output-metadata">Approved output metadata path</label>
          <input id="emas-output-metadata" value={outputMetadataPath} onChange={(event) => setOutputMetadataPath(event.target.value)} placeholder="projects/Vanessa/ads/.../outputs/draft/output-1.json" />
          <button type="button" className="primary" onClick={() => runAction(async () => { const result = await publishEmasOutput({ projectName, adName, outputId, actor, platform: 'instagram', format: 'reels-9x16', intendedUse: 'social_media', outputMetadataPath }); setPublishResult(result); await refresh(); })} disabled={busy || !canPublish}>Publish export package</button>
          {!canPublish && <p className="empty-state">Run a passing preflight and provide approved output metadata before publishing.</p>}
          {publishResult && <div className="message-box"><strong>{publishResult.state}</strong><p>{publishResult.manifestPath || 'No manifest created.'}</p><span>{publishResult.auditEventId}</span></div>}
          <div className="message-box"><strong>Frame readiness</strong><p>{approvedFrames.length} approved / {pendingFrames.length} pending.</p></div>
        </section>
      </div>
    </section>
  );
}
