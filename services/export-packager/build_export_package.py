#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

PACKAGE_MAP = {
    "author-review": [
        "manuscript",
        "storyboards",
        "reports",
    ],
    "screenplay-review": [
        "screenplay",
        "reports",
    ],
    "full-project": [
        "canon",
        "characters",
        "story",
        "manuscript",
        "storyboards",
        "screenplay",
        "reports",
    ],
}


def collect_paths(project_root: Path, package_type: str) -> list[str]:
    selected = PACKAGE_MAP.get(package_type, [])
    collected: list[str] = []

    for name in selected:
        target = project_root / name
        if target.exists():
            collected.append(str(target))

    return collected


def write_package(project_root: Path, package_type: str, collected: list[str]) -> None:
    package_dir = project_root / "exports/packages" / package_type
    package_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "package_type": package_type,
        "artifact_count": len(collected),
        "artifacts": collected,
    }

    manifest_path = package_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    contents_path = package_dir / "contents.md"

    lines = ["# Export Package", ""]

    for item in collected:
        lines.append(f"- {item}")

    contents_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    parser.add_argument("package_type")
    args = parser.parse_args()

    collected = collect_paths(args.project_root, args.package_type)

    write_package(args.project_root, args.package_type, collected)

    print(f"Created export package: {args.package_type}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
