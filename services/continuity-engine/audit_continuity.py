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

SEVERITY_WEIGHTS = {
    "critical": 40,
    "high": 20,
    "medium": 10,
    "low": 5,
    "info": 1,
}


def classify_term(term: str) -> str:
    if term in {"canon", "timeline"}:
        return "medium"
    if term in {"relationship", "character"}:
        return "low"
    return "info"


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
                    "severity": classify_term(term),
                    "line": index,
                    "term": term,
                    "content": line.strip(),
                })

    return findings


def score_findings(findings: list[dict]) -> dict:
    penalty = 0

    for finding in findings:
        severity = finding.get("severity", "info")
        penalty += SEVERITY_WEIGHTS.get(severity, 1)

    score = max(0, 100 - penalty)

    if score >= 90:
        status = "pass"
    elif score >= 70:
        status = "warn"
    else:
        status = "fail"

    return {
        "score": score,
        "status": status,
        "penalty": penalty,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    parser.add_argument("--report", type=Path, default=Path("reports/continuity-audit-report.json"))
    parser.add_argument("--fail-under", type=int, default=70)
    args = parser.parse_args()

    findings = scan_markdown(args.target)
    score = score_findings(findings)

    payload = {
        "target": str(args.target),
        "finding_count": len(findings),
        "score": score,
        "findings": findings,
    }

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"Continuity audit complete. Report: {args.report}")
    print(f"Continuity score: {score['score']} ({score['status']})")

    if score["score"] < args.fail_under:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
