"""Provider-neutral voice synthesis contracts and no-provider adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class VoiceSynthesisRequest:
    project_id: str
    segment_id: str
    text: str
    voice_id: str
    role: str
    output_format: str = "wav"
    mode: str = "plain-text"
    ssml: str | None = None
    timing_required: bool = False
    commercial_use: bool = False
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class VoiceSynthesisResult:
    provider_name: str
    segment_id: str
    status: str
    output_path: str | None
    duration_seconds: float | None
    usage: dict[str, float]
    provider_metadata: dict[str, str]
    manifest: dict[str, object]
    errors: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class VoiceProviderProfile:
    provider_name: str
    supports_batch: bool
    supports_streaming: bool
    supports_ssml: bool
    supports_voice_clone: bool
    supports_alignment: bool
    supports_commercial_use_metadata: bool
    max_characters_per_request: int | None
    supported_output_formats: tuple[str, ...]


class VoiceProvider(Protocol):
    profile: VoiceProviderProfile

    def generate_audio(self, request: VoiceSynthesisRequest) -> VoiceSynthesisResult:
        """Generate or map an audio request without exposing provider-specific fields."""


class FakeVoiceProvider:
    profile = VoiceProviderProfile(
        provider_name="fake",
        supports_batch=True,
        supports_streaming=False,
        supports_ssml=True,
        supports_voice_clone=False,
        supports_alignment=True,
        supports_commercial_use_metadata=True,
        max_characters_per_request=20_000,
        supported_output_formats=("wav", "mp3"),
    )

    def generate_audio(self, request: VoiceSynthesisRequest) -> VoiceSynthesisResult:
        errors = validate_voice_request(request, self.profile)
        status = "failed" if errors else "completed"
        output_path = None if errors else f"artifacts/audio/{request.project_id}/{request.segment_id}.{request.output_format}"
        return VoiceSynthesisResult(
            provider_name=self.profile.provider_name,
            segment_id=request.segment_id,
            status=status,
            output_path=output_path,
            duration_seconds=None if errors else max(len(request.text) / 14.0, 1.0),
            usage={"characters": float(len(request.text)), "estimatedCostUsd": 0.0},
            provider_metadata={"dryRun": "true"},
            manifest=voice_manifest(request, self.profile.provider_name, output_path),
            errors=errors,
        )


class AzureSpeechProvider:
    profile = VoiceProviderProfile(
        provider_name="azure-speech",
        supports_batch=True,
        supports_streaming=True,
        supports_ssml=True,
        supports_voice_clone=False,
        supports_alignment=False,
        supports_commercial_use_metadata=True,
        max_characters_per_request=10_000,
        supported_output_formats=("wav", "mp3"),
    )

    def __init__(self, *, region: str | None, endpoint: str | None = None, configured: bool = False) -> None:
        self.region = region
        self.endpoint = endpoint
        self.configured = configured

    def generate_audio(self, request: VoiceSynthesisRequest) -> VoiceSynthesisResult:
        errors = validate_voice_request(request, self.profile)
        errors.extend(validate_azure_config(region=self.region, configured=self.configured))
        provider_request = map_azure_request(request, region=self.region, endpoint=self.endpoint)
        status = "blocked" if errors else "mapped"
        output_path = None if errors else f"artifacts/audio/{request.project_id}/{request.segment_id}.azure.{request.output_format}"
        return VoiceSynthesisResult(
            provider_name=self.profile.provider_name,
            segment_id=request.segment_id,
            status=status,
            output_path=output_path,
            duration_seconds=None,
            usage={"characters": float(len(request.text)), "estimatedCostUsd": 0.0},
            provider_metadata=provider_request,
            manifest=voice_manifest(request, self.profile.provider_name, output_path),
            errors=errors,
        )


def validate_voice_request(request: VoiceSynthesisRequest, profile: VoiceProviderProfile) -> list[str]:
    errors: list[str] = []
    if request.output_format not in profile.supported_output_formats:
        errors.append(f"unsupported output format: {request.output_format}")
    if request.mode == "ssml" and not profile.supports_ssml:
        errors.append("SSML is not supported by this provider")
    if request.mode == "ssml" and not request.ssml:
        errors.append("SSML mode requires ssml content")
    if profile.max_characters_per_request and len(request.text) > profile.max_characters_per_request:
        errors.append("text exceeds provider character limit")
    if request.commercial_use and not profile.supports_commercial_use_metadata:
        errors.append("commercial-use metadata is not supported by this provider")
    return errors


def validate_azure_config(*, region: str | None, configured: bool) -> list[str]:
    errors: list[str] = []
    if not region:
        errors.append("Azure Speech region is required")
    if configured is False:
        errors.append("Azure Speech credentials or managed identity are not configured")
    return errors


def map_azure_request(
    request: VoiceSynthesisRequest,
    *,
    region: str | None,
    endpoint: str | None,
) -> dict[str, str]:
    return {
        "region": region or "",
        "endpoint": endpoint or "",
        "voiceName": request.voice_id,
        "inputMode": request.mode,
        "outputFormat": request.output_format,
        "segmentId": request.segment_id,
        "projectId": request.project_id,
    }


def voice_manifest(
    request: VoiceSynthesisRequest,
    provider_name: str,
    output_path: str | None,
) -> dict[str, object]:
    return {
        "artifactType": "voice-synthesis-result",
        "projectId": request.project_id,
        "segmentId": request.segment_id,
        "provider": provider_name,
        "voiceId": request.voice_id,
        "role": request.role,
        "outputPath": output_path,
        "timingRequired": request.timing_required,
        "commercialUse": request.commercial_use,
        "metadata": request.metadata,
    }
