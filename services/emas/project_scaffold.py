"""Project and ad scaffolding services for EchoMedia Ad Studio.

This sprint turns the EMAS service primitives into a usable workflow:
create the Vanessa ad project structure, seed scripts/storyboard templates,
and emit audit events for project creation.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .audit import AppendOnlyAuditLogger, AuditEvent


AD_DIRECTORIES = [
    "script",
    "storyboard/frames/pending",
    "storyboard/frames/approved",
    "storyboard/frames/rejected",
    "storyboard/prompts",
    "references/raw-uploads",
    "references/approved",
    "references/rejected",
    "references/by-outfit/neutral-starting-outfit",
    "references/by-outfit/pink-updated-outfit",
    "references/by-expression/neutral",
    "references/by-expression/surprised",
    "references/by-expression/amused",
    "references/by-expression/smiling",
    "references/by-pose/seated-at-computer",
    "references/by-pose/looking-at-screen",
    "references/by-pose/speaking-to-christina",
    "website-mockups/pending",
    "website-mockups/approved",
    "logo-assets/echomedia",
    "logo-assets/lantern",
    "logo-assets/lockups",
    "audio/vanessa-lines",
    "audio/christina-lines",
    "audio/music",
    "exports/reels-9x16",
    "exports/story-9x16",
    "exports/square-1x1",
    "exports/feed-4x5",
    "exports/captions",
    "metadata",
]

SCRIPT_FILES = {
    "script/final-script.md": """# Final Script\n\n[Vanessa sits at her computer reviewing the EchoMedia.ai site.]\n\nVanessa:\nSeriously?\n\n[She shakes her head at the outfit on the screen.]\n\nVanessa:\nChristina, update my outfit to something pink.\n\nChristina:\nNoted. I’ll get it done.\n\n[The EchoMedia site updates. The image refreshes. Vanessa’s outfit changes to pink.]\n\nChristina:\nVanessa, please let me know if you are satisfied with your outfit.\n\n[Vanessa reviews the updated page and smiles.]\n\nVanessa:\nThanks as always, Christina.\n\nVanessa:\nWe wouldn’t have time to live our lives without you.\n\n[Logo end card.]\n\nEchoMedia.ai\nPowered by Lantern Protocol\n\nCreate faster. Live more.\n""",
    "script/short-script.md": """# Short Script\n\nVanessa:\nNope. Christina, update my outfit to something pink.\n\nChristina:\nNoted. I’ll get it done.\n\nChristina:\nVanessa, please let me know if you are satisfied with your outfit.\n\nVanessa:\nPerfect. Thanks as always, Christina. We wouldn’t have time to live our lives without you.\n\nEchoMedia.ai\nPowered by Lantern Protocol\nCreate faster. Live more.\n""",
    "script/captions.md": """# Captions\n\nVanessa: Christina, update my outfit to something pink.\n\nChristina: Noted. I’ll get it done.\n\nChristina: Vanessa, please let me know if you are satisfied with your outfit.\n\nVanessa: Thanks as always, Christina. We wouldn’t have time to live our lives without you.\n""",
    "script/voiceover.md": """# Voiceover Lines\n\n## Vanessa\n- Seriously?\n- Christina, update my outfit to something pink.\n- Thanks as always, Christina.\n- We wouldn’t have time to live our lives without you.\n\n## Christina\n- Noted. I’ll get it done.\n- Vanessa, please let me know if you are satisfied with your outfit.\n""",
}

SCENES = [
    {
        "scene_id": "scene-01",
        "title": "Vanessa at computer",
        "duration_seconds": 3,
        "dialogue": "",
        "status": "pending",
        "approved_frame_id": None,
        "required_assets": ["Vanessa seated at computer", "EchoMedia website mockup"],
        "reference_image_tags": ["seated-at-computer", "looking-at-screen", "neutral-starting-outfit", "soft-light"],
    },
    {
        "scene_id": "scene-02",
        "title": "Vanessa notices outfit",
        "duration_seconds": 4,
        "dialogue": "Seriously?",
        "status": "pending",
        "approved_frame_id": None,
        "required_assets": ["EchoMedia before outfit mockup"],
        "reference_image_tags": ["surprised", "amused", "looking-at-screen", "neutral-starting-outfit"],
    },
    {
        "scene_id": "scene-03",
        "title": "Vanessa asks Christina",
        "duration_seconds": 4,
        "dialogue": "Christina, update my outfit to something pink.",
        "status": "pending",
        "approved_frame_id": None,
        "required_assets": ["Vanessa speaking at computer"],
        "reference_image_tags": ["speaking-to-christina", "seated-at-computer"],
    },
    {
        "scene_id": "scene-04",
        "title": "Christina responds",
        "duration_seconds": 3,
        "dialogue": "Noted. I’ll get it done.",
        "status": "pending",
        "approved_frame_id": None,
        "required_assets": ["Christina UI panel or waveform"],
        "reference_image_tags": ["website-review"],
    },
    {
        "scene_id": "scene-05",
        "title": "Website and outfit update",
        "duration_seconds": 6,
        "dialogue": "",
        "status": "pending",
        "approved_frame_id": None,
        "required_assets": ["before mockup", "after pink outfit mockup", "pink outfit Vanessa image"],
        "reference_image_tags": ["pink-updated-outfit", "website-review"],
    },
    {
        "scene_id": "scene-06",
        "title": "Vanessa reviews result",
        "duration_seconds": 4,
        "dialogue": "Thanks as always, Christina.",
        "status": "pending",
        "approved_frame_id": None,
        "required_assets": ["Vanessa smiling at screen"],
        "reference_image_tags": ["smiling", "looking-at-screen", "pink-updated-outfit"],
    },
    {
        "scene_id": "scene-07",
        "title": "Emotional payoff",
        "duration_seconds": 5,
        "dialogue": "We wouldn’t have time to live our lives without you.",
        "status": "pending",
        "approved_frame_id": None,
        "required_assets": ["Vanessa relaxed satisfied hero shot"],
        "reference_image_tags": ["smiling", "hero-shot", "pink-updated-outfit"],
    },
    {
        "scene_id": "scene-08",
        "title": "EchoMedia and Lantern logo card",
        "duration_seconds": 3,
        "dialogue": "",
        "status": "pending",
        "approved_frame_id": None,
        "required_assets": ["EchoMedia logo", "Lantern Protocol logo", "brand lockup"],
        "reference_image_tags": ["logo-card-compatible"],
    },
]


@dataclass(frozen=True)
class CreateAdProjectRequest:
    project_name: str
    ad_name: str
    actor: str
    root_path: str = "."
    force: bool = False


@dataclass(frozen=True)
class CreateAdProjectResult:
    created: bool
    ad_path: str
    warnings: list[str]


class AdProjectScaffoldService:
    def __init__(self, audit_logger: AppendOnlyAuditLogger | None = None):
        self.audit_logger = audit_logger

    def create_ad_project(self, request: CreateAdProjectRequest) -> CreateAdProjectResult:
        root = Path(request.root_path)
        project_root = root / "projects" / request.project_name
        ad_root = project_root / "ads" / request.ad_name
        warnings: list[str] = []

        if not project_root.exists():
            raise FileNotFoundError(f"Parent likeness project does not exist: {project_root}")

        source_registry = project_root / "source-registry.json"
        if not source_registry.exists():
            warnings.append("Source registry is missing; consent-gated workflows will block until it exists.")

        if ad_root.exists() and not request.force:
            raise FileExistsError(f"Ad project already exists: {ad_root}")

        for directory in AD_DIRECTORIES:
            path = ad_root / directory
            path.mkdir(parents=True, exist_ok=True)
            gitkeep = path / ".gitkeep"
            if not any(path.iterdir()):
                gitkeep.write_text("", encoding="utf-8")

        (ad_root / "README.md").write_text(self._readme(request), encoding="utf-8")
        (ad_root / "production-brief.md").write_text(self._production_brief(request), encoding="utf-8")

        for relative_path, content in SCRIPT_FILES.items():
            (ad_root / relative_path).write_text(content, encoding="utf-8")

        (ad_root / "storyboard" / "storyboard.md").write_text(self._storyboard_markdown(), encoding="utf-8")
        (ad_root / "storyboard" / "shot-list.md").write_text(self._shot_list_markdown(), encoding="utf-8")
        for scene in SCENES:
            prompt_path = ad_root / "storyboard" / "prompts" / f"{scene['scene_id']}-{slug(scene['title'])}.md"
            prompt_path.write_text(self._scene_prompt(scene), encoding="utf-8")

        (ad_root / "metadata" / "asset-index.json").write_text("[]\n", encoding="utf-8")
        (ad_root / "metadata" / "scene-index.json").write_text(json.dumps(SCENES, indent=2), encoding="utf-8")
        (ad_root / "metadata" / "approval-log.jsonl").write_text("", encoding="utf-8")
        (ad_root / "metadata" / "production-log.jsonl").write_text("", encoding="utf-8")

        if self.audit_logger:
            self.audit_logger.append(
                AuditEvent(
                    actor=request.actor,
                    action="ad_project_created",
                    project_name=request.project_name,
                    ad_name=request.ad_name,
                    result="success",
                    target_type="ad_project",
                    target_id=request.ad_name,
                    metadata={"path": str(ad_root), "createdAt": datetime.now(timezone.utc).isoformat()},
                )
            )

        return CreateAdProjectResult(True, str(ad_root), warnings)

    @staticmethod
    def _readme(request: CreateAdProjectRequest) -> str:
        return f"""# {request.ad_name}\n\nParent project: `{request.project_name}`\n\nProduction format: Instagram Reel / Story / Feed export package.\n\nThis ad project is managed by EchoMedia Ad Studio. All Vanessa reference images must remain consent-gated, tagged, reviewed, and approved before use.\n"""

    @staticmethod
    def _production_brief(request: CreateAdProjectRequest) -> str:
        return f"""# Production Brief\n\n## Ad\n\n{request.ad_name}\n\n## Premise\n\nVanessa reviews the EchoMedia site, notices her outfit is not the right vibe, asks Christina to update it to pink, and then confirms the updated result.\n\n## Brand Lockup\n\nEchoMedia.ai / Lantern Protocol\n\n## CTA\n\nCreate faster. Live more.\n"""

    @staticmethod
    def _storyboard_markdown() -> str:
        lines = ["# Storyboard", ""]
        for scene in SCENES:
            lines.extend(
                [
                    f"## {scene['scene_id']}: {scene['title']}",
                    "",
                    f"Duration: {scene['duration_seconds']} seconds",
                    f"Dialogue: {scene['dialogue'] or 'None'}",
                    f"Reference tags: {', '.join(scene['reference_image_tags'])}",
                    "",
                ]
            )
        return "\n".join(lines)

    @staticmethod
    def _shot_list_markdown() -> str:
        lines = ["# Shot List", "", "| Scene | Shot | Assets |", "|---|---|---|"]
        for scene in SCENES:
            lines.append(f"| {scene['scene_id']} | {scene['title']} | {', '.join(scene['required_assets'])} |")
        return "\n".join(lines) + "\n"

    @staticmethod
    def _scene_prompt(scene: dict) -> str:
        return f"""# {scene['scene_id']} Prompt - {scene['title']}\n\nCreate a vertical 9:16 Instagram storyboard frame.\n\nScene:\n{scene['title']}\n\nDialogue:\n{scene['dialogue'] or 'No dialogue in this frame.'}\n\nReference tags:\n{', '.join(scene['reference_image_tags'])}\n\nMood:\nPremium, calm, modern creator/business owner energy.\n\nSafety:\nAuthorized synthetic likeness only. Non-deceptive. No claim that this is documentary footage or a real event.\n\nOutput:\nStoryboard frame, 9:16.\n"""


def slug(value: str) -> str:
    return "-".join("".join(ch.lower() if ch.isalnum() else " " for ch in value).split())
