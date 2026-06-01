"""Storyboard frame approval workflow for EchoMedia Ad Studio."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .audit import AppendOnlyAuditLogger, AuditEvent


@dataclass(frozen=True)
class SubmitFrameRequest:
    project_name: str
    ad_name: str
    scene_id: str
    source_path: str
    actor: str
    root_path: str = "."
    notes: str = ""


@dataclass(frozen=True)
class ReviewFrameRequest:
    project_name: str
    ad_name: str
    frame_id: str
    actor: str
    approved: bool
    root_path: str = "."
    notes: str = ""


class FrameReviewService:
    def __init__(self, audit_logger: AppendOnlyAuditLogger | None = None):
        self.audit_logger = audit_logger

    def submit_frame(self, request: SubmitFrameRequest) -> dict:
        source = Path(request.source_path)
        if not source.exists():
            raise FileNotFoundError(f"Storyboard frame source does not exist: {source}")
        ad_root = _ad_root(request.root_path, request.project_name, request.ad_name)
        if not ad_root.exists():
            raise FileNotFoundError(f"Ad project does not exist: {ad_root}")

        frame_id = f"frame-{uuid4().hex[:12]}"
        destination = ad_root / "storyboard" / "frames" / "pending" / f"{frame_id}{source.suffix.lower()}"
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        frame = {
            "frame_id": frame_id,
            "scene_id": request.scene_id,
            "filename": destination.name,
            "path": str(destination),
            "state": "pending",
            "submitted_by": request.actor,
            "submitted_at": _now(),
            "reviewed_by": None,
            "reviewed_at": None,
            "notes": request.notes,
        }
        frames = _read_frames(ad_root)
        frames.append(frame)
        _write_frames(ad_root, frames)
        self._audit(request.actor, "storyboard_frame_submitted", request.project_name, request.ad_name, frame_id, {"sceneId": request.scene_id})
        return frame

    def review_frame(self, request: ReviewFrameRequest) -> dict:
        ad_root = _ad_root(request.root_path, request.project_name, request.ad_name)
        frames = _read_frames(ad_root)
        for frame in frames:
            if frame.get("frame_id") == request.frame_id:
                source = Path(frame["path"])
                target_state = "approved" if request.approved else "rejected"
                destination = ad_root / "storyboard" / "frames" / target_state / source.name
                destination.parent.mkdir(parents=True, exist_ok=True)
                if source.exists() and source != destination:
                    shutil.move(str(source), str(destination))
                frame["path"] = str(destination)
                frame["state"] = target_state
                frame["reviewed_by"] = request.actor
                frame["reviewed_at"] = _now()
                frame["notes"] = request.notes or frame.get("notes") or ""
                _write_frames(ad_root, frames)
                _append_approval_log(ad_root, frame)
                self._audit(request.actor, f"storyboard_frame_{target_state}", request.project_name, request.ad_name, request.frame_id, {"sceneId": frame.get("scene_id")})
                return frame
        raise KeyError(f"Frame not found: {request.frame_id}")

    def list_frames(self, project_name: str, ad_name: str, root_path: str = ".") -> dict:
        ad_root = _ad_root(root_path, project_name, ad_name)
        frames = _read_frames(ad_root)
        return {"project": project_name, "ad": ad_name, "frames": frames, "count": len(frames)}

    def _audit(self, actor: str, action: str, project_name: str, ad_name: str, frame_id: str, metadata: dict) -> None:
        if not self.audit_logger:
            return
        self.audit_logger.append(
            AuditEvent(
                actor=actor,
                action=action,
                project_name=project_name,
                ad_name=ad_name,
                target_type="storyboard_frame",
                target_id=frame_id,
                result="success",
                metadata=metadata,
            )
        )


def _ad_root(root_path: str | Path, project_name: str, ad_name: str) -> Path:
    return Path(root_path) / "projects" / project_name / "ads" / ad_name


def _frames_index_path(ad_root: Path) -> Path:
    return ad_root / "metadata" / "frame-index.json"


def _read_frames(ad_root: Path) -> list[dict]:
    path = _frames_index_path(ad_root)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8") or "[]")


def _write_frames(ad_root: Path, frames: list[dict]) -> None:
    path = _frames_index_path(ad_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(frames, indent=2, sort_keys=True), encoding="utf-8")


def _append_approval_log(ad_root: Path, frame: dict) -> None:
    path = ad_root / "metadata" / "approval-log.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"timestamp": _now(), "type": "storyboard_frame_review", "frame": frame}, sort_keys=True) + "\n")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
