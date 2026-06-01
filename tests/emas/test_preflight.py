import json

from services.emas import (
    AppendOnlyAuditLogger,
    GenerationPreflightRequest,
    GenerationPreflightService,
    JsonFileSourceRegistryAdapter,
    SourceRegistryService,
)


def write_registry(path, status="approved"):
    path.write_text(
        json.dumps(
            {
                "records": [
                    {
                        "subjectId": "Vanessa",
                        "projectName": "Vanessa",
                        "displayName": "Vanessa",
                        "consentStatus": status,
                        "allowedUses": ["social_media"],
                        "restrictedUses": ["deceptive_impersonation"],
                        "allowedPlatforms": ["instagram"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def make_service(tmp_path, status="approved"):
    registry = tmp_path / "source-registry.json"
    write_registry(registry, status=status)
    audit = AppendOnlyAuditLogger(tmp_path / "audit.jsonl")
    source_registry = SourceRegistryService(JsonFileSourceRegistryAdapter(registry), audit)
    return GenerationPreflightService(source_registry, audit), audit


def request(**overrides):
    data = {
        "project_name": "Vanessa",
        "ad_name": "Ad",
        "subject_id": "Vanessa",
        "intended_use": "social_media",
        "platform": "instagram",
        "actor": "tester",
        "prompt": "Create the outfit update scene.",
        "reference_paths": [],
        "output_count": 1,
    }
    data.update(overrides)
    return GenerationPreflightRequest(**data)


def test_preflight_allows_approved_consent(tmp_path):
    service, audit = make_service(tmp_path)

    result = service.validate(request())

    assert result.allowed is True
    assert result.source_registry_verified is True
    assert audit.verify() is True


def test_preflight_blocks_pending_consent(tmp_path):
    service, audit = make_service(tmp_path, status="pending")

    result = service.validate(request())

    assert result.allowed is False
    assert result.source_registry_verified is False
    assert any("pending" in reason for reason in result.reasons)
    assert audit.verify() is True


def test_preflight_blocks_bad_output_count(tmp_path):
    service, _ = make_service(tmp_path)

    result = service.validate(request(output_count=11))

    assert result.allowed is False
    assert any("Output count" in reason for reason in result.reasons)


def test_preflight_normalizes_risky_terms(tmp_path):
    service, _ = make_service(tmp_path)

    result = service.validate(request(prompt="Make a perfect clone for the ad."))

    assert "authorized synthetic likeness" in result.normalized_prompt.lower()
