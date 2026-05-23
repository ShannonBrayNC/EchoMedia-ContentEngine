#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from memory_store import search_memory


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_id")
    parser.add_argument("query")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    results = search_memory(args.project_id, args.query, top_k=args.top_k)

    print(json.dumps(results, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
