"""Verified Lantern asset gates and SignalForge handoff payloads."""

from __future__ import annotations

import hashlib
from typing import Any

RIGHTS_STATUSES = {"unknown", "review-required", "cleared", "blocked"}
APPROVAL_STATES = {"not-required", "required", "pending", "approved", "rejected"}
CONSENT_STATES = {"not-required", "requested", "granted", "denied", "revoked", "expired"}
RELEASE_GATE_STATUSES = {"draft", "blocked", "ready-for-review", "released"}


def build_lantern_asset_manifest(payload: dict[str, Any]) -> dict[str, Any]:
    required = [
        "artifactId",
        "canonId",
        "projectId",
        "assetType",
        "provider",
        "promptTemplateVersion",
        "rightsStatus",
        "approvalState",
        "consentState",
        "sourceFiles",
        "reviewOwner",
    ]
    missing = [field for field in required if not payload.get(field)]
    if missing:
        raise ValueError(f"Missing manifest fields: {', '.join(missing)}")

    if payload["rightsStatus"] not in RIGHTS_STATUSES:
        raise ValueError(f"Unsupported rights status: {payload['rightsStatus']}")
    if payload["approvalState"] not in APPROVAL_STATES:
        raise ValueError(f"Unsupported approval state: {payload['approvalState']}")
    if payload["consentState"] not in CONSENT_STATES:
        raise ValueError(f"Unsupported consent state: {payload['consentState']}")

    evidence_hash = payload.get("evidenceHash") or hash_manifest_evidence(payload)
    release_gate_status = evaluate_release_gate(
        rights_status=payload["rightsStatus"],
        approval_state=payload["approvalState"],
        consent_state=payload["consentState"],
        evidence_hash=evidence_hash,
        ets_proof_ref=payload.get("etsProofRef"),
    )

    return {
        "schemaVersion": "1.0.0",
        "artifactId": payload["artifactId"],
        "canonId": payload["canonId"],
        "projectId": payload["projectId"],
        "assetType": payload["assetType"],
        "provider": payload["provider"],
        "promptTemplateVersion": payload["promptTemplateVersion"],
        "rightsStatus": payload["rightsStatus"],
        "approvalState": payload["approvalState"],
        "consentState": payload["consentState"],
        "evidenceHash": evidence_hash,
        "etsProofRef": payload.get("etsProofRef"),
        "sourceFiles": payload["sourceFiles"],
        "reviewOwner": payload["reviewOwner"],
        "releaseGateStatus": release_gate_status,
        "productionReady": release_gate_status == "released",
    }


def build_signalforge_artifact_handoff(manifest: dict[str, Any]) -> dict[str, Any]:
    if manifest["releaseGateStatus"] != "released":
        raise PermissionError("Only released Lantern asset manifests can be routed as verified SignalForge artifacts.")

    return {
        "eventType": "artifact.created",
        "sourceRepo": "ShannonBrayNC/EchoMedia-ContentEngine",
        "sourceSystem": "content-engine",
        "targetSystem": "signalforge",
        "actionType": "publication",
        "approvalState": manifest["approvalState"],
        "consentState": manifest["consentState"],
        "etsProofRef": manifest["etsProofRef"],
        "payload": {
            "artifactId": manifest["artifactId"],
            "canonId": manifest["canonId"],
            "projectId": manifest["projectId"],
            "assetType": manifest["assetType"],
            "releaseGateStatus": manifest["releaseGateStatus"],
            "evidenceHash": manifest["evidenceHash"],
        },
    }


def evaluate_release_gate(
    *,
    rights_status: str,
    approval_state: str,
    consent_state: str,
    evidence_hash: str | None,
    ets_proof_ref: str | None,
) -> str:
    if rights_status == "blocked" or approval_state == "rejected" or consent_state in {"denied", "revoked", "expired"}:
        return "blocked"

    if (
        rights_status == "cleared"
        and approval_state == "approved"
        and consent_state in {"granted", "not-required"}
        and evidence_hash
        and ets_proof_ref
    ):
        return "released"

    if rights_status == "cleared" and approval_state in {"pending", "approved"}:
        return "ready-for-review"

    return "draft"


def hash_manifest_evidence(payload: dict[str, Any]) -> str:
    evidence = {
        "artifactId": payload.get("artifactId"),
        "canonId": payload.get("canonId"),
        "projectId": payload.get("projectId"),
        "assetType": payload.get("assetType"),
        "provider": payload.get("provider"),
        "promptTemplateVersion": payload.get("promptTemplateVersion"),
        "sourceFiles": payload.get("sourceFiles", []),
    }
    return hashlib.sha256(repr(sorted(evidence.items())).encode("utf-8")).hexdigest()
