"""Provider-neutral video generation contracts and no-provider profiles."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol


class VideoMode(StrEnum):
    TEXT_TO_VIDEO = "text-to-video"
    IMAGE_TO_VIDEO = "image-to-video"
    VIDEO_EDIT = "video-edit"
    VIDEO_EXTEND = "video-extend"


@dataclass(frozen=True)
class VideoGenerationRequest:
    project_id: str
    scene_id: str
    shot_id: str
    prompt: str
    mode: VideoMode
    duration_seconds: int
    aspect_ratio: str
    model: str
    reference_assets: tuple[str, ...] = ()
    voice_refs: tuple[str, ...] = ()
    audio_refs: tuple[str, ...] = ()
    timing_refs: tuple[str, ...] = ()
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class VideoGenerationJob:
    provider_name: str
    job_id: str
    status: str
    provider_request: dict[str, object]
    output_assets: tuple[str, ...]
    manifest: dict[str, object]
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class VideoProviderProfile:
    provider_name: str
    status: str
    supports_text_to_video: bool
    supports_image_to_video: bool
    supports_video_edit: bool
    supports_video_extend: bool
    supports_reference_images: bool
    supports_characters: bool
    supports_native_audio: bool
    supports_audio_conditioning: bool
    supports_webhooks: bool
    supported_aspect_ratios: tuple[str, ...]
    supported_durations: tuple[int, ...]
    supported_models: tuple[str, ...]
    official_api_required: bool = False


class VideoProvider(Protocol):
    profile: VideoProviderProfile

    def create_video(self, request: VideoGenerationRequest) -> VideoGenerationJob:
        """Create a provider-neutral video job."""

    def get_job(self, job_id: str) -> VideoGenerationJob:
        """Return a job by provider-neutral job ID."""


class ProfileVideoProvider:
    def __init__(self, profile: VideoProviderProfile) -> None:
        self.profile = profile
        self._jobs: dict[str, VideoGenerationJob] = {}

    def create_video(self, request: VideoGenerationRequest) -> VideoGenerationJob:
        errors = validate_video_request(request, self.profile)
        job_id = f"{self.profile.provider_name}-{request.project_id}-{request.scene_id}-{request.shot_id}"
        status = "blocked" if errors else "queued"
        job = VideoGenerationJob(
            provider_name=self.profile.provider_name,
            job_id=job_id,
            status=status,
            provider_request=map_provider_request(request, self.profile),
            output_assets=(),
            manifest=video_manifest(request, self.profile.provider_name, job_id),
            errors=tuple(errors),
        )
        self._jobs[job_id] = job
        return job

    def get_job(self, job_id: str) -> VideoGenerationJob:
        return self._jobs[job_id]


def provider_profiles() -> dict[str, VideoProviderProfile]:
    return {
        "runway": VideoProviderProfile(
            provider_name="runway",
            status="ready-for-mapping",
            supports_text_to_video=True,
            supports_image_to_video=True,
            supports_video_edit=True,
            supports_video_extend=True,
            supports_reference_images=True,
            supports_characters=True,
            supports_native_audio=False,
            supports_audio_conditioning=False,
            supports_webhooks=True,
            supported_aspect_ratios=("16:9", "9:16", "1:1"),
            supported_durations=(5, 10),
            supported_models=("runway-configured-model",),
        ),
        "openai-video": VideoProviderProfile(
            provider_name="openai-video",
            status="ready-for-mapping",
            supports_text_to_video=True,
            supports_image_to_video=True,
            supports_video_edit=True,
            supports_video_extend=True,
            supports_reference_images=True,
            supports_characters=True,
            supports_native_audio=False,
            supports_audio_conditioning=True,
            supports_webhooks=False,
            supported_aspect_ratios=("16:9", "9:16", "1:1"),
            supported_durations=(4, 8, 12),
            supported_models=("openai-configured-video-model",),
        ),
        "luma": VideoProviderProfile(
            provider_name="luma",
            status="ready-for-mapping",
            supports_text_to_video=True,
            supports_image_to_video=True,
            supports_video_edit=True,
            supports_video_extend=True,
            supports_reference_images=True,
            supports_characters=False,
            supports_native_audio=False,
            supports_audio_conditioning=False,
            supports_webhooks=True,
            supported_aspect_ratios=("16:9", "9:16", "1:1"),
            supported_durations=(5, 10),
            supported_models=("luma-configured-model",),
        ),
        "kling": planned_profile("kling"),
        "pika": planned_profile("pika"),
    }


def planned_profile(provider_name: str) -> VideoProviderProfile:
    return VideoProviderProfile(
        provider_name=provider_name,
        status="planned-blocked-until-api-verified",
        supports_text_to_video=True,
        supports_image_to_video=True,
        supports_video_edit=False,
        supports_video_extend=False,
        supports_reference_images=True,
        supports_characters=True,
        supports_native_audio=False,
        supports_audio_conditioning=False,
        supports_webhooks=False,
        supported_aspect_ratios=("16:9", "9:16", "1:1"),
        supported_durations=(5, 10),
        supported_models=(f"{provider_name}-official-api-tbd",),
        official_api_required=True,
    )


def validate_video_request(request: VideoGenerationRequest, profile: VideoProviderProfile) -> list[str]:
    errors: list[str] = []
    if profile.official_api_required:
        errors.append(f"{profile.provider_name} live use blocked until official API signatures are verified")
    if request.model not in profile.supported_models:
        errors.append(f"unsupported model for {profile.provider_name}: {request.model}")
    if request.duration_seconds not in profile.supported_durations:
        errors.append(f"unsupported duration for {profile.provider_name}: {request.duration_seconds}")
    if request.aspect_ratio not in profile.supported_aspect_ratios:
        errors.append(f"unsupported aspect ratio for {profile.provider_name}: {request.aspect_ratio}")
    if request.mode == VideoMode.TEXT_TO_VIDEO and not profile.supports_text_to_video:
        errors.append("text-to-video is not supported")
    if request.mode == VideoMode.IMAGE_TO_VIDEO and not profile.supports_image_to_video:
        errors.append("image-to-video is not supported")
    if request.mode == VideoMode.IMAGE_TO_VIDEO and not request.reference_assets:
        errors.append("image-to-video requires reference assets")
    if request.mode == VideoMode.VIDEO_EDIT and not profile.supports_video_edit:
        errors.append("video edit is not supported")
    if request.mode == VideoMode.VIDEO_EXTEND and not profile.supports_video_extend:
        errors.append("video extend is not supported")
    return errors


def map_provider_request(
    request: VideoGenerationRequest,
    profile: VideoProviderProfile,
) -> dict[str, object]:
    return {
        "provider": profile.provider_name,
        "projectId": request.project_id,
        "sceneId": request.scene_id,
        "shotId": request.shot_id,
        "prompt": request.prompt,
        "mode": request.mode.value,
        "durationSeconds": request.duration_seconds,
        "aspectRatio": request.aspect_ratio,
        "model": request.model,
        "referenceAssets": list(request.reference_assets),
        "voiceRefs": list(request.voice_refs),
        "audioRefs": list(request.audio_refs),
        "timingRefs": list(request.timing_refs),
        "metadata": request.metadata,
    }


def video_manifest(
    request: VideoGenerationRequest,
    provider_name: str,
    job_id: str,
) -> dict[str, object]:
    return {
        "artifactType": "video-generation-job",
        "provider": provider_name,
        "jobId": job_id,
        "projectId": request.project_id,
        "sceneId": request.scene_id,
        "shotId": request.shot_id,
        "promptHashSource": request.prompt,
        "voiceRefs": list(request.voice_refs),
        "audioRefs": list(request.audio_refs),
        "timingRefs": list(request.timing_refs),
        "metadata": request.metadata,
    }
