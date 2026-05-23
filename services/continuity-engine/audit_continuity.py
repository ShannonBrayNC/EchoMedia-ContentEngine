#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

KEY_TERMS = [
    "timeline",
    "relationship",
    "canon",
    "continuity",
    "character",
]


def scan_markdown(path: Path) -> list[dict]:
    findings: list[dict] = []

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return [{"severity": "critical", "message": f"File not found: {path}"}]

    for index, line in enumerate(lines, start=1):
        for term in KEY_TERMS:
            if term in line.lower():
                findings.append({
                    "line": index,
                    "term": term,
                    "content": line.strip(),
                })

    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    parser.add_argument("--report", type=Path, default=Path("reports/continuity-audit-report.json"))
    args = parser.parse_args()

    findings = scan_markdown(args.target)

    payload = {
        "target": str(args.target),
        "finding_count": len(findings),
        "findings": findings,
    }

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"Continuity audit complete. Report: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
