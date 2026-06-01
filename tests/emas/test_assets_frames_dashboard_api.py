import json

from services.emas import route_emas


def seed_project(tmp_path, status="approved"):
    project = tmp_path / "projects" / "Vanessa"
    (project / "metadata").mkdir(parents=True)
    (project / "source-registry.json").write_text(
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
    return project


def create_ad(tmp_path):
    seed_project(tmp_path)
    result = route_emas(
        "POST",
        "/api/ad-studio/projects/Vanessa/ads",
        {"adName": "Vanessa-Christina-Outfit-Update-Ad", "actor": "tester"},
        root_path=str(tmp_path),
    )
    assert result.status == 201
    return tmp_path / "projects" / "Vanessa" / "ads" / "Vanessa-Christina-Outfit-Update-Ad"


def test_route_creates_ad_project_and_dashboard(tmp_path):
    create_ad(tmp_path)

    dashboard = route_emas("GET", "/api/ad-studio/projects/Vanessa/ads/Vanessa-Christina-Outfit-Update-Ad/dashboard", root_path=str(tmp_path))

    assert dashboard.status == 200
    assert dashboard.body["status"] == "Storyboard Draft"
    assert dashboard.body["counts"]["scenes"] == 8


def test_route_uploads_and_tags_reference(tmp_path):
    create_ad(tmp_path)
    source = tmp_path / "vanessa.jpg"
    source.write_bytes(b"fake image")

    uploaded = route_emas(
        "POST",
        "/api/ad-studio/projects/Vanessa/ads/Vanessa-Christina-Outfit-Update-Ad/references",
        {"sourcePath": str(source), "actor": "tester", "tags": ["pink-updated-outfit"], "outfit": "pink-updated-outfit"},
        root_path=str(tmp_path),
    )
    assert uploaded.status == 201
    asset_id = uploaded.body["asset"]["asset_id"]

    tagged = route_emas(
        "POST",
        f"/api/ad-studio/projects/Vanessa/ads/Vanessa-Christina-Outfit-Update-Ad/references/{asset_id}/tag",
        {"actor": "tester", "tags": ["smiling"], "approved": True},
        root_path=str(tmp_path),
    )
    assert tagged.status == 200
    assert tagged.body["asset"]["approved"] is True

    listed = route_emas("GET", "/api/ad-studio/projects/Vanessa/ads/Vanessa-Christina-Outfit-Update-Ad/references", root_path=str(tmp_path))
    assert listed.body["count"] == 1


def test_route_submits_and_approves_frame(tmp_path):
    create_ad(tmp_path)
    source = tmp_path / "frame.png"
    source.write_bytes(b"fake frame")

    submitted = route_emas(
        "POST",
        "/api/ad-studio/projects/Vanessa/ads/Vanessa-Christina-Outfit-Update-Ad/storyboard/frames",
        {"sourcePath": str(source), "sceneId": "scene-01", "actor": "tester"},
        root_path=str(tmp_path),
    )
    assert submitted.status == 201
    frame_id = submitted.body["frame"]["frame_id"]

    approved = route_emas(
        "POST",
        f"/api/ad-studio/projects/Vanessa/ads/Vanessa-Christina-Outfit-Update-Ad/storyboard/frames/{frame_id}/approve",
        {"actor": "tester", "notes": "approved"},
        root_path=str(tmp_path),
    )
    assert approved.status == 200
    assert approved.body["frame"]["state"] == "approved"


def test_route_generation_preflight_blocks_pending_consent(tmp_path):
    seed_project(tmp_path, status="pending")
    # Force create ad structure with service precondition satisfied.
    route_emas("POST", "/api/ad-studio/projects/Vanessa/ads", {"adName": "Ad", "actor": "tester"}, root_path=str(tmp_path))

    result = route_emas(
        "POST",
        "/api/ad-studio/projects/Vanessa/ads/Ad/generate/preflight",
        {"actor": "tester", "intendedUse": "social_media", "platform": "instagram", "prompt": "Create the ad scene."},
        root_path=str(tmp_path),
    )

    assert result.status == 409
    assert result.body["allowed"] is False
    assert any("pending" in reason for reason in result.body["reasons"])


def test_route_publish_package(tmp_path):
    ad_root = create_ad(tmp_path)
    asset = tmp_path / "final-video.mp4"
    asset.write_bytes(b"fake video")
    output_metadata = tmp_path / "output.json"
    output_metadata.write_text(
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

    result = route_emas(
        "POST",
        "/api/ad-studio/projects/Vanessa/ads/Vanessa-Christina-Outfit-Update-Ad/outputs/output-1/publish",
        {"actor": "tester", "outputMetadataPath": str(output_metadata), "exportRoot": str(ad_root / "exports")},
        root_path=str(tmp_path),
    )

    assert result.status == 202
    assert result.body["published"] is True
    assert result.body["manifestPath"].endswith("publish-manifest.json")
