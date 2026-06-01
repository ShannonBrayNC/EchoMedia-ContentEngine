"""Export-package publish workflow for EchoMedia Ad Studio.

This module closes EMAS-006 for the production RC lane.
For RC, publish means creating a verified export package and manifest,
not auto-posting to Instagram.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .audit import AppendOnlyAuditLogger, AuditEvent
from .source_registry import ConsentVerificationRequest, SourceRegistryService


ALLOWED_SOURCE_STATES = {"approved", "publish_ready"}


@dataclass(frozen=True)
class PublishRequest:
    project_name: str
    ad_name: str
    output_id: str
    platform: str
    format: str
    requested_by: str
    intended_use: str
    output_metadata_path: str
    export_root: str


@dataclass(frozen=True)
class PublishResult:
    published: bool
    output_id: str
    state: str
    package_path: str
    manifest_path: str
    caption_path: str | None
    audit_event_id: str


@dataclass(frozen=True)
class PublishManifest:
    publish_id: str
    project: str
    ad: str
    platform: str
    format: str
    published_at: str
    published_by: str
    output_id: str
    assets: list[str]
    disclosure: str
    source_registry_verified: bool
    audit_event_id: str

    def to_dict(self) -> dict:
        return {
            "publish_id": self.publish_id,
            "project": self.project,
            "ad": self.ad,
            "platform": self.platform,
            "format": self.format,
            "published_at": self.published_at,
            "published_by": self.published_by,
            "output_id": self.output_id,
            "assets": self.assets,
            "disclosure": self.disclosure,
            "source_registry_verified": self.source_registry_verified,
            "audit_event_id": self.audit_event_id,
        }


class PublishBlocked(RuntimeError):
    pass


class ExportPackagePublishAdapter:
    """Creates a publish-ready package and manifest from an approved output."""

    def __init__(self, source_registry: SourceRegistryService, audit_logger: AppendOnlyAuditLogger):
        self.source_registry = source_registry
        self.audit_logger = audit_logger

    def publish(self, request: PublishRequest) -> PublishResult:
        metadata_path = Path(request.output_metadata_path)
        if not metadata_path.exists():
            return self._blocked(request, "missing_output_metadata", "Output metadata does not exist.")

        output_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        state = output_metadata.get("state")
        if state not in ALLOWED_SOURCE_STATES:
            return self._blocked(request, "invalid_state", f"Cannot publish output in state: {state}.")

        disclosure = output_metadata.get("disclosure") or output_metadata.get("disclosureText")
        if not disclosure:
            return self._blocked(request, "missing_disclosure", "Disclosure metadata is required before publishing.")

        consent = self.source_registry.verify_consent(
            ConsentVerificationRequest(
                project_name=request.project_name,
                subject_id=request.project_name,
                intended_use=request.intended_use,
                platform=request.platform,
                action="publish",
                actor=request.requested_by,
                ad_name=request.ad_name,
            )
        )
        if not consent.allowed:
            return self._blocked(request, "consent_blocked", consent.reason or "Source-registry consent verification failed.")

        assets = output_metadata.get("assets") or []
        if not assets:
            return self._blocked(request, "missing_assets", "At least one approved asset is required to publish.")

        export_dir = Path(request.export_root) / request.format
        export_dir.mkdir(parents=True, exist_ok=True)

        copied_assets: list[str] = []
        for asset in assets:
            asset_path = Path(asset)
            if not asset_path.exists():
                return self._blocked(request, "missing_asset_file", f"Asset does not exist: {asset}")
            destination = export_dir / asset_path.name
            shutil.copy2(asset_path, destination)
            copied_assets.append(str(destination))

        caption_path = None
        caption_text = output_metadata.get("caption")
        if caption_text:
            caption_file = export_dir / "caption.txt"
            caption_file.write_text(caption_text, encoding="utf-8")
            caption_path = str(caption_file)

        audit_event = self.audit_logger.append(
            AuditEvent(
                actor=request.requested_by,
                action="publish_completed",
                project_name=request.project_name,
                ad_name=request.ad_name,
                target_type="output",
                target_id=request.output_id,
                result="success",
                metadata={
                    "platform": request.platform,
                    "format": request.format,
                    "intendedUse": request.intended_use,
                    "assets": copied_assets,
                },
            )
        )

        manifest = PublishManifest(
            publish_id=str(uuid4()),
            project=request.project_name,
            ad=request.ad_name,
            platform=request.platform,
            format=request.format,
            published_at=datetime.now(timezone.utc).isoformat(),
            published_by=request.requested_by,
            output_id=request.output_id,
            assets=copied_assets,
            disclosure=disclosure,
            source_registry_verified=True,
            audit_event_id=audit_event.event_id,
        )
        manifest_path = export_dir / "publish-manifest.json"
        manifest_path.write_text(json.dumps(manifest.to_dict(), indent=2, sort_keys=True), encoding="utf-8")

        output_metadata["state"] = "published"
        output_metadata["publishedAt"] = manifest.published_at
        output_metadata["publishManifestPath"] = str(manifest_path)
        metadata_path.write_text(json.dumps(output_metadata, indent=2, sort_keys=True), encoding="utf-8")

        return PublishResult(
            published=True,
            output_id=request.output_id,
            state="published",
            package_path=str(export_dir),
            manifest_path=str(manifest_path),
            caption_path=caption_path,
            audit_event_id=audit_event.event_id,
        )

    def _blocked(self, request: PublishRequest, reason_code: str, reason: str) -> PublishResult:
        audit_event = self.audit_logger.append(
            AuditEvent(
                actor=request.requested_by,
                action="publish_blocked",
                project_name=request.project_name,
                ad_name=request.ad_name,
                target_type="output",
                target_id=request.output_id,
                result="blocked",
                reason=reason,
                metadata={
                    "reasonCode": reason_code,
                    "platform": request.platform,
                    "format": request.format,
                    "intendedUse": request.intended_use,
                },
            )
        )
        return PublishResult(
            published=False,
            output_id=request.output_id,
            state="blocked",
            package_path="",
            manifest_path="",
            caption_path=None,
            audit_event_id=audit_event.event_id,
        )
