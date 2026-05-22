#!/usr/bin/env python3
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript"
CHAPTERS = MANUSCRIPT / "chapters"
REPORT = ROOT / "exports" / "lantern-protocol-novel-audit.md"

LEGACY_NAMES = [
    "Elias Bray",
    "Maya Rios",
    "Jon Keller",
    "Daniel Cross",
]

LANTERN_INTERIOR_POV = [
    "Lantern felt",
    "Lantern wanted",
    "Lantern wondered",
    "Lantern feared",
    "Lantern hoped",
    "Lantern regretted",
]

LANTERN_EMBODIMENT_RISKS = [
    "Lantern avatar",
    "humanoid Lantern",
    "robot Lantern",
    "Lantern face",
    "Lantern's face",
]

REQUIRED_DOCTRINE = [
    "Prediction is not permission",
    "Assistance is not authority",
    "Rescue is not ownership",
    "Human error does not void human dignity",
]


@dataclass
class Finding:
    severity: str
    area: str
    issue: str
    fix: str


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def chapter_number(path: Path) -> int:
    match = re.search(r"chapter-(\d+)", path.name, flags=re.IGNORECASE)
    return int(match.group(1)) if match else 999


def find_patterns(patterns: Iterable[str], text: str) -> List[str]:
    hay = text.lower()
    return [pattern for pattern in patterns if pattern.lower() in hay]


def audit() -> List[Finding]:
    findings: List[Finding] = []
    chapter_files = sorted(CHAPTERS.glob("chapter-*.md"), key=chapter_number)

    if not chapter_files:
        findings.append(
            Finding(
                "Critical",
                "Manuscript Coverage",
                "No chapter files found under novel/manuscript/chapters.",
                "Create at least chapter-01 before running the audit.",
            )
        )
        return findings

    all_text = "\n".join(read_text(path) for path in chapter_files)

    legacy_hits = find_patterns(LEGACY_NAMES, all_text)
    if legacy_hits:
        findings.append(
            Finding(
                "High",
                "Legacy Canon Leakage",
                f"Legacy v0 names found in active manuscript: {', '.join(legacy_hits)}.",
                "Replace with active canon names or move the text to the archive.",
            )
        )

    pov_hits = find_patterns(LANTERN_INTERIOR_POV, all_text)
    if pov_hits:
        findings.append(
            Finding(
                "High",
                "Lantern POV",
                f"Lantern interior/emotional POV phrases found: {', '.join(pov_hits)}.",
                "Rewrite Lantern presence through logs, dashboards, public records, constrained dialogue, or human interpretation.",
            )
        )

    embodiment_hits = find_patterns(LANTERN_EMBODIMENT_RISKS, all_text)
    if embodiment_hits:
        findings.append(
            Finding(
                "High",
                "Lantern Embodiment",
                f"Risky Lantern embodiment phrases found: {', '.join(embodiment_hits)}.",
                "Keep Lantern faceless and system-bound.",
            )
        )

    chapter_01 = CHAPTERS / "chapter-01-the-first-quiet-failure.md"
    chapter_01_words = word_count(read_text(chapter_01))
    if chapter_01.exists() and chapter_01_words < 3500:
        findings.append(
            Finding(
                "Medium",
                "Chapter 1 Word Count",
                f"Chapter 1 is {chapter_01_words} words; target is 3,500-4,500 words.",
                "Expand Chapter 1 from scaffold into full first-pass prose.",
            )
        )
    elif chapter_01.exists() and chapter_01_words > 4500:
        findings.append(
            Finding(
                "Medium",
                "Chapter 1 Word Count",
                f"Chapter 1 is {chapter_01_words} words; target is 3,500-4,500 words.",
                "Trim or move excess material into later chapters/inserts.",
            )
        )

    final_chapters = [path for path in chapter_files if chapter_number(path) >= 29]
    if final_chapters:
        final_text = "\n".join(read_text(path) for path in final_chapters)
        missing_doctrine = [line for line in REQUIRED_DOCTRINE if line.lower() not in final_text.lower()]
        if missing_doctrine:
            findings.append(
                Finding(
                    "Medium",
                    "Final Doctrine",
                    f"Final chapters may be missing doctrine lines: {', '.join(missing_doctrine)}.",
                    "Ensure the final protocol chapters carry the complete doctrine.",
                )
            )

    return findings


def write_report(findings: List[Finding]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    counts = {severity: 0 for severity in ["Critical", "High", "Medium", "Low"]}
    for finding in findings:
        counts[finding.severity] = counts.get(finding.severity, 0) + 1

    lines = [
        "# Lantern Protocol — Novel Manuscript Audit",
        "",
        "## Summary",
        "",
        f"- Total issues: {len(findings)}",
        f"- Critical: {counts.get('Critical', 0)}",
        f"- High: {counts.get('High', 0)}",
        f"- Medium: {counts.get('Medium', 0)}",
        f"- Low: {counts.get('Low', 0)}",
        "",
        "## Findings",
        "",
        "| Severity | Area | Issue | Recommended Fix |",
        "|---|---|---|---|",
    ]

    if not findings:
        lines.append("| — | — | No issues found. | — |")
    else:
        for finding in findings:
            lines.append(f"| {finding.severity} | {finding.area} | {finding.issue} | {finding.fix} |")

    REPORT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {REPORT}")
    print(f"Total issues: {len(findings)}")


def main() -> None:
    findings = audit()
    write_report(findings)


if __name__ == "__main__":
    main()
