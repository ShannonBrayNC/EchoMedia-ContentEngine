#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

VALID_STATES = {
    "draft",
    "candidate",
    "approved",
    "released",
    "superseded",
    "archived",
}


def build_manifest(project_root: Path, version: str, state: str) -> dict:
    exports_dir = project_root / "exports"
    screenplay_dir = project_root / "screenplay"

    artifacts = []

    if exports_dir.exists():
        artifacts.append(str(exports_dir))

    if screenplay_dir.exists():
        artifacts.append(str(screenplay_dir))

    return {
        "version": version,
        "release_state": state,
        "generated_at": datetime.now(UTC).isoformat(),
        "artifacts": artifacts,
        "governance": {
            "canon_validation_required": True,
            "continuity_validation_required": True,
            "semantic_validation_required": True,
        },
    }


def write_release(project_root: Path, version: str, manifest: dict) -> None:
    release_dir = project_root / "releases" / version
    release_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = release_dir / "release-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    notes_path = release_dir / "release-notes.md"
    notes_path.write_text(
        "\n".join(
            [
                f"# Release {manifest['version']}",
                "",
                f"State: {manifest['release_state']}",
                "",
                "## Included Artifacts",
                "",
                *[f"- {artifact}" for artifact in manifest["artifacts"]],
            ]
        ) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    parser.add_argument("version")
    parser.add_argument("release_state")
    args = parser.parse_args()

    if args.release_state not in VALID_STATES:
        raise SystemExit(f"Invalid release state: {args.release_state}")

    manifest = build_manifest(args.project_root, args.version, args.release_state)

    write_release(args.project_root, args.version, manifest)

    print(f"Created release manifest for version {args.version}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
