#!/usr/bin/env python3
"""No-provider Content Engine API service.

This service intentionally uses only the Python standard library so Sprint 4 can
run in CI without provider credentials or framework dependencies. It provides a
small HTTP API plus reusable functions for deterministic E2E tests.
"""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
STATE_ROOT = Path(os.environ.get("CONTENT_ENGINE_STATE_ROOT", ROOT / ".content-engine" / "state"))
STATE_FILE = STATE_ROOT / "content-engine-state.json"
SUPPORTED_GENERATION_TYPES = [
    "idea-intake",
    "production-package",
    "screenplay-scene",
    "storyboard-pack",
    "visual-prompt-pack",
    "voice-script",
    "video-package",
    "pitch-package",
]
ARTIFACT_STATES_READY = {"review", "approved", "exported", "released", "planned"}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def now_id(prefix: str) -> str:
    return f"{prefix}-{int(time.time() * 1000)}"


def load_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        return {"projects": {}, "artifacts": {}, "jobs": {}, "exports": {}}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def save_state(state: dict[str, Any]) -> None:
    STATE_ROOT.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def reset_state() -> None:
    if STATE_FILE.exists():
        STATE_FILE.unlink()


def project_summary(project: dict[str, Any]) -> dict[str, Any]:
    return {
        "projectId": project["projectId"],
        "displayTitle": project["displayTitle"],
        "status": project.get("status", "planning"),
        "rootPath": project["rootPath"],
        "supportedGenerationTypes": project.get("supportedGenerationTypes", SUPPORTED_GENERATION_TYPES),
        "exportTargets": project.get("exportTargets", ["generic-json"]),
    }


def create_project(payload: dict[str, Any]) -> dict[str, Any]:
    state = load_state()
    display_title = payload.get("displayTitle") or payload.get("title") or "Untitled Project"
    project_id = slugify(payload.get("projectId") or display_title)
    root_path = f"projects/{project_id}"
    folders = [
        "canon",
        "characters",
        "story",
        "manuscript",
        "storyboards",
        "visual-bible",
        "screenplay",
        "movie-generation",
        "audio",
        "pitch",
        "reports",
    ]
    project = {
        "projectId": project_id,
        "displayTitle": display_title,
        "universe": payload.get("universe", ""),
        "storyType": payload.get("storyType", "novel-to-film"),
        "status": "planning",
        "rootPath": root_path,
        "supportedGenerationTypes": SUPPORTED_GENERATION_TYPES,
        "exportTargets": payload.get("targetFormats") or ["generic-json"],
        "folders": [f"{root_path}/{folder}/" for folder in folders],
        "starterArtifacts": [
            {"artifactType": "project-manifest", "path": f"{root_path}/project.json", "state": "planned"},
            {"artifactType": "idea-intake", "path": f"{root_path}/story/idea-intake.md", "state": "planned"},
            {"artifactType": "canon-seed", "path": f"{root_path}/canon/canon-seed.md", "state": "planned"},
            {"artifactType": "character-seed", "path": f"{root_path}/characters/character-seed.md", "state": "planned"},
            {"artifactType": "readiness-checklist", "path": f"{root_path}/reports/readiness-checklist.md", "state": "planned"},
        ],
        "nextSteps": ["Load idea intake", "Add canon seed", "Add character seed", "Generate outline", "Run readiness check"],
    }
    state["projects"][project_id] = project
    save_state(state)
    return {"project": project_summary(project), "folders": project["folders"], "starterArtifacts": project["starterArtifacts"], "nextSteps": project["nextSteps"]}


def list_projects() -> dict[str, Any]:
    state = load_state()
    return {"projects": [project_summary(project) for project in state["projects"].values()]}


def get_project(project_id: str) -> dict[str, Any]:
    state = load_state()
    if project_id not in state["projects"]:
        raise KeyError("Project not found")
    return project_summary(state["projects"][project_id])


def create_idea_intake(project_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    state = load_state()
    if project_id not in state["projects"]:
        raise KeyError("Project not found")
    raw_input = (payload.get("rawInput") or "").strip()
    direction = (payload.get("direction") or "Extract story structure, canon candidates, character seeds, and production roadmap.").strip()
    if not raw_input:
        raise ValueError("rawInput is required")
    first_sentence = re.split(r"[.!?]", raw_input)[0].strip() or "Untitled idea"
    artifact_id = now_id("idea")
    root_path = state["projects"][project_id]["rootPath"]
    preview = f"# Idea Intake Draft\n\nProject: {project_id}\n\n## Summary\n{first_sentence}.\n\n## Direction\n{direction}\n\n## Canon candidates\n- Define the governing technology.\n- Define the political pressure system.\n- Define the personal cost.\n\nDraft only. Nothing is promoted to canon until reviewed."
    artifact = {
        "artifactId": artifact_id,
        "projectId": project_id,
        "artifactType": "idea-intake",
        "state": "review",
        "path": f"{root_path}/story/idea-intake.md",
        "manifestId": f"manifest-{artifact_id}",
        "preview": preview,
        "rawInput": raw_input,
        "direction": direction,
        "sourceRefs": ["raw-input:idea-intake"],
        "templateVersion": "idea-intake-template@1.0.0-draft",
        "contextManifestId": f"context-{project_id}-mock",
    }
    state["artifacts"][artifact_id] = artifact
    save_state(state)
    return artifact


def create_generation_job(payload: dict[str, Any]) -> dict[str, Any]:
    state = load_state()
    project_id = payload.get("projectId")
    artifact_type = payload.get("artifactType")
    if project_id not in state["projects"]:
        raise KeyError("Project not found")
    if not artifact_type:
        raise ValueError("artifactType is required")
    job_id = now_id("job")
    artifact_id = now_id("artifact")
    root_path = state["projects"][project_id]["rootPath"]
    preview = f"# Draft {artifact_type}\n\nProject: {project_id}\n\nDirection: {payload.get('userDirection', 'No direction supplied.')}\n\nThis deterministic no-provider artifact is waiting for review before export."
    artifact = {
        "artifactId": artifact_id,
        "projectId": project_id,
        "artifactType": artifact_type,
        "state": "review",
        "path": f"{root_path}/.content-engine/drafts/{artifact_id}.md",
        "manifestId": f"manifest-{artifact_id}",
        "preview": preview,
        "sourceRefs": payload.get("sourceRefs", []),
        "templateVersion": f"{artifact_type}-template@1.0.0-draft",
        "contextManifestId": f"context-{project_id}-mock",
        "generationJobId": job_id,
    }
    job = {
        "jobId": job_id,
        "projectId": project_id,
        "artifactType": artifact_type,
        "status": "needs-review",
        "progress": 100,
        "artifactIds": [artifact_id],
        "warnings": ["No-provider deterministic generation."],
        "correlationId": f"trace-{job_id}",
    }
    state["artifacts"][artifact_id] = artifact
    state["jobs"][job_id] = job
    save_state(state)
    return job


def get_job(job_id: str) -> dict[str, Any]:
    state = load_state()
    if job_id not in state["jobs"]:
        raise KeyError("Job not found")
    return state["jobs"][job_id]


def list_artifacts(project_id: str) -> dict[str, Any]:
    state = load_state()
    artifacts = [artifact_summary(a) for a in state["artifacts"].values() if a["projectId"] == project_id]
    return {"artifacts": artifacts}


def artifact_summary(artifact: dict[str, Any]) -> dict[str, Any]:
    return {key: artifact.get(key) for key in ["artifactId", "projectId", "artifactType", "state", "path", "manifestId"]}


def get_artifact(artifact_id: str) -> dict[str, Any]:
    state = load_state()
    if artifact_id not in state["artifacts"]:
        raise KeyError("Artifact not found")
    return state["artifacts"][artifact_id]


def set_artifact_state(artifact_id: str, new_state: str) -> dict[str, Any]:
    state = load_state()
    if artifact_id not in state["artifacts"]:
        raise KeyError("Artifact not found")
    state["artifacts"][artifact_id]["state"] = new_state
    save_state(state)
    return artifact_summary(state["artifacts"][artifact_id])


def get_preview(artifact_id: str, mode: str = "markdown") -> dict[str, Any]:
    artifact = get_artifact(artifact_id)
    preview = artifact.get("preview", "")
    if mode in {"json", "manifest"}:
        preview = json.dumps({"artifact": artifact_summary(artifact), "manifestId": artifact.get("manifestId")}, indent=2)
    elif mode == "text":
        preview = re.sub(r"[#*`]", "", preview)
    elif mode == "timeline":
        preview = "00:00 - 00:05 Mock opening beat\n00:05 - 00:12 Draft review segment"
    elif mode.endswith("-ref"):
        preview = f"{mode} preview\nPath: {artifact.get('path')}\nState: {artifact.get('state')}"
    return {"artifactId": artifact_id, "mode": mode, "content": preview, "readOnly": True}


def get_traceability(artifact_id: str) -> dict[str, Any]:
    artifact = get_artifact(artifact_id)
    return {
        "artifactId": artifact_id,
        "artifactType": artifact.get("artifactType"),
        "state": artifact.get("state"),
        "sourceRefs": artifact.get("sourceRefs", []),
        "templateVersion": artifact.get("templateVersion"),
        "contextManifestId": artifact.get("contextManifestId"),
        "generationJobId": artifact.get("generationJobId"),
        "manifestId": artifact.get("manifestId"),
        "readinessImpact": f"{artifact.get('artifactType')} is currently {artifact.get('state')}.",
    }


def export_artifact(artifact_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    state = load_state()
    if artifact_id not in state["artifacts"]:
        raise KeyError("Artifact not found")
    artifact = state["artifacts"][artifact_id]
    if artifact["state"] != "approved":
        raise PermissionError("Artifact must be approved before export")
    export_id = now_id("export")
    package = {
        "exportId": export_id,
        "artifactId": artifact_id,
        "projectId": artifact["projectId"],
        "packageType": (payload or {}).get("packageType", "generic-json"),
        "state": "exported",
        "manifestId": f"export-manifest-{export_id}",
        "providerReady": True,
    }
    artifact["state"] = "exported"
    state["exports"][export_id] = package
    save_state(state)
    return package


def get_readiness(project_id: str) -> dict[str, Any]:
    state = load_state()
    if project_id not in state["projects"]:
        raise KeyError("Project not found")
    artifacts = [a for a in state["artifacts"].values() if a["projectId"] == project_id]
    has_idea = any(a["artifactType"] == "idea-intake" for a in artifacts)
    has_approved = any(a["state"] in {"approved", "exported"} for a in artifacts)
    checks = [
        ("project-metadata", "structure", True, "complete", "Create project scaffold"),
        ("folder-structure", "structure", True, "complete", "Create project scaffold"),
        ("idea-intake", "content", has_idea, "needs-review" if has_idea else "missing", "Load ideas"),
        ("canon-seed", "content", False, "missing", "Promote reviewed idea facts to canon seed"),
        ("character-seed", "content", False, "missing", "Generate character seed"),
        ("story-outline", "content", False, "missing", "Generate story outline"),
        ("production-package", "content", has_approved, "complete" if has_approved else "missing", "Generate and approve production package"),
        ("voice-readiness", "export", False, "missing", "Create voice package"),
        ("visual-readiness", "export", False, "missing", "Create visual prompt pack"),
        ("export-profile", "export", False, "missing", "Select export profile"),
        ("review-approval", "export", has_approved, "complete" if has_approved else "needs-review", "Approve required draft artifacts"),
    ]
    items = [{"id": i, "category": c, "label": i.replace("-", " ").title(), "complete": complete, "status": status, "nextAction": action} for i, c, complete, status, action in checks]
    complete_count = sum(1 for item in items if item["complete"])
    first_incomplete = next((item for item in items if not item["complete"]), None)
    return {
        "projectId": project_id,
        "percent": round((complete_count / len(items)) * 100),
        "summary": f"{complete_count} of {len(items)} readiness items complete.",
        "items": items,
        "blockers": [],
        "nextBestAction": first_incomplete["nextAction"] if first_incomplete else "All readiness items complete.",
    }


def get_inventory(project_id: str) -> dict[str, Any]:
    state = load_state()
    if project_id not in state["projects"]:
        raise KeyError("Project not found")
    root = state["projects"][project_id]["rootPath"]
    artifacts = [a for a in state["artifacts"].values() if a["projectId"] == project_id]
    by_type = {a["artifactType"]: a for a in artifacts}
    required_types = ["idea-intake", "canon-seed", "character-seed", "story-outline", "screenplay-scene", "production-package", "visual-prompt-pack", "voice-script", "scene-timeline", "export-manifest"]
    definitions = [
        ("idea-intake", "Idea intake", "idea intake", f"{root}/story/idea-intake.md"),
        ("canon-seed", "Canon seed", "canon", f"{root}/canon/canon-seed.md"),
        ("character-seed", "Character seed", "characters", f"{root}/characters/character-seed.md"),
        ("story-outline", "Story outline", "story outline", f"{root}/story/story-outline.md"),
        ("manuscript", "Manuscript draft", "manuscript", f"{root}/manuscript/"),
        ("screenplay-scene", "Screenplay scene package", "screenplay", f"{root}/screenplay/"),
        ("production-package", "Production package", "production package", f"{root}/movie-generation/production-package.json"),
        ("visual-prompt-pack", "Visual prompt pack", "visual prompts", f"{root}/visual-bible/visual-prompt-pack.json"),
        ("voice-script", "Voice package", "voice packages", f"{root}/audio/voice-package.json"),
        ("scene-timeline", "Scene timeline", "timelines", f"{root}/timelines/"),
        ("export-manifest", "Export manifest", "export manifests", f"{root}/provider-manifests/"),
        ("release-package", "Release package", "release package", f"{root}/release/"),
    ]
    items = []
    for artifact_type, label, category, path in definitions:
        artifact = by_type.get(artifact_type)
        required = artifact_type in required_types
        state_value = artifact["state"] if artifact else "missing"
        actions = ["preview", "review", "export"] if artifact else ["generate"]
        items.append({
            "artifactId": artifact.get("artifactId") if artifact else f"missing-{artifact_type}",
            "label": label,
            "category": category,
            "artifactType": artifact_type,
            "state": state_value,
            "required": required,
            "path": artifact.get("path") if artifact else path,
            "readinessImpact": "Required before polished export." if required else "Optional project output.",
            "actions": actions,
        })
    required_items = [item for item in items if item["required"]]
    complete_required = [item for item in required_items if item["state"] in ARTIFACT_STATES_READY]
    return {"projectId": project_id, "items": items, "requiredCount": len(required_items), "completeRequiredCount": len(complete_required), "summary": f"{len(complete_required)} of {len(required_items)} required artifacts are present or planned."}


@dataclass
class RouteResult:
    status: int
    body: dict[str, Any]


class Handler(BaseHTTPRequestHandler):
    def _json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("content-length", 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def _send(self, result: RouteResult) -> None:
        body = json.dumps(result.body).encode("utf-8")
        self.send_response(result.status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        self._send(route("GET", self.path, {}))

    def do_POST(self) -> None:  # noqa: N802
        self._send(route("POST", self.path, self._json_body()))

    def log_message(self, format: str, *args: Any) -> None:
        if os.environ.get("CONTENT_ENGINE_LOG_LEVEL", "info") == "debug":
            super().log_message(format, *args)


def route(method: str, raw_path: str, payload: dict[str, Any]) -> RouteResult:
    parsed = urlparse(raw_path)
    path = parsed.path
    query = parse_qs(parsed.query)
    try:
        if method == "GET" and path == "/health":
            return RouteResult(200, {"status": "ok", "version": "1.0.0-draft"})
        if method == "GET" and path == "/config/runtime":
            return RouteResult(200, {"environment": os.environ.get("CONTENT_ENGINE_ENV", "local"), "noProviderMode": True, "liveProvidersEnabled": False, "dryRunProviders": True})
        if method == "GET" and path == "/projects":
            return RouteResult(200, list_projects())
        if method == "POST" and path == "/projects":
            return RouteResult(201, create_project(payload))
        parts = [part for part in path.split("/") if part]
        if method == "GET" and len(parts) == 2 and parts[0] == "projects":
            return RouteResult(200, get_project(parts[1]))
        if method == "POST" and len(parts) == 3 and parts[0] == "projects" and parts[2] == "idea-intake":
            return RouteResult(201, create_idea_intake(parts[1], payload))
        if method == "GET" and len(parts) == 3 and parts[0] == "projects" and parts[2] == "readiness":
            return RouteResult(200, get_readiness(parts[1]))
        if method == "GET" and len(parts) == 3 and parts[0] == "projects" and parts[2] == "artifact-inventory":
            return RouteResult(200, get_inventory(parts[1]))
        if method == "GET" and len(parts) == 3 and parts[0] == "projects" and parts[2] == "artifacts":
            return RouteResult(200, list_artifacts(parts[1]))
        if method == "POST" and path == "/generation/jobs":
            return RouteResult(202, create_generation_job(payload))
        if method == "GET" and len(parts) == 3 and parts[:2] == ["generation", "jobs"]:
            return RouteResult(200, get_job(parts[2]))
        if method == "GET" and len(parts) == 2 and parts[0] == "artifacts":
            return RouteResult(200, artifact_summary(get_artifact(parts[1])))
        if method == "GET" and len(parts) == 3 and parts[0] == "artifacts" and parts[2] == "preview":
            return RouteResult(200, get_preview(parts[1], query.get("mode", ["markdown"])[0]))
        if method == "GET" and len(parts) == 3 and parts[0] == "artifacts" and parts[2] == "traceability":
            return RouteResult(200, get_traceability(parts[1]))
        if method == "POST" and len(parts) == 3 and parts[0] == "reviews":
            states = {"approve": "approved", "reject": "rejected", "request-revision": "needs-revision", "supersede": "superseded"}
            if parts[2] in states:
                return RouteResult(200, set_artifact_state(parts[1], states[parts[2]]))
        if method == "POST" and len(parts) == 3 and parts[0] == "exports" and parts[1] == "packages":
            return RouteResult(202, export_artifact(parts[2], payload))
        return RouteResult(404, {"error": {"code": "not_found", "message": f"No route for {method} {path}"}})
    except PermissionError as exc:
        return RouteResult(409, {"error": {"code": "review_gate", "message": str(exc)}})
    except KeyError as exc:
        return RouteResult(404, {"error": {"code": "not_found", "message": str(exc)}})
    except ValueError as exc:
        return RouteResult(400, {"error": {"code": "bad_request", "message": str(exc)}})


def run_server() -> None:
    host = os.environ.get("CONTENT_ENGINE_API_HOST", "127.0.0.1")
    port = int(os.environ.get("CONTENT_ENGINE_API_PORT", "8080"))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Content Engine API listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
