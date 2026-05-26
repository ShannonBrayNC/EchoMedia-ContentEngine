#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';

const repoRoot = process.cwd();
const registryPath = process.argv[2] || 'config/project-registry.json';
const absoluteRegistryPath = path.resolve(repoRoot, registryPath);

const requiredProjectFields = [
  'slug',
  'title',
  'root_path',
  'status',
  'artifact_paths',
  'supported_generation_types'
];

const requiredArtifactPathKeys = [
  'canon',
  'characters',
  'story',
  'manuscript',
  'storyboards',
  'visual_bible',
  'screenplay',
  'movie_generation',
  'pitch',
  'reports'
];

const allowedStatuses = new Set([
  'draft',
  'active',
  'paused',
  'locked',
  'archived'
]);

const allowedVisibility = new Set([
  'visible',
  'hidden'
]);

const allowedGenerationTypes = new Set([
  'canon',
  'character',
  'story-outline',
  'manuscript',
  'screenplay',
  'scene-card',
  'storyboard',
  'visual-prompt',
  'production-package',
  'pitch',
  'audio-script',
  'tool-export'
]);

const slugPattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

const report = {
  errors: [],
  warnings: [],
  info: []
};

function addError(message) {
  report.errors.push(message);
}

function addWarning(message) {
  report.warnings.push(message);
}

function addInfo(message) {
  report.info.push(message);
}

function existsRelative(relativePath) {
  return fs.existsSync(path.resolve(repoRoot, relativePath));
}

function readJson(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`Registry file not found: ${filePath}`);
  }

  const raw = fs.readFileSync(filePath, 'utf8');
  return JSON.parse(raw);
}

let registry;

try {
  registry = readJson(absoluteRegistryPath);
} catch (error) {
  console.error(`ERROR: ${error.message}`);
  process.exit(1);
}

if (!registry || typeof registry !== 'object') {
  addError('Registry root must be an object.');
}

if (!registry.version || typeof registry.version !== 'string') {
  addError('Registry must include a string version.');
}

if (!Array.isArray(registry.projects)) {
  addError('Registry must include a projects array.');
}

const seenSlugs = new Set();

for (const project of registry.projects || []) {
  const label = project?.slug || project?.title || '<unknown project>';

  for (const field of requiredProjectFields) {
    if (!(field in project)) {
      addError(`${label}: missing required field '${field}'.`);
    }
  }

  if (typeof project.slug !== 'string' || !slugPattern.test(project.slug)) {
    addError(`${label}: slug must be kebab-case lowercase alphanumeric.`);
  }

  if (seenSlugs.has(project.slug)) {
    addError(`${label}: duplicate project slug '${project.slug}'.`);
  }
  seenSlugs.add(project.slug);

  if (!allowedStatuses.has(project.status)) {
    addError(`${label}: unsupported status '${project.status}'.`);
  }

  if (project.visibility && !allowedVisibility.has(project.visibility)) {
    addError(`${label}: unsupported visibility '${project.visibility}'.`);
  }

  if (project.root_path && !existsRelative(project.root_path)) {
    addWarning(`${label}: root_path does not currently exist: ${project.root_path}`);
  }

  if (!project.artifact_paths || typeof project.artifact_paths !== 'object') {
    addError(`${label}: artifact_paths must be an object.`);
  } else {
    for (const key of requiredArtifactPathKeys) {
      const artifactPath = project.artifact_paths[key];
      if (!artifactPath) {
        addError(`${label}: missing artifact path '${key}'.`);
        continue;
      }

      if (!existsRelative(artifactPath)) {
        addWarning(`${label}: artifact path '${key}' does not currently exist: ${artifactPath}`);
      }
    }
  }

  if (!Array.isArray(project.supported_generation_types)) {
    addError(`${label}: supported_generation_types must be an array.`);
  } else {
    for (const generationType of project.supported_generation_types) {
      if (!allowedGenerationTypes.has(generationType)) {
        addError(`${label}: unsupported generation type '${generationType}'.`);
      }
    }
  }

  if (project.export_targets && !Array.isArray(project.export_targets)) {
    addError(`${label}: export_targets must be an array when provided.`);
  }

  addInfo(`${label}: checked registry entry.`);
}

console.log('Project Registry Validation Report');
console.log('==================================');
console.log(`Registry: ${registryPath}`);
console.log(`Projects: ${(registry.projects || []).length}`);
console.log(`Errors: ${report.errors.length}`);
console.log(`Warnings: ${report.warnings.length}`);
console.log('');

if (report.errors.length) {
  console.log('Errors');
  for (const error of report.errors) {
    console.log(`- ${error}`);
  }
  console.log('');
}

if (report.warnings.length) {
  console.log('Warnings');
  for (const warning of report.warnings) {
    console.log(`- ${warning}`);
  }
  console.log('');
}

if (report.info.length) {
  console.log('Checked');
  for (const info of report.info) {
    console.log(`- ${info}`);
  }
  console.log('');
}

if (report.errors.length) {
  process.exit(1);
}

process.exit(0);
