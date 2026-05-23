from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[2]

app = FastAPI(title="EchoMedia Content Engine API", version="0.1.0")


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


@app.post("/projects/validate-canon")
def validate_canon(request: CanonValidationRequest) -> dict:
    return run_python(
        "services/canon-validator/validate_canon.py",
        [request.manifest_path],
    )


@app.post("/projects/audit-continuity")
def audit_continuity(request: ContinuityAuditRequest) -> dict:
    return run_python(
        "services/continuity-engine/audit_continuity.py",
        [request.target_path, "--fail-under", str(request.fail_under)],
    )


@app.post("/projects/build-chapter-packet")
def build_chapter_packet(request: ChapterPacketRequest) -> dict:
    return run_python(
        "services/chapter-engine/build_chapter_packet.py",
        [request.project_root, str(request.chapter_number), request.chapter_title],
    )


@app.post("/projects/assemble-screenplay")
def assemble_screenplay(request: ProjectRequest) -> dict:
    return run_python(
        "services/screenplay-assembler/assemble_screenplay.py",
        [request.project_root],
    )


@app.post("/projects/build-export-package")
def build_export_package(request: ExportPackageRequest) -> dict:
    return run_python(
        "services/export-packager/build_export_package.py",
        [request.project_root, request.package_type],
    )


@app.post("/projects/create-release")
def create_release(request: ReleaseRequest) -> dict:
    return run_python(
        "services/release-manager/create_release_manifest.py",
        [request.project_root, request.version, request.release_state],
    )


@app.get("/projects/status")
def project_status(project_root: str, project_name: Optional[str] = None) -> dict:
    root = ROOT / project_root
    return {
        "project": project_name or root.name,
        "project_root": str(root),
        "exists": root.exists(),
        "has_canon": (root / "canon").exists(),
        "has_manuscript": (root / "manuscript").exists(),
        "has_screenplay": (root / "screenplay").exists(),
        "has_releases": (root / "releases").exists(),
    }
