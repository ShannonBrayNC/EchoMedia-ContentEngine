#!/usr/bin/env python3
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
FRONT_MATTER = ROOT / "manuscript" / "front-matter"
CHAPTERS = ROOT / "manuscript" / "chapters"
EXPORTS = ROOT / "exports"

OUTPUT_MANUSCRIPT = EXPORTS / "lantern-protocol-novel-draft.md"
OUTPUT_REPORT = EXPORTS / "lantern-protocol-novel-report.md"

MANUSCRIPT_START = "## Manuscript"
NOTES_STARTERS = ["## Continuity Notes", "## Revision Notes"]


@dataclass(frozen=True)
class ChapterStats:
    path: Path
    chapter_number: int
    title: str
    total_words: int
    body_words: int
    has_manuscript_section: bool


def chapter_sort_key(path: Path) -> int:
    match = re.search(r"chapter-(\d+)", path.name, flags=re.IGNORECASE)
    return int(match.group(1)) if match else 999


def front_matter_sort_key(path: Path) -> int:
    order = {
        "preface": 10,
        "foreword": 20,
        "introduction": 30,
        "author-note": 40,
    }
    return order.get(path.stem.lower(), 999)


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+(?:['-]\w+)?\b", text))


def get_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def manuscript_body(text: str) -> str:
    start = text.find(MANUSCRIPT_START)
    if start == -1:
        return text

    body = text[start + len(MANUSCRIPT_START):]
    earliest_note = len(body)
    for marker in NOTES_STARTERS:
        idx = body.find(marker)
        if idx != -1:
            earliest_note = min(earliest_note, idx)
    return body[:earliest_note].strip()


def chapter_stats(path: Path) -> ChapterStats:
    text = path.read_text(encoding="utf-8")
    chapter_no = chapter_sort_key(path)
    body = manuscript_body(text)
    return ChapterStats(
        path=path,
        chapter_number=chapter_no,
        title=get_title(text, path.stem),
        total_words=word_count(text),
        body_words=word_count(body),
        has_manuscript_section=MANUSCRIPT_START in text,
    )


def build_report(stats: List[ChapterStats], front_matter_files: List[Path]) -> str:
    total_words = sum(item.total_words for item in stats)
    total_body_words = sum(item.body_words for item in stats)
    front_matter_words = sum(word_count(path.read_text(encoding="utf-8")) for path in front_matter_files)

    lines = [
        "# Lantern Protocol — Novel Assembly Report",
        "",
        "## Front Matter",
        "",
        "| Order | File | Words |",
        "|---:|---|---:|",
    ]

    if front_matter_files:
        for idx, path in enumerate(front_matter_files, start=1):
            lines.append(f"| {idx} | `{path.name}` | {word_count(path.read_text(encoding='utf-8'))} |")
    else:
        lines.append("| - | None | 0 |")

    lines.extend(
        [
            "",
            "## Chapters",
            "",
            "| Chapter | Title | File | Total Words | Manuscript Body Words | Manuscript Section |",
            "|---:|---|---|---:|---:|---|",
        ]
    )

    for item in stats:
        has_section = "Yes" if item.has_manuscript_section else "No"
        lines.append(
            f"| {item.chapter_number} | {item.title} | `{item.path.name}` | {item.total_words} | {item.body_words} | {has_section} |"
        )

    lines.extend(
        [
            "",
            f"**Front matter files:** {len(front_matter_files)}",
            f"**Front matter words:** {front_matter_words}",
            f"**Total chapters:** {len(stats)}",
            f"**Total words:** {total_words + front_matter_words}",
            f"**Total chapter words:** {total_words}",
            f"**Total manuscript body words:** {total_body_words}",
            "",
            "## Notes",
            "",
            "- Total words include front matter, chapter metadata, canon sources, continuity notes, and revision notes.",
            "- Manuscript body words count only text after `## Manuscript` and before continuity/revision notes inside chapter files.",
            "- Use manuscript body words for draft-length tracking.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    EXPORTS.mkdir(parents=True, exist_ok=True)

    chapters = sorted(CHAPTERS.glob("chapter-*.md"), key=chapter_sort_key)
    if not chapters:
        raise FileNotFoundError(f"No chapter files found under {CHAPTERS}")

    front_matter_files = []
    if FRONT_MATTER.exists():
        front_matter_files = sorted(FRONT_MATTER.glob("*.md"), key=front_matter_sort_key)

    stats = [chapter_stats(chapter) for chapter in chapters]

    manuscript_parts = [
        "# Lantern Protocol — Novel Draft",
        "",
        "> Auto-assembled from `novel/manuscript/front-matter/` and `novel/manuscript/chapters/`.",
        "",
        "---",
        "",
    ]

    for front_matter in front_matter_files:
        text = front_matter.read_text(encoding="utf-8")
        manuscript_parts.append(f"<!-- SOURCE: front-matter/{front_matter.name} -->")
        manuscript_parts.append(text.rstrip())
        manuscript_parts.append("")
        manuscript_parts.append("---")
        manuscript_parts.append("")

    for chapter in chapters:
        text = chapter.read_text(encoding="utf-8")
        manuscript_parts.append(f"<!-- SOURCE: chapters/{chapter.name} -->")
        manuscript_parts.append(text.rstrip())
        manuscript_parts.append("")
        manuscript_parts.append("---")
        manuscript_parts.append("")

    OUTPUT_MANUSCRIPT.write_text("\n".join(manuscript_parts).rstrip() + "\n", encoding="utf-8")
    OUTPUT_REPORT.write_text(build_report(stats, front_matter_files), encoding="utf-8")

    total_body_words = sum(item.body_words for item in stats)
    print(f"Wrote {OUTPUT_MANUSCRIPT}")
    print(f"Wrote {OUTPUT_REPORT}")
    print(f"Front matter files: {len(front_matter_files)}")
    print(f"Total chapters: {len(stats)}")
    print(f"Total manuscript body words: {total_body_words}")


if __name__ == "__main__":
    main()
