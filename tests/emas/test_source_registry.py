import json
from datetime import datetime, timedelta, timezone

from services.emas.audit import AppendOnlyAuditLogger
from services.emas.source_registry import (
    ConsentVerificationRequest,
    JsonFileSourceRegistryAdapter,
    SourceRegistryService,
)


def write_registry(path, record):
    path.write_text(json.dumps({"records": [record]}), encoding="utf-8")


def base_record(**overrides):
    record = {
        "subjectId": "Vanessa",
        "projectName": "Vanessa",
        "displayName": "Vanessa",
        "consentStatus": "approved",
        "allowedUses": ["social_media", "marketing"],
        "restrictedUses": ["deceptive_impersonation"],
        "allowedPlatforms": ["instagram"],
    }
    record.update(overrides)
    return record


def request(**overrides):
    data = {
        "project_name": "Vanessa",
        "subject_id": "Vanessa",
        "intended_use": "social_media",
        "platform": "instagram",
        "action": "publish",
        "actor": "tester",
        "ad_name": "ad",
    }
    data.update(overrides)
    return ConsentVerificationRequest(**data)


def test_allows_approved_use_and_platform(tmp_path):
    registry_path = tmp_path / "source-registry.json"
    write_registry(registry_path, base_record())
    audit = AppendOnlyAuditLogger(tmp_path / "audit.jsonl")
    service = SourceRegistryService(JsonFileSourceRegistryAdapter(registry_path), audit)

    result = service.verify_consent(request())

    assert result.allowed is True
    assert audit.verify() is True


def test_blocks_missing_record(tmp_path):
    service = SourceRegistryService(JsonFileSourceRegistryAdapter(tmp_path / "missing.json"))

    result = service.verify_consent(request())

    assert result.allowed is False
    assert result.status == "missing"


def test_blocks_revoked_consent(tmp_path):
    registry_path = tmp_path / "source-registry.json"
    write_registry(registry_path, base_record(consentStatus="revoked"))
    service = SourceRegistryService(JsonFileSourceRegistryAdapter(registry_path))

    result = service.verify_consent(request())

    assert result.allowed is False
    assert result.status == "revoked"


def test_blocks_expired_consent(tmp_path):
    registry_path = tmp_path / "source-registry.json"
    expired = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    write_registry(registry_path, base_record(expiresAt=expired))
    service = SourceRegistryService(JsonFileSourceRegistryAdapter(registry_path))

    result = service.verify_consent(request())

    assert result.allowed is False
    assert result.status == "expired"


def test_blocks_wrong_platform(tmp_path):
    registry_path = tmp_path / "source-registry.json"
    write_registry(registry_path, base_record())
    service = SourceRegistryService(JsonFileSourceRegistryAdapter(registry_path))

    result = service.verify_consent(request(platform="tiktok"))

    assert result.allowed is False
    assert "Platform not allowed" in result.reason
