"""Dashboard payloads for EchoMedia Ad Studio.

These functions produce UI-friendly summaries without requiring the dashboard to
know the filesystem layout.
"""

from __future__ import annotations

import json
from pathlib import Path


DASHBOARD_TABS = [
    "Production Brief",
    "Script",
    "Storyboard",
    "References",
    "Website Mockups",
    "Audio",
    "Logo Assets",
    "Approvals",
    "Exports",
]


def get_ad_dashboard(project_name: str, ad_name: str, root_path: str = ".") -> dict:
    ad_root = Path(root_path) / "projects" / project_name / "ads" / ad_name
    if not ad_root.exists():
        raise FileNotFoundError(f"Ad project does not exist: {ad_root}")

    assets = _read_json(ad_root / "metadata" / "asset-index.json", [])
    scenes = _read_json(ad_root / "metadata" / "scene-index.json", [])
    frames = _read_json(ad_root / "metadata" / "frame-index.json", [])
    approved_frames = [frame for frame in frames if frame.get("state") == "approved"]
    approved_audio = _count_files(ad_root / "audio" / "vanessa-lines") + _count_files(ad_root / "audio" / "christina-lines")
    exports = _list_exports(ad_root)
    missing_assets = _missing_assets(ad_root, assets, frames)

    return {
        "project": project_name,
        "ad": ad_name,
        "status": _status(len(scenes), len(approved_frames), len(exports)),
        "format": "Instagram Reel / Story / Feed",
        "durationSeconds": sum(int(scene.get("duration_seconds", 0)) for scene in scenes),
        "tabs": DASHBOARD_TABS,
        "counts": {
            "references": len(assets),
            "approvedReferences": len([asset for asset in assets if asset.get("approved")]),
            "scenes": len(scenes),
            "frames": len(frames),
            "approvedFrames": len(approved_frames),
            "approvedAudio": approved_audio,
            "exports": len(exports),
        },
        "missingAssets": missing_assets,
        "nextBestAction": _next_best_action(assets, scenes, approved_frames, exports),
        "paths": {
            "adRoot": str(ad_root),
            "assetIndex": str(ad_root / "metadata" / "asset-index.json"),
            "sceneIndex": str(ad_root / "metadata" / "scene-index.json"),
            "frameIndex": str(ad_root / "metadata" / "frame-index.json"),
        },
    }


def _read_json(path: Path, default):
    if not path.exists():
        return default
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return default
    return json.loads(raw)


def _count_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.iterdir() if item.is_file() and item.name != ".gitkeep")


def _list_exports(ad_root: Path) -> list[str]:
    exports_root = ad_root / "exports"
    if not exports_root.exists():
        return []
    return [str(path) for path in exports_root.rglob("publish-manifest.json")]


def _missing_assets(ad_root: Path, assets: list[dict], frames: list[dict]) -> list[str]:
    missing = []
    if not assets:
        missing.append("Vanessa reference uploads")
    if not any(asset.get("outfit") == "pink-updated-outfit" or "pink-updated-outfit" in (asset.get("tags") or []) for asset in assets):
        missing.append("pink outfit reference")
    if not any(frame.get("state") == "approved" for frame in frames):
        missing.append("approved storyboard frames")
    if not any((ad_root / "website-mockups" / "approved").glob("*")):
        missing.append("approved website mockups")
    if not any((ad_root / "logo-assets" / "lockups").glob("*")):
        missing.append("EchoMedia/Lantern logo lockup")
    return missing


def _status(scene_count: int, approved_frame_count: int, export_count: int) -> str:
    if export_count:
        return "Exported"
    if approved_frame_count >= max(scene_count, 1):
        return "Ready for Export"
    if approved_frame_count:
        return "Storyboard Review"
    return "Storyboard Draft"


def _next_best_action(assets: list[dict], scenes: list[dict], approved_frames: list[dict], exports: list[str]) -> str:
    if not assets:
        return "Upload Vanessa reference images."
    if not approved_frames:
        return "Submit and approve storyboard frames."
    if len(approved_frames) < len(scenes):
        return "Approve remaining storyboard frames."
    if not exports:
        return "Create publish-ready export package."
    return "Review final export package."
