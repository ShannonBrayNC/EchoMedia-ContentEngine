#!/usr/bin/env python3
"""No-provider tests for voice and video provider contracts."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from services.video_providers import (  # noqa: E402
    ProfileVideoProvider,
    VideoGenerationRequest,
    VideoMode,
    provider_profiles,
)
from services.voice_providers import (  # noqa: E402
    AzureSpeechProvider,
    FakeVoiceProvider,
    VoiceSynthesisRequest,
)


def voice_request(**overrides: object) -> VoiceSynthesisRequest:
    values = {
        "project_id": "lantern-protocol",
        "segment_id": "seg-001",
        "text": "The system may suggest. The human decides.",
        "voice_id": "en-US-AvaMultilingualNeural",
        "role": "narrator",
        "output_format": "wav",
        "commercial_use": True,
    }
    values.update(overrides)
    return VoiceSynthesisRequest(**values)


def video_request(provider: str, **overrides: object) -> VideoGenerationRequest:
    profile = provider_profiles()[provider]
    values = {
        "project_id": "lantern-protocol",
        "scene_id": "scene-001",
        "shot_id": "shot-001",
        "prompt": "A civic dashboard illuminates a verifiable consent trail.",
        "mode": VideoMode.TEXT_TO_VIDEO,
        "duration_seconds": profile.supported_durations[0],
        "aspect_ratio": profile.supported_aspect_ratios[0],
        "model": profile.supported_models[0],
        "voice_refs": ("voice-seg-001",),
        "audio_refs": ("audio-seg-001",),
        "timing_refs": ("timeline-001",),
    }
    values.update(overrides)
    return VideoGenerationRequest(**values)


def test_fake_voice_provider_generates_manifest_without_external_calls() -> None:
    result = FakeVoiceProvider().generate_audio(voice_request())

    assert result.status == "completed"
    assert result.output_path == "artifacts/audio/lantern-protocol/seg-001.wav"
    assert result.manifest["provider"] == "fake"
    assert result.manifest["commercialUse"] is True
    assert result.errors == []


def test_azure_speech_adapter_maps_request_and_blocks_missing_config() -> None:
    result = AzureSpeechProvider(region="eastus", configured=False).generate_audio(voice_request(mode="ssml", ssml="<speak>Hello</speak>"))

    assert result.provider_name == "azure-speech"
    assert result.status == "blocked"
    assert result.provider_metadata["region"] == "eastus"
    assert result.provider_metadata["voiceName"] == "en-US-AvaMultilingualNeural"
    assert "Azure Speech credentials or managed identity are not configured" in result.errors


def test_runway_openai_and_luma_profiles_map_video_jobs() -> None:
    for provider_name in ("runway", "openai-video", "luma"):
        provider = ProfileVideoProvider(provider_profiles()[provider_name])
        job = provider.create_video(video_request(provider_name))

        assert job.status == "queued"
        assert job.provider_name == provider_name
        assert job.provider_request["voiceRefs"] == ["voice-seg-001"]
        assert job.provider_request["audioRefs"] == ["audio-seg-001"]
        assert job.manifest["artifactType"] == "video-generation-job"
        assert provider.get_job(job.job_id) == job


def test_video_validation_blocks_unsupported_duration_and_missing_image_reference() -> None:
    provider = ProfileVideoProvider(provider_profiles()["runway"])
    job = provider.create_video(
        video_request(
            "runway",
            mode=VideoMode.IMAGE_TO_VIDEO,
            duration_seconds=99,
            reference_assets=(),
        )
    )

    assert job.status == "blocked"
    assert "unsupported duration for runway: 99" in job.errors
    assert "image-to-video requires reference assets" in job.errors


def test_kling_and_pika_profiles_are_planned_and_block_live_use() -> None:
    for provider_name in ("kling", "pika"):
        profile = provider_profiles()[provider_name]
        provider = ProfileVideoProvider(profile)
        job = provider.create_video(video_request(provider_name))

        assert profile.status == "planned-blocked-until-api-verified"
        assert profile.official_api_required is True
        assert job.status == "blocked"
        assert f"{provider_name} live use blocked until official API signatures are verified" in job.errors


if __name__ == "__main__":
    test_fake_voice_provider_generates_manifest_without_external_calls()
    test_azure_speech_adapter_maps_request_and_blocks_missing_config()
    test_runway_openai_and_luma_profiles_map_video_jobs()
    test_video_validation_blocks_unsupported_duration_and_missing_image_reference()
    test_kling_and_pika_profiles_are_planned_and_block_live_use()
    print("Voice/video provider contract tests passed.")
