#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def collect_chapters(chapter_dir: Path) -> list[Path]:
    return sorted(chapter_dir.glob("chapter-*.md"))


def assemble(chapters: list[Path]) -> str:
    output: list[str] = []

    output.append("# Screenplay Draft\n")

    for chapter in chapters:
        content = chapter.read_text(encoding="utf-8")

        output.append("\n---\n")
        output.append(f"\n## Source: {chapter.name}\n")
        output.append(content)

    return "\n".join(output)


def write_outputs(project_root: Path, screenplay: str, chapter_count: int) -> None:
    export_dir = project_root / "screenplay/exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    screenplay_path = export_dir / "screenplay-draft.md"
    screenplay_path.write_text(screenplay, encoding="utf-8")

    report = {
        "chapter_count": chapter_count,
        "status": "assembled",
        "output": str(screenplay_path),
    }

    report_path = export_dir / "screenplay-assembly-report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    args = parser.parse_args()

    chapter_dir = args.project_root / "manuscript/chapters"
    chapters = collect_chapters(chapter_dir)

    screenplay = assemble(chapters)

    write_outputs(args.project_root, screenplay, len(chapters))

    print(f"Assembled screenplay draft from {len(chapters)} chapter(s).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
