"""Dry-run renderer adapter for profile-driven image and video jobs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .profiles import ProfileRegistry, utc_now


class DryRunRenderer:
    """Writes deterministic manifests without calling paid or local media providers."""

    def __init__(self, root: Path | str = ".", adapter_name: str = "manual-export") -> None:
        self.root = Path(root)
        self.adapter_name = adapter_name
        self.registry = ProfileRegistry(self.root)

    def render_image_job(self, job: dict[str, Any]) -> dict[str, Any]:
        prompt_hash = hashlib.sha256(job["prompt"].encode("utf-8")).hexdigest()[:16]
        output_id = f"out-{job['jobId']}-{prompt_hash}"
        output_dir = self.root / "generated" / "outputs" / output_id
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest = {
            "schema": "lantern.contentengine.outputManifest.v1",
            "outputId": output_id,
            "jobId": job["jobId"],
            "createdAt": utc_now(),
            "mode": "dry-run",
            "renderer": self.adapter_name,
            "seed": prompt_hash,
            "profileIds": job.get("profileIds", []),
            "profileVersions": job.get("profileVersions", {}),
            "referencesUsed": job.get("referencesUsed", []),
            "promptHash": prompt_hash,
            "prompt": job["prompt"],
            "negativePrompt": job.get("negativePrompt", ""),
            "generatedFilePath": None,
            "reviewStatus": "pending",
            "rejectionReason": None,
        }
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=False) + "\n", encoding="utf-8")
        self.registry.emit_event(
            "output.generated",
            {"id": job["subjectProfileId"], "version": job["profileVersions"][job["subjectProfileId"]]},
            extra={"jobId": job["jobId"], "outputId": output_id, "dryRun": True},
        )
        return manifest

    def export_storyboard(self, *, profile_id: str, project_title: str, scenes: list[str], format: str = "short") -> dict[str, Any]:
        profile = self.registry.get_profile(profile_id)
        self.registry.assert_generation_allowed(profile)
        storyboard = {
            "schema": "lantern.contentengine.videoProject.v1",
            "projectTitle": project_title,
            "format": format,
            "runtimeTarget": "dry-run",
            "profileId": profile["id"],
            "profileVersion": profile["version"],
            "reviewGates": {
                "storyboard": "pending",
                "stillFrames": "blocked_until_storyboard_approved",
                "clips": "blocked_until_stills_approved",
                "final": "blocked_until_clips_approved",
            },
            "shotCards": [
                {
                    "shotId": f"shot-{index:03d}",
                    "scene": scene,
                    "imageJob": self.registry.build_image_job(profile_id, scene=scene),
                    "videoJob": None,
                }
                for index, scene in enumerate(scenes, start=1)
            ],
            "voicePlan": {"status": "placeholder"},
            "subtitlePlan": {"status": "placeholder"},
            "musicPlan": {"status": "placeholder"},
            "publishTarget": {"status": "blocked_until_final_review"},
        }
        output_dir = self.root / "generated" / "storyboards"
        output_dir.mkdir(parents=True, exist_ok=True)
        slug = project_title.lower().replace(" ", "-")
        (output_dir / f"{slug}.json").write_text(json.dumps(storyboard, indent=2) + "\n", encoding="utf-8")
        return storyboard
