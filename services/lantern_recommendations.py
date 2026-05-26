"""Content Engine recommendation export for Christina and SignalForge."""

from __future__ import annotations

import hashlib
import re
from copy import deepcopy
from typing import Any

OWNER_REPO = "ShannonBrayNC/EchoMedia-ContentEngine"
RECOMMENDATION_TYPES = {
    "software-change",
    "process-change",
    "content-workflow-change",
    "documentation-change",
    "investigation",
    "campaign-opportunity",
}
PRIORITIES = {"urgent", "high", "medium", "low"}
STATUSES = {"open", "planned", "in-progress", "blocked", "done", "deferred"}


def create_recommendation(payload: dict[str, Any]) -> dict[str, Any]:
    required = ["title", "type", "source", "priority", "status", "targetSprint", "duplicateKey"]
    missing = [field for field in required if not payload.get(field)]
    if missing:
        raise ValueError(f"Missing recommendation fields: {', '.join(missing)}")
    if payload["type"] not in RECOMMENDATION_TYPES:
        raise ValueError(f"Unsupported recommendation type: {payload['type']}")
    if payload["priority"] not in PRIORITIES:
        raise ValueError(f"Unsupported recommendation priority: {payload['priority']}")
    if payload["status"] not in STATUSES:
        raise ValueError(f"Unsupported recommendation status: {payload['status']}")

    duplicate_key = payload["duplicateKey"]
    recommendation = {
        "id": payload.get("id") or stable_id("content-engine-rec", duplicate_key),
        "title": payload["title"],
        "type": payload["type"],
        "source": payload["source"],
        "priority": payload["priority"],
        "status": payload["status"],
        "ownerRepo": payload.get("ownerRepo", OWNER_REPO),
        "targetSprint": payload["targetSprint"],
        "duplicateKey": duplicate_key,
        "signalForgeRegistryKey": f"signalforge:{stable_slug(duplicate_key)}",
        "linkedIssues": payload.get("linkedIssues", []),
        "relatedAssets": payload.get("relatedAssets", []),
        "relatedCampaigns": payload.get("relatedCampaigns", []),
        "relatedDrafts": payload.get("relatedDrafts", []),
        "approvalStates": payload.get("approvalStates", []),
        "sourceVerticalOutputs": payload.get("sourceVerticalOutputs", []),
        "targetChannel": payload.get("targetChannel"),
        "approvalRequired": payload.get("approvalRequired", True),
        "reviewNotes": payload.get("reviewNotes", []),
        "notes": payload.get("notes", ""),
    }
    return recommendation


def default_recommendations() -> list[dict[str, Any]]:
    return [
        create_recommendation(
            {
                "title": "Expose open recommendations to Christina and Lantern",
                "type": "software-change",
                "source": "lantern-operating-loop",
                "priority": "high",
                "status": "open",
                "targetSprint": "Sprint 10",
                "duplicateKey": "content-engine:lantern:recommendation-export",
                "linkedIssues": [102],
                "relatedAssets": ["docs/recommendation-registry.md"],
                "targetChannel": "signalforge",
                "notes": "Machine-readable export should prevent duplicate issue creation.",
            }
        ),
        create_recommendation(
            {
                "title": "Maintain RC readiness report and JSON export",
                "type": "process-change",
                "source": "technical-review",
                "priority": "high",
                "status": "open",
                "targetSprint": "Sprint 10",
                "duplicateKey": "content-engine:rc:readiness-report",
                "linkedIssues": [105],
                "relatedAssets": ["docs/reports/rc-readiness-2026-05-24.md"],
                "targetChannel": "christina",
                "notes": "Report must summarize readiness areas, blockers, and next actions.",
            }
        ),
        create_recommendation(
            {
                "title": "Verify canon, consent, rights, and proof gates for Lantern assets",
                "type": "content-workflow-change",
                "source": "lantern-protocol",
                "priority": "high",
                "status": "planned",
                "targetSprint": "Sprint 10",
                "duplicateKey": "content-engine:lantern:verified-asset-pipeline",
                "linkedIssues": [106],
                "relatedAssets": [
                    "docs/lantern/LANTERN_CANON_REGISTRY.md",
                    "docs/lantern/CONSENT_THEME_BIBLE.md",
                    "docs/lantern/LANTERN_ASSET_MANIFEST_SCHEMA.md",
                ],
                "approvalStates": ["required"],
                "targetChannel": "signalforge",
                "notes": "Production-ready assets require rights, consent, approval, manifest, and ETS proof reference.",
            }
        ),
    ]


def upsert_recommendation(registry: list[dict[str, Any]], recommendation: dict[str, Any]) -> list[dict[str, Any]]:
    duplicate_index = next(
        (
            index
            for index, item in enumerate(registry)
            if item["duplicateKey"] == recommendation["duplicateKey"]
            or bool(set(item.get("linkedIssues", [])) & set(recommendation.get("linkedIssues", [])))
        ),
        None,
    )
    if duplicate_index is None:
        return [*registry, recommendation]

    merged = {**registry[duplicate_index], **recommendation}
    merged["reviewNotes"] = [*registry[duplicate_index].get("reviewNotes", []), *recommendation.get("reviewNotes", [])]
    return [item if index != duplicate_index else merged for index, item in enumerate(registry)]


def export_open_recommendations(registry: list[dict[str, Any]]) -> dict[str, Any]:
    open_items = [
        item
        for item in registry
        if item["status"] in {"open", "planned", "in-progress", "blocked"}
    ]
    open_items.sort(key=lambda item: priority_rank(item["priority"]), reverse=True)
    duplicate_keys = [item["duplicateKey"] for item in registry]
    return {
        "schemaVersion": "1.0.0",
        "ownerRepo": OWNER_REPO,
        "exportType": "content-engine-recommendation-registry",
        "recommendations": open_items,
        "duplicateKeys": duplicate_keys,
        "signalForgeReady": True,
    }


def build_sprint_candidates(registry: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "candidateId": stable_id("content-engine-sprint", item["duplicateKey"]),
            "sourceRecommendationId": item["id"],
            "title": item["title"],
            "priority": item["priority"],
            "targetSprint": item["targetSprint"],
            "ownerRepo": item["ownerRepo"],
            "linkedIssues": item["linkedIssues"],
            "approvalRequired": item["approvalRequired"],
        }
        for item in export_open_recommendations(registry)["recommendations"]
        if item["status"] != "blocked"
    ]


def append_review_note(recommendation: dict[str, Any], author: str, note: str, created_at: str) -> dict[str, Any]:
    updated = deepcopy(recommendation)
    updated["reviewNotes"] = [
        *updated.get("reviewNotes", []),
        {"author": author, "note": note, "createdAt": created_at},
    ]
    return updated


def update_status(recommendation: dict[str, Any], status: str) -> dict[str, Any]:
    if status not in STATUSES:
        raise ValueError(f"Unsupported recommendation status: {status}")
    updated = deepcopy(recommendation)
    updated["status"] = status
    return updated


def build_rc_readiness_report(registry: list[dict[str, Any]]) -> dict[str, Any]:
    areas = [
        readiness_area("repo-hygiene", "green", "README, runbook, schemas, and baseline validation exist.", "Keep current as sprints evolve."),
        readiness_area("ci", "green", "No-provider pytest and baseline validation pass locally.", "Confirm latest GitHub Actions after merge."),
        readiness_area("ui-workflow", "yellow", "Dashboard compiles and has review/export controls.", "Add UI smoke coverage beyond compile."),
        readiness_area("api-workflow", "yellow", "Standard-library API and no-provider E2E are present.", "Expand route coverage and contract tests."),
        readiness_area("provider-safety", "yellow", "Provider calls are dry-run/no-provider safe by default.", "Keep live provider calls opt-in."),
        readiness_area("webhook-readiness", "yellow", "Provider event helpers and webhook fixtures exist.", "Wire production runtime route and provider-native verification."),
        readiness_area("artifact-traceability", "yellow", "Exports include traceability metadata.", "Enforce traceability on every provider output."),
        readiness_area("rights-release-gates", "yellow", "Lantern asset manifest defines release gates.", "Block all production-ready exports without rights, proof, and approval."),
        readiness_area("docs", "green", "Lantern adapter and registry docs exist.", "Keep generated exports linked from docs."),
        readiness_area("deployment", "red", "Deployment path is documented but not RC-proven.", "Define hosted route and environment configuration."),
    ]
    return {
        "schemaVersion": "1.0.0",
        "ownerRepo": OWNER_REPO,
        "status": "pre-RC / RC-hardening candidate",
        "readinessAreas": areas,
        "openRecommendations": export_open_recommendations(registry)["recommendations"],
        "sprintCandidates": build_sprint_candidates(registry),
        "safeToShare": True,
    }


def readiness_area(area: str, status: str, evidence: str, next_action: str) -> dict[str, str]:
    return {"area": area, "status": status, "evidence": evidence, "nextAction": next_action}


def priority_rank(priority: str) -> int:
    return {"low": 1, "medium": 2, "high": 3, "urgent": 4}[priority]


def stable_id(prefix: str, value: str) -> str:
    return f"{prefix}-{stable_slug(value)}-{hashlib.sha256(value.encode('utf-8')).hexdigest()[:10]}"


def stable_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:72]
