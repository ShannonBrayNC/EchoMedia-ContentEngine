from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "projects/project-registry.json"

DEFAULT_REGISTRY = {
    "active_project": None,
    "projects": [],
}


def load_registry() -> dict:
    if not REGISTRY_PATH.exists():
        return DEFAULT_REGISTRY.copy()

    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def save_registry(data: dict) -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def register_project(project_id: str, project_path: str, project_type: str) -> dict:
    registry = load_registry()

    existing = next((p for p in registry["projects"] if p["project_id"] == project_id), None)

    if existing:
        return existing

    project = {
        "project_id": project_id,
        "project_path": project_path,
        "project_type": project_type,
        "status": "active",
        "created_at": datetime.now(UTC).isoformat(),
        "last_opened": datetime.now(UTC).isoformat(),
    }

    registry["projects"].append(project)

    if not registry.get("active_project"):
        registry["active_project"] = project_id

    save_registry(registry)

    return project


def list_projects() -> list[dict]:
    return load_registry().get("projects", [])


def set_active_project(project_id: str) -> dict:
    registry = load_registry()

    project = next((p for p in registry["projects"] if p["project_id"] == project_id), None)

    if not project:
        raise ValueError(f"Unknown project: {project_id}")

    project["last_opened"] = datetime.now(UTC).isoformat()
    registry["active_project"] = project_id

    save_registry(registry)

    return project


def get_active_project() -> dict | None:
    registry = load_registry()
    active = registry.get("active_project")

    if not active:
        return None

    return next((p for p in registry["projects"] if p["project_id"] == active), None)
