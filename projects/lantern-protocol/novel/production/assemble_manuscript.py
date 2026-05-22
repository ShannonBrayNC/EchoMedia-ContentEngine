#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "manuscript" / "chapters"
EXPORTS = ROOT / "exports"

OUTPUT_MANUSCRIPT = EXPORTS / "lantern-protocol-novel-draft.md"
OUTPUT_REPORT = EXPORTS / "lantern-protocol-novel-report.md"


def chapter_sort_key(path: Path) -> int:
    match = re.search(r"chapter-(\d+)", path.name, flags=re.IGNORECASE)
    return int(match.group(1)) if match else 999


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def main() -> None:
    EXPORTS.mkdir(parents=True, exist_ok=True)

    chapters = sorted(CHAPTERS.glob("chapter-*.md"), key=chapter_sort_key)
    if not chapters:
        raise FileNotFoundError(f"No chapter files found under {CHAPTERS}")

    manuscript_parts = [
        "# Lantern Protocol — Novel Draft",
        "",
        "> Auto-assembled from `novel/manuscript/chapters/`.",
        "",
        "---",
        "",
    ]

    report_lines = [
        "# Lantern Protocol — Novel Assembly Report",
        "",
        "| Chapter File | Words |",
        "|---|---:|",
    ]

    total_words = 0

    for chapter in chapters:
        text = chapter.read_text(encoding="utf-8")
        words = word_count(text)
        total_words += words

        manuscript_parts.append(f"<!-- SOURCE: {chapter.name} -->")
        manuscript_parts.append(text.rstrip())
        manuscript_parts.append("")
        manuscript_parts.append("---")
        manuscript_parts.append("")

        report_lines.append(f"| `{chapter.name}` | {words} |")

    report_lines.extend([
        "",
        f"**Total chapters:** {len(chapters)}",
        f"**Total words:** {total_words}",
        "",
    ])

    OUTPUT_MANUSCRIPT.write_text("\n".join(manuscript_parts).rstrip() + "\n", encoding="utf-8")
    OUTPUT_REPORT.write_text("\n".join(report_lines).rstrip() + "\n", encoding="utf-8")

    print(f"Wrote {OUTPUT_MANUSCRIPT}")
    print(f"Wrote {OUTPUT_REPORT}")
    print(f"Total words: {total_words}")


if __name__ == "__main__":
    main()
