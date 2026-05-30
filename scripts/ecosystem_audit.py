#!/usr/bin/env python3
"""Inventory local Echo* repos and generate an ecosystem audit report."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime


DEFAULT_ROOT = pathlib.Path(os.environ.get("ECOSYSTEM_ROOT", r"C:\GitHub"))
STALE_DAYS = 60
CLONE_SUFFIXES = (
    "-codex-",
    "-pr",
    "-lantern-test",
    "-starter",
    "-christina-",
)


@dataclass
class RepoInventory:
    name: str
    path: str
    remote: str = ""
    branch: str = ""
    last_commit_date: str = ""
    last_commit_subject: str = ""
    dirty_files: int = 0
    manifests: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    duplicate_group: str = ""
    is_clone: bool = False
    is_stale: bool = False


def run_git(repo: pathlib.Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout.strip()


def discover_repos(root: pathlib.Path) -> list[pathlib.Path]:
    if not root.exists():
        return []
    return sorted(
        path
        for path in root.iterdir()
        if path.is_dir() and (path / ".git").exists()
    )


def manifest_paths(repo: pathlib.Path) -> list[str]:
    names = {
        "package.json",
        "pyproject.toml",
        "requirements.txt",
        "go.mod",
        "Cargo.toml",
        "pom.xml",
        "docker-compose.yml",
        "Dockerfile",
    }
    ignored = {"node_modules", ".git", ".venv", "dist", "build", "__pycache__"}
    found: list[str] = []
    for path in repo.rglob("*"):
        if not path.is_file() or path.name not in names:
            continue
        if ignored.intersection(path.relative_to(repo).parts):
            continue
        found.append(str(path.relative_to(repo)))
    return sorted(found)


def file_contains(repo: pathlib.Path, patterns: list[str]) -> bool:
    lowered = [pattern.lower() for pattern in patterns]
    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(repo)
        if any(part in {".git", "node_modules", ".venv", "dist", "build"} for part in relative.parts):
            continue
        if path.suffix.lower() not in {".md", ".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".yml", ".yaml", ".toml", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            continue
        if any(pattern in text for pattern in lowered):
            return True
    return False


def infer_capabilities(repo: pathlib.Path, manifests: list[str]) -> list[str]:
    capabilities: set[str] = set()
    manifest_blob = " ".join(manifests).lower()
    name = repo.name.lower()

    if "package.json" in manifest_blob:
        capabilities.add("frontend or node automation")
    if "pyproject.toml" in manifest_blob or "requirements.txt" in manifest_blob:
        capabilities.add("python service or automation")
    if "dockerfile" in manifest_blob or "docker-compose.yml" in manifest_blob:
        capabilities.add("containerized service")
    if "contentengine" in name or file_contains(repo, ["content engine", "artifact manifest", "generation job"]):
        capabilities.add("content production pipeline")
    if "opshelm" in name or file_contains(repo, ["opshelm", "ticket", "governance receipt"]):
        capabilities.add("operations orchestration")
    if "echocode" in name or file_contains(repo, ["echocode", "assessment workflow"]):
        capabilities.add("code assessment workflow")
    if "christina" in name or file_contains(repo, ["christina"]):
        capabilities.add("assistant/review automation")
    if "living" in name or file_contains(repo, ["recommendation registry", "lantern adapter"]):
        capabilities.add("recommendation/adaptation workflow")
    if "lantern" in name or file_contains(repo, ["lantern protocol", "civic"]):
        capabilities.add("lantern domain assets")
    if "website" in name:
        capabilities.add("public web presence")
    if "linkedin" in name:
        capabilities.add("linkedin integration")
    if "migration" in name:
        capabilities.add("migration toolkit")

    return sorted(capabilities or {"unclassified"})


def infer_dependencies(manifests: list[str]) -> list[str]:
    deps: set[str] = set()
    for manifest in manifests:
        normalized = manifest.replace("\\", "/").lower()
        if normalized.endswith("package.json"):
            deps.add("node/npm")
        if normalized.endswith(("pyproject.toml", "requirements.txt")):
            deps.add("python")
        if normalized.endswith(("dockerfile", "docker-compose.yml")):
            deps.add("docker")
        if "frontend" in normalized or "ui/" in normalized:
            deps.add("browser runtime")
        if "backend" in normalized or "api" in normalized:
            deps.add("api runtime")
    return sorted(deps)


def canonical_remote(remote: str, name: str) -> str:
    if not remote:
        return name.lower()
    cleaned = remote.removesuffix(".git")
    return cleaned.rsplit("/", 1)[-1].lower()


def clone_like(name: str, remote_group: str) -> bool:
    lowered = name.lower()
    return lowered != remote_group and any(marker in lowered for marker in CLONE_SUFFIXES)


def parse_commit_date(value: str) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def inventory_repo(repo: pathlib.Path, today: date) -> RepoInventory:
    remote = run_git(repo, ["remote", "get-url", "origin"])
    branch = run_git(repo, ["branch", "--show-current"])
    commit_date = run_git(repo, ["log", "-1", "--format=%cs"])
    subject = run_git(repo, ["log", "-1", "--format=%h %s"])
    dirty = len([line for line in run_git(repo, ["status", "--short"]).splitlines() if line.strip()])
    manifests = manifest_paths(repo)
    remote_group = canonical_remote(remote, repo.name)
    last_date = parse_commit_date(commit_date)

    return RepoInventory(
        name=repo.name,
        path=str(repo),
        remote=remote,
        branch=branch,
        last_commit_date=commit_date,
        last_commit_subject=subject,
        dirty_files=dirty,
        manifests=manifests,
        capabilities=infer_capabilities(repo, manifests),
        dependencies=infer_dependencies(manifests),
        duplicate_group=remote_group,
        is_clone=clone_like(repo.name, remote_group),
        is_stale=bool(last_date and (today - last_date).days > STALE_DAYS),
    )


def build_issues(repos: list[RepoInventory]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    groups: dict[str, list[RepoInventory]] = defaultdict(list)
    for repo in repos:
        groups[repo.duplicate_group].append(repo)

    dirty = [repo for repo in repos if repo.dirty_files]
    clones = [repo for repo in repos if repo.is_clone]
    stale = [repo for repo in repos if repo.is_stale]
    duplicate_groups = {group: items for group, items in groups.items() if len(items) > 1}

    if duplicate_groups:
        issues.append({
            "priority": "P0",
            "title": "Consolidate duplicate local clones and PR worktrees",
            "body": f"{len(duplicate_groups)} remote groups have multiple local checkouts; choose canonical working copies before cross-repo implementation.",
        })
    if dirty:
        issues.append({
            "priority": "P0",
            "title": "Resolve dirty worktrees before ecosystem-wide changes",
            "body": f"{len(dirty)} repos have uncommitted files. Capture, commit, or intentionally park them before automated changes.",
        })
    if clones:
        issues.append({
            "priority": "P1",
            "title": "Archive or merge temporary Codex/test clones",
            "body": f"{len(clones)} repos look like task-specific clones. Fold useful changes into canonical repos and remove stale checkouts.",
        })
    if stale:
        issues.append({
            "priority": "P1",
            "title": "Review stale initiatives for ownership",
            "body": f"{len(stale)} repos have not had a commit in more than {STALE_DAYS} days.",
        })

    capability_index: dict[str, list[str]] = defaultdict(list)
    for repo in repos:
        for capability in repo.capabilities:
            capability_index[capability].append(repo.name)
    overlaps = {cap: names for cap, names in capability_index.items() if len(names) > 1 and cap != "unclassified"}
    if overlaps:
        issues.append({
            "priority": "P2",
            "title": "Assign clear system ownership for overlapping capabilities",
            "body": f"{len(overlaps)} capabilities appear in multiple repos. Document source-of-truth boundaries and adapter contracts.",
        })

    return issues


def as_dict(repo: RepoInventory) -> dict[str, object]:
    return {
        "name": repo.name,
        "path": repo.path,
        "remote": repo.remote,
        "branch": repo.branch,
        "last_commit_date": repo.last_commit_date,
        "last_commit_subject": repo.last_commit_subject,
        "dirty_files": repo.dirty_files,
        "manifests": repo.manifests,
        "capabilities": repo.capabilities,
        "dependencies": repo.dependencies,
        "duplicate_group": repo.duplicate_group,
        "is_clone": repo.is_clone,
        "is_stale": repo.is_stale,
    }


def render_markdown(repos: list[RepoInventory], issues: list[dict[str, str]], today: date, root: pathlib.Path) -> str:
    groups: dict[str, list[RepoInventory]] = defaultdict(list)
    capabilities: dict[str, list[str]] = defaultdict(list)
    dependencies: dict[str, list[str]] = defaultdict(list)

    for repo in repos:
        groups[repo.duplicate_group].append(repo)
        for capability in repo.capabilities:
            capabilities[capability].append(repo.name)
        for dependency in repo.dependencies:
            dependencies[dependency].append(repo.name)

    lines = [
        f"# Ecosystem Audit - {today.isoformat()}",
        "",
        f"Scope: local Git repositories under `{root}`.",
        "",
        "## Inventory",
        "",
        "| Repo | Remote group | Branch | Last commit | Dirty | Capabilities |",
        "| --- | --- | --- | --- | ---: | --- |",
    ]
    for repo in repos:
        caps = ", ".join(repo.capabilities)
        lines.append(
            f"| {repo.name} | {repo.duplicate_group} | {repo.branch or '(detached)'} | "
            f"{repo.last_commit_date or 'unknown'} | {repo.dirty_files} | {caps} |"
        )

    lines.extend(["", "## Dependency Graph", ""])
    for dependency, names in sorted(dependencies.items()):
        lines.append(f"- `{dependency}` -> {', '.join(sorted(names))}")

    lines.extend(["", "## Capability Map", ""])
    for capability, names in sorted(capabilities.items()):
        lines.append(f"- {capability}: {', '.join(sorted(names))}")

    lines.extend(["", "## Overlap And Duplicate Services", ""])
    for group, items in sorted(groups.items()):
        if len(items) > 1:
            names = ", ".join(repo.name for repo in items)
            lines.append(f"- `{group}` has {len(items)} local checkouts: {names}")

    overlapping_caps = {cap: names for cap, names in capabilities.items() if len(names) > 1 and cap != "unclassified"}
    for capability, names in sorted(overlapping_caps.items()):
        lines.append(f"- Capability overlap `{capability}`: {', '.join(sorted(names))}")

    abandoned = [repo for repo in repos if repo.is_stale]
    lines.extend(["", "## Abandoned Or At-Risk Initiatives", ""])
    if abandoned:
        for repo in abandoned:
            lines.append(f"- {repo.name}: last commit {repo.last_commit_date}; branch `{repo.branch or '(detached)'}`")
    else:
        lines.append("- No repo crossed the stale threshold in this local scan.")

    lines.extend(["", "## Generated Issues", ""])
    for index, issue in enumerate(issues, start=1):
        lines.append(f"{index}. [{issue['priority']}] {issue['title']}: {issue['body']}")

    lines.extend(
        [
            "",
            "## Implementation Order",
            "",
            "1. P0: choose canonical checkout per duplicate remote group and resolve dirty worktrees.",
            "2. P0: keep this audit script in CI or a scheduled local run so ecosystem drift becomes visible.",
            "3. P1: merge or archive temporary Codex/test clones after useful deltas are harvested.",
            "4. P1: assign owner and disposition for stale repos.",
            "5. P2: document capability boundaries and adapter contracts for overlapping services.",
            "",
            "## Highest Priority Sprint",
            "",
            "Sprint launched: ecosystem audit automation in `EchoMedia-ContentEngine`.",
            "",
            "Acceptance criteria:",
            "- `python scripts/ecosystem_audit.py --root C:\\GitHub --output docs/reports/ecosystem-audit-2026-05-30.md --json-output docs/reports/ecosystem-audit-2026-05-30.json` regenerates this report.",
            "- Unit tests cover duplicate detection, stale detection, dependency inference, and issue prioritization.",
            "- The report identifies P0/P1/P2 work before any cross-repo code changes.",
            "",
            "## Re-Evaluation Loop",
            "",
            "Repeat this audit after each consolidation PR, then reprioritize the generated issues from the new report.",
        ]
    )
    return "\n".join(lines) + "\n"


def audit(root: pathlib.Path, today: date) -> tuple[list[RepoInventory], list[dict[str, str]]]:
    repos = [inventory_repo(repo, today) for repo in discover_repos(root)]
    return repos, build_issues(repos)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=pathlib.Path, default=DEFAULT_ROOT)
    parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path("docs/reports/ecosystem-audit.md"))
    parser.add_argument("--json-output", type=pathlib.Path)
    parser.add_argument("--date", default=date.today().isoformat())
    args = parser.parse_args()

    today = datetime.strptime(args.date, "%Y-%m-%d").date()
    repos, issues = audit(args.root, today)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_markdown(repos, issues, today, args.root), encoding="utf-8")

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps({"repos": [as_dict(repo) for repo in repos], "issues": issues}, indent=2),
            encoding="utf-8",
        )

    print(f"Audited {len(repos)} repos.")
    print(f"Wrote {args.output}.")
    if args.json_output:
        print(f"Wrote {args.json_output}.")


if __name__ == "__main__":
    main()
