import json

from services.emas.audit import AppendOnlyAuditLogger
from services.emas.publishing import ExportPackagePublishAdapter, PublishRequest
from services.emas.source_registry import JsonFileSourceRegistryAdapter, SourceRegistryService


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
                        "allowedUses": ["social_media", "marketing"],
                        "restrictedUses": ["deceptive_impersonation"],
                        "allowedPlatforms": ["instagram"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def publish_request(tmp_path, metadata_path):
    return PublishRequest(
        project_name="Vanessa",
        ad_name="Vanessa-Christina-Outfit-Update-Ad",
        output_id="output-1",
        platform="instagram",
        format="reels-9x16",
        requested_by="tester",
        intended_use="social_media",
        output_metadata_path=str(metadata_path),
        export_root=str(tmp_path / "exports"),
    )


def make_service(tmp_path, status="approved"):
    registry_path = tmp_path / "source-registry.json"
    write_registry(registry_path, status=status)
    audit = AppendOnlyAuditLogger(tmp_path / "audit.jsonl")
    source_registry = SourceRegistryService(JsonFileSourceRegistryAdapter(registry_path), audit)
    return ExportPackagePublishAdapter(source_registry, audit), audit


def test_cannot_publish_draft(tmp_path):
    metadata_path = tmp_path / "output.json"
    metadata_path.write_text(json.dumps({"state": "draft", "disclosure": "AI-generated authorized likeness image.", "assets": []}))
    service, audit = make_service(tmp_path)

    result = service.publish(publish_request(tmp_path, metadata_path))

    assert result.published is False
    assert result.state == "blocked"
    assert audit.verify() is True


def test_cannot_publish_without_disclosure(tmp_path):
    asset = tmp_path / "final-video.mp4"
    asset.write_text("fake video", encoding="utf-8")
    metadata_path = tmp_path / "output.json"
    metadata_path.write_text(json.dumps({"state": "approved", "assets": [str(asset)]}))
    service, _ = make_service(tmp_path)

    result = service.publish(publish_request(tmp_path, metadata_path))

    assert result.published is False


def test_can_publish_approved_output(tmp_path):
    asset = tmp_path / "final-video.mp4"
    asset.write_text("fake video", encoding="utf-8")
    metadata_path = tmp_path / "output.json"
    metadata_path.write_text(
        json.dumps(
            {
                "state": "approved",
                "disclosure": "AI-generated authorized likeness image.",
                "assets": [str(asset)],
                "caption": "EchoMedia.ai | Powered by Lantern Protocol",
            }
        ),
        encoding="utf-8",
    )
    service, audit = make_service(tmp_path)

    result = service.publish(publish_request(tmp_path, metadata_path))

    assert result.published is True
    assert result.state == "published"
    assert result.manifest_path.endswith("publish-manifest.json")
    assert audit.verify() is True
    updated = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert updated["state"] == "published"


def test_consent_blocks_publish(tmp_path):
    asset = tmp_path / "final-video.mp4"
    asset.write_text("fake video", encoding="utf-8")
    metadata_path = tmp_path / "output.json"
    metadata_path.write_text(json.dumps({"state": "approved", "disclosure": "AI-generated authorized likeness image.", "assets": [str(asset)]}))
    service, audit = make_service(tmp_path, status="revoked")

    result = service.publish(publish_request(tmp_path, metadata_path))

    assert result.published is False
    assert audit.verify() is True
