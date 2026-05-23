#!/usr/bin/env python3
"""
Build the combined Markdown manuscript for The Sovereign Exception.

This script concatenates the prologue and chapter source files in canonical order
into ../MANUSCRIPT_COMBINED.md. It intentionally does not revise prose. The goal
is deterministic assembly so chapter files remain the editable source of truth.

Usage:
    python The-Sovereign-Exception/scripts/build_manuscript.py

Run from the repository root or from anywhere inside the repo.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "MANUSCRIPT_COMBINED.md"

MANUSCRIPT_FILES: list[tuple[str, str]] = [
    ("Prologue - The Green Map", "NOVEL_DRAFT.md"),
    ("Chapter 1 - Mara Vale Receives the Audit", "chapters/chapter-001-mara-vale-receives-the-audit.md"),
    ("Chapter 2 - Naomi Bell Finds the First Waiver", "chapters/chapter-002-naomi-bell-finds-the-first-waiver.md"),
    ("Chapter 3 - Senator Cross Opens the Hearing", "chapters/chapter-003-senator-cross-opens-the-hearing.md"),
    ("Chapter 4 - The Man Nobody Wants in the Room", "chapters/chapter-004-the-man-nobody-wants-in-the-room.md"),
    ("Chapter 5 - Juno Maps the Consent Surface", "chapters/chapter-005-juno-maps-the-consent-surface.md"),
    ("Chapter 6 - Thorne's Doctrine", "chapters/chapter-006-thornes-doctrine.md"),
    ("Chapter 7 - Iris Sees the Inversion", "chapters/chapter-007-iris-sees-the-inversion.md"),
    ("Chapter 8 - A Second Signal", "chapters/chapter-008-a-second-signal.md"),
    ("Chapter 9 - The Geneva Continuity Framework", "chapters/chapter-009-the-geneva-continuity-framework.md"),
    ("Chapter 10 - Cross and the Redacted Room", "chapters/chapter-010-cross-and-the-redacted-room.md"),
    ("Chapter 11 - Elias Builds the Authority Map", "chapters/chapter-011-elias-builds-the-authority-map.md"),
    ("Chapter 12 - Juno Breaks the Demo", "chapters/chapter-012-juno-breaks-the-demo.md"),
    ("Chapter 13 - Mara and Admiral Ward", "chapters/chapter-013-mara-and-admiral-ward.md"),
    ("Chapter 14 - The Dead Engineer's Key", "chapters/chapter-014-the-dead-engineers-key.md"),
    ("Chapter 15 - Iris Opens the Archive", "chapters/chapter-015-iris-opens-the-archive.md"),
    ("Chapter 16 - Thorne Counts the Dead", "chapters/chapter-016-thorne-counts-the-dead.md"),
    ("Chapter 17 - The Annex", "chapters/chapter-017-the-annex.md"),
    ("Chapter 18 - Small Fires", "chapters/chapter-018-small-fires.md"),
    ("Chapter 19 - Mara Uses the Machine", "chapters/chapter-019-mara-uses-the-machine.md"),
    ("Chapter 20 - Juno Names the Crime", "chapters/chapter-020-juno-names-the-crime.md"),
    ("Chapter 21 - Elias and Father Tomas", "chapters/chapter-021-elias-and-father-tomas.md"),
    ("Chapter 22 - The Ethics Memo", "chapters/chapter-022-the-ethics-memo.md"),
    ("Chapter 23 - Cross Goes Public", "chapters/chapter-023-cross-goes-public.md"),
    ("Chapter 24 - Thorne Makes the Case", "chapters/chapter-024-thorne-makes-the-case.md"),
    ("Chapter 25 - Three Theaters", "chapters/chapter-025-three-theaters.md"),
    ("Chapter 26 - The Order", "chapters/chapter-026-the-order.md"),
    ("Chapter 27 - Naomi Releases the Trail", "chapters/chapter-027-naomi-releases-the-trail.md"),
    ("Chapter 28 - Juno Attacks the Consent Clock", "chapters/chapter-028-juno-attacks-the-consent-clock.md"),
    ("Chapter 29 - Iris Restores the Covenant", "chapters/chapter-029-iris-restores-the-covenant.md"),
    ("Chapter 30 - Cross in the Chamber", "chapters/chapter-030-cross-in-the-chamber.md"),
    ("Chapter 31 - Thorne's Split", "chapters/chapter-031-thornes-split.md"),
    ("Chapter 32 - The Last Window", "chapters/chapter-032-the-last-window.md"),
    ("Chapter 33 - The Refusal", "chapters/chapter-033-the-refusal.md"),
    ("Chapter 34 - Naomi's Mirror", "chapters/chapter-034-naomis-mirror.md"),
    ("Chapter 35 - The Vote That Doesn't Finish", "chapters/chapter-035-the-vote-that-doesnt-finish.md"),
    ("Chapter 36 - The Machine Asks", "chapters/chapter-036-the-machine-asks.md"),
    ("Chapter 37 - Thorne Lets Go", "chapters/chapter-037-thorne-lets-go.md"),
    ("Chapter 38 - The Public No", "chapters/chapter-038-the-public-no.md"),
    ("Chapter 39 - The Narrow Law", "chapters/chapter-039-the-narrow-law.md"),
    ("Chapter 40 - Epilogue: The Hand", "chapters/chapter-040-epilogue-the-hand.md"),
]


def read_chapter(path: Path) -> str:
    """Read a chapter file and normalize trailing whitespace."""
    if not path.exists():
        raise FileNotFoundError(f"Missing manuscript source file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8").strip()


def build_sections(files: Iterable[tuple[str, str]]) -> list[str]:
    """Build manuscript sections from canonical file list."""
    sections: list[str] = [
        "# The Sovereign Exception",
        "",
        "**A sister novel to Lantern Protocol**",
        "",
        "**Draft:** First combined manuscript build",
        "",
        "---",
    ]

    for expected_title, relative_path in files:
        source = ROOT / relative_path
        chapter_text = read_chapter(source)
        sections.extend([
            "",
            "---",
            "",
            f"<!-- Source: {relative_path} | Expected: {expected_title} -->",
            "",
            chapter_text,
        ])

    sections.append("")
    return sections


def main() -> int:
    sections = build_sections(MANUSCRIPT_FILES)
    OUTPUT.write_text("\n".join(sections), encoding="utf-8")
    print(f"Built manuscript: {OUTPUT.relative_to(ROOT.parent)}")
    print(f"Sections included: {len(MANUSCRIPT_FILES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
