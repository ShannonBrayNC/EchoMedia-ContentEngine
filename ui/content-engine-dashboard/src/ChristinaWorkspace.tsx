import { useState } from 'react';
import { ContentEngineApi } from './api';

export default function ChristinaWorkspace() {
  const [projectRoot, setProjectRoot] = useState('projects/example');
  const [output, setOutput] = useState('Christina operator console ready.');
  const [loading, setLoading] = useState(false);

  async function runAssembly() {
    setLoading(true);

    try {
      const result = await ContentEngineApi.assembleScreenplay(projectRoot);
      setOutput(JSON.stringify(result, null, 2));
    } catch (error) {
      setOutput(String(error));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ border: '1px solid #aaa', borderRadius: 12, padding: 16 }}>
      <h2>Christina Workspace</h2>

      <div style={{ marginBottom: 12 }}>
        <label>
          Project Root
          <input
            value={projectRoot}
            onChange={(event) => setProjectRoot(event.target.value)}
            style={{ width: '100%', padding: 8, marginTop: 6 }}
          />
        </label>
      </div>

      <button onClick={runAssembly} disabled={loading}>
        {loading ? 'Running...' : 'Assemble Screenplay'}
      </button>

      <pre
        style={{
          marginTop: 16,
          background: '#111',
          color: '#0f0',
          padding: 12,
          borderRadius: 8,
          overflow: 'auto',
        }}
      >
        {output}
      </pre>
    </div>
  );
}
