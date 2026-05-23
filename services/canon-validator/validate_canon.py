#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

VALID_STATES = [
    "draft",
    "candidate",
    "approved",
    "locked",
    "superseded",
    "archived",
]

REQUIRED_FIELDS = [
    "project",
    "canon_state",
    "active_canon_files",
    "locked_fields",
    "visual_consistency_keys",
]


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"__error__": f"File not found: {path}"}
    except json.JSONDecodeError as exc:
        return {"__error__": f"Invalid JSON: {exc}"}


def validate(path: Path) -> list[dict]:
    data = read_json(path)
    issues: list[dict] = []

    if "__error__" in data:
        return [{"severity": "critical", "message": data["__error__"]}]

    for field in REQUIRED_FIELDS:
        if field not in data:
            issues.append({"severity": "high", "field": field, "message": "Missing required field"})

    state = data.get("canon_state")
    if state and state not in VALID_STATES:
        issues.append({"severity": "high", "field": "canon_state", "message": f"Invalid state: {state}"})

    for field in ["active_canon_files", "locked_fields", "visual_consistency_keys"]:
        if field in data and not isinstance(data[field], list):
            issues.append({"severity": "medium", "field": field, "message": "Expected list"})

    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--report", type=Path, default=Path("reports/canon-validation-report.json"))
    args = parser.parse_args()

    issues = validate(args.manifest)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps({"issues": issues, "passed": not issues}, indent=2) + "\n", encoding="utf-8")

    if issues:
        print(f"Canon validation failed. Report: {args.report}")
        return 1

    print(f"Canon validation passed. Report: {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
