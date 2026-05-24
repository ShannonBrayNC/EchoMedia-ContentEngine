#!/usr/bin/env python3
"""Deterministic no-provider E2E test for Sprint 4."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from services import content_engine_api as api  # noqa: E402


def test_manuscript_idea_to_approved_export() -> None:
    api.reset_state()

    project_scaffold = api.create_project(
        {
            "displayTitle": "Sprint Four E2E Thriller",
            "projectId": "sprint-four-e2e-thriller",
            "universe": "EchoMedia Test Universe",
            "storyType": "novel-to-film",
            "targetFormats": ["generic-json", "openai-video", "elevenlabs", "azure-speech"],
        }
    )
    project_id = project_scaffold["project"]["projectId"]
    assert project_id == "sprint-four-e2e-thriller"
    assert project_scaffold["folders"]

    idea = api.create_idea_intake(
        project_id,
        {
            "rawInput": "A cryptographer finds that a benevolent AI is saving cities by quietly narrowing human choices.",
            "direction": "Prepare this for cinematic pre-production with consent, liberty, and technical realism as core themes.",
        },
    )
    assert idea["state"] == "review"
    assert idea["artifactType"] == "idea-intake"

    job = api.create_generation_job(
        {
            "projectId": project_id,
            "artifactType": "production-package",
            "sourceRefs": [{"artifactId": idea["artifactId"], "role": "idea-intake"}],
            "userDirection": "Create a provider-ready production package skeleton for video services.",
            "dryRun": True,
        }
    )
    assert job["status"] == "needs-review"
    assert len(job["artifactIds"]) == 1

    artifact_id = job["artifactIds"][0]
    preview = api.get_preview(artifact_id, "markdown")
    assert preview["readOnly"] is True
    assert "Draft production-package" in preview["content"]

    traceability = api.get_traceability(artifact_id)
    assert traceability["generationJobId"] == job["jobId"]
    assert traceability["manifestId"].startswith("manifest-")

    blocked = False
    try:
        api.export_artifact(artifact_id, {"packageType": "generic-json"})
    except PermissionError:
        blocked = True
    assert blocked, "unapproved artifacts must not export"

    approved = api.set_artifact_state(artifact_id, "approved")
    assert approved["state"] == "approved"

    export_package = api.export_artifact(artifact_id, {"packageType": "generic-json"})
    assert export_package["providerReady"] is True
    assert export_package["state"] == "exported"

    inventory = api.get_inventory(project_id)
    assert inventory["requiredCount"] >= 1
    assert any(item["artifactType"] == "production-package" and item["state"] == "exported" for item in inventory["items"])

    readiness = api.get_readiness(project_id)
    assert readiness["percent"] > 0
    assert readiness["projectId"] == project_id


if __name__ == "__main__":
    test_manuscript_idea_to_approved_export()
    print("No-provider manuscript-to-export E2E passed.")
