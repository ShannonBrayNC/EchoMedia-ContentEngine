from __future__ import annotations

from datetime import date

from scripts.ecosystem_audit import (
    RepoInventory,
    build_issues,
    clone_like,
    infer_dependencies,
    parse_commit_date,
)


def repo(
    name: str,
    group: str,
    *,
    dirty: int = 0,
    stale: bool = False,
    clone: bool = False,
    capabilities: list[str] | None = None,
) -> RepoInventory:
    return RepoInventory(
        name=name,
        path=f"C:\\GitHub\\{name}",
        duplicate_group=group,
        dirty_files=dirty,
        is_stale=stale,
        is_clone=clone,
        capabilities=capabilities or ["content production pipeline"],
    )


def test_dependency_inference_from_manifest_paths() -> None:
    dependencies = infer_dependencies(
        [
            "frontend/package.json",
            "backend/requirements.txt",
            "docker-compose.yml",
        ]
    )

    assert dependencies == ["api runtime", "browser runtime", "docker", "node/npm", "python"]


def test_clone_like_detects_task_specific_checkout_names() -> None:
    assert clone_like("EchoMedia-ContentEngine-pr112", "echomedia-contentengine")
    assert clone_like("OpsHelm-codex-christina", "opshelm")
    assert not clone_like("OpsHelm", "opshelm")


def test_parse_commit_date_returns_none_for_missing_dates() -> None:
    assert parse_commit_date("") is None
    assert parse_commit_date("not-a-date") is None
    assert parse_commit_date("2026-05-30") == date(2026, 5, 30)


def test_build_issues_prioritizes_duplicate_and_dirty_worktrees() -> None:
    issues = build_issues(
        [
            repo("EchoMedia-ContentEngine", "echomedia-contentengine"),
            repo("EchoMedia-ContentEngine-pr112", "echomedia-contentengine", clone=True),
            repo("OpsHelm", "opshelm", dirty=2, stale=True, capabilities=["operations orchestration"]),
        ]
    )

    priorities = [issue["priority"] for issue in issues]
    titles = [issue["title"] for issue in issues]

    assert priorities[:2] == ["P0", "P0"]
    assert "Consolidate duplicate local clones and PR worktrees" in titles
    assert "Resolve dirty worktrees before ecosystem-wide changes" in titles
    assert "Archive or merge temporary Codex/test clones" in titles
    assert "Review stale initiatives for ownership" in titles


def test_build_issues_detects_capability_overlap_as_p2() -> None:
    issues = build_issues(
        [
            repo("a", "a", capabilities=["assistant/review automation"]),
            repo("b", "b", capabilities=["assistant/review automation"]),
        ]
    )

    assert issues[-1]["priority"] == "P2"
    assert issues[-1]["title"] == "Assign clear system ownership for overlapping capabilities"
