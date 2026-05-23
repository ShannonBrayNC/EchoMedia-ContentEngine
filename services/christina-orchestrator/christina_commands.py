#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

COMMAND_MAP = {
    "status": "Show project status and available artifacts.",
    "assemble screenplay": "Queue or run screenplay assembly for the selected project.",
    "build release": "Create a release manifest for the selected project.",
    "search memory": "Search project semantic memory.",
    "analyze pacing": "Run cinematic pacing analysis.",
    "create tv map": "Create a TV adaptation episode map.",
    "create commercials": "Create commercial package scaffolds.",
}


def run(args: list[str]) -> dict:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "ok": result.returncode == 0,
    }


def interpret(command: str, project_id: str, project_root: str) -> dict:
    normalized = command.strip().lower()

    if normalized.startswith("help"):
        return {"intent": "help", "commands": COMMAND_MAP}

    if "status" in normalized:
        return {
            "intent": "status",
            "project_id": project_id,
            "project_root": project_root,
            "artifacts": {
                "canon": (ROOT / project_root / "canon").exists(),
                "manuscript": (ROOT / project_root / "manuscript").exists(),
                "screenplay": (ROOT / project_root / "screenplay").exists(),
                "releases": (ROOT / project_root / "releases").exists(),
            },
        }

    if "assemble" in normalized and "screenplay" in normalized:
        return {
            "intent": "assemble-screenplay",
            "result": run(["python", "services/screenplay-assembler/assemble_screenplay.py", project_root]),
        }

    if "pacing" in normalized:
        return {
            "intent": "analyze-pacing",
            "result": run(["python", "services/pacing-analysis/analyze_pacing.py", project_root]),
        }

    if "tv" in normalized or "episode" in normalized:
        return {
            "intent": "create-tv-map",
            "result": run(["python", "services/tv-adaptation/create_tv_adaptation.py", project_root]),
        }

    if "commercial" in normalized or "ad" in normalized:
        return {
            "intent": "create-commercials",
            "result": run(["python", "services/commercial-engine/create_commercial_package.py", project_root]),
        }

    if "release" in normalized:
        return {
            "intent": "create-release",
            "result": run(["python", "services/release-manager/create_release_manifest.py", project_root, "0.1.0", "candidate"]),
        }

    if "memory" in normalized or "search" in normalized:
        query = normalized.replace("search", "").replace("memory", "").strip() or "continuity"
        return {
            "intent": "search-memory",
            "query": query,
            "result": run(["python", "services/embedding-memory/search_project_memory.py", project_id, query]),
        }

    return {
        "intent": "unknown",
        "message": "I could not map that command yet.",
        "supported_commands": COMMAND_MAP,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_id")
    parser.add_argument("project_root")
    parser.add_argument("command")
    args = parser.parse_args()

    result = interpret(args.command, args.project_id, args.project_root)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
