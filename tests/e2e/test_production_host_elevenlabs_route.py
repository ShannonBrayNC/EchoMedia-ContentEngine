#!/usr/bin/env python3
"""Production host route test for the ElevenLabs webhook endpoint."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from services import content_engine_api as api  # noqa: E402


def test_production_host_elevenlabs_webhook_route() -> None:
    api.reset_state()

    payload = {
        "event_id": "evt-route-test-001",
        "type": "transcription_completed",
        "webhook_metadata": {
            "projectId": "lantern-protocol",
            "jobId": "job-route-001",
            "artifactId": "artifact-route-001",
        },
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer should-not-leak",
    }

    response = api.route("POST", "/api/webhooks/elevenlabs", payload, headers)
    assert response.status == 202
    assert response.body["ok"] is True
    assert response.body["event"]["provider"] == "elevenlabs"
    assert response.body["event"]["safeHeaders"]["Authorization"] == "[redacted]"

    duplicate = api.route("POST", "/api/webhooks/elevenlabs", payload, headers)
    assert duplicate.status == 200
    assert duplicate.body["duplicate"] is True

    events = api.route("GET", "/api/webhooks/events?provider=elevenlabs", {}, {})
    assert events.status == 200
    assert events.body["count"] == 1
    assert events.body["events"][0]["providerEventType"] == "transcription_completed"

    health = api.route("GET", "/health", {}, {})
    assert health.status == 200
    assert "/api/webhooks/elevenlabs" in health.body["webhooks"]


if __name__ == "__main__":
    test_production_host_elevenlabs_webhook_route()
    print("Production host ElevenLabs route test passed.")
