#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

from job_store import list_jobs, load_job, update_job

ROOT = Path(__file__).resolve().parents[2]

WORKFLOW_COMMANDS = {
    "assemble-screenplay": lambda payload: [
        "python",
        str(ROOT / "services/screenplay-assembler/assemble_screenplay.py"),
        payload["project_root"],
    ],
    "build-export-package": lambda payload: [
        "python",
        str(ROOT / "services/export-packager/build_export_package.py"),
        payload["project_root"],
        payload.get("package_type", "author-review"),
    ],
    "create-release": lambda payload: [
        "python",
        str(ROOT / "services/release-manager/create_release_manifest.py"),
        payload["project_root"],
        payload["version"],
        payload.get("release_state", "candidate"),
    ],
}


def execute_job(job_id: str) -> dict:
    job = load_job(job_id)

    if job.get("cancel_requested"):
        return update_job(job_id, state="cancelled")

    workflow = job["workflow"]

    if workflow not in WORKFLOW_COMMANDS:
        return update_job(job_id, state="failed", error=f"Unsupported workflow: {workflow}")

    update_job(job_id, state="running", started_at=job.get("started_at") or job.get("updated_at"))

    command = WORKFLOW_COMMANDS[workflow](job["payload"])

    result = subprocess.run(command, capture_output=True, text=True, cwd=ROOT)

    if result.returncode == 0:
        return update_job(
            job_id,
            state="completed",
            finished_at=job.get("updated_at"),
            result={
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
        )

    attempts = job.get("attempts", 0) + 1

    if attempts < job.get("max_attempts", 3):
        return update_job(
            job_id,
            attempts=attempts,
            state="retrying",
            error=result.stderr,
        )

    return update_job(
        job_id,
        attempts=attempts,
        state="failed",
        finished_at=job.get("updated_at"),
        error=result.stderr,
    )


def main() -> int:
    queued = list_jobs(state="queued") + list_jobs(state="retrying")

    for item in queued:
        execute_job(item["job_id"])

    print(f"Processed {len(queued)} queued job(s).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
