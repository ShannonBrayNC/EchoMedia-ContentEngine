#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

INTENSITY_TERMS = {
    "danger": 12,
    "fight": 14,
    "escape": 14,
    "betrayal": 13,
    "truth": 9,
    "reveal": 11,
    "death": 15,
    "warning": 8,
    "final": 10,
    "choice": 8,
    "storm": 7,
    "fire": 10,
    "blood": 12,
    "silence": 6,
}

EMOTIONAL_TERMS = {
    "fear": 8,
    "grief": 9,
    "love": 7,
    "anger": 8,
    "hope": 6,
    "mercy": 7,
    "guilt": 8,
    "trust": 6,
    "loss": 8,
}


def load_scene_index(project_root: Path) -> list[dict]:
    scene_index = project_root / "screenplay/scenes/scene-index.json"
    if not scene_index.exists():
        raise SystemExit(f"Scene index not found: {scene_index}")
    data = json.loads(scene_index.read_text(encoding="utf-8"))
    return data.get("scenes", [])


def score_scene(scene: dict) -> dict:
    text = " ".join(
        str(scene.get(field, ""))
        for field in ["title", "story_objective", "emotional_objective"]
    ).lower()

    trailer_score = scene.get("trailer_suitability", {}).get("score", 0)
    runtime_seconds = int(scene.get("estimated_runtime_seconds", 0))

    term_score = sum(score for term, score in INTENSITY_TERMS.items() if term in text)
    emotional_score = sum(score for term, score in EMOTIONAL_TERMS.items() if term in text)
    runtime_score = min(20, int(runtime_seconds / 30))

    intensity = min(100, term_score + emotional_score + runtime_score + int(trailer_score / 3))

    if intensity >= 70:
        pacing_band = "climax"
    elif intensity >= 45:
        pacing_band = "escalation"
    elif intensity >= 25:
        pacing_band = "development"
    else:
        pacing_band = "setup"

    return {
        "scene_id": scene.get("scene_id"),
        "title": scene.get("title"),
        "runtime_seconds": runtime_seconds,
        "runtime": scene.get("estimated_runtime"),
        "intensity": intensity,
        "pacing_band": pacing_band,
        "trailer_score": trailer_score,
    }


def build_report(project_root: Path) -> dict:
    scenes = load_scene_index(project_root)
    scored = [score_scene(scene) for scene in scenes]
    total_runtime = sum(scene["runtime_seconds"] for scene in scored)
    average_intensity = round(sum(scene["intensity"] for scene in scored) / len(scored), 2) if scored else 0
    climax_scenes = [scene for scene in scored if scene["pacing_band"] == "climax"]

    return {
        "project_root": str(project_root),
        "scene_count": len(scored),
        "total_runtime_seconds": total_runtime,
        "average_intensity": average_intensity,
        "climax_density": round(len(climax_scenes) / len(scored), 4) if scored else 0,
        "pacing_curve": scored,
        "trailer_overlay": [
            {
                "scene_id": scene["scene_id"],
                "title": scene["title"],
                "trailer_score": scene["trailer_score"],
                "intensity": scene["intensity"],
            }
            for scene in scored
            if scene["trailer_score"] >= 40
        ],
        "heatmap": [scene["intensity"] for scene in scored],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()

    report = build_report(args.project_root)
    report_path = args.report or args.project_root / "reports/pacing-analysis.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"Pacing analysis complete. Report: {report_path}")
    print(f"Average intensity: {report['average_intensity']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
