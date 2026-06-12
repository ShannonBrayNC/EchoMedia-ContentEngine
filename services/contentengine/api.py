"""FastAPI scaffold for profile-aware ContentEngine operations.

The API intentionally mirrors the CLI and defaults to dry-run behavior. Provider
calls belong behind renderer adapters and must remain disabled unless explicitly
configured.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .profiles import ProfileRegistry, summarize_profiles
from .renderer import DryRunRenderer

app = FastAPI(title="EchoMedia ContentEngine Runtime", version="0.1.0")
ROOT = Path(".")


class ImageJobRequest(BaseModel):
    profile: str
    scene: str
    brand: str | None = None
    production: str | None = None


class StoryboardRequest(BaseModel):
    profile: str
    title: str
    scenes: list[str] = Field(min_length=1)
    format: str = "short"


def registry() -> ProfileRegistry:
    return ProfileRegistry(ROOT)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "dry-run"}


@app.get("/profiles")
def list_profiles(profile_type: str | None = None, status: str | None = None, tag: str | None = None) -> list[dict[str, Any]]:
    return summarize_profiles(registry().list_profiles(profile_type=profile_type, status=status, tag=tag))


@app.get("/profiles/{profile_id}")
def get_profile(profile_id: str) -> dict[str, Any]:
    try:
        return registry().get_profile(profile_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/image-jobs/dry-run")
def create_image_job(request: ImageJobRequest) -> dict[str, Any]:
    try:
        return registry().build_image_job(request.profile, scene=request.scene, brand=request.brand, production=request.production)
    except (KeyError, PermissionError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/render/dry-run")
def render_dry_run(request: ImageJobRequest) -> dict[str, Any]:
    try:
        job = registry().build_image_job(request.profile, scene=request.scene, brand=request.brand, production=request.production)
        return DryRunRenderer(ROOT).render_image_job(job)
    except (KeyError, PermissionError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/storyboards/dry-run")
def storyboard_dry_run(request: StoryboardRequest) -> dict[str, Any]:
    try:
        return DryRunRenderer(ROOT).export_storyboard(
            profile_id=request.profile,
            project_title=request.title,
            scenes=request.scenes,
            format=request.format,
        )
    except (KeyError, PermissionError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
