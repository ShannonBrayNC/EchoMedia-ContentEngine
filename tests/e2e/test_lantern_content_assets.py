#!/usr/bin/env python3
"""No-provider Lantern content asset pipeline tests."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from services import lantern_content_assets as assets  # noqa: E402


def sample_source_artifact() -> dict[str, object]:
    return {
        "artifactId": "lantern-opportunity-001",
        "sourceVertical": "echoliving",
        "sourceRepo": "ShannonBrayNC/EchoLiving",
        "sourceEventId": "evt-guest-question-001",
        "title": "Recurring early check-in question",
        "summary": "Guests repeatedly ask whether early check-in is possible before the property is ready.",
        "audience": "short-term rental hosts",
        "tone": "practical and reassuring",
        "reuseRights": "anonymized",
        "priority": "high",
        "brandVoiceProfile": "echoliving-host-operator",
        "sourceContextRefs": ["memory:guest-question:early-check-in"],
        "etsProofRef": "mock-ets-proof-001",
    }


def test_lantern_artifact_becomes_three_reusable_assets() -> None:
    pipeline = assets.build_asset_pipeline(sample_source_artifact())

    assert pipeline["eventType"] == "opportunity.detected"
    assert len(pipeline["assets"]) == 3
    assert len(pipeline["backlog"]) == 3
    assert {asset["assetType"] for asset in pipeline["assets"]} == {
        "linkedin-post",
        "short-form-script",
        "email-sequence",
    }

    for asset in pipeline["assets"]:
        assert asset["metadata"]["sourceVertical"] == "echoliving"
        assert asset["metadata"]["audience"] == "short-term rental hosts"
        assert asset["metadata"]["tone"] == "practical and reassuring"
        assert asset["metadata"]["approvalState"] == "required"
        assert asset["metadata"]["reuseRights"] == "anonymized"
        assert asset["metadata"]["status"] == "draft"
        assert asset["traceability"]["sourceRepo"] == "ShannonBrayNC/EchoLiving"
        assert asset["traceability"]["sourceEventId"] == "evt-guest-question-001"


def test_formatting_is_approval_gated_until_human_approval() -> None:
    pipeline = assets.build_asset_pipeline(sample_source_artifact(), ["newsletter"])
    draft_asset = pipeline["assets"][0]

    blocked_preview = assets.format_for_channel(draft_asset)
    assert blocked_preview["targetChannel"] == "newsletter"
    assert blocked_preview["publishAllowed"] is False
    assert "Publishing is blocked" in blocked_preview["formattedPreview"]

    approved_asset = assets.approve_content_asset(draft_asset, "Christina")
    approved_preview = assets.format_for_channel(approved_asset)
    assert approved_preview["approvalState"] == "approved"
    assert approved_preview["publishAllowed"] is True


def test_reuse_rights_block_unsafe_source_artifacts() -> None:
    source = sample_source_artifact()
    source["reuseRights"] = "blocked"

    blocked = False
    try:
        assets.build_asset_pipeline(source)
    except ValueError as exc:
        blocked = "Blocked source artifacts" in str(exc)

    assert blocked


if __name__ == "__main__":
    test_lantern_artifact_becomes_three_reusable_assets()
    test_formatting_is_approval_gated_until_human_approval()
    test_reuse_rights_block_unsafe_source_artifacts()
    print("Lantern content asset pipeline tests passed.")
