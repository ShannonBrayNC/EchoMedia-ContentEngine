#!/usr/bin/env python3
"""Export Lantern recommendation registry and RC readiness JSON artifacts."""

from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services import lantern_recommendations as recs  # noqa: E402


def main() -> None:
    reports_dir = ROOT / "docs" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    registry = recs.default_recommendations()
    exports = {
        "content-engine-recommendation-export-2026-05-26.json": recs.export_open_recommendations(registry),
        "rc-readiness-2026-05-26.json": recs.build_rc_readiness_report(registry),
    }

    for filename, payload in exports.items():
        (reports_dir / filename).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Exported Lantern recommendation registry and RC readiness JSON.")


if __name__ == "__main__":
    main()
