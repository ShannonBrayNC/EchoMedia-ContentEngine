#!/usr/bin/env python3
"""Deterministic ElevenLabs webhook event contract tests."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from services import provider_events  # noqa: E402


def test_elevenlabs_webhook_event_contract() -> None:
    provider_events.reset_provider_events()

    payload = {
        "event_id": "evt-elevenlabs-transcription-001",
        "type": "transcription_completed",
        "transcription_id": "trn_001",
        "webhook_metadata": {
            "projectId": "lantern-protocol",
            "jobId": "job-audio-001",
            "artifactId": "artifact-audio-001",
            "chapterId": "chapter-01",
            "sceneId": "scene-01",
            "audioAssetId": "audio-001",
        },
        "api_key": "should-not-be-persisted",
        "result": {"text": "A deterministic transcript fixture."},
    }
    headers = {
        "Content-Type": "application/json",
        "X-ElevenLabs-Delivery-Id": "delivery-001",
        "Authorization": "Bearer should-not-be-logged",
    }

    result = provider_events.handle_elevenlabs_webhook(payload, headers)
    assert result["ok"] is True
    assert result["statusCode"] == 202
    assert result["duplicate"] is False

    event = result["event"]
    assert event["provider"] == "elevenlabs"
    assert event["providerEventType"] == "transcription_completed"
    assert event["correlation"]["projectId"] == "lantern-protocol"
    assert event["correlation"]["jobId"] == "job-audio-001"
    assert event["safeHeaders"]["Authorization"] == "[redacted]"
    assert event["safePayload"]["api_key"] == "[redacted]"

    duplicate = provider_events.handle_elevenlabs_webhook(payload, headers)
    assert duplicate["ok"] is True
    assert duplicate["statusCode"] == 200
    assert duplicate["duplicate"] is True
    assert duplicate["event"]["duplicateDeliveries"] == 1

    orphan = provider_events.handle_elevenlabs_webhook(
        {
            "event_id": "evt-elevenlabs-voice-removal-001",
            "type": "voice_removal_notice",
            "voice_id": "voice_001",
        },
        {"Content-Type": "application/json"},
    )
    assert orphan["ok"] is True
    assert orphan["event"]["warnings"] == ["missing-correlation-metadata"]

    invalid = provider_events.handle_elevenlabs_webhook(["not", "object"], {})  # type: ignore[arg-type]
    assert invalid["ok"] is False
    assert invalid["statusCode"] == 400


if __name__ == "__main__":
    test_elevenlabs_webhook_event_contract()
    print("ElevenLabs webhook event contract tests passed.")
