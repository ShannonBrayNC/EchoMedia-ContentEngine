from __future__ import annotations

import json
from pathlib import Path

import pytest

from services.contentengine.profiles import ProfileRegistry
from services.contentengine.renderer import DryRunRenderer


def write_registry(root: Path, profiles: list[dict]) -> None:
    registry_path = root / "profiles" / "registry.json"
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(
        json.dumps({"schema": "lantern.contentengine.profileRegistry.v1", "updatedAt": "2026-06-11T00:00:00Z", "profiles": profiles}),
        encoding="utf-8",
    )


def active_profile(profile_id: str = "shannon") -> dict:
    return {
        "id": profile_id,
        "name": profile_id.title(),
        "type": "human_subject",
        "status": "active",
        "version": 1,
        "owner": "tests",
        "description": "Approved test human subject profile.",
        "tags": ["test"],
        "visibility": "private",
        "createdAt": "2026-06-11T00:00:00Z",
        "updatedAt": "2026-06-11T00:00:00Z",
        "governance": {
            "realPerson": True,
            "likenessConsent": True,
            "commercialUse": True,
            "publicUse": False,
            "requiresApproval": True,
        },
        "references": [
            {"id": "ref-identity-001", "type": "identity", "path": "profiles/shannon/references/identity-001.png", "approvalStatus": "approved"}
        ],
    }


def draft_profile_without_consent() -> dict:
    profile = active_profile("vanessa")
    profile["status"] = "draft"
    profile["governance"]["likenessConsent"] = False
    return profile


def test_registry_lists_and_filters_profiles(tmp_path: Path) -> None:
    write_registry(tmp_path, [active_profile("shannon"), draft_profile_without_consent()])
    registry = ProfileRegistry(tmp_path)

    assert [profile["id"] for profile in registry.list_profiles(status="active")] == ["shannon"]
    assert registry.get_profile("Shannon")["id"] == "shannon"


def test_profile_generation_blocks_unapproved_human_subject(tmp_path: Path) -> None:
    write_registry(tmp_path, [draft_profile_without_consent()])
    registry = ProfileRegistry(tmp_path)

    with pytest.raises(PermissionError):
        registry.build_image_job("vanessa", scene="presenting Lantern to investors")


def test_profile_generation_creates_traceable_image_job(tmp_path: Path) -> None:
    write_registry(tmp_path, [active_profile("shannon")])
    registry = ProfileRegistry(tmp_path)

    job = registry.build_image_job("shannon", scene="presenting Lantern to investors", brand="Lantern")

    assert job["subjectProfileId"] == "shannon"
    assert job["profileVersions"] == {"shannon": 1}
    assert job["referencesUsed"] == ["ref-identity-001"]
    assert job["dryRun"] is True
    assert "negativePrompt" in job


def test_dry_run_renderer_writes_output_manifest(tmp_path: Path) -> None:
    write_registry(tmp_path, [active_profile("shannon")])
    registry = ProfileRegistry(tmp_path)
    renderer = DryRunRenderer(tmp_path, adapter_name="comfyui")

    job = registry.build_image_job("shannon", scene="founder portrait")
    manifest = renderer.render_image_job(job)

    assert manifest["mode"] == "dry-run"
    assert manifest["renderer"] == "comfyui"
    assert manifest["profileIds"] == ["shannon"]
    assert (tmp_path / "generated" / "outputs" / manifest["outputId"] / "manifest.json").exists()


def test_storyboard_export_uses_profile_and_review_gates(tmp_path: Path) -> None:
    write_registry(tmp_path, [active_profile("shannon")])
    renderer = DryRunRenderer(tmp_path)

    storyboard = renderer.export_storyboard(
        profile_id="shannon",
        project_title="Lantern Founder Short",
        scenes=["open in command center", "explain the trust layer"],
    )

    assert storyboard["schema"] == "lantern.contentengine.videoProject.v1"
    assert storyboard["profileId"] == "shannon"
    assert storyboard["reviewGates"]["storyboard"] == "pending"
    assert len(storyboard["shotCards"]) == 2
    assert storyboard["shotCards"][0]["imageJob"]["subjectProfileId"] == "shannon"
