from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / 'config/project-registry.json'


def load_registry() -> dict:
    if not REGISTRY_PATH.exists():
        return {'active_project': None, 'projects': []}

    return json.loads(REGISTRY_PATH.read_text(encoding='utf-8'))


def save_registry(data: dict) -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def list_projects() -> list[dict]:
    return load_registry().get('projects', [])


def get_active_project() -> dict | None:
    registry = load_registry()
    active = registry.get('active_project')

    for project in registry.get('projects', []):
        if project.get('project_id') == active:
            return project

    return None


def select_project(project_id: str) -> dict:
    registry = load_registry()

    for project in registry.get('projects', []):
        if project.get('project_id') == project_id:
            registry['active_project'] = project_id
            save_registry(registry)
            return project

    raise ValueError(f'Unknown project: {project_id}')
