#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_episode_map(project_root: Path, season: int, episode_count: int) -> dict:
    scenes_path = project_root / "screenplay/scenes/scene-index.json"
    scenes = []

    if scenes_path.exists():
        scenes = json.loads(scenes_path.read_text(encoding="utf-8")).get("scenes", [])

    episodes = []
    for episode_number in range(1, episode_count + 1):
        assigned = scenes[episode_number - 1 :: episode_count]
        episodes.append(
            {
                "episode_id": f"S{season:02d}E{episode_number:02d}",
                "title": f"Episode {episode_number}",
                "status": "draft",
                "cold_open": "TODO",
                "act_breaks": [],
                "cliffhanger": "TODO",
                "assigned_scenes": [scene.get("scene_id") for scene in assigned],
                "runtime_target_minutes": 45,
            }
        )

    return {
        "season": season,
        "episode_count": episode_count,
        "status": "draft",
        "season_arc": "TODO",
        "episodes": episodes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--season", type=int, default=1)
    parser.add_argument("--episodes", type=int, default=8)
    args = parser.parse_args()

    output = build_episode_map(args.project_root, args.season, args.episodes)
    out_dir = args.project_root / "tv-adaptation"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"season-{args.season:02d}-episode-map.json"
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")

    print(f"Created TV adaptation map: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
