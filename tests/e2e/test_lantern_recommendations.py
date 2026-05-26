#!/usr/bin/env python3
"""No-provider tests for Content Engine recommendation export."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from services import lantern_recommendations as recs  # noqa: E402


def test_exports_open_recommendations_for_signalforge() -> None:
    registry = recs.default_recommendations()
    exported = recs.export_open_recommendations(registry)

    assert exported["exportType"] == "content-engine-recommendation-registry"
    assert exported["signalForgeReady"] is True
    assert len(exported["recommendations"]) == 3
    assert exported["recommendations"][0]["priority"] == "high"
    assert exported["recommendations"][0]["ownerRepo"] == "ShannonBrayNC/EchoMedia-ContentEngine"
    assert exported["recommendations"][0]["signalForgeRegistryKey"].startswith("signalforge:")
    assert "content-engine:lantern:recommendation-export" in exported["duplicateKeys"]


def test_upsert_blocks_duplicate_issue_creation() -> None:
    first = recs.create_recommendation(
        {
            "title": "Expose registry",
            "type": "software-change",
            "source": "issue",
            "priority": "high",
            "status": "open",
            "targetSprint": "Sprint 10",
            "duplicateKey": "content-engine:lantern:recommendation-export",
            "linkedIssues": [102],
        }
    )
    second = recs.create_recommendation(
        {
            "title": "Expose registry with sprint candidates",
            "type": "software-change",
            "source": "christina",
            "priority": "high",
            "status": "in-progress",
            "targetSprint": "Sprint 10",
            "duplicateKey": "content-engine:lantern:recommendation-export",
            "linkedIssues": [102],
            "reviewNotes": [{"author": "christina", "note": "Update existing issue.", "createdAt": "2026-05-26T12:00:00Z"}],
        }
    )

    registry = recs.upsert_recommendation(recs.upsert_recommendation([], first), second)

    assert len(registry) == 1
    assert registry[0]["title"] == "Expose registry with sprint candidates"
    assert registry[0]["status"] == "in-progress"
    assert registry[0]["reviewNotes"][0]["author"] == "christina"


def test_builds_sprint_candidates_and_allows_status_notes() -> None:
    registry = recs.default_recommendations()
    candidates = recs.build_sprint_candidates(registry)

    assert len(candidates) == 3
    assert all(candidate["ownerRepo"] == "ShannonBrayNC/EchoMedia-ContentEngine" for candidate in candidates)
    assert any(candidate["linkedIssues"] == [105] for candidate in candidates)

    with_note = recs.append_review_note(registry[0], "lantern", "Ready for Christina sync.", "2026-05-26T12:00:00Z")
    done = recs.update_status(with_note, "done")
    assert done["status"] == "done"
    assert done["reviewNotes"][0]["note"] == "Ready for Christina sync."


def test_rc_readiness_report_is_safe_to_share() -> None:
    report = recs.build_rc_readiness_report(recs.default_recommendations())

    assert report["safeToShare"] is True
    assert report["status"] == "pre-RC / RC-hardening candidate"
    assert {area["area"] for area in report["readinessAreas"]} >= {
        "repo-hygiene",
        "ci",
        "ui-workflow",
        "api-workflow",
        "provider-safety",
        "webhook-readiness",
        "artifact-traceability",
        "rights-release-gates",
        "docs",
        "deployment",
    }
    assert report["openRecommendations"]
    assert report["sprintCandidates"]


if __name__ == "__main__":
    test_exports_open_recommendations_for_signalforge()
    test_upsert_blocks_duplicate_issue_creation()
    test_builds_sprint_candidates_and_allows_status_notes()
    test_rc_readiness_report_is_safe_to_share()
    print("Lantern recommendation export tests passed.")
