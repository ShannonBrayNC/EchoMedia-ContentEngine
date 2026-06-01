"""Framework-neutral API route handlers for EchoMedia Ad Studio.

The existing Content Engine API uses standard-library route functions. This module
keeps that pattern and exposes route_emas() so the current server, FastAPI, Azure
Functions, or tests can call the same production workflow logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .assets import AssetService, TagAssetRequest, UploadReferenceRequest
from .audit import AppendOnlyAuditLogger
from .dashboard import get_ad_dashboard
from .frames import FrameReviewService, ReviewFrameRequest, SubmitFrameRequest
from .preflight import GenerationPreflightRequest, GenerationPreflightService
from .project_scaffold import AdProjectScaffoldService, CreateAdProjectRequest
from .publishing import ExportPackagePublishAdapter, PublishRequest
from .source_registry import JsonFileSourceRegistryAdapter, SourceRegistryService


@dataclass(frozen=True)
class EmasRouteResult:
    status: int
    body: dict[str, Any]


def route_emas(method: str, raw_path: str, payload: dict[str, Any] | None = None, root_path: str = ".") -> EmasRouteResult:
    """Route EMAS API requests.

    Supported route family:
    /api/ad-studio/projects/{projectName}/ads/{adName}/...
    """

    payload = payload or {}
    method = method.upper()
    parts = [part for part in raw_path.split("?")[0].split("/") if part]

    try:
        if len(parts) < 4 or parts[:3] != ["api", "ad-studio", "projects"]:
            return EmasRouteResult(404, _error("not_found", f"No EMAS route for {method} {raw_path}"))

        project_name = parts[3]

        # POST /api/ad-studio/projects/{projectName}/ads
        if method == "POST" and len(parts) == 5 and parts[4] == "ads":
            ad_name = _required(payload, "adName")
            actor = payload.get("actor") or "api"
            audit = _audit_logger(root_path, project_name)
            result = AdProjectScaffoldService(audit).create_ad_project(
                CreateAdProjectRequest(
                    project_name=project_name,
                    ad_name=ad_name,
                    actor=actor,
                    root_path=root_path,
                    force=bool(payload.get("force", False)),
                )
            )
            return EmasRouteResult(201, {"created": result.created, "adPath": result.ad_path, "warnings": result.warnings})

        if len(parts) < 6 or parts[4] != "ads":
            return EmasRouteResult(404, _error("not_found", f"No EMAS route for {method} {raw_path}"))

        ad_name = parts[5]

        # GET /api/ad-studio/projects/{projectName}/ads/{adName}/dashboard
        if method == "GET" and len(parts) == 7 and parts[6] == "dashboard":
            return EmasRouteResult(200, get_ad_dashboard(project_name, ad_name, root_path))

        # References
        if len(parts) >= 7 and parts[6] == "references":
            service = AssetService(_audit_logger(root_path, project_name))
            if method == "GET" and len(parts) == 7:
                return EmasRouteResult(200, service.list_assets(project_name, ad_name, root_path))
            if method == "POST" and len(parts) == 7:
                result = service.upload_reference(
                    UploadReferenceRequest(
                        project_name=project_name,
                        ad_name=ad_name,
                        source_path=_required(payload, "sourcePath"),
                        actor=payload.get("actor") or "api",
                        root_path=root_path,
                        tags=list(payload.get("tags") or []),
                        outfit=payload.get("outfit"),
                        expression=payload.get("expression"),
                        pose=payload.get("pose"),
                        scene_candidates=list(payload.get("sceneCandidates") or []),
                        quality_score=payload.get("qualityScore"),
                        notes=payload.get("notes") or "",
                    )
                )
                return EmasRouteResult(201, {"asset": result})
            if method == "POST" and len(parts) == 9 and parts[8] == "tag":
                result = service.tag_asset(
                    TagAssetRequest(
                        project_name=project_name,
                        ad_name=ad_name,
                        asset_id=parts[7],
                        actor=payload.get("actor") or "api",
                        root_path=root_path,
                        tags=list(payload.get("tags") or []),
                        outfit=payload.get("outfit"),
                        expression=payload.get("expression"),
                        pose=payload.get("pose"),
                        scene_candidates=list(payload.get("sceneCandidates") or []),
                        quality_score=payload.get("qualityScore"),
                        notes=payload.get("notes"),
                        approved=payload.get("approved"),
                    )
                )
                return EmasRouteResult(200, {"asset": result})

        # Storyboard frames
        if len(parts) >= 8 and parts[6:8] == ["storyboard", "frames"]:
            service = FrameReviewService(_audit_logger(root_path, project_name))
            if method == "GET" and len(parts) == 8:
                return EmasRouteResult(200, service.list_frames(project_name, ad_name, root_path))
            if method == "POST" and len(parts) == 8:
                result = service.submit_frame(
                    SubmitFrameRequest(
                        project_name=project_name,
                        ad_name=ad_name,
                        scene_id=_required(payload, "sceneId"),
                        source_path=_required(payload, "sourcePath"),
                        actor=payload.get("actor") or "api",
                        root_path=root_path,
                        notes=payload.get("notes") or "",
                    )
                )
                return EmasRouteResult(201, {"frame": result})
            if method == "POST" and len(parts) == 10 and parts[9] in {"approve", "reject"}:
                result = service.review_frame(
                    ReviewFrameRequest(
                        project_name=project_name,
                        ad_name=ad_name,
                        frame_id=parts[8],
                        actor=payload.get("actor") or "api",
                        approved=parts[9] == "approve",
                        root_path=root_path,
                        notes=payload.get("notes") or "",
                    )
                )
                return EmasRouteResult(200, {"frame": result})

        # POST /api/ad-studio/projects/{projectName}/ads/{adName}/generate/preflight
        if method == "POST" and len(parts) == 8 and parts[6:8] == ["generate", "preflight"]:
            source_registry = SourceRegistryService(_registry_adapter(root_path, project_name), _audit_logger(root_path, project_name))
            result = GenerationPreflightService(source_registry, _audit_logger(root_path, project_name)).validate(
                GenerationPreflightRequest(
                    project_name=project_name,
                    ad_name=ad_name,
                    subject_id=payload.get("subjectId") or project_name,
                    intended_use=_required(payload, "intendedUse"),
                    platform=payload.get("platform"),
                    actor=payload.get("actor") or "api",
                    prompt=_required(payload, "prompt"),
                    reference_paths=list(payload.get("referencePaths") or []),
                    output_count=int(payload.get("outputCount") or 1),
                )
            )
            return EmasRouteResult(200 if result.allowed else 409, {
                "allowed": result.allowed,
                "reasons": result.reasons,
                "normalizedPrompt": result.normalized_prompt,
                "sourceRegistryVerified": result.source_registry_verified,
            })

        # POST /api/ad-studio/projects/{projectName}/ads/{adName}/outputs/{outputId}/publish
        if method == "POST" and len(parts) == 9 and parts[6] == "outputs" and parts[8] == "publish":
            audit = _audit_logger(root_path, project_name)
            source_registry = SourceRegistryService(_registry_adapter(root_path, project_name), audit)
            result = ExportPackagePublishAdapter(source_registry, audit).publish(
                PublishRequest(
                    project_name=project_name,
                    ad_name=ad_name,
                    output_id=parts[7],
                    platform=payload.get("platform") or "instagram",
                    format=payload.get("format") or "reels-9x16",
                    requested_by=payload.get("actor") or "api",
                    intended_use=payload.get("intendedUse") or "social_media",
                    output_metadata_path=payload.get("outputMetadataPath") or str(_ad_root(root_path, project_name, ad_name) / "outputs" / "draft" / f"{parts[7]}.json"),
                    export_root=payload.get("exportRoot") or str(_ad_root(root_path, project_name, ad_name) / "exports"),
                )
            )
            return EmasRouteResult(202 if result.published else 409, {
                "published": result.published,
                "outputId": result.output_id,
                "state": result.state,
                "packagePath": result.package_path,
                "manifestPath": result.manifest_path,
                "captionPath": result.caption_path,
                "auditEventId": result.audit_event_id,
            })

        return EmasRouteResult(404, _error("not_found", f"No EMAS route for {method} {raw_path}"))
    except FileExistsError as exc:
        return EmasRouteResult(409, _error("already_exists", str(exc)))
    except FileNotFoundError as exc:
        return EmasRouteResult(404, _error("not_found", str(exc)))
    except KeyError as exc:
        return EmasRouteResult(404, _error("not_found", str(exc)))
    except ValueError as exc:
        return EmasRouteResult(400, _error("bad_request", str(exc)))


def _required(payload: dict[str, Any], key: str) -> Any:
    value = payload.get(key)
    if value is None or value == "":
        raise ValueError(f"{key} is required")
    return value


def _error(code: str, message: str) -> dict[str, Any]:
    return {"error": {"code": code, "message": message}}


def _ad_root(root_path: str | Path, project_name: str, ad_name: str) -> Path:
    return Path(root_path) / "projects" / project_name / "ads" / ad_name


def _audit_logger(root_path: str | Path, project_name: str) -> AppendOnlyAuditLogger:
    return AppendOnlyAuditLogger(Path(root_path) / "projects" / project_name / "metadata" / "audit-log.jsonl")


def _registry_adapter(root_path: str | Path, project_name: str) -> JsonFileSourceRegistryAdapter:
    return JsonFileSourceRegistryAdapter(Path(root_path) / "projects" / project_name / "source-registry.json")
