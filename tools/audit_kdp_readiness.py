from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path.cwd()

WORD_RE = re.compile(r"\b[\w'’-]+\b")
CHAPTER_RE = re.compile(r"^chapter-(\d{2})-.+\.md$")
PLACEHOLDER_RE = re.compile(r"Draft placeholder|Replace this section|TODO|TBD", re.IGNORECASE)

BOOKS = {
    "book-1": {
        "title": "The Living Anchor",
        "chapters": ROOT / "projects" / "lantern-protocol" / "novel" / "manuscript" / "chapters",
        "minimum_total_words": 38000,
        "target_total_words": 45000,
        "minimum_chapter_words": 1000,
        "warn_chapter_words": 1500,
    },
    "book-2": {
        "title": "The Separate Agreements",
        "chapters": ROOT / "projects" / "lantern-protocol" / "novel" / "book-ii" / "manuscript" / "chapters",
        "minimum_total_words": 70000,
        "target_total_words": 78000,
        "minimum_chapter_words": 2000,
        "warn_chapter_words": 2500,
    },
}


@dataclass
class ChapterAudit:
    name: str
    words: int
    placeholder: bool
    has_manuscript: bool


def extract_section(content: str, start_heading: str, end_pattern: str) -> str:
    start = content.find(start_heading)
    if start < 0:
        return ""
    rest = content[start + len(start_heading):]
    match = re.search(end_pattern, rest, flags=re.MULTILINE)
    return (rest[: match.start()] if match else rest).strip()


def extract_manuscript(content: str) -> str:
    return extract_section(
        content,
        "## Manuscript",
        r"\n##\s+(Continuity Notes|Revision Notes|Processing Metadata)\b",
    ).strip()


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def chapter_files(path: Path) -> list[Path]:
    if not path.exists():
        raise FileNotFoundError(f"Chapter folder not found: {path}")
    files = [p for p in path.iterdir() if CHAPTER_RE.match(p.name)]
    return sorted(files, key=lambda p: int(CHAPTER_RE.match(p.name).group(1)))


def audit_book(book_key: str) -> tuple[dict, list[ChapterAudit]]:
    config = BOOKS[book_key]
    audits: list[ChapterAudit] = []

    for path in chapter_files(config["chapters"]):
        content = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        body = extract_manuscript(content)
        audits.append(
            ChapterAudit(
                name=path.name,
                words=word_count(body),
                placeholder=bool(PLACEHOLDER_RE.search(content)),
                has_manuscript=bool(body),
            )
        )

    return config, audits


def print_audit(book_key: str) -> bool:
    config, audits = audit_book(book_key)
    total = sum(item.words for item in audits)

    print(f"{book_key}: {config['title']}")
    print(f"  chapters: {len(audits)}")
    print(f"  total manuscript words: {total}")
    print(f"  minimum total words: {config['minimum_total_words']}")
    print(f"  target total words: {config['target_total_words']}")
    print()

    failed = False

    if total < config["minimum_total_words"]:
        failed = True
        print(f"  FAIL: total is below minimum by {config['minimum_total_words'] - total} words")
    elif total < config["target_total_words"]:
        print(f"  WARN: total is below target by {config['target_total_words'] - total} words")
    else:
        print("  PASS: total meets target")

    for item in audits:
        notes: list[str] = []
        if not item.has_manuscript:
            notes.append("missing manuscript body")
        if item.placeholder:
            notes.append("placeholder detected")
        if item.words < config["minimum_chapter_words"]:
            notes.append(f"below minimum chapter floor ({item.words} words)")
        elif item.words < config["warn_chapter_words"]:
            notes.append(f"below warning chapter target ({item.words} words)")

        if notes:
            if "below minimum" in " ".join(notes) or item.placeholder or not item.has_manuscript:
                failed = True
            print(f"  - {item.name}: {'; '.join(notes)}")

    print()
    print("  RESULT:", "FAIL" if failed else "PASS")
    print()
    return not failed


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Lantern Protocol KDP manuscript readiness.")
    parser.add_argument("--book", choices=["book-1", "book-2", "all"], default="all")
    args = parser.parse_args()

    books = ["book-1", "book-2"] if args.book == "all" else [args.book]
    all_passed = True

    for book_key in books:
        all_passed = print_audit(book_key) and all_passed

    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
