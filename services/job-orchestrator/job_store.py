from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
JOB_ROOT = ROOT / "jobs"
JOB_INDEX = JOB_ROOT / "job-index.json"

VALID_STATES = {
    "queued",
    "running",
    "completed",
    "failed",
    "cancelled",
    "retrying",
}


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def load_index() -> dict:
    if not JOB_INDEX.exists():
        return {"jobs": []}
    return json.loads(JOB_INDEX.read_text(encoding="utf-8"))


def save_index(index: dict) -> None:
    JOB_ROOT.mkdir(parents=True, exist_ok=True)
    JOB_INDEX.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")


def job_path(job_id: str) -> Path:
    return JOB_ROOT / f"{job_id}.json"


def save_job(job: dict) -> None:
    JOB_ROOT.mkdir(parents=True, exist_ok=True)
    job_path(job["job_id"]).write_text(json.dumps(job, indent=2) + "\n", encoding="utf-8")

    index = load_index()
    index["jobs"] = [item for item in index.get("jobs", []) if item["job_id"] != job["job_id"]]
    index["jobs"].append({
        "job_id": job["job_id"],
        "workflow": job["workflow"],
        "state": job["state"],
        "project_id": job.get("project_id"),
        "priority": job.get("priority", 100),
        "created_at": job["created_at"],
        "updated_at": job["updated_at"],
    })
    save_index(index)


def load_job(job_id: str) -> dict:
    path = job_path(job_id)
    if not path.exists():
        raise FileNotFoundError(f"Unknown job: {job_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def create_job(workflow: str, payload: dict[str, Any], project_id: str | None = None, priority: int = 100) -> dict:
    job = {
        "job_id": str(uuid.uuid4()),
        "workflow": workflow,
        "project_id": project_id,
        "payload": payload,
        "priority": priority,
        "state": "queued",
        "attempts": 0,
        "max_attempts": 3,
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "started_at": None,
        "finished_at": None,
        "result": None,
        "error": None,
        "cancel_requested": False,
    }
    save_job(job)
    return job


def update_job(job_id: str, **changes: Any) -> dict:
    job = load_job(job_id)
    job.update(changes)
    job["updated_at"] = utc_now()
    save_job(job)
    return job


def list_jobs(state: str | None = None) -> list[dict]:
    index = load_index()
    jobs = index.get("jobs", [])
    if state:
        jobs = [job for job in jobs if job.get("state") == state]
    return sorted(jobs, key=lambda job: (job.get("priority", 100), job.get("created_at", "")))


def cancel_job(job_id: str) -> dict:
    return update_job(job_id, cancel_requested=True, state="cancelled")
