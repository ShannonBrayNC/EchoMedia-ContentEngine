"""Lantern reusable content asset pipeline.

The module is deliberately no-provider and deterministic so Lantern handoffs can
be tested in CI without calling external content, social, or email systems.
"""

from __future__ import annotations

import hashlib
import re
from copy import deepcopy
from typing import Any

SOURCE_VERTICALS = {"ets", "opshelm", "opshelm-support", "echoliving", "echoalpha", "christina", "signalforge"}
ASSET_TYPES = {
    "linkedin-post",
    "short-form-script",
    "email-sequence",
    "newsletter",
    "knowledge-base-article",
    "sales-collateral",
    "campaign-brief",
}
APPROVAL_STATES = {"not-required", "required", "pending", "approved", "rejected"}
REUSE_RIGHTS = {"internal-only", "anonymized", "approved-public", "blocked"}
ASSET_STATUSES = {"backlog", "draft", "in-review", "approved", "published", "blocked"}


def build_asset_pipeline(source_artifact: dict[str, Any], asset_types: list[str] | None = None) -> dict[str, Any]:
    """Convert a Lantern artifact into reusable, approval-aware content assets."""

    validate_source_artifact(source_artifact)
    requested_types = asset_types or ["linkedin-post", "short-form-script", "email-sequence"]
    assets = [build_content_asset(source_artifact, asset_type) for asset_type in requested_types]

    return {
        "pipelineId": stable_id("pipeline", source_artifact["artifactId"]),
        "sourceArtifactId": source_artifact["artifactId"],
        "sourceVertical": source_artifact["sourceVertical"],
        "eventType": "opportunity.detected",
        "backlog": build_content_backlog(source_artifact, assets),
        "assets": assets,
    }


def build_content_asset(source_artifact: dict[str, Any], asset_type: str) -> dict[str, Any]:
    """Create one reusable content asset from a Lantern source artifact."""

    validate_source_artifact(source_artifact)
    if asset_type not in ASSET_TYPES:
        raise ValueError(f"Unsupported asset type: {asset_type}")

    metadata = {
        "sourceVertical": source_artifact["sourceVertical"],
        "audience": source_artifact["audience"],
        "tone": source_artifact["tone"],
        "approvalState": "required",
        "reuseRights": source_artifact.get("reuseRights", "anonymized"),
        "targetChannel": target_channel_for(asset_type),
        "status": "draft",
        "brandVoiceProfile": source_artifact.get("brandVoiceProfile", "lantern-clear-practical"),
        "sourceContextRefs": source_artifact.get("sourceContextRefs", []),
        "etsProofRef": source_artifact.get("etsProofRef"),
    }
    validate_asset_metadata(metadata)

    asset_id = stable_id("asset", source_artifact["artifactId"], asset_type, metadata["targetChannel"])
    return {
        "assetId": asset_id,
        "assetType": asset_type,
        "title": f"{source_artifact['title']} - {humanize_asset_type(asset_type)}",
        "sourceArtifactId": source_artifact["artifactId"],
        "traceability": {
            "sourceRepo": source_artifact.get("sourceRepo", "unknown"),
            "sourceEventId": source_artifact.get("sourceEventId"),
            "sourceHash": source_artifact.get("sourceHash") or hash_payload(source_artifact),
        },
        "metadata": metadata,
        "draft": format_asset_draft(source_artifact, asset_type),
        "performance": {
            "status": "not-connected",
            "feedbackSignals": [],
        },
    }


def build_content_backlog(source_artifact: dict[str, Any], assets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Create backlog records from opportunity.detected events."""

    return [
        {
            "backlogItemId": stable_id("backlog", source_artifact["artifactId"], asset["assetType"]),
            "sourceEventType": "opportunity.detected",
            "sourceArtifactId": source_artifact["artifactId"],
            "assetId": asset["assetId"],
            "priority": source_artifact.get("priority", "medium"),
            "status": "backlog",
            "approvalState": asset["metadata"]["approvalState"],
        }
        for asset in assets
    ]


def format_for_channel(asset: dict[str, Any]) -> dict[str, Any]:
    """Return a channel-ready preview that is still blocked from publishing."""

    validate_asset_metadata(asset["metadata"])
    return {
        "assetId": asset["assetId"],
        "targetChannel": asset["metadata"]["targetChannel"],
        "approvalState": asset["metadata"]["approvalState"],
        "publishAllowed": asset["metadata"]["approvalState"] == "approved",
        "formattedPreview": asset["draft"],
    }


def approve_content_asset(asset: dict[str, Any], approver: str) -> dict[str, Any]:
    """Mark an asset approved while preserving traceability and reuse metadata."""

    approved = deepcopy(asset)
    approved["metadata"]["approvalState"] = "approved"
    approved["metadata"]["status"] = "approved"
    approved["approval"] = {"approvedBy": approver, "approvalGate": "human-review"}
    return approved


def validate_source_artifact(source_artifact: dict[str, Any]) -> None:
    required = ["artifactId", "sourceVertical", "title", "summary", "audience", "tone"]
    missing = [field for field in required if not source_artifact.get(field)]
    if missing:
        raise ValueError(f"Missing Lantern source artifact fields: {', '.join(missing)}")

    if source_artifact["sourceVertical"] not in SOURCE_VERTICALS:
        raise ValueError(f"Unsupported source vertical: {source_artifact['sourceVertical']}")

    reuse_rights = source_artifact.get("reuseRights", "anonymized")
    if reuse_rights not in REUSE_RIGHTS:
        raise ValueError(f"Unsupported reuse rights: {reuse_rights}")

    if reuse_rights == "blocked":
        raise ValueError("Blocked source artifacts cannot become reusable content assets")


def validate_asset_metadata(metadata: dict[str, Any]) -> None:
    required = ["sourceVertical", "audience", "tone", "approvalState", "reuseRights", "targetChannel", "status"]
    missing = [field for field in required if not metadata.get(field)]
    if missing:
        raise ValueError(f"Missing asset metadata fields: {', '.join(missing)}")

    if metadata["approvalState"] not in APPROVAL_STATES:
        raise ValueError(f"Unsupported approval state: {metadata['approvalState']}")
    if metadata["reuseRights"] not in REUSE_RIGHTS:
        raise ValueError(f"Unsupported reuse rights: {metadata['reuseRights']}")
    if metadata["status"] not in ASSET_STATUSES:
        raise ValueError(f"Unsupported asset status: {metadata['status']}")


def target_channel_for(asset_type: str) -> str:
    return {
        "linkedin-post": "linkedin",
        "short-form-script": "short-video",
        "email-sequence": "email",
        "newsletter": "newsletter",
        "knowledge-base-article": "knowledge-base",
        "sales-collateral": "sales",
        "campaign-brief": "campaign",
    }[asset_type]


def format_asset_draft(source_artifact: dict[str, Any], asset_type: str) -> str:
    summary = source_artifact["summary"].strip()
    audience = source_artifact["audience"].strip()
    tone = source_artifact["tone"].strip()
    return (
        f"{humanize_asset_type(asset_type)} draft for {audience}.\n\n"
        f"Tone: {tone}.\n"
        f"Source: {source_artifact['sourceVertical']} / {source_artifact['artifactId']}.\n"
        f"Core point: {summary}\n\n"
        "Publishing is blocked until human approval is recorded."
    )


def humanize_asset_type(asset_type: str) -> str:
    return asset_type.replace("-", " ").title()


def stable_id(prefix: str, *parts: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", "-".join(parts).lower()).strip("-")
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{slug[:48]}-{digest}"


def hash_payload(payload: dict[str, Any]) -> str:
    return hashlib.sha256(repr(sorted(payload.items())).encode("utf-8")).hexdigest()
