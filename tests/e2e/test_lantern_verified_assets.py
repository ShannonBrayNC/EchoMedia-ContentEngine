#!/usr/bin/env python3
"""No-provider tests for verified Lantern asset gates."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from services import lantern_verified_assets as verified  # noqa: E402


def base_manifest_payload() -> dict[str, object]:
    return {
        "artifactId": "asset-lantern-001",
        "canonId": "lantern-origin-001",
        "projectId": "lantern-protocol",
        "assetType": "marketing-package",
        "provider": "provider-neutral",
        "promptTemplateVersion": "lantern-content-v1",
        "rightsStatus": "review-required",
        "approvalState": "required",
        "consentState": "requested",
        "sourceFiles": ["docs/lantern/LANTERN_CANON_REGISTRY.md"],
        "reviewOwner": "human",
    }


def test_draft_asset_is_not_production_ready() -> None:
    manifest = verified.build_lantern_asset_manifest(base_manifest_payload())

    assert manifest["releaseGateStatus"] == "draft"
    assert manifest["productionReady"] is False
    assert manifest["evidenceHash"]


def test_missing_rights_gate_blocks_release() -> None:
    payload = base_manifest_payload()
    payload.update(
        {
            "rightsStatus": "blocked",
            "approvalState": "approved",
            "consentState": "granted",
            "etsProofRef": "mock-ets-proof-asset-001",
        }
    )

    manifest = verified.build_lantern_asset_manifest(payload)

    assert manifest["releaseGateStatus"] == "blocked"
    assert manifest["productionReady"] is False


def test_approved_asset_with_proof_is_released_manifest() -> None:
    payload = base_manifest_payload()
    payload.update(
        {
            "rightsStatus": "cleared",
            "approvalState": "approved",
            "consentState": "granted",
            "etsProofRef": "mock-ets-proof-asset-001",
        }
    )

    manifest = verified.build_lantern_asset_manifest(payload)

    assert manifest["releaseGateStatus"] == "released"
    assert manifest["productionReady"] is True


def test_released_manifest_can_emit_signalforge_artifact_payload() -> None:
    payload = base_manifest_payload()
    payload.update(
        {
            "rightsStatus": "cleared",
            "approvalState": "approved",
            "consentState": "granted",
            "etsProofRef": "mock-ets-proof-asset-001",
        }
    )
    manifest = verified.build_lantern_asset_manifest(payload)
    handoff = verified.build_signalforge_artifact_handoff(manifest)

    assert handoff["eventType"] == "artifact.created"
    assert handoff["targetSystem"] == "signalforge"
    assert handoff["etsProofRef"] == "mock-ets-proof-asset-001"
    assert handoff["payload"]["releaseGateStatus"] == "released"
    assert handoff["payload"]["canonId"] == "lantern-origin-001"


def test_unreleased_manifest_cannot_emit_signalforge_payload() -> None:
    manifest = verified.build_lantern_asset_manifest(base_manifest_payload())

    blocked = False
    try:
        verified.build_signalforge_artifact_handoff(manifest)
    except PermissionError as exc:
        blocked = "Only released" in str(exc)

    assert blocked


if __name__ == "__main__":
    test_draft_asset_is_not_production_ready()
    test_missing_rights_gate_blocks_release()
    test_approved_asset_with_proof_is_released_manifest()
    test_released_manifest_can_emit_signalforge_artifact_payload()
    test_unreleased_manifest_cannot_emit_signalforge_payload()
    print("Lantern verified asset tests passed.")
