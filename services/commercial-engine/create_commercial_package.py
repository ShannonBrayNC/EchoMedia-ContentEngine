#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

COMMERCIAL_TYPES = [
    "15-second-social",
    "30-second-commercial",
    "60-second-trailer",
]


def build_package(project_root: Path) -> dict:
    commercials = []

    for commercial_type in COMMERCIAL_TYPES:
        commercials.append(
            {
                "commercial_type": commercial_type,
                "status": "draft",
                "hook": "TODO",
                "voiceover": "TODO",
                "call_to_action": "TODO",
                "target_platforms": ["YouTube", "TikTok", "Instagram"],
            }
        )

    return {
        "project_root": str(project_root),
        "commercials": commercials,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    args = parser.parse_args()

    package = build_package(args.project_root)
    out_dir = args.project_root / "commercials"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "commercial-package.json"
    out_path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")

    print(f"Created commercial package: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
