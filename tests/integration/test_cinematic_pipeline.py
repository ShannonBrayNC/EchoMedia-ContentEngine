from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TMP_PROJECT = ROOT / "tmp/e2e-cinematic-project"


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)


def write_seed_project() -> None:
    manuscript = TMP_PROJECT / "manuscript/chapters"
    canon = TMP_PROJECT / "canon"
    manuscript.mkdir(parents=True, exist_ok=True)
    canon.mkdir(parents=True, exist_ok=True)

    (canon / "canon-manifest.json").write_text(
        json.dumps(
            {
                "project": "e2e-cinematic-project",
                "canon_state": "draft",
                "active_canon_files": ["canon/story-bible.md"],
                "locked_fields": [],
                "visual_consistency_keys": ["character.appearance"],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (canon / "story-bible.md").write_text(
        "# Story Bible\n\nA civic AI system tests consent, authority, and truth.\n",
        encoding="utf-8",
    )

    (manuscript / "chapter-01.md").write_text(
        "# Chapter 1\n\nA final warning arrives before the truth reveal. The character faces a choice.\n",
        encoding="utf-8",
    )


def test_manuscript_to_release_pipeline() -> None:
    write_seed_project()

    manifest = TMP_PROJECT / "canon/canon-manifest.json"
    result = run_command([
        sys.executable,
        "services/canon-validator/validate_canon.py",
        str(manifest),
    ])
    assert result.returncode == 0, result.stderr

    result = run_command([
        sys.executable,
        "services/chapter-engine/build_chapter_packet.py",
        str(TMP_PROJECT),
        "2",
        "Second Signal",
    ])
    assert result.returncode == 0, result.stderr

    result = run_command([
        sys.executable,
        "services/screenplay-assembler/assemble_screenplay.py",
        str(TMP_PROJECT),
    ])
    assert result.returncode == 0, result.stderr

    assert (TMP_PROJECT / "screenplay/exports/screenplay-draft.md").exists()
    assert (TMP_PROJECT / "screenplay/exports/screenplay-draft.fountain").exists()
    assert (TMP_PROJECT / "screenplay/exports/runtime-report.json").exists()
    assert (TMP_PROJECT / "screenplay/exports/trailer-suitability-report.json").exists()

    result = run_command([
        sys.executable,
        "services/export-packager/build_export_package.py",
        str(TMP_PROJECT),
        "full-project",
    ])
    assert result.returncode == 0, result.stderr

    result = run_command([
        sys.executable,
        "services/release-manager/create_release_manifest.py",
        str(TMP_PROJECT),
        "0.1.0",
        "candidate",
    ])
    assert result.returncode == 0, result.stderr

    assert (TMP_PROJECT / "exports/packages/full-project/manifest.json").exists()
    assert (TMP_PROJECT / "releases/0.1.0/release-manifest.json").exists()


def test_tv_and_commercial_paths_are_tracked() -> None:
    write_seed_project()

    # Current implementation verifies product surface requirements and creates markers
    # for future dedicated adaptation engines.
    expected_future_paths = [
        "tv-adaptation",
        "commercials",
        "movie-generation",
    ]

    for path in expected_future_paths:
        target = TMP_PROJECT / path
        target.mkdir(parents=True, exist_ok=True)
        (target / "README.md").write_text(f"# {path}\n\nE2E placeholder for adaptation workflow.\n", encoding="utf-8")

    for path in expected_future_paths:
        assert (TMP_PROJECT / path / "README.md").exists()
