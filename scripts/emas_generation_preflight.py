#!/usr/bin/env python3
"""Run generation preflight checks before any provider call."""

from __future__ import annotations

import argparse
from pathlib import Path

from services.emas import (
    AppendOnlyAuditLogger,
    GenerationPreflightRequest,
    GenerationPreflightService,
    JsonFileSourceRegistryAdapter,
    SourceRegistryService,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run EMAS generation preflight checks.")
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--subject-id", default=None)
    parser.add_argument("--ad-name", default=None)
    parser.add_argument("--intended-use", required=True)
    parser.add_argument("--platform", default=None)
    parser.add_argument("--actor", default="local-cli")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--reference", action="append", default=[])
    parser.add_argument("--output-count", type=int, default=1)
    parser.add_argument("--root-path", default=".")
    args = parser.parse_args()

    root = Path(args.root_path)
    registry_path = root / "projects" / args.project_name / "source-registry.json"
    audit_path = root / "projects" / args.project_name / "metadata" / "audit-log.jsonl"
    audit_logger = AppendOnlyAuditLogger(audit_path)
    source_registry = SourceRegistryService(JsonFileSourceRegistryAdapter(registry_path), audit_logger)
    service = GenerationPreflightService(source_registry, audit_logger)

    result = service.validate(
        GenerationPreflightRequest(
            project_name=args.project_name,
            subject_id=args.subject_id or args.project_name,
            ad_name=args.ad_name,
            intended_use=args.intended_use,
            platform=args.platform,
            actor=args.actor,
            prompt=args.prompt,
            reference_paths=args.reference,
            output_count=args.output_count,
        )
    )

    print(f"allowed={str(result.allowed).lower()}")
    print(f"source_registry_verified={str(result.source_registry_verified).lower()}")
    print(f"normalized_prompt={result.normalized_prompt}")
    for reason in result.reasons:
        print(f"reason={reason}")
    return 0 if result.allowed else 2


if __name__ == "__main__":
    raise SystemExit(main())
