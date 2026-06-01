import json

import pytest

from services.emas import AdProjectScaffoldService, AppendOnlyAuditLogger, CreateAdProjectRequest


def test_create_ad_project_scaffold(tmp_path):
    project = tmp_path / "projects" / "Vanessa"
    (project / "metadata").mkdir(parents=True)
    (project / "source-registry.json").write_text('{"records": []}', encoding="utf-8")
    audit = AppendOnlyAuditLogger(project / "metadata" / "audit-log.jsonl")
    service = AdProjectScaffoldService(audit)

    result = service.create_ad_project(
        CreateAdProjectRequest(
            project_name="Vanessa",
            ad_name="Vanessa-Christina-Outfit-Update-Ad",
            actor="tester",
            root_path=str(tmp_path),
        )
    )

    ad_root = tmp_path / "projects" / "Vanessa" / "ads" / "Vanessa-Christina-Outfit-Update-Ad"
    assert result.created is True
    assert ad_root.exists()
    assert (ad_root / "script" / "final-script.md").exists()
    assert (ad_root / "storyboard" / "storyboard.md").exists()
    assert (ad_root / "metadata" / "scene-index.json").exists()
    scenes = json.loads((ad_root / "metadata" / "scene-index.json").read_text(encoding="utf-8"))
    assert len(scenes) == 8
    assert audit.verify() is True


def test_create_ad_project_requires_parent_project(tmp_path):
    service = AdProjectScaffoldService()

    with pytest.raises(FileNotFoundError):
        service.create_ad_project(
            CreateAdProjectRequest(
                project_name="Vanessa",
                ad_name="Ad",
                actor="tester",
                root_path=str(tmp_path),
            )
        )


def test_create_ad_project_refuses_duplicate_without_force(tmp_path):
    project = tmp_path / "projects" / "Vanessa"
    (project / "metadata").mkdir(parents=True)
    service = AdProjectScaffoldService()
    request = CreateAdProjectRequest(
        project_name="Vanessa",
        ad_name="Ad",
        actor="tester",
        root_path=str(tmp_path),
    )

    service.create_ad_project(request)

    with pytest.raises(FileExistsError):
        service.create_ad_project(request)
