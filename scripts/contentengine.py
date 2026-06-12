#!/usr/bin/env python3
"""ContentEngine runtime CLI.

Examples:
  python scripts/contentengine.py profiles list
  python scripts/contentengine.py profiles show shannon
  python scripts/contentengine.py image-job shannon --scene "presenting Lantern to investors"
  python scripts/contentengine.py render-dry-run shannon --scene "tech founder portrait"
  python scripts/contentengine.py storyboard shannon --title "Lantern Founder Short" --scene "opens in command center" --scene "explains trust layer"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from services.contentengine.profiles import ProfileRegistry, summarize_profiles
from services.contentengine.renderer import DryRunRenderer


def print_json(payload: Any) -> None:
    print(json.dumps(payload, indent=2, sort_keys=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="EchoMedia ContentEngine runtime CLI")
    parser.add_argument("--root", default=".", help="Repository root. Defaults to current directory.")
    subcommands = parser.add_subparsers(dest="command", required=True)

    profiles = subcommands.add_parser("profiles", help="Profile registry operations")
    profile_commands = profiles.add_subparsers(dest="profile_command", required=True)

    profile_list = profile_commands.add_parser("list", help="List profiles")
    profile_list.add_argument("--type", dest="profile_type")
    profile_list.add_argument("--status")
    profile_list.add_argument("--tag")

    profile_show = profile_commands.add_parser("show", help="Show one profile by id or name")
    profile_show.add_argument("profile")

    profile_archive = profile_commands.add_parser("archive", help="Archive one profile")
    profile_archive.add_argument("profile")
    profile_archive.add_argument("--actor", default="cli")

    image_job = subcommands.add_parser("image-job", help="Build a profile-driven image job manifest")
    image_job.add_argument("profile")
    image_job.add_argument("--scene", required=True)
    image_job.add_argument("--brand")
    image_job.add_argument("--production")

    render = subcommands.add_parser("render-dry-run", help="Create a dry-run output manifest for an image job")
    render.add_argument("profile")
    render.add_argument("--scene", required=True)
    render.add_argument("--brand")
    render.add_argument("--production")
    render.add_argument("--adapter", default="manual-export")

    storyboard = subcommands.add_parser("storyboard", help="Export a dry-run storyboard/video project manifest")
    storyboard.add_argument("profile")
    storyboard.add_argument("--title", required=True)
    storyboard.add_argument("--format", default="short")
    storyboard.add_argument("--scene", action="append", required=True)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.root)
    registry = ProfileRegistry(root)

    if args.command == "profiles":
        if args.profile_command == "list":
            print_json(summarize_profiles(registry.list_profiles(profile_type=args.profile_type, status=args.status, tag=args.tag)))
            return 0
        if args.profile_command == "show":
            print_json(registry.get_profile(args.profile))
            return 0
        if args.profile_command == "archive":
            print_json(registry.archive_profile(args.profile, actor=args.actor))
            return 0

    if args.command == "image-job":
        print_json(registry.build_image_job(args.profile, scene=args.scene, brand=args.brand, production=args.production))
        return 0

    if args.command == "render-dry-run":
        job = registry.build_image_job(args.profile, scene=args.scene, brand=args.brand, production=args.production)
        print_json(DryRunRenderer(root, adapter_name=args.adapter).render_image_job(job))
        return 0

    if args.command == "storyboard":
        print_json(DryRunRenderer(root).export_storyboard(profile_id=args.profile, project_title=args.title, scenes=args.scene, format=args.format))
        return 0

    raise SystemExit(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
