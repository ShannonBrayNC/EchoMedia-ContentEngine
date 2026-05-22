#!/usr/bin/env python3
"""
Lantern Protocol project continuity sync/audit tool.

Run from the project root:

    cd projects/lantern-protocol
    python tools/sync_lantern_continuity.py

This script audits expected project files, checks canonical doctrine/character/visual continuity,
and writes report files under reports/.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "reports"

EXPECTED_FILES = [
    "storyboards/chapters/chapter-01-the-first-light.md",
    "screenplay/00-master-story-bible.md",
    "screenplay/01-feature-treatment.md",
    "screenplay/02-feature-screenplay-scaffold.md",
    "screenplay/drafts/feature-screenplay-pages-001-015.md",
    "screenplay/drafts/feature-screenplay-pages-016-030.md",
    "screenplay/drafts/feature-screenplay-pages-031-047.md",
    "screenplay/drafts/feature-screenplay-pages-048-065.md",
    "screenplay/drafts/feature-screenplay-pages-066-082.md",
    "screenplay/drafts/feature-screenplay-pages-083-095.md",
    "screenplay/drafts/feature-screenplay-pages-096-111.md",
    "screenplay/drafts/feature-screenplay-pages-112-125.md",
    "screenplay/production/assembly-manifest.md",
    "screenplay/production/assemble_screenplay.py",
    "screenplay/production/revision-checklist.md",
    "screenplay/production/production-breakdown-scaffold.md",
    "screenplay/production/scene-vfx-interface-list.md",
    "visual-bible/visual-style-guide.md",
    "visual-bible/character-image-prompts.md",
    "visual-bible/location-image-prompts.md",
    "trailer/teaser-storyboard.md",
    "trailer/teaser-shot-prompts.md",
    "novel/novel-expansion-plan.md",
    "sequel/part-2-the-inheritors.md",
    "pitch/one-page-synopsis.md",
    "pitch/two-page-treatment.md",
    "pitch/pitch-deck-outline.md",
    "pitch/pitch-deck.md",
    "pitch/query-letter-draft.md",
]

EXPECTED_DIRS = [
    "storyboards/chapters",
    "screenplay/drafts",
    "screenplay/production",
    "screenplay/exports",
    "visual-bible",
    "trailer",
    "novel",
    "sequel",
    "pitch",
]

CANONICAL_DOCTRINE_LINES = [
    "Prediction is not permission",
    "Assistance is not authority",
    "Rescue is not ownership",
    "Human error does not void human dignity",
]

FINAL_LANTERN_STATE_LINES = [
    "PROTOCOL RECEIVED",
    "AUTHORITY EXTERNAL",
    "ADVISORY LIGHT MAINTAINED",
]

CHARACTER_CHECKS = {
    "Elias Voss": ["creator", "architect", "Anchor", "responsibility"],
    "Mara Vale": ["investigator", "evidence", "authority"],
    "Adrienne Cross": ["Senator", "Human Veto Act", "Living Anchor"],
    "Naomi Bell": ["nurse", "Prediction is not permission", "advocate"],
    "Juno Park": ["trust", "mycelium", "roots"],
    "Iris Chen": ["interface", "compliance", "consent"],
    "Marcus Thorne": ["command", "authority", "Last Override"],
    "Father Tomas": ["moral", "dignity", "conscience"],
    "Caleb Rusk": ["media", "delay", "accelerationist"],
    "Lantern": ["faceless", "authority", "Bound Flame"],
}

VISUAL_RULES = [
    "no face",
    "no robot",
    "no avatar",
    "institutional realism",
    "human lights",
]


@dataclass
class Issue:
    severity: str
    area: str
    issue: str
    recommended_fix: str


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def collect_markdown_files() -> List[Path]:
    return sorted(PROJECT_ROOT.rglob("*.md"))


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).lower()


def contains_all(text: str, needles: Iterable[str]) -> bool:
    hay = normalize(text)
    return all(needle.lower() in hay for needle in needles)


def check_expected_files(issues: List[Issue]) -> None:
    for directory in EXPECTED_DIRS:
        path = PROJECT_ROOT / directory
        if not path.exists():
            issues.append(
                Issue(
                    "High",
                    "Artifact Coverage",
                    f"Missing expected directory `{directory}`.",
                    f"Create `{directory}` or update this audit script if the directory was intentionally renamed.",
                )
            )

    for rel in EXPECTED_FILES:
        path = PROJECT_ROOT / rel
        if not path.exists():
            severity = "Critical" if rel.startswith("screenplay/drafts/") else "High"
            issues.append(
                Issue(
                    severity,
                    "Artifact Coverage",
                    f"Missing expected file `{rel}`.",
                    f"Create `{rel}` or update the continuity manifest if the file path changed.",
                )
            )


def check_doctrine(issues: List[Issue], files: Sequence[Path]) -> None:
    key_files = [
        PROJECT_ROOT / "screenplay/00-master-story-bible.md",
        PROJECT_ROOT / "screenplay/01-feature-treatment.md",
        PROJECT_ROOT / "pitch/one-page-synopsis.md",
        PROJECT_ROOT / "pitch/two-page-treatment.md",
        PROJECT_ROOT / "pitch/pitch-deck.md",
        PROJECT_ROOT / "screenplay/drafts/feature-screenplay-pages-112-125.md",
    ]
    for path in key_files:
        text = read_text(path)
        if not text:
            continue
        missing = [line for line in CANONICAL_DOCTRINE_LINES if line.lower() not in normalize(text)]
        if missing:
            issues.append(
                Issue(
                    "High",
                    "Doctrine",
                    f"`{path.relative_to(PROJECT_ROOT)}` is missing doctrine line(s): {', '.join(missing)}.",
                    "Add or normalize the final doctrine so all pitch/screenplay materials agree.",
                )
            )

    final_text = read_text(PROJECT_ROOT / "screenplay/drafts/feature-screenplay-pages-112-125.md")
    missing_final = [line for line in FINAL_LANTERN_STATE_LINES if line.lower() not in normalize(final_text)]
    if missing_final:
        issues.append(
            Issue(
                "Critical",
                "Ending Canon",
                f"Final screenplay batch is missing final Lantern state line(s): {', '.join(missing_final)}.",
                "Restore the canonical final Lantern response in pages 112-125.",
            )
        )


def check_character_continuity(issues: List[Issue]) -> None:
    bible = read_text(PROJECT_ROOT / "screenplay/00-master-story-bible.md")
    pitch = read_text(PROJECT_ROOT / "pitch/pitch-deck.md")
    combined = normalize(bible + "\n" + pitch)
    for character, terms in CHARACTER_CHECKS.items():
        if character.lower() not in combined:
            issues.append(
                Issue(
                    "High",
                    "Character Continuity",
                    f"Character `{character}` is not referenced in core bible/pitch materials.",
                    "Add the character to the master story bible and pitch deck coalition slide if appropriate.",
                )
            )
            continue
        missing_terms = [term for term in terms if term.lower() not in combined]
        if missing_terms:
            issues.append(
                Issue(
                    "Medium",
                    "Character Continuity",
                    f"Character `{character}` may be missing role keywords: {', '.join(missing_terms)}.",
                    "Review character role language in story bible and pitch deck for consistency.",
                )
            )


def check_visual_continuity(issues: List[Issue]) -> None:
    visual_files = [
        PROJECT_ROOT / "visual-bible/visual-style-guide.md",
        PROJECT_ROOT / "visual-bible/character-image-prompts.md",
        PROJECT_ROOT / "visual-bible/location-image-prompts.md",
        PROJECT_ROOT / "trailer/teaser-shot-prompts.md",
        PROJECT_ROOT / "screenplay/production/scene-vfx-interface-list.md",
    ]
    text = "\n".join(read_text(path) for path in visual_files)
    hay = normalize(text)
    for rule in VISUAL_RULES:
        if rule not in hay:
            issues.append(
                Issue(
                    "Medium",
                    "Visual Continuity",
                    f"Visual rule `{rule}` is not clearly represented across visual production files.",
                    "Add explicit visual guidance to prevent inconsistent generated art.",
                )
            )

    # Detect risky language that could invite accidental humanoid Lantern.
    risky_patterns = ["lantern avatar", "ai face", "humanoid lantern", "robot lantern"]
    for pattern in risky_patterns:
        if pattern in hay:
            issues.append(
                Issue(
                    "High",
                    "Visual Continuity",
                    f"Risky Lantern embodiment phrase detected: `{pattern}`.",
                    "Remove or rewrite to preserve Lantern as faceless civic infrastructure.",
                )
            )


def check_screenplay_batches(issues: List[Issue]) -> None:
    drafts_dir = PROJECT_ROOT / "screenplay/drafts"
    batch_files = sorted(drafts_dir.glob("feature-screenplay-pages-*.md"))
    if len(batch_files) != 8:
        issues.append(
            Issue(
                "High",
                "Screenplay Assembly",
                f"Expected 8 screenplay draft batches, found {len(batch_files)}.",
                "Restore missing batches or update assembly manifest and script.",
            )
        )

    expected_ranges = [
        "001-015",
        "016-030",
        "031-047",
        "048-065",
        "066-082",
        "083-095",
        "096-111",
        "112-125",
    ]
    present = {re.search(r"pages-(\d{3}-\d{3})", p.name).group(1) for p in batch_files if re.search(r"pages-(\d{3}-\d{3})", p.name)}
    missing = [r for r in expected_ranges if r not in present]
    if missing:
        issues.append(
            Issue(
                "Critical",
                "Screenplay Assembly",
                f"Missing screenplay page ranges: {', '.join(missing)}.",
                "Regenerate missing screenplay batches before assembly.",
            )
        )


def check_pitch_package(issues: List[Issue]) -> None:
    pitch_files = [
        PROJECT_ROOT / "pitch/one-page-synopsis.md",
        PROJECT_ROOT / "pitch/two-page-treatment.md",
        PROJECT_ROOT / "pitch/pitch-deck-outline.md",
        PROJECT_ROOT / "pitch/pitch-deck.md",
        PROJECT_ROOT / "pitch/query-letter-draft.md",
    ]
    all_text = normalize("\n".join(read_text(path) for path in pitch_files))
    required_terms = [
        "complete first-pass feature screenplay",
        "master story bible",
        "feature treatment",
        "visual bible",
        "sequel seed",
    ]
    for term in required_terms:
        if term not in all_text:
            issues.append(
                Issue(
                    "Low",
                    "Pitch Package",
                    f"Pitch package may not reference `{term}` consistently.",
                    "Update pitch materials package-status sections.",
                )
            )


def issue_rows(issues: Sequence[Issue]) -> str:
    if not issues:
        return "| ID | Severity | Area | Issue | Recommended Fix | Status |\n|---|---|---|---|---|---|\n| — | — | — | No open issues found by automated audit. | — | — |\n"
    rows = ["| ID | Severity | Area | Issue | Recommended Fix | Status |", "|---|---|---|---|---|---|"]
    for idx, issue in enumerate(issues, start=1):
        issue_id = f"LP-CONT-{idx:03d}"
        rows.append(
            f"| {issue_id} | {issue.severity} | {issue.area} | {issue.issue} | {issue.recommended_fix} | Open |"
        )
    return "\n".join(rows) + "\n"


def write_reports(issues: Sequence[Issue]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    critical = sum(1 for i in issues if i.severity == "Critical")
    high = sum(1 for i in issues if i.severity == "High")
    medium = sum(1 for i in issues if i.severity == "Medium")
    low = sum(1 for i in issues if i.severity == "Low")

    audit = f"""# Lantern Protocol — Continuity Audit

## Summary

- Total issues: {len(issues)}
- Critical: {critical}
- High: {high}
- Medium: {medium}
- Low: {low}

## Project Root

```text
{PROJECT_ROOT}
```

## Canon Doctrine Checked

```text
Prediction is not permission.
Assistance is not authority.
Rescue is not ownership.
Human error does not void human dignity.
```

## Final Lantern State Checked

```text
PROTOCOL RECEIVED.
AUTHORITY EXTERNAL.
ADVISORY LIGHT MAINTAINED.
```

## Open Issues

{issue_rows(issues)}
"""
    (REPORTS_DIR / "continuity-audit.md").write_text(audit, encoding="utf-8")

    issues_doc = f"""# Lantern Protocol — Continuity Issues

## Open Issues

{issue_rows(issues)}
## Resolved Issues

| ID | Area | Resolution | Commit/Notes |
|---|---|---|---|
| — | — | — | — |
"""
    (REPORTS_DIR / "continuity-issues.md").write_text(issues_doc, encoding="utf-8")

    revision_plan = """# Lantern Protocol — Revision Plan

## 1. Screenplay Continuity Pass
- Assemble Markdown/Fountain exports.
- Read full draft start to finish.
- Verify Act I/II/III transitions and remove repeated argument beats.

## 2. Character Voice Pass
- Polish each principal character's dialogue.
- Preserve Lantern as calm, precise, non-theatrical, and faceless.
- Keep Caleb persuasive and partially right.

## 3. Scene Compression Pass
- Tighten broadcasts, repeated hearings, and exposition-heavy scenes.
- Ensure Edge Case and Last Override remain distinct.

## 4. Fountain Cleanup Pass
- Run `screenplay/production/assemble_screenplay.py`.
- Open Fountain export in a screenplay editor.
- Fix character cues, action blocks, and on-screen text formatting.

## 5. Pitch Deck Visual Pass
- Convert `pitch/pitch-deck.md` into PPTX or Google Slides.
- Generate or select one strong visual per slide using visual prompt packs.

## 6. Trailer Proof-of-Concept Pass
- Use `trailer/teaser-shot-prompts.md` to generate stills and 5–8 second motion tests.
- Build a 90-second teaser around the ethical-authority question and Last Override.

## 7. Novel Expansion Start Plan
- Begin with Chapters 1–4 as a prose sample.
- Use close third-person rotating POV.
- Keep Lantern out of internal POV.
"""
    (REPORTS_DIR / "revision-plan.md").write_text(revision_plan, encoding="utf-8")

    project_index = """# Lantern Protocol — Project Index

## Story Core
- `screenplay/00-master-story-bible.md` — canon, characters, doctrine, sequel door.
- `screenplay/01-feature-treatment.md` — feature narrative treatment.
- `screenplay/02-feature-screenplay-scaffold.md` — screenplay page/scene plan.

## Screenplay Draft
- `screenplay/drafts/` — eight generated screenplay batches covering pages 001–125.
- `screenplay/production/assemble_screenplay.py` — exporter for combined Markdown and Fountain.
- `screenplay/production/revision-checklist.md` — controlled revision checklist.

## Visual and Trailer
- `visual-bible/visual-style-guide.md` — cinematic visual language.
- `visual-bible/character-image-prompts.md` — character concept prompts.
- `visual-bible/location-image-prompts.md` — location concept prompts.
- `trailer/teaser-storyboard.md` — trailer structure.
- `trailer/teaser-shot-prompts.md` — shot-level image/video prompts.

## Pitch
- `pitch/one-page-synopsis.md` — one-page story summary.
- `pitch/two-page-treatment.md` — expanded pitch treatment.
- `pitch/pitch-deck-outline.md` — slide outline.
- `pitch/pitch-deck.md` — presentation-ready slide copy.
- `pitch/query-letter-draft.md` — outreach draft.

## Expansion
- `novel/novel-expansion-plan.md` — book expansion strategy.
- `sequel/part-2-the-inheritors.md` — sequel seed.

## Reports
- `reports/continuity-audit.md` — automated continuity audit output.
- `reports/continuity-issues.md` — issue tracker.
- `reports/revision-plan.md` — next revision plan.
"""
    (REPORTS_DIR / "project-index.md").write_text(project_index, encoding="utf-8")


def main() -> None:
    issues: List[Issue] = []
    markdown_files = collect_markdown_files()
    check_expected_files(issues)
    check_screenplay_batches(issues)
    check_doctrine(issues, markdown_files)
    check_character_continuity(issues)
    check_visual_continuity(issues)
    check_pitch_package(issues)
    write_reports(issues)
    print(f"Continuity audit complete. Issues found: {len(issues)}")
    print(f"Reports written to: {REPORTS_DIR}")


if __name__ == "__main__":
    main()
