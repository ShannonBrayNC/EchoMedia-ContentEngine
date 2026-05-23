type PacingScene = {
  scene_id: string;
  title: string;
  intensity: number;
  pacing_band: string;
};

type Props = {
  scenes?: PacingScene[];
};

export default function PacingPanel({ scenes = [] }: Props) {
  return (
    <div style={{ border: '1px solid #ccc', borderRadius: 12, padding: 16 }}>
      <h2>Cinematic Pacing</h2>

      {scenes.length === 0 ? (
        <p>No pacing analysis loaded.</p>
      ) : (
        <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end', height: 180 }}>
          {scenes.map((scene) => (
            <div key={scene.scene_id} style={{ textAlign: 'center', flex: 1 }}>
              <div
                title={`${scene.title} (${scene.intensity})`}
                style={{
                  height: `${Math.max(10, scene.intensity)}px`,
                  borderRadius: 6,
                  background: '#444',
                }}
              />
              <small>{scene.scene_id}</small>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
