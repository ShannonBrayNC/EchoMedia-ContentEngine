"""Asset upload and tagging services for EchoMedia Ad Studio.

This module supports the API/dashboard sprint by copying Vanessa reference
images into ad-project folders, maintaining asset metadata, and tagging assets
by outfit, pose, expression, scene, and quality signals.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from uuid import uuid4

from .audit import AppendOnlyAuditLogger, AuditEvent


@dataclass(frozen=True)
class UploadReferenceRequest:
    project_name: str
    ad_name: str
    source_path: str
    actor: str
    root_path: str = "."
    tags: list[str] = field(default_factory=list)
    outfit: str | None = None
    expression: str | None = None
    pose: str | None = None
    scene_candidates: list[str] = field(default_factory=list)
    quality_score: float | None = None
    notes: str = ""


@dataclass(frozen=True)
class TagAssetRequest:
    project_name: str
    ad_name: str
    asset_id: str
    actor: str
    root_path: str = "."
    tags: list[str] = field(default_factory=list)
    outfit: str | None = None
    expression: str | None = None
    pose: str | None = None
    scene_candidates: list[str] = field(default_factory=list)
    quality_score: float | None = None
    notes: str | None = None
    approved: bool | None = None


class AssetService:
    def __init__(self, audit_logger: AppendOnlyAuditLogger | None = None):
        self.audit_logger = audit_logger

    def upload_reference(self, request: UploadReferenceRequest) -> dict:
        source = Path(request.source_path)
        if not source.exists():
            raise FileNotFoundError(f"Source asset does not exist: {source}")

        ad_root = _ad_root(request.root_path, request.project_name, request.ad_name)
        if not ad_root.exists():
            raise FileNotFoundError(f"Ad project does not exist: {ad_root}")

        asset_id = f"asset-{uuid4().hex[:12]}"
        destination = ad_root / "references" / "raw-uploads" / f"{asset_id}{source.suffix.lower()}"
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

        metadata = {
            "asset_id": asset_id,
            "project": request.project_name,
            "ad_project": request.ad_name,
            "filename": destination.name,
            "original_filename": source.name,
            "sha256": _sha256(destination),
            "source_path": str(destination),
            "approved": False,
            "approval_state": "pending",
            "tags": sorted(set(request.tags)),
            "outfit": request.outfit,
            "expression": request.expression,
            "pose": request.pose,
            "scene_candidates": request.scene_candidates,
            "quality_score": request.quality_score,
            "notes": request.notes,
            "uploaded_at": _now(),
            "updated_at": _now(),
        }
        assets = _read_asset_index(ad_root)
        assets.append(metadata)
        _write_asset_index(ad_root, assets)
        self._audit(request.actor, "reference_uploaded", request.project_name, request.ad_name, asset_id, {"path": str(destination), "tags": metadata["tags"]})
        return metadata

    def tag_asset(self, request: TagAssetRequest) -> dict:
        ad_root = _ad_root(request.root_path, request.project_name, request.ad_name)
        assets = _read_asset_index(ad_root)
        for asset in assets:
            if asset.get("asset_id") == request.asset_id:
                asset["tags"] = sorted(set((asset.get("tags") or []) + request.tags))
                if request.outfit is not None:
                    asset["outfit"] = request.outfit
                if request.expression is not None:
                    asset["expression"] = request.expression
                if request.pose is not None:
                    asset["pose"] = request.pose
                if request.scene_candidates:
                    asset["scene_candidates"] = sorted(set((asset.get("scene_candidates") or []) + request.scene_candidates))
                if request.quality_score is not None:
                    asset["quality_score"] = request.quality_score
                if request.notes is not None:
                    asset["notes"] = request.notes
                if request.approved is not None:
                    asset["approved"] = request.approved
                    asset["approval_state"] = "approved" if request.approved else "pending"
                asset["updated_at"] = _now()
                _write_asset_index(ad_root, assets)
                self._audit(request.actor, "asset_tagged", request.project_name, request.ad_name, request.asset_id, {"tags": asset.get("tags", [])})
                return asset
        raise KeyError(f"Asset not found: {request.asset_id}")

    def list_assets(self, project_name: str, ad_name: str, root_path: str = ".") -> dict:
        ad_root = _ad_root(root_path, project_name, ad_name)
        assets = _read_asset_index(ad_root)
        return {"project": project_name, "ad": ad_name, "assets": assets, "count": len(assets)}

    def _audit(self, actor: str, action: str, project_name: str, ad_name: str, asset_id: str, metadata: dict) -> None:
        if not self.audit_logger:
            return
        self.audit_logger.append(
            AuditEvent(
                actor=actor,
                action=action,
                project_name=project_name,
                ad_name=ad_name,
                target_type="asset",
                target_id=asset_id,
                result="success",
                metadata=metadata,
            )
        )


def _ad_root(root_path: str | Path, project_name: str, ad_name: str) -> Path:
    return Path(root_path) / "projects" / project_name / "ads" / ad_name


def _asset_index_path(ad_root: Path) -> Path:
    return ad_root / "metadata" / "asset-index.json"


def _read_asset_index(ad_root: Path) -> list[dict]:
    path = _asset_index_path(ad_root)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8") or "[]")


def _write_asset_index(ad_root: Path, assets: list[dict]) -> None:
    path = _asset_index_path(ad_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(assets, indent=2, sort_keys=True), encoding="utf-8")


def _sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
