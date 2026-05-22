#!/usr/bin/env python3
"""
Generate Lantern Protocol art/artifact packs across all local Git branches.

Default behavior:
- Reads all local branches without checking them out.
- Scans text files for visual prompts, storyboard beats, pitch artifacts, trailer shots,
  chapter material, and in-universe artifacts.
- Writes prompt packs, image job manifests, storyboard cards, placeholders, and reports
  under projects/lantern-protocol/_generated.
- Does not overwrite canon source files.
- Does not generate real images unless --generate-images and OPENAI_API_KEY are supplied.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


REPO_NAME = "ShannonBrayNC/EchoMedia-ContentEngine"

DEFAULT_BRANCH_ORDER = [
    "cleanup/lantern-canon-freeze-v2",
    "cleanup/lantern-canon-freeze",
    "lantern-canon-sync-manuscript",
    "main",
]

TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".json",
    ".fountain",
    ".log",
    ".csv",
}

SKIP_PARTS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "dist",
    "build",
    "_generated",
}

GLOBAL_NEGATIVE_PROMPT = (
    "no humanoid Lantern body, no robot avatar for Lantern, no AI face, "
    "no superhero styling, no neon cyberpunk excess, no cartoon style, "
    "no gore, no explicit sexual content, no copyrighted character imitation"
)

GLOBAL_STYLE_TAGS = [
    "cinematic near-future techno-political thriller",
    "institutional realism",
    "grounded human detail",
    "clean civic AI interface glow",
    "realistic lighting",
    "film still",
    "high detail",
    "emotionally tense atmosphere",
]


@dataclass
class SourceFile:
    logical_id: str
    branch: str
    path: str
    role: str
    sha: str
    line_count: int


@dataclass
class PromptJob:
    id: str
    category: str
    title: str
    source_branch: str
    source_path: str
    prompt: str
    negative_prompt: str
    style_tags: list[str]
    output_path: str
    status: str = "planned"


def run_git(args: list[str], cwd: Path) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed:\n{proc.stderr}")
    return proc.stdout


def local_branches(repo_root: Path) -> list[str]:
    raw = run_git(["for-each-ref", "--format=%(refname:short)", "refs/heads"], repo_root)
    branches = [line.strip() for line in raw.splitlines() if line.strip()]
    ordered = [b for b in DEFAULT_BRANCH_ORDER if b in branches]
    ordered.extend([b for b in branches if b not in ordered])
    return ordered


def list_branch_files(repo_root: Path, branch: str) -> list[str]:
    raw = run_git(["ls-tree", "-r", "--name-only", branch], repo_root)
    return [line.strip() for line in raw.splitlines() if line.strip()]


def read_branch_file(repo_root: Path, branch: str, path: str) -> str:
    return run_git(["show", f"{branch}:{path}"], repo_root)


def is_candidate_text_file(path: str, include_archive: bool) -> bool:
    p = Path(path)
    if p.suffix.lower() not in TEXT_EXTENSIONS:
        return False
    parts = set(p.parts)
    if parts & SKIP_PARTS:
        return False
    if not include_archive and ("_archive" in parts or "fiction" in parts):
        return False
    projectish = (
        path.startswith("projects/lantern-protocol/")
        or path.startswith("_archive/lantern-protocol-v0-novel/")
        or path.startswith("fiction/lantern-protocol/")
    )
    return projectish


def classify_role(path: str) -> str:
    lower = path.lower()
    if "visual-bible/character-image-prompts" in lower:
        return "character_prompts"
    if "visual-bible/location-image-prompts" in lower:
        return "location_prompts"
    if "visual-bible/visual-style-guide" in lower:
        return "visual_style"
    if "/trailer/" in lower:
        return "trailer"
    if "/storyboards/" in lower:
        return "storyboard"
    if "/novel/manuscript/chapters/" in lower or "/04-manuscript" in lower:
        return "chapter"
    if "/pitch/" in lower or "/11-pitch/" in lower:
        return "pitch"
    if "/05-artifacts/" in lower or "/artifacts/" in lower:
        return "in_universe_artifact"
    if "/screenplay/" in lower:
        return "screenplay"
    if "/sequel/" in lower:
        return "sequel"
    if "/reports/" in lower:
        return "report"
    return "supporting_text"


def stable_id(*parts: str) -> str:
    seed = "::".join(parts)
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:12]


def slugify(value: str, fallback: str = "item") -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return value or fallback


def title_from_path(path: str) -> str:
    stem = Path(path).stem
    stem = re.sub(r"^\d+[-_]", "", stem)
    stem = stem.replace("-", " ").replace("_", " ")
    return stem.title()


def extract_fenced_text_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    for match in re.finditer(r"```(?:text|prompt)?\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE):
        block = match.group(1).strip()
        if len(block) > 40:
            blocks.append(block)
    return blocks


def extract_headed_sections(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^(#{1,3})\s+(.+?)\s*$", text, re.MULTILINE))
    sections: list[tuple[str, str]] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        title = match.group(2).strip()
        body = text[start:end].strip()
        if body:
            sections.append((title, body))
    return sections


def compact_summary(text: str, max_chars: int = 1200) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned[:max_chars].rstrip()


def make_prompt_job(
    category: str,
    title: str,
    branch: str,
    path: str,
    prompt: str,
    generated_root: Path,
) -> PromptJob:
    job_id = stable_id(category, title, branch, path, prompt[:160])
    safe = slugify(title, job_id)
    out_rel = f"{generated_root.name}/images/{category}/{safe}-{job_id}.png"
    return PromptJob(
        id=job_id,
        category=category,
        title=title,
        source_branch=branch,
        source_path=path,
        prompt=prompt.strip(),
        negative_prompt=GLOBAL_NEGATIVE_PROMPT,
        style_tags=list(GLOBAL_STYLE_TAGS),
        output_path=out_rel,
    )


def build_jobs_from_source(source: SourceFile, text: str, generated_root: Path) -> list[PromptJob]:
    jobs: list[PromptJob] = []
    role = source.role

    if role in {"character_prompts", "location_prompts", "trailer"}:
        blocks = extract_fenced_text_blocks(text)
        for idx, block in enumerate(blocks, start=1):
            nearby_title = f"{title_from_path(source.path)} {idx:02d}"
            jobs.append(make_prompt_job(role, nearby_title, source.branch, source.path, block, generated_root))
        return jobs

    if role == "storyboard":
        sections = extract_headed_sections(text)
        useful = sections[:8] if sections else [(title_from_path(source.path), text)]
        for idx, (heading, body) in enumerate(useful, start=1):
            prompt = (
                f"{heading}. {compact_summary(body, 900)}\n\n"
                f"Render as cinematic storyboard frame, institutional realism, practical human light, "
                f"clean civic interface elements where appropriate."
            )
            jobs.append(make_prompt_job("chapter_storyboard", f"{title_from_path(source.path)} frame {idx:02d}", source.branch, source.path, prompt, generated_root))
        return jobs

    if role == "chapter":
        sections = extract_headed_sections(text)
        title = title_from_path(source.path)
        lead = compact_summary(text, 1100)
        prompt = (
            f"Key art for {title}. Use this chapter material as visual context: {lead}\n\n"
            f"Create one cinematic representative still that captures the chapter's central human conflict, "
            f"the Lantern Protocol visual language, and the contrast between warm human light and cold civic systems."
        )
        jobs.append(make_prompt_job("chapter_key_art", title, source.branch, source.path, prompt, generated_root))

        for idx, (heading, body) in enumerate(sections[:4], start=1):
            prompt = (
                f"Storyboard frame for {title}, section {heading}: {compact_summary(body, 700)}\n\n"
                f"Film still, grounded human detail, civic systems visible when relevant."
            )
            jobs.append(make_prompt_job("chapter_storyboard", f"{title} {idx:02d} {heading}", source.branch, source.path, prompt, generated_root))
        return jobs

    if role == "pitch":
        prompt = (
            f"Pitch deck visual for {title_from_path(source.path)}. Source summary: {compact_summary(text, 900)}\n\n"
            f"Make it feel premium, serious, cinematic, and marketable without losing institutional realism."
        )
        jobs.append(make_prompt_job("pitch_visual", title_from_path(source.path), source.branch, source.path, prompt, generated_root))
        return jobs

    if role == "in_universe_artifact":
        prompt = (
            f"Create an in-universe document/prop visual based on {title_from_path(source.path)}. "
            f"Source excerpt: {compact_summary(text, 900)}\n\n"
            f"Looks like a real leaked civic document, hearing exhibit, emergency memo, dashboard printout, "
            f"or public system artifact from the Lantern Protocol world."
        )
        jobs.append(make_prompt_job("in_universe_artifact", title_from_path(source.path), source.branch, source.path, prompt, generated_root))
        return jobs

    return jobs


def write_text(path: Path, content: str, overwrite: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return
    path.write_text(content, encoding="utf-8")


def markdown_prompt_pack(title: str, jobs: Iterable[PromptJob]) -> str:
    rows = [f"# {title}", ""]
    for job in jobs:
        rows.extend(
            [
                f"## {job.title}",
                "",
                f"- **Job ID:** `{job.id}`",
                f"- **Category:** `{job.category}`",
                f"- **Source:** `{job.source_branch}:{job.source_path}`",
                f"- **Output:** `{job.output_path}`",
                "",
                "```text",
                job.prompt,
                "```",
                "",
                "**Negative prompt:**",
                "",
                "```text",
                job.negative_prompt,
                "```",
                "",
                "---",
                "",
            ]
        )
    return "\n".join(rows).rstrip() + "\n"


def write_storyboard_cards(generated_root: Path, jobs: list[PromptJob]) -> list[str]:
    out_paths: list[str] = []
    grouped: dict[str, list[PromptJob]] = {}
    for job in jobs:
        if job.category not in {"chapter_storyboard", "chapter_key_art"}:
            continue
        key = slugify(Path(job.source_path).stem)
        grouped.setdefault(key, []).append(job)

    cards_dir = generated_root / "storyboard-cards"
    for key, group in grouped.items():
        title = group[0].title
        body = [f"# Storyboard Card — {title}", ""]
        body.append(f"- **Source:** `{group[0].source_branch}:{group[0].source_path}`")
        body.append(f"- **Frames:** {len(group)}")
        body.append("")
        for idx, job in enumerate(group, start=1):
            body.extend(
                [
                    f"## Frame {idx}: {job.title}",
                    "",
                    "```text",
                    job.prompt,
                    "```",
                    "",
                    f"Planned output: `{job.output_path}`",
                    "",
                ]
            )
        card_path = cards_dir / f"{key}.md"
        write_text(card_path, "\n".join(body).rstrip() + "\n")
        out_paths.append(str(card_path))
    return out_paths


def write_placeholders(generated_root: Path, jobs: list[PromptJob]) -> list[str]:
    out_paths: list[str] = []
    placeholder_dir = generated_root / "placeholders"
    for job in jobs:
        category_dir = placeholder_dir / job.category
        path = category_dir / f"{slugify(job.title)}-{job.id}.md"
        body = f"""# Image Placeholder — {job.title}

- **Job ID:** `{job.id}`
- **Category:** `{job.category}`
- **Source:** `{job.source_branch}:{job.source_path}`
- **Intended output:** `{job.output_path}`
- **Status:** `{job.status}`

## Prompt

```text
{job.prompt}
```

## Negative Prompt

```text
{job.negative_prompt}
```

## Manual Generation Notes

Use this card in ChatGPT, OpenAI Images, Midjourney, Runway, Leonardo, or your chosen art pipeline. Keep Lantern faceless and system-embedded. Preserve institutional realism.
"""
        write_text(path, body)
        out_paths.append(str(path))
    return out_paths


def maybe_generate_images(repo_root: Path, jobs: list[PromptJob], generated_root: Path, max_images: int, overwrite: bool) -> list[str]:
    if max_images <= 0:
        return []
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not set; skipping image generation.", file=sys.stderr)
        return []

    try:
        from openai import OpenAI
    except Exception as exc:
        print(f"openai package unavailable; skipping image generation: {exc}", file=sys.stderr)
        return []

    client = OpenAI()
    model = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1")
    written: list[str] = []

    for job in jobs[:max_images]:
        out_path = repo_root / "projects/lantern-protocol" / job.output_path
        if out_path.exists() and not overwrite:
            continue
        out_path.parent.mkdir(parents=True, exist_ok=True)

        prompt = f"{job.prompt}\n\nStyle tags: {', '.join(job.style_tags)}\nNegative constraints: {job.negative_prompt}"

        try:
            result = client.images.generate(
                model=model,
                prompt=prompt,
                size=os.getenv("OPENAI_IMAGE_SIZE", "1024x1024"),
            )
            b64 = result.data[0].b64_json
            out_path.write_bytes(base64.b64decode(b64))
            job.status = "generated"
            written.append(str(out_path))
        except Exception as exc:
            job.status = f"failed: {exc}"
            print(f"Image generation failed for {job.id}: {exc}", file=sys.stderr)

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Lantern Protocol art/artifact packs.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Default: current directory.")
    parser.add_argument("--project", default="projects/lantern-protocol", help="Project path.")
    parser.add_argument("--include-archive", action="store_true", help="Include _archive and fiction legacy paths.")
    parser.add_argument("--dry-run", action="store_true", help="Scan only; do not write outputs.")
    parser.add_argument("--generate-images", action="store_true", help="Generate real images when OPENAI_API_KEY is set.")
    parser.add_argument("--max-images", type=int, default=0, help="Maximum images to generate. Default: 0.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing generated image files.")
    parser.add_argument("--output-dir", default="_generated", help="Generated output directory name under --project. Default: _generated.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    project_root = repo_root / args.project
    generated_root = project_root / args.output_dir

    if not (repo_root / ".git").exists():
        raise SystemExit(f"Not a Git repository root: {repo_root}")

    branches = local_branches(repo_root)
    missing_preferred = [b for b in DEFAULT_BRANCH_ORDER if b not in branches]
    warnings: list[str] = []
    if missing_preferred:
        warnings.append(f"Preferred branches missing locally: {', ' .join(missing_preferred)}")
    source_files: list[SourceFile] = []
    seen_logical: dict[str, SourceFile] = {}

    for branch in branches:
        try:
            paths = list_branch_files(repo_root, branch)
        except Exception as exc:
            warnings.append(f"Could not list branch {branch}: {exc}")
            continue

        for path in paths:
            if not is_candidate_text_file(path, include_archive=args.include_archive):
                continue

            role = classify_role(path)
            logical_id = f"{role}:{Path(path).name}:{slugify(str(Path(path).parent))}"

            try:
                text = read_branch_file(repo_root, branch, path)
            except Exception as exc:
                warnings.append(f"Could not read {branch}:{path}: {exc}")
                continue

            sha = hashlib.sha1(text.encode("utf-8", errors="replace")).hexdigest()
            sf = SourceFile(
                logical_id=logical_id,
                branch=branch,
                path=path,
                role=role,
                sha=sha,
                line_count=len(text.splitlines()),
            )
            source_files.append(sf)

            if logical_id not in seen_logical:
                seen_logical[logical_id] = sf

    selected_sources = list(seen_logical.values())

    prompt_jobs: list[PromptJob] = []
    source_text_cache: dict[tuple[str, str], str] = {}

    for sf in selected_sources:
        try:
            text = read_branch_file(repo_root, sf.branch, sf.path)
            source_text_cache[(sf.branch, sf.path)] = text
            prompt_jobs.extend(build_jobs_from_source(sf, text, generated_root))
        except Exception as exc:
            warnings.append(f"Could not build jobs from {sf.branch}:{sf.path}: {exc}")

    prompt_jobs.sort(key=lambda j: (j.category, j.source_path, j.title))

    if args.dry_run:
        print(json.dumps({
            "branches": branches,
            "source_file_count": len(source_files),
            "selected_source_count": len(selected_sources),
            "prompt_job_count": len(prompt_jobs),
            "warnings": warnings,
        }, indent=2))
        return 0

    generated_root.mkdir(parents=True, exist_ok=True)

    generated_images: list[str] = []
    if args.generate_images:
        generated_images = maybe_generate_images(repo_root, prompt_jobs, generated_root, args.max_images, args.overwrite)

    prompt_pack_dir = generated_root / "prompt-packs"
    pitch_dir = generated_root / "pitch-artifacts"
    reports_dir = generated_root / "reports"

    categories = {
        "characters": ["character_prompts"],
        "locations": ["location_prompts"],
        "trailer-shots": ["trailer"],
        "chapter-storyboards": ["chapter_storyboard", "chapter_key_art"],
    }

    artifact_outputs: list[str] = []

    for pack_name, cats in categories.items():
        pack_jobs = [job for job in prompt_jobs if job.category in cats]
        path = prompt_pack_dir / f"{pack_name}.md"
        write_text(path, markdown_prompt_pack(f"Lantern Protocol — {pack_name.replace('-', ' ').title()}", pack_jobs))
        artifact_outputs.append(str(path))

    pitch_jobs = [job for job in prompt_jobs if job.category in {"pitch_visual", "in_universe_artifact"}]
    pitch_path = pitch_dir / "visual-pitch-pack.md"
    write_text(pitch_path, markdown_prompt_pack("Lantern Protocol — Visual Pitch Pack", pitch_jobs))
    artifact_outputs.append(str(pitch_path))

    storyboard_cards = write_storyboard_cards(generated_root, prompt_jobs)
    placeholders = write_placeholders(generated_root, prompt_jobs)
    artifact_outputs.extend(storyboard_cards)
    artifact_outputs.extend(placeholders)

    image_jobs_path = generated_root / "image-jobs.jsonl"
    write_text(image_jobs_path, "\n".join(json.dumps(asdict(job), ensure_ascii=False) for job in prompt_jobs) + "\n")
    artifact_outputs.append(str(image_jobs_path))

    manifest = {
        "generated_at": dt.datetime.now(dt.UTC).isoformat(),
        "repo": REPO_NAME,
        "branch_order": branches,
        "source_files": [asdict(sf) for sf in source_files],
        "selected_sources": [asdict(sf) for sf in selected_sources],
        "prompt_jobs": [asdict(job) for job in prompt_jobs],
        "artifact_outputs": artifact_outputs,
        "generated_images": generated_images,
        "warnings": warnings,
        "counts": {
            "branches": len(branches),
            "source_files": len(source_files),
            "selected_sources": len(selected_sources),
            "prompt_jobs": len(prompt_jobs),
            "artifact_outputs": len(artifact_outputs),
            "generated_images": len(generated_images),
        },
    }

    manifest_path = generated_root / "artifact-manifest.json"
    write_text(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False))
    artifact_outputs.append(str(manifest_path))

    index_lines = [
        "# Lantern Protocol — Generated Artifact Index",
        "",
        f"Generated at: `{manifest['generated_at']}`",
        "",
        "## Counts",
        "",
    ]
    for key, value in manifest["counts"].items():
        index_lines.append(f"- **{key}:** {value}")

    index_lines.extend(["", "## Outputs", ""])
    for path in sorted(set(artifact_outputs)):
        rel = Path(path)
        try:
            rel = rel.relative_to(repo_root)
        except Exception:
            pass
        index_lines.append(f"- `{rel}`")

    index_lines.extend(["", "## Warnings", ""])
    if warnings:
        index_lines.extend(f"- {w}" for w in warnings)
    else:
        index_lines.append("- None.")

    index_path = generated_root / "artifact-index.md"
    write_text(index_path, "\n".join(index_lines) + "\n")

    readme = f"""# Lantern Protocol Generated Artifacts

This folder is generated by:

```bash
python scripts/generate_content_artifacts.py --project {args.project}
```

The generator scans all local Git branches, extracts visual/artifact seeds, and writes prompt packs, image job manifests, storyboard cards, placeholder cards, and a generation report.

## Common Commands

Dry run:

```bash
python scripts/generate_content_artifacts.py --project {args.project} --dry-run
```

Include legacy archive material:

```bash
python scripts/generate_content_artifacts.py --project {args.project} --include-archive
```

Generate a limited real image batch when `OPENAI_API_KEY` is available:

```bash
python scripts/generate_content_artifacts.py --project {args.project} --include-archive --generate-images --max-images 12
```

## Safety

The generator does not modify manuscript/source canon. It writes only inside `_generated` unless the script itself is edited.
"""
    write_text(generated_root / "README.md", readme)

    report = f"""# Lantern Protocol — Generation Report

- Branches scanned: {len(branches)}
- Source files discovered: {len(source_files)}
- Selected source files after dedupe: {len(selected_sources)}
- Prompt/image jobs created: {len(prompt_jobs)}
- Generated images: {len(generated_images)}

## Branch Order

{chr(10).join(f"- `{branch}`" for branch in branches)}

## Notes

- Canon/source files were not modified.
- Lantern should remain faceless and represented through systems, terminals, dashboards, logs, and civic infrastructure.
- Use `image-jobs.jsonl` for external generation queues.
"""
    write_text(reports_dir / "generation-report.md", report)

    print(f"Wrote generated artifacts to {generated_root}")
    print(f"Prompt jobs: {len(prompt_jobs)}")
    print(f"Generated images: {len(generated_images)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
