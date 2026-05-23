#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from memory_store import upsert_memory


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_id")
    parser.add_argument("target_root", type=Path)
    args = parser.parse_args()

    indexed = 0

    for path in args.target_root.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        upsert_memory(args.project_id, str(path), content, memory_type="markdown")
        indexed += 1

    for path in args.target_root.rglob("*.json"):
        content = path.read_text(encoding="utf-8")
        upsert_memory(args.project_id, str(path), content, memory_type="json")
        indexed += 1

    print(f"Indexed {indexed} artifact(s) into semantic memory.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
