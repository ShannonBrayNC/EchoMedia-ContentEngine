"""Source-registry consent verification for EchoMedia Ad Studio.

This module closes EMAS-003 for the production RC lane by verifying
whether a specific action, intended use, and platform are allowed.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from .audit import AppendOnlyAuditLogger, AuditEvent


ConsentStatus = Literal["missing", "pending", "approved", "expired", "revoked", "rejected"]
ConsentAction = Literal["generate", "approve", "publish", "export"]


@dataclass(frozen=True)
class SourceRegistryRecord:
    subject_id: str
    project_name: str
    display_name: str
    consent_status: ConsentStatus
    allowed_uses: list[str] = field(default_factory=list)
    restricted_uses: list[str] = field(default_factory=list)
    allowed_platforms: list[str] = field(default_factory=list)
    consent_document_path: str | None = None
    signed_at: str | None = None
    expires_at: str | None = None
    revoked_at: str | None = None
    verified_by: str | None = None

    @staticmethod
    def from_dict(value: dict) -> "SourceRegistryRecord":
        return SourceRegistryRecord(
            subject_id=value["subjectId"],
            project_name=value["projectName"],
            display_name=value.get("displayName") or value["subjectId"],
            consent_status=value.get("consentStatus", "missing"),
            allowed_uses=value.get("allowedUses") or [],
            restricted_uses=value.get("restrictedUses") or [],
            allowed_platforms=value.get("allowedPlatforms") or [],
            consent_document_path=value.get("consentDocumentPath"),
            signed_at=value.get("signedAt"),
            expires_at=value.get("expiresAt"),
            revoked_at=value.get("revokedAt"),
            verified_by=value.get("verifiedBy"),
        )


@dataclass(frozen=True)
class ConsentVerificationRequest:
    project_name: str
    subject_id: str
    intended_use: str
    action: ConsentAction
    actor: str
    platform: str | None = None
    ad_name: str | None = None


@dataclass(frozen=True)
class ConsentVerificationResult:
    allowed: bool
    status: ConsentStatus
    reason: str | None = None
    matched_record: SourceRegistryRecord | None = None


class SourceRegistryAdapter:
    def get_record(self, project_name: str, subject_id: str) -> SourceRegistryRecord | None:
        raise NotImplementedError


class JsonFileSourceRegistryAdapter(SourceRegistryAdapter):
    """Reads source-registry records from a JSON file.

    Expected shape:
    {
      "records": [
        {
          "subjectId": "Vanessa",
          "projectName": "Vanessa",
          "consentStatus": "approved",
          "allowedUses": ["social_media", "marketing"],
          "allowedPlatforms": ["instagram"]
        }
      ]
    }
    """

    def __init__(self, registry_path: str | Path):
        self.registry_path = Path(registry_path)

    def get_record(self, project_name: str, subject_id: str) -> SourceRegistryRecord | None:
        if not self.registry_path.exists():
            return None
        data = json.loads(self.registry_path.read_text(encoding="utf-8"))
        for record in data.get("records", []):
            if record.get("projectName") == project_name and record.get("subjectId") == subject_id:
                return SourceRegistryRecord.from_dict(record)
        return None


class SourceRegistryService:
    def __init__(self, adapter: SourceRegistryAdapter, audit_logger: AppendOnlyAuditLogger | None = None):
        self.adapter = adapter
        self.audit_logger = audit_logger

    def verify_consent(self, request: ConsentVerificationRequest) -> ConsentVerificationResult:
        record = self.adapter.get_record(request.project_name, request.subject_id)

        if not record:
            result = ConsentVerificationResult(False, "missing", "No source-registry record found.")
            self._audit(request, result)
            return result

        if record.consent_status != "approved":
            result = ConsentVerificationResult(
                False,
                record.consent_status,
                f"Consent is {record.consent_status}.",
                record,
            )
            self._audit(request, result)
            return result

        now = datetime.now(timezone.utc)

        if record.expires_at and _parse_datetime(record.expires_at) <= now:
            result = ConsentVerificationResult(False, "expired", "Consent has expired.", record)
            self._audit(request, result)
            return result

        if record.revoked_at:
            result = ConsentVerificationResult(False, "revoked", "Consent has been revoked.", record)
            self._audit(request, result)
            return result

        if request.intended_use not in record.allowed_uses:
            result = ConsentVerificationResult(
                False,
                "approved",
                f"Use not allowed: {request.intended_use}.",
                record,
            )
            self._audit(request, result)
            return result

        if request.intended_use in record.restricted_uses:
            result = ConsentVerificationResult(
                False,
                "approved",
                f"Use is restricted: {request.intended_use}.",
                record,
            )
            self._audit(request, result)
            return result

        if request.platform and record.allowed_platforms and request.platform not in record.allowed_platforms:
            result = ConsentVerificationResult(
                False,
                "approved",
                f"Platform not allowed: {request.platform}.",
                record,
            )
            self._audit(request, result)
            return result

        result = ConsentVerificationResult(True, "approved", matched_record=record)
        self._audit(request, result)
        return result

    def _audit(self, request: ConsentVerificationRequest, result: ConsentVerificationResult) -> None:
        if not self.audit_logger:
            return
        self.audit_logger.append(
            AuditEvent(
                actor=request.actor,
                action="source_registry_consent_verified",
                project_name=request.project_name,
                ad_name=request.ad_name,
                target_type="subject",
                target_id=request.subject_id,
                result="success" if result.allowed else "blocked",
                reason=result.reason,
                metadata={
                    "action": request.action,
                    "intendedUse": request.intended_use,
                    "platform": request.platform,
                    "consentStatus": result.status,
                },
            )
        )


def _parse_datetime(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed
