import projectRegistry from '../../../config/project-registry.json';

const DEFAULT_VISIBLE_STATUSES = new Set(['draft', 'active', 'paused', 'locked']);

export function getProjectRegistry() {
  return projectRegistry;
}

export function getVisibleProjects(registry = projectRegistry) {
  const projects = Array.isArray(registry?.projects) ? registry.projects : [];

  return projects
    .filter((project) => project.visibility !== 'hidden')
    .filter((project) => DEFAULT_VISIBLE_STATUSES.has(project.status))
    .sort((a, b) => a.title.localeCompare(b.title));
}

export function getProjectBySlug(slug, registry = projectRegistry) {
  if (!slug) {
    return null;
  }

  const projects = Array.isArray(registry?.projects) ? registry.projects : [];
  return projects.find((project) => project.slug === slug) || null;
}

export function getProjectArtifactPath(project, artifactPathKey) {
  if (!project || !artifactPathKey) {
    return null;
  }

  return project.artifact_paths?.[artifactPathKey] || null;
}

export function getDefaultProject(registry = projectRegistry) {
  const visibleProjects = getVisibleProjects(registry);
  return visibleProjects[0] || null;
}

export function toProjectPickerOption(project) {
  return {
    value: project.slug,
    label: project.title,
    description: [project.series, project.universe].filter(Boolean).join(' · '),
    status: project.status,
    canonState: project.canon_state,
    supportedGenerationTypes: project.supported_generation_types || [],
    exportTargets: project.export_targets || []
  };
}
