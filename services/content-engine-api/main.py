from __future__ import annotations

import json
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[2]
AUDIT_LOG = ROOT / "reports/api-audit-log.jsonl"

ROLE_PERMISSIONS = {
    "admin": {
        "validate-canon",
        "audit-continuity",
        "build-chapter-packet",
        "assemble-screenplay",
        "build-export-package",
        "create-release",
        "read-status",
    },
    "christina": {
        "validate-canon",
        "audit-continuity",
        "build-chapter-packet",
        "assemble-screenplay",
        "build-export-package",
        "create-release",
        "read-status",
    },
    "creator": {
        "validate-canon",
        "audit-continuity",
        "build-chapter-packet",
        "assemble-screenplay",
        "build-export-package",
        "read-status",
    },
    "reviewer": {
        "validate-canon",
        "audit-continuity",
        "read-status",
    },
    "automation": {
        "validate-canon",
        "audit-continuity",
        "assemble-screenplay",
        "build-export-package",
        "read-status",
    },
}

app = FastAPI(title="EchoMedia Content Engine API", version="0.1.0")


class Principal(BaseModel):
    name: str
    role: str
    project_scope: Optional[str] = None


class ProjectRequest(BaseModel):
    project_root: str


class ChapterPacketRequest(BaseModel):
    project_root: str
    chapter_number: int
    chapter_title: str


class ReleaseRequest(BaseModel):
    project_root: str
    version: str
    release_state: str = "candidate"


class ExportPackageRequest(BaseModel):
    project_root: str
    package_type: str = "author-review"


class CanonValidationRequest(BaseModel):
    manifest_path: str


class ContinuityAuditRequest(BaseModel):
    target_path: str
    fail_under: int = 70


def parse_static_token(raw_token: str) -> Optional[Principal]:
    token_map_raw = os.getenv("CONTENT_ENGINE_API_TOKENS", "")
    if not token_map_raw:
        return None

    for entry in token_map_raw.split(","):
        parts = entry.strip().split(":")
        if len(parts) < 3:
            continue
        token, role, name = parts[:3]
        project_scope = parts[3] if len(parts) >= 4 else None
        if raw_token == token:
            return Principal(name=name, role=role, project_scope=project_scope)

    return None


def get_principal(
    authorization: Annotated[Optional[str], Header()] = None,
    x_content_engine_role: Annotated[Optional[str], Header()] = None,
    x_content_engine_user: Annotated[Optional[str], Header()] = None,
    x_content_engine_project: Annotated[Optional[str], Header()] = None,
) -> Principal:
    if authorization and authorization.lower().startswith("bearer "):
        raw_token = authorization.split(" ", 1)[1]
        principal = parse_static_token(raw_token)
        if principal:
            return principal

    allow_dev_headers = os.getenv("CONTENT_ENGINE_ALLOW_DEV_HEADERS", "true").lower() == "true"
    if allow_dev_headers and x_content_engine_role:
        return Principal(
            name=x_content_engine_user or "dev-user",
            role=x_content_engine_role,
            project_scope=x_content_engine_project,
        )

    raise HTTPException(status_code=401, detail="Authentication required")


def require_permission(permission: str):
    def dependency(principal: Principal = Depends(get_principal)) -> Principal:
        allowed = ROLE_PERMISSIONS.get(principal.role, set())
        if permission not in allowed:
            raise HTTPException(status_code=403, detail=f"Role {principal.role} cannot perform {permission}")
        return principal

    return dependency


def assert_project_scope(principal: Principal, project_root: str) -> None:
    if not principal.project_scope:
        return
    normalized = project_root.replace("\\", "/")
    scope = principal.project_scope.replace("\\", "/")
    if not normalized.startswith(scope):
        raise HTTPException(status_code=403, detail="Project outside principal scope")


def audit_event(principal: Principal, action: str, target: str, result: dict) -> None:
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(UTC).isoformat(),
        "principal": principal.model_dump(),
        "action": action,
        "target": target,
        "ok": result.get("ok", True),
        "returncode": result.get("returncode"),
    }
    with AUDIT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event) + "\n")


def run_python(script: str, args: list[str]) -> dict:
    script_path = ROOT / script
    command = ["python", str(script_path), *args]
    result = subprocess.run(command, capture_output=True, text=True, cwd=ROOT)
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "ok": result.returncode == 0,
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "content-engine-api"}


@app.get("/auth/me")
def auth_me(principal: Principal = Depends(get_principal)) -> dict:
    return {"principal": principal.model_dump(), "permissions": sorted(ROLE_PERMISSIONS.get(principal.role, set()))}


@app.post("/projects/validate-canon")
def validate_canon(
    request: CanonValidationRequest,
    principal: Principal = Depends(require_permission("validate-canon")),
) -> dict:
    result = run_python("services/canon-validator/validate_canon.py", [request.manifest_path])
    audit_event(principal, "validate-canon", request.manifest_path, result)
    return result


@app.post("/projects/audit-continuity")
def audit_continuity(
    request: ContinuityAuditRequest,
    principal: Principal = Depends(require_permission("audit-continuity")),
) -> dict:
    result = run_python(
        "services/continuity-engine/audit_continuity.py",
        [request.target_path, "--fail-under", str(request.fail_under)],
    )
    audit_event(principal, "audit-continuity", request.target_path, result)
    return result


@app.post("/projects/build-chapter-packet")
def build_chapter_packet(
    request: ChapterPacketRequest,
    principal: Principal = Depends(require_permission("build-chapter-packet")),
) -> dict:
    assert_project_scope(principal, request.project_root)
    result = run_python(
        "services/chapter-engine/build_chapter_packet.py",
        [request.project_root, str(request.chapter_number), request.chapter_title],
    )
    audit_event(principal, "build-chapter-packet", request.project_root, result)
    return result


@app.post("/projects/assemble-screenplay")
def assemble_screenplay(
    request: ProjectRequest,
    principal: Principal = Depends(require_permission("assemble-screenplay")),
) -> dict:
    assert_project_scope(principal, request.project_root)
    result = run_python("services/screenplay-assembler/assemble_screenplay.py", [request.project_root])
    audit_event(principal, "assemble-screenplay", request.project_root, result)
    return result


@app.post("/projects/build-export-package")
def build_export_package(
    request: ExportPackageRequest,
    principal: Principal = Depends(require_permission("build-export-package")),
) -> dict:
    assert_project_scope(principal, request.project_root)
    result = run_python(
        "services/export-packager/build_export_package.py",
        [request.project_root, request.package_type],
    )
    audit_event(principal, "build-export-package", request.project_root, result)
    return result


@app.post("/projects/create-release")
def create_release(
    request: ReleaseRequest,
    principal: Principal = Depends(require_permission("create-release")),
) -> dict:
    assert_project_scope(principal, request.project_root)
    result = run_python(
        "services/release-manager/create_release_manifest.py",
        [request.project_root, request.version, request.release_state],
    )
    audit_event(principal, "create-release", request.project_root, result)
    return result


@app.get("/projects/status")
def project_status(
    project_root: str,
    project_name: Optional[str] = None,
    principal: Principal = Depends(require_permission("read-status")),
) -> dict:
    assert_project_scope(principal, project_root)
    root = ROOT / project_root
    result = {
        "project": project_name or root.name,
        "project_root": str(root),
        "exists": root.exists(),
        "has_canon": (root / "canon").exists(),
        "has_manuscript": (root / "manuscript").exists(),
        "has_screenplay": (root / "screenplay").exists(),
        "has_releases": (root / "releases").exists(),
    }
    audit_event(principal, "read-status", project_root, {"ok": True})
    return result
