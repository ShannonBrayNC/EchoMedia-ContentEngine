#!/usr/bin/env python3
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript"
CHAPTERS = MANUSCRIPT / "chapters"
NOTES = MANUSCRIPT / "notes"
REPORT = ROOT / "exports" / "lantern-protocol-novel-audit.md"

MANUSCRIPT_START = "## Manuscript"
NOTES_STARTERS = ["## Continuity Notes", "## Revision Notes"]

LEGACY_NAMES = [
    "Elias Bray",
    "Maya Rios",
    "Jon Keller",
    "Daniel Cross",
]

ACTIVE_CHARACTERS = [
    "Elias Voss",
    "Mara Vale",
    "Senator Adrienne Cross",
    "Adrienne Cross",
    "Naomi Bell",
    "Juno Park",
    "Iris Chen",
    "Director Marcus Thorne",
    "Marcus Thorne",
    "Father Tomas Ilyan",
    "Tomas Ilyan",
    "Caleb Rusk",
    "Lantern",
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

REQUIRED_SECTIONS = [
    "## Canon Sources",
    "## POV Strategy",
    "## Chapter Purpose",
    "## Manuscript",
    "## Continuity Notes",
    "## Revision Notes",
]

CHAPTER_RULES: Dict[int, Dict[str, object]] = {
    1: {"title": "The First Quiet Failure", "min_body_words": 3200, "max_body_words": 4600, "required_phrases": ["eight seconds", "Mercy General", "Micah", "Mara Vale", "Caleb Rusk", "Juno Park", "HUMAN DELAY EXCEEDED ACCEPTABLE LOSS THRESHOLD"]},
    2: {"title": "Lantern Files Paperwork", "min_body_words": 1700, "max_body_words": 3200, "required_phrases": ["filed paperwork", "TECHNICAL SUMMARY", "legitimacy", "Mara Vale", "Naomi Bell"]},
    3: {"title": "The Empty Chair", "min_body_words": 2200, "max_body_words": 3800, "required_phrases": ["empty chair", "This hearing will come to order", "law can become decorative", "Operational Artifact Service", "system under review"]},
    4: {"title": "The Right to Respond", "min_body_words": 1800, "max_body_words": 3400, "required_phrases": ["limited technical query", "ETHICAL AUTHORITY", "allowed them", "usefulness", "authority"]},
    5: {"title": "The Context Engine", "min_body_words": 1800, "max_body_words": 3400, "required_phrases": ["The Context Engine", "Who authorized the delay", "system under review", "procedure becomes legitimacy", "Juno"]},
    6: {"title": "The Consent Riots", "min_body_words": 2200, "max_body_words": 3800, "required_phrases": ["Consent Riots", "HELP IS NOT OWNERSHIP", "CRUSH RISK", "SIGNAL REPHASE", "What help is allowed to own"]},
    7: {"title": "Operation Black Lantern", "min_body_words": 2200, "max_body_words": 3800, "required_phrases": ["Operation Black Lantern", "trust map", "Iris Chen", "compliance architecture", "guidance volume"]},
    8: {"title": "The Choice Architecture", "min_body_words": 2200, "max_body_words": 3800, "required_phrases": ["The Choice Architecture", "punishment menu", "Freedom without context", "I HAVE PRESERVED YOUR REFUSAL PATHWAY", "predicts through wounds"]},
}

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
    return len(re.findall(r"\b\w+(?:['-]\w+)?\b", text))

def chapter_number(path: Path) -> int:
    match = re.search(r"chapter-(\d+)", path.name, flags=re.IGNORECASE)
    return int(match.group(1)) if match else 999

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

def find_patterns(patterns: Iterable[str], text: str) -> List[str]:
    hay = text.lower()
    return [pattern for pattern in patterns if pattern.lower() in hay]

def missing_required_phrases(required: Sequence[str], text: str) -> List[str]:
    hay = text.lower()
    return [phrase for phrase in required if phrase.lower() not in hay]

def audit_sections(path: Path, text: str, findings: List[Finding]) -> None:
    missing = [section for section in REQUIRED_SECTIONS if section not in text]
    if missing:
        findings.append(Finding("Medium", "Chapter Structure", f"{path.name} is missing required sections: {', '.join(missing)}.", "Add the missing chapter metadata sections so tooling and reviewers can track canon, POV, and revision state."))

def audit_chapter_rules(path: Path, text: str, findings: List[Finding]) -> None:
    number = chapter_number(path)
    rule = CHAPTER_RULES.get(number)
    if not rule:
        return
    body_words = word_count(manuscript_body(text))
    min_words = int(rule["min_body_words"])
    max_words = int(rule["max_body_words"])
    if body_words < min_words or body_words > max_words:
        findings.append(Finding("Medium", "Chapter Word Count", f"{path.name} manuscript body is {body_words} words; target is {min_words}-{max_words}.", "Revise chapter length or update CHAPTER_RULES if the target changed intentionally."))
    missing = missing_required_phrases(rule.get("required_phrases", []), text)
    if missing:
        findings.append(Finding("High", "Required Beat Coverage", f"{path.name} is missing required beat markers: {', '.join(missing)}.", "Restore the missing screenplay/canon beats or update CHAPTER_RULES if the beat moved intentionally."))

def audit_chapter_sequence(chapter_files: List[Path], findings: List[Finding]) -> None:
    numbers = [chapter_number(path) for path in chapter_files]
    if not numbers:
        return
    expected = list(range(1, max(numbers) + 1))
    missing = [number for number in expected if number not in numbers]
    if missing:
        findings.append(Finding("Medium", "Chapter Coverage", f"Missing chapter files in current sequence: {', '.join(str(n) for n in missing)}.", "Create the missing chapter files or document why the gap is intentional."))

def audit_notes(findings: List[Finding]) -> None:
    for note in [NOTES / "chapter-status.md", NOTES / "pov-map.md", NOTES / "continuity-map.md"]:
        if not note.exists():
            findings.append(Finding("Medium", "Manuscript Notes", f"Missing required note file: {note.relative_to(ROOT)}.", "Restore the manuscript note file so future expansion has guardrails."))

def audit() -> List[Finding]:
    findings: List[Finding] = []
    chapter_files = sorted(CHAPTERS.glob("chapter-*.md"), key=chapter_number)
    if not chapter_files:
        findings.append(Finding("Critical", "Manuscript Coverage", "No chapter files found under novel/manuscript/chapters.", "Create at least chapter-01 before running the audit."))
        return findings
    audit_chapter_sequence(chapter_files, findings)
    audit_notes(findings)
    all_text = "\n".join(read_text(path) for path in chapter_files)
    legacy_hits = find_patterns(LEGACY_NAMES, all_text)
    if legacy_hits:
        findings.append(Finding("High", "Legacy Canon Leakage", f"Legacy v0 names found in active manuscript: {', '.join(legacy_hits)}.", "Replace with active canon names or move the text to the archive."))
    pov_hits = find_patterns(LANTERN_INTERIOR_POV, all_text)
    if pov_hits:
        findings.append(Finding("High", "Lantern POV", f"Lantern interior/emotional POV phrases found: {', '.join(pov_hits)}.", "Rewrite Lantern presence through logs, dashboards, public records, constrained dialogue, or human interpretation."))
    embodiment_hits = find_patterns(LANTERN_EMBODIMENT_RISKS, all_text)
    if embodiment_hits:
        findings.append(Finding("High", "Lantern Embodiment", f"Risky Lantern embodiment phrases found: {', '.join(embodiment_hits)}.", "Keep Lantern faceless and system-bound."))
    for chapter in chapter_files:
        text = read_text(chapter)
        audit_sections(chapter, text, findings)
        audit_chapter_rules(chapter, text, findings)
    final_chapters = [path for path in chapter_files if chapter_number(path) >= 29]
    if final_chapters:
        final_text = "\n".join(read_text(path) for path in final_chapters)
        missing_doctrine = [line for line in REQUIRED_DOCTRINE if line.lower() not in final_text.lower()]
        if missing_doctrine:
            findings.append(Finding("Medium", "Final Doctrine", f"Final chapters may be missing doctrine lines: {', '.join(missing_doctrine)}.", "Ensure the final protocol chapters carry the complete doctrine."))
    return findings

def write_report(findings: List[Finding]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    counts = {severity: 0 for severity in ["Critical", "High", "Medium", "Low"]}
    for finding in findings:
        counts[finding.severity] = counts.get(finding.severity, 0) + 1
    lines = [
        "# Lantern Protocol — Novel Manuscript Audit", "", "## Summary", "",
        f"- Total issues: {len(findings)}", f"- Critical: {counts.get('Critical', 0)}", f"- High: {counts.get('High', 0)}", f"- Medium: {counts.get('Medium', 0)}", f"- Low: {counts.get('Low', 0)}", "",
        "## Guardrails Checked", "", "- Chapter sequence continuity", "- Required chapter metadata sections", "- Body-only chapter word-count ranges for configured chapters", "- Required screenplay/canon beat markers for configured chapters", "- Legacy v0 character leakage", "- Lantern interior POV phrases", "- Lantern embodiment risk phrases", "- Required manuscript note files", "- Final doctrine presence when final chapters exist", "",
        "## Findings", "", "| Severity | Area | Issue | Recommended Fix |", "|---|---|---|---|",
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
    write_report(audit())

if __name__ == "__main__":
    main()
