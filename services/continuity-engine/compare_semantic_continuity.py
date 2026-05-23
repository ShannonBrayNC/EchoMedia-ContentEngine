#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "was",
    "with",
}


def tokenize(text: str) -> set[str]:
    tokens = re.findall(r"\b[a-zA-Z][a-zA-Z0-9_-]*\b", text.lower())
    return {token for token in tokens if token not in STOP_WORDS and len(token) > 2}


def load_tokens(path: Path) -> set[str]:
    try:
        return tokenize(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"File not found: {path}")


def jaccard_score(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def classify(score: float) -> str:
    if score >= 0.65:
        return "aligned"
    if score >= 0.35:
        return "review"
    return "drift-risk"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--report", type=Path, default=Path("reports/semantic-continuity-report.json"))
    parser.add_argument("--fail-under", type=float, default=0.25)
    args = parser.parse_args()

    source_tokens = load_tokens(args.source)
    candidate_tokens = load_tokens(args.candidate)
    score = jaccard_score(source_tokens, candidate_tokens)

    shared = sorted(source_tokens & candidate_tokens)
    missing = sorted(source_tokens - candidate_tokens)
    added = sorted(candidate_tokens - source_tokens)

    payload = {
        "source": str(args.source),
        "candidate": str(args.candidate),
        "score": round(score, 4),
        "status": classify(score),
        "shared_terms": shared[:100],
        "missing_source_terms": missing[:100],
        "added_candidate_terms": added[:100],
    }

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"Semantic continuity score: {score:.4f} ({payload['status']})")
    print(f"Report: {args.report}")

    if score < args.fail_under:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
