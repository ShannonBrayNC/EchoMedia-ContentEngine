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
    "docs/idea-intake-workflow.md",
    "docs/project-readiness-roadmap.md",
    "docs/artifact-inventory-and-output-map.md",
    "docs/artifact-preview-and-review-workspace.md",
    "docs/api-contract.md",
    "docs/generation-job-and-review-gate.md",
    "docs/testing-strategy.md",
    "docs/ui-workflow-redesign.md",
    "docs/lantern-adapter.md",
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
    "schemas/idea-intake.schema.json",
    "services/content_engine_api.py",
    "tests/e2e/test_no_provider_manuscript_to_export.py",
    "ui/content-engine-dashboard/README.md",
    "ui/content-engine-dashboard/package.json",
    "ui/content-engine-dashboard/index.html",
    "ui/content-engine-dashboard/tsconfig.json",
    "ui/content-engine-dashboard/vite.config.ts",
    "ui/content-engine-dashboard/src/vite-env.d.ts",
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
    "schemas/project-scaffold.schema.json",
    "schemas/idea-intake.schema.json"
]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


def require_terms(path: str, terms: list[str]) -> None:
    text = (ROOT / path).read_text(encoding="utf-8")
    for term in terms:
        if term not in text:
            fail(f"{path} missing expected term: {term}")


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

    require_terms(".env.example", ["OPENAI_API_KEY", "ELEVENLABS_API_KEY", "AZURE_OPENAI_API_KEY", "AZURE_SPEECH_KEY", "CONTENT_ENGINE_PROVIDER_ALLOWLIST", "VITE_CONTENT_ENGINE_API_BASE_URL"])
    require_terms("openapi/content-engine.openapi.yaml", ["openapi:", "/health:", "/projects:", "/projects/{projectId}/idea-intake", "/projects/{projectId}/readiness", "/projects/{projectId}/artifact-inventory", "/artifacts/{artifactId}/preview", "/artifacts/{artifactId}/traceability", "/reviews/{artifactId}/request-revision", "/reviews/{artifactId}/supersede", "/exports/packages/{artifactId}", "/generation/jobs:", "ProjectReadiness", "ProjectArtifactInventory", "ArtifactPreview", "ArtifactTraceability", "ExportPackage", "components:"])
    require_terms("services/content_engine_api.py", ["ThreadingHTTPServer", "create_project", "create_idea_intake", "create_generation_job", "get_readiness", "get_inventory", "get_preview", "get_traceability", "export_artifact", "Artifact must be approved before export"])
    require_terms("docs/lantern-adapter.md", ["opportunity.detected", "services/lantern_content_assets.py", "approvalState=required", "publishAllowed"])
    require_terms("tests/e2e/test_no_provider_manuscript_to_export.py", ["test_manuscript_idea_to_approved_export", "create_project", "create_idea_intake", "create_generation_job", "export_artifact", "unapproved artifacts must not export"])
    require_terms("ui/content-engine-dashboard/src/vite-env.d.ts", ["VITE_CONTENT_ENGINE_API_BASE_URL"])
    require_terms("ui/content-engine-dashboard/src/App.tsx", ["Create New Project", "Create project scaffold", "Load Ideas", "Create idea intake draft", "Project Readiness", "Readiness Roadmap", "Artifact Inventory", "ProjectArtifactInventory", "inventoryByCategory", "Artifact Preview and Review", "Preview mode", "Compare draft vs approved", "Request revision", "Supersede", "Export from preview", "traceability", "Next best action", "Why this order?", "Current production step", "Validate", "Generate draft", "Status rail", "Approve", "export package"])
    require_terms("ui/content-engine-dashboard/src/api.ts", ["VITE_CONTENT_ENGINE_API_BASE_URL", "apiRequest", "fetch", "ProjectScaffold", "createProjectScaffold", "IdeaIntake", "createIdeaIntake", "ProjectReadiness", "ReadinessItem", "getProjectReadiness", "ProjectArtifactInventory", "ArtifactInventoryItem", "getProjectArtifactInventory", "WorkflowStep", "workflowSteps", "getWorkflowStep", "starterArtifacts", "nextSteps"])
    require_terms("ui/content-engine-dashboard/src/styles.css", ["inline-order-hint", "order-badge", "compact-workflow-list", "readiness-score", "progress-track", "readiness-list", "readiness-item", "artifact-inventory-panel", "inventory-group", "inventory-item", "state-pill", "required-pill", "review-workspace", "preview-toolbar", "traceability-grid", "compare-grid", "approved-preview"])

    print("Repository baseline validation passed.")


if __name__ == "__main__":
    main()
