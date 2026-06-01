"""Generation preflight checks for EchoMedia Ad Studio.

This sprint wires source-registry consent and audit logging into generation readiness.
Provider calls must not happen unless this preflight succeeds.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .audit import AppendOnlyAuditLogger, AuditEvent
from .source_registry import ConsentVerificationRequest, SourceRegistryService


@dataclass(frozen=True)
class GenerationPreflightRequest:
    project_name: str
    ad_name: str | None
    subject_id: str
    intended_use: str
    platform: str | None
    actor: str
    prompt: str
    reference_paths: list[str] = field(default_factory=list)
    output_count: int = 1


@dataclass(frozen=True)
class GenerationPreflightResult:
    allowed: bool
    reasons: list[str]
    normalized_prompt: str
    source_registry_verified: bool


class GenerationPreflightService:
    def __init__(self, source_registry: SourceRegistryService, audit_logger: AppendOnlyAuditLogger | None = None):
        self.source_registry = source_registry
        self.audit_logger = audit_logger

    def validate(self, request: GenerationPreflightRequest) -> GenerationPreflightResult:
        reasons: list[str] = []
        normalized_prompt = normalize_prompt(request.prompt)

        if not request.prompt.strip():
            reasons.append("Prompt is required.")

        if request.output_count < 1 or request.output_count > 10:
            reasons.append("Output count must be between 1 and 10.")

        for reference in request.reference_paths:
            path = Path(reference)
            if not path.exists():
                reasons.append(f"Reference does not exist: {reference}")
            if "references/rejected" in reference.replace("\\", "/"):
                reasons.append(f"Rejected reference cannot be used: {reference}")
            if "references/pending" in reference.replace("\\", "/"):
                reasons.append(f"Pending reference cannot be used: {reference}")

        consent = self.source_registry.verify_consent(
            ConsentVerificationRequest(
                project_name=request.project_name,
                subject_id=request.subject_id,
                intended_use=request.intended_use,
                platform=request.platform,
                action="generate",
                actor=request.actor,
                ad_name=request.ad_name,
            )
        )

        if not consent.allowed:
            reasons.append(consent.reason or "Source-registry consent verification failed.")

        allowed = len(reasons) == 0

        result = GenerationPreflightResult(
            allowed=allowed,
            reasons=reasons,
            normalized_prompt=normalized_prompt,
            source_registry_verified=consent.allowed,
        )

        if self.audit_logger:
            self.audit_logger.append(
                AuditEvent(
                    actor=request.actor,
                    action="generation_preflight_completed" if allowed else "generation_preflight_blocked",
                    project_name=request.project_name,
                    ad_name=request.ad_name,
                    target_type="generation_request",
                    target_id=request.subject_id,
                    result="success" if allowed else "blocked",
                    reason="; ".join(reasons) if reasons else None,
                    metadata={
                        "intendedUse": request.intended_use,
                        "platform": request.platform,
                        "outputCount": request.output_count,
                        "sourceRegistryVerified": consent.allowed,
                    },
                )
            )

        return result


def normalize_prompt(prompt: str) -> str:
    value = " ".join(prompt.strip().split())
    replacements = {
        "perfect clone": "authorized synthetic likeness",
        "clone": "authorized synthetic likeness",
        "deepfake": "authorized synthetic likeness",
        "make it look real": "make it polished and clearly synthetic",
    }
    lowered = value.lower()
    for needle, replacement in replacements.items():
        if needle in lowered:
            value = value.replace(needle, replacement).replace(needle.title(), replacement)
            lowered = value.lower()
    if value and "authorized" not in lowered:
        value = f"Authorized synthetic likeness request. {value}"
    return value
