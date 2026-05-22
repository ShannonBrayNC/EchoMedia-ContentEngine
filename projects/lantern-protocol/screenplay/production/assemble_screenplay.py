#!/usr/bin/env python3
"""
Lantern Protocol screenplay assembler.

Builds combined Markdown and Fountain starter exports from the screenplay draft batches.
Run from the screenplay directory:

    cd projects/lantern-protocol/screenplay
    python production/assemble_screenplay.py

Outputs:
    exports/lantern-protocol-feature-screenplay-full-draft.md
    exports/lantern-protocol-feature-screenplay.fountain
    exports/lantern-protocol-assembly-report.md
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "drafts"
EXPORTS = ROOT / "exports"

BATCH_FILES = [
    "feature-screenplay-pages-001-015.md",
    "feature-screenplay-pages-016-030.md",
    "feature-screenplay-pages-031-047.md",
    "feature-screenplay-pages-048-065.md",
    "feature-screenplay-pages-066-082.md",
    "feature-screenplay-pages-083-095.md",
    "feature-screenplay-pages-096-111.md",
    "feature-screenplay-pages-112-125.md",
]

OUTPUT_MD = EXPORTS / "lantern-protocol-feature-screenplay-full-draft.md"
OUTPUT_FOUNTAIN = EXPORTS / "lantern-protocol-feature-screenplay.fountain"
OUTPUT_REPORT = EXPORTS / "lantern-protocol-assembly-report.md"


@dataclass
class Batch:
    filename: str
    content: str
    body: str
    notes: str


def split_body_and_notes(content: str) -> Tuple[str, str]:
    """Split a batch into screenplay body and continuity notes."""
    marker = "\n---\n\n# Continuity Notes"
    if marker in content:
        body, notes = content.split(marker, 1)
        return body.rstrip(), "# Continuity Notes" + notes.rstrip()

    marker2 = "\n---\n\n# Full Draft Continuity Notes"
    if marker2 in content:
        body, notes = content.split(marker2, 1)
        return body.rstrip(), "# Full Draft Continuity Notes" + notes.rstrip()

    return content.rstrip(), ""


def read_batches() -> List[Batch]:
    batches: List[Batch] = []
    for filename in BATCH_FILES:
        path = DRAFTS / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing batch: {path}")
        content = path.read_text(encoding="utf-8")
        body, notes = split_body_and_notes(content)
        batches.append(Batch(filename=filename, content=content, body=body, notes=notes))
    return batches


def strip_batch_headers(body: str, index: int) -> str:
    """Remove repeated document title/header boilerplate while preserving screenplay content."""
    lines = body.splitlines()
    cleaned: List[str] = []
    skip_patterns = [
        r"^# Lantern Protocol — Feature Screenplay Draft$",
        r"^## Pages ",
        r"^> Continuation from ",
        r"^> Draft format note:",
        r"^---$",
        r"^## FADE IN:$",
        r"^### FADE IN:$",
    ]
    for line in lines:
        if any(re.match(pattern, line) for pattern in skip_patterns):
            continue
        cleaned.append(line)
    text = "\n".join(cleaned).strip()
    if index == 0:
        text = "FADE IN:\n\n" + text
    return text


def build_combined_markdown(batches: Iterable[Batch]) -> str:
    parts = [
        "# Lantern Protocol — Feature Screenplay Full Draft",
        "",
        "> Auto-assembled from screenplay draft batches. Edit source batch files or revision files, then regenerate exports.",
        "",
        "---",
        "",
    ]
    appendix = [
        "",
        "---",
        "",
        "# Appendix: Batch Continuity Notes",
        "",
    ]

    for index, batch in enumerate(batches):
        parts.append(f"<!-- SOURCE: {batch.filename} -->")
        parts.append(strip_batch_headers(batch.body, index))
        parts.append("")
        if batch.notes:
            appendix.append(f"## {batch.filename}")
            appendix.append("")
            appendix.append(batch.notes)
            appendix.append("")

    parts.extend(appendix)
    return "\n".join(parts).rstrip() + "\n"


def md_to_fountain(markdown: str) -> str:
    """Best-effort Markdown screenplay draft to Fountain starter conversion."""
    lines = markdown.splitlines()
    out: List[str] = [
        "Title: Lantern Protocol",
        "Credit: Written by Shannon Bray with AI-assisted drafting",
        "Draft date: First assembled draft",
        "",
    ]

    in_notes = False
    pending_character: str | None = None

    for raw in lines:
        line = raw.rstrip()

        if line.startswith("# Appendix:"):
            in_notes = True
            continue
        if in_notes:
            continue
        if line.startswith("<!-- SOURCE:"):
            out.append(f"/* {line.strip('<!-> ')} */")
            continue
        if line.startswith("# Lantern Protocol") or line.startswith("> Auto-assembled"):
            continue
        if line.strip() == "---":
            continue

        scene = re.match(r"^###\s+((?:INT\.|EXT\.|INT\./EXT\.|EXT\./INT\.).+)$", line)
        if scene:
            out.append("")
            out.append(scene.group(1).upper())
            pending_character = None
            continue

        heading = re.match(r"^##\s+(FADE IN:|CUT TO BLACK\.|FADE OUT\.|THE END.*)$", line)
        if heading:
            out.append(heading.group(1).upper())
            pending_character = None
            continue

        char_line = re.match(r"^\*\*([A-Z][A-Z0-9 .()'\-]+)\*\*\s*$", line)
        if char_line:
            pending_character = char_line.group(1).strip().upper()
            out.append("")
            out.append(pending_character)
            continue

        dialogue_inline = re.match(r"^\*\*([A-Z][A-Z0-9 .()'\-]+)\*\*\s{2,}(.*)$", line)
        if dialogue_inline:
            out.append("")
            out.append(dialogue_inline.group(1).strip().upper())
            out.append(dialogue_inline.group(2).strip())
            pending_character = None
            continue

        if line.startswith("> "):
            text = line[2:].strip()
            if text:
                out.append(f"TEXT ON SCREEN: {text}")
            pending_character = None
            continue

        if line.startswith("### ") or line.startswith("## ") or line.startswith("# "):
            # Drop Markdown-only section headings.
            pending_character = None
            continue

        out.append(line)
        if line.strip():
            pending_character = None

    return "\n".join(out).replace("\n\n\n", "\n\n").strip() + "\n"


def build_report(batches: List[Batch], combined: str, fountain: str) -> str:
    scene_count = len(re.findall(r"^###\s+(?:INT\.|EXT\.|INT\./EXT\.|EXT\./INT\.)", combined, flags=re.MULTILINE))
    md_words = len(re.findall(r"\b\w+\b", combined))
    fountain_words = len(re.findall(r"\b\w+\b", fountain))

    rows = [
        "# Lantern Protocol — Assembly Report",
        "",
        "## Inputs",
        "",
    ]
    for batch in batches:
        rows.append(f"- `{batch.filename}`")
    rows.extend(
        [
            "",
            "## Outputs",
            "",
            f"- `{OUTPUT_MD.relative_to(ROOT)}`",
            f"- `{OUTPUT_FOUNTAIN.relative_to(ROOT)}`",
            f"- `{OUTPUT_REPORT.relative_to(ROOT)}`",
            "",
            "## Basic Metrics",
            "",
            f"- Source batches: {len(batches)}",
            f"- Approximate scene headings: {scene_count}",
            f"- Combined Markdown word count: {md_words}",
            f"- Fountain starter word count: {fountain_words}",
            "",
            "## Notes",
            "",
            "- Fountain conversion is a starter export, not a final production screenplay file.",
            "- Review character cues, parentheticals, on-screen text, and Markdown artifacts manually after export.",
            "- Keep batch files as canonical generated source until a polished full-draft branch is created.",
        ]
    )
    return "\n".join(rows) + "\n"


def main() -> None:
    EXPORTS.mkdir(parents=True, exist_ok=True)
    batches = read_batches()
    combined = build_combined_markdown(batches)
    fountain = md_to_fountain(combined)
    report = build_report(batches, combined, fountain)

    OUTPUT_MD.write_text(combined, encoding="utf-8")
    OUTPUT_FOUNTAIN.write_text(fountain, encoding="utf-8")
    OUTPUT_REPORT.write_text(report, encoding="utf-8")

    print(f"Wrote {OUTPUT_MD}")
    print(f"Wrote {OUTPUT_FOUNTAIN}")
    print(f"Wrote {OUTPUT_REPORT}")


if __name__ == "__main__":
    main()
