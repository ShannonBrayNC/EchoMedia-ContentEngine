type Project = {
  project_id: string;
  project_type?: string;
};

type Props = {
  projects: Project[];
  activeProject?: string;
  onSelect: (projectId: string) => void;
};

export default function ProjectSelector({ projects, activeProject, onSelect }: Props) {
  return (
    <div style={{ marginBottom: 16 }}>
      <label>
        Active Project
        <select
          value={activeProject}
          onChange={(event) => onSelect(event.target.value)}
          style={{ marginLeft: 12, padding: 8 }}
        >
          {projects.map((project) => (
            <option key={project.project_id} value={project.project_id}>
              {project.project_id}
            </option>
          ))}
        </select>
      </label>
    </div>
  );
}
