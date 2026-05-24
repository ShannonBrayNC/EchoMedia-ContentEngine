#!/usr/bin/env python3
"""Validate the repository baseline without external provider calls."""

from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    ".env.example",
    "docs/local-development.md",
    "docs/configuration.md",
    "docs/architecture.md",
    "docs/project-registry-and-folder-contract.md",
    "docs/schema-and-traceability.md",
    "docs/artifact-storage-and-manifest-policy.md",
    "docs/context-assembly.md",
    "docs/legacy-artifact-migration-plan.md",
    "docs/new-project-creation-workflow.md",
    "docs/api-contract.md",
    "docs/generation-job-and-review-gate.md",
    "docs/testing-strategy.md",
    "docs/ui-workflow-redesign.md",
    "docs/sprint-plan.md",
    "docs/reports/branch-reconciliation-2026-05-23.md",
    "openapi/content-engine.openapi.yaml",
    "schemas/production-package.schema.json",
    "schemas/generated-asset-manifest.schema.json",
    "schemas/voice-package.schema.json",
    "schemas/scene-timeline.schema.json",
    "schemas/template-record.schema.json",
    "schemas/generation-job.schema.json",
    "schemas/project-scaffold.schema.json",
    "ui/content-engine-dashboard/README.md",
    "ui/content-engine-dashboard/package.json",
    "ui/content-engine-dashboard/index.html",
    "ui/content-engine-dashboard/tsconfig.json",
    "ui/content-engine-dashboard/vite.config.ts",
    "ui/content-engine-dashboard/src/api.ts",
    "ui/content-engine-dashboard/src/App.tsx",
    "ui/content-engine-dashboard/src/main.tsx",
    "ui/content-engine-dashboard/src/styles.css"
]

SCHEMA_FILES = [
    "schemas/production-package.schema.json",
    "schemas/generated-asset-manifest.schema.json",
    "schemas/voice-package.schema.json",
    "schemas/scene-timeline.schema.json",
    "schemas/template-record.schema.json",
    "schemas/generation-job.schema.json",
    "schemas/project-scaffold.schema.json"
]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        fail("Missing required files: " + ", ".join(missing))

    for schema_path in SCHEMA_FILES:
        path = ROOT / schema_path
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"Invalid JSON in {schema_path}: {exc}")
        if "$schema" not in data:
            fail(f"Schema file lacks $schema: {schema_path}")
        if "title" not in data:
            fail(f"Schema file lacks title: {schema_path}")

    openapi_text = (ROOT / "openapi/content-engine.openapi.yaml").read_text(encoding="utf-8")
    required_openapi_terms = ["openapi:", "/health:", "/projects:", "/generation/jobs:", "components:"]
    for term in required_openapi_terms:
        if term not in openapi_text:
            fail(f"OpenAPI contract missing expected term: {term}")

    app_text = (ROOT / "ui/content-engine-dashboard/src/App.tsx").read_text(encoding="utf-8")
    required_ui_terms = [
        "Create New Project",
        "Create project scaffold",
        "Validate",
        "Generate draft",
        "Status rail",
        "Approve",
        "Export package"
    ]
    for term in required_ui_terms:
        if term not in app_text:
            fail(f"Dashboard missing expected UI term: {term}")

    api_text = (ROOT / "ui/content-engine-dashboard/src/api.ts").read_text(encoding="utf-8")
    required_api_terms = ["ProjectScaffold", "createProjectScaffold", "starterArtifacts", "nextSteps"]
    for term in required_api_terms:
        if term not in api_text:
            fail(f"Dashboard API missing expected project scaffold term: {term}")

    print("Repository baseline validation passed.")


if __name__ == "__main__":
    main()
