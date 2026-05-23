#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_JSON = ROOT / "asset-manifest" / "art-asset-manifest.json"
REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / "asset-manifest" / "art-asset-manifest.md",
    MANIFEST_JSON,
    ROOT / "prompts" / "shared-negative-prompts.md",
    ROOT / "prompts" / "characters" / "character-portrait-pack.md",
    ROOT / "prompts" / "locations" / "location-pack.md",
    ROOT / "prompts" / "key-scenes" / "key-scene-pack.md",
    ROOT / "prompts" / "trailer" / "trailer-shot-pack.md",
    ROOT / "prompts" / "pitch-deck" / "pitch-deck-pack.md",
    ROOT / "prompts" / "ui-system" / "ui-system-pack.md",
    ROOT / "production" / "art-generation-runbook.md",
]
REPORT = ROOT / "qa" / "art-package-validation-report.md"

missing = [str(p.relative_to(ROOT)) for p in REQUIRED_FILES if not p.exists()]
json_ok = True
err = ""
try:
    data = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
    guardrails = data.get("guardrails", [])
    doctrine = data.get("doctrine", [])
    assert len(guardrails) >= 8
    assert len(doctrine) == 4
except Exception as exc:
    json_ok = False
    err = str(exc)

REPORT.parent.mkdir(parents=True, exist_ok=True)
status = "PASS" if not missing and json_ok else "FAIL"
REPORT.write_text(
    "\n".join([
        "# Art Package Validation Report",
        "",
        f"Status: **{status}**",
        "",
        "## Missing Files",
        "- None" if not missing else "\n".join(f"- {m}" for m in missing),
        "",
        "## Manifest JSON",
        "- Valid" if json_ok else f"- Invalid: {err}",
    ]),
    encoding="utf-8",
)
print(status)
