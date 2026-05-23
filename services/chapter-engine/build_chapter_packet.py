#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

CHAPTER_BRIEF = """# Chapter Brief\n\n- Chapter Number: {chapter_number}\n- Chapter Title: {chapter_title}\n- Canon State: draft\n\n## Purpose\n\nTODO\n"""

CHAPTER_DRAFT = """# Chapter {chapter_number}: {chapter_title}\n\nDraft content goes here.\n"""

STORYBOARD = """# Storyboard\n\n## Scene Beats\n\n- Beat 1\n- Beat 2\n"""

IMAGE_GUIDE = """# Chapter Image Prompts\n\n1. Establishing shot\n2. Character moment\n3. Conflict shot\n"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build(project_root: Path, chapter_number: int, chapter_title: str) -> None:
    write(
        project_root / "manuscript/chapter-briefs" / f"chapter-{chapter_number:02d}.md",
        CHAPTER_BRIEF.format(chapter_number=chapter_number, chapter_title=chapter_title),
    )

    write(
        project_root / "manuscript/chapters" / f"chapter-{chapter_number:02d}.md",
        CHAPTER_DRAFT.format(chapter_number=chapter_number, chapter_title=chapter_title),
    )

    write(
        project_root / "storyboards/chapters" / f"chapter-{chapter_number:02d}-storyboard.md",
        STORYBOARD,
    )

    write(
        project_root / "visual-bible/chapter-image-prompts" / f"chapter-{chapter_number:02d}-images.md",
        IMAGE_GUIDE,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    parser.add_argument("chapter_number", type=int)
    parser.add_argument("chapter_title")
    args = parser.parse_args()

    build(args.project_root, args.chapter_number, args.chapter_title)

    print(
        f"Created chapter packet for chapter {args.chapter_number}: {args.chapter_title}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
