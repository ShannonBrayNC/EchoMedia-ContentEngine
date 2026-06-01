#!/usr/bin/env python3
"""Create an EchoMedia Ad Studio project scaffold."""

from __future__ import annotations

import argparse
from pathlib import Path

from services.emas import AdProjectScaffoldService, AppendOnlyAuditLogger, CreateAdProjectRequest


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an EchoMedia Ad Studio ad project scaffold.")
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--ad-name", required=True)
    parser.add_argument("--actor", default="local-cli")
    parser.add_argument("--root-path", default=".")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    audit_path = Path(args.root_path) / "projects" / args.project_name / "metadata" / "audit-log.jsonl"
    audit_logger = AppendOnlyAuditLogger(audit_path)
    service = AdProjectScaffoldService(audit_logger)
    result = service.create_ad_project(
        CreateAdProjectRequest(
            project_name=args.project_name,
            ad_name=args.ad_name,
            actor=args.actor,
            root_path=args.root_path,
            force=args.force,
        )
    )

    print(f"Created: {result.ad_path}")
    for warning in result.warnings:
        print(f"WARNING: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
