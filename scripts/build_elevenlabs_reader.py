#!/usr/bin/env python3
"""Build plain-text listening files from Book 1 Pass 2 markdown chapters.

Usage:
    python scripts/build_elevenlabs_reader.py --repo-root .
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

BOOK_ROOT = Path(
    "projects/lantern-universe/series/silver-bullet-trilogy/books/book-01-silver-bullet"
)
SOURCE_DIR = BOOK_ROOT / "manuscript" / "pass-02"
OUTPUT_DIR = Path("build/elevenlabs/book-01-silver-bullet")

CHAPTERS = [f"chapter-{i:02d}.md" for i in range(1, 31)]


def clean_markdown(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"^#\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.replace("—", " — ")
    text = text.replace("  —  ", " — ")
    return text.strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    source_dir = repo_root / SOURCE_DIR
    out_dir = repo_root / OUTPUT_DIR
    chapter_out = out_dir / "chapters"
    chapter_out.mkdir(parents=True, exist_ok=True)

    combined_parts: list[str] = []

    missing: list[str] = []
    for chapter_name in CHAPTERS:
        source = source_dir / chapter_name
        if not source.exists():
            missing.append(str(source))
            continue
        raw = source.read_text(encoding="utf-8")
        clean = clean_markdown(raw)
        out_name = chapter_name.replace(".md", ".txt")
        (chapter_out / out_name).write_text(clean, encoding="utf-8")
        combined_parts.append(clean)

    if missing:
        raise FileNotFoundError("Missing chapters:\n" + "\n".join(missing))

    full_text = "\n\n".join(combined_parts).strip() + "\n"
    (out_dir / "full-book.txt").write_text(full_text, encoding="utf-8")

    print(f"Wrote: {out_dir / 'full-book.txt'}")
    print(f"Wrote chapter files to: {chapter_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
