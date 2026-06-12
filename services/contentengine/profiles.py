"""Durable profile registry runtime for EchoMedia ContentEngine.

This module intentionally uses only the Python standard library so it can run in
safe local mode, CI, and Christina/EchoCodex automation without provider keys.
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

PROFILE_TYPES = {
    "human_subject",
    "persona",
    "fictional_character",
    "brand",
    "production",
}

REFERENCE_TYPES = {
    "identity",
    "wardrobe",
    "pose",
    "scene",
    "mood",
    "expression",
    "full_body",
}

REQUIRED_PROFILE_FIELDS = {
    "id",
    "name",
    "type",
    "status",
    "version",
    "owner",
    "description",
    "tags",
    "visibility",
    "governance",
    "createdAt",
    "updatedAt",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class RegistryPaths:
    root: Path

    @property
    def registry(self) -> Path:
        return self.root / "profiles" / "registry.json"

    @property
    def audit_log(self) -> Path:
        return self.root / "generated" / "profile-audit.jsonl"

    @property
    def outputs_root(self) -> Path:
        return self.root / "generated" / "outputs"


class ProfileRegistry:
    def __init__(self, root: Path | str = ".") -> None:
        self.paths = RegistryPaths(Path(root))

    def load(self) -> dict[str, Any]:
        if not self.paths.registry.exists():
            return {"schema": "lantern.contentengine.profileRegistry.v1", "updatedAt": utc_now(), "profiles": []}
        with self.paths.registry.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        self.validate_registry(data)
        return data

    def save(self, data: dict[str, Any]) -> None:
        self.validate_registry(data)
        data["updatedAt"] = utc_now()
        self.paths.registry.parent.mkdir(parents=True, exist_ok=True)
        self.paths.registry.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")

    def list_profiles(self, *, profile_type: str | None = None, status: str | None = None, tag: str | None = None) -> list[dict[str, Any]]:
        profiles = self.load()["profiles"]
        if profile_type:
            profiles = [profile for profile in profiles if profile.get("type") == profile_type]
        if status:
            profiles = [profile for profile in profiles if profile.get("status") == status]
        if tag:
            profiles = [profile for profile in profiles if tag in profile.get("tags", [])]
        return copy.deepcopy(profiles)

    def get_profile(self, profile_id_or_name: str) -> dict[str, Any]:
        needle = profile_id_or_name.lower()
        for profile in self.load()["profiles"]:
            if profile["id"].lower() == needle or profile["name"].lower() == needle:
                return copy.deepcopy(profile)
        raise KeyError(f"Profile not found: {profile_id_or_name}")

    def upsert_profile(self, profile: dict[str, Any], *, actor: str = "system") -> dict[str, Any]:
        data = self.load()
        existing_index = None
        for index, current in enumerate(data["profiles"]):
            if current["id"] == profile["id"]:
                existing_index = index
                break

        now = utc_now()
        next_profile = copy.deepcopy(profile)
        next_profile.setdefault("createdAt", now)
        next_profile["updatedAt"] = now
        next_profile.setdefault("references", [])
        self.validate_profile(next_profile)

        if existing_index is None:
            next_profile.setdefault("version", 1)
            data["profiles"].append(next_profile)
            self.emit_event("profile.created", next_profile, actor=actor)
        else:
            previous = data["profiles"][existing_index]
            next_profile["createdAt"] = previous.get("createdAt", now)
            next_profile["version"] = int(previous.get("version", 0)) + 1
            data["profiles"][existing_index] = next_profile
            self.emit_event("profile.updated", next_profile, actor=actor)

        self.save(data)
        return copy.deepcopy(next_profile)

    def archive_profile(self, profile_id: str, *, actor: str = "system") -> dict[str, Any]:
        profile = self.get_profile(profile_id)
        profile["status"] = "archived"
        archived = self.upsert_profile(profile, actor=actor)
        self.emit_event("profile.archived", archived, actor=actor)
        return archived

    def delete_profile(self, profile_id: str, *, actor: str = "system", hard_delete: bool = False, approval_id: str | None = None) -> dict[str, Any]:
        if hard_delete and not approval_id:
            raise PermissionError("Hard delete requires explicit approval_id metadata.")

        data = self.load()
        profile = self.get_profile(profile_id)
        if hard_delete:
            data["profiles"] = [item for item in data["profiles"] if item["id"] != profile["id"]]
            self.save(data)
            self.emit_event("profile.deleted", profile, actor=actor, extra={"hardDelete": True, "approvalId": approval_id})
            return {"id": profile["id"], "status": "hard_deleted", "approvalId": approval_id}

        profile["status"] = "deleted"
        profile["deletedAt"] = utc_now()
        deleted = self.upsert_profile(profile, actor=actor)
        self.emit_event("profile.deleted", deleted, actor=actor, extra={"hardDelete": False})
        return deleted

    def approved_references(self, profile: dict[str, Any]) -> list[dict[str, Any]]:
        references = profile.get("references", [])
        return [reference for reference in references if reference.get("approvalStatus") == "approved"]

    def assert_generation_allowed(self, profile: dict[str, Any]) -> None:
        governance = profile.get("governance", {})
        if profile.get("type") == "human_subject" and not governance.get("likenessConsent"):
            raise PermissionError(f"Profile {profile['id']} is a human subject without likeness consent.")
        if governance.get("requiresApproval") and profile.get("status") != "active":
            raise PermissionError(f"Profile {profile['id']} must be active before generation.")

    def build_image_job(self, subject: str, *, scene: str, brand: str | None = None, production: str | None = None) -> dict[str, Any]:
        subject_profile = self.get_profile(subject)
        self.assert_generation_allowed(subject_profile)
        approved_references = self.approved_references(subject_profile)
        now = utc_now()
        prompt_parts = [subject_profile["description"], scene]
        if brand:
            prompt_parts.append(f"Brand context: {brand}.")
        if production:
            prompt_parts.append(f"Production profile: {production}.")

        job = {
            "schema": "lantern.contentengine.imageJob.v1",
            "jobId": f"img-{subject_profile['id']}-{now.replace(':', '').replace('-', '')}",
            "createdAt": now,
            "subjectProfileId": subject_profile["id"],
            "profileIds": [subject_profile["id"]],
            "profileVersions": {subject_profile["id"]: subject_profile["version"]},
            "referencesUsed": [reference.get("id") or reference.get("path") for reference in approved_references],
            "prompt": " ".join(prompt_parts),
            "negativePrompt": "nudity, explicit sexual pose, minor-coded styling, watermark, username, unsafe identity blending",
            "approvalStatus": "draft",
            "renderer": "manual-export",
            "dryRun": True,
        }
        self.emit_event("profile.used", subject_profile, extra={"jobId": job["jobId"]})
        return job

    def emit_event(self, event_type: str, profile: dict[str, Any], *, actor: str = "system", extra: dict[str, Any] | None = None) -> None:
        self.paths.audit_log.parent.mkdir(parents=True, exist_ok=True)
        event = {
            "eventType": event_type,
            "timestamp": utc_now(),
            "actor": actor,
            "profileId": profile.get("id"),
            "profileVersion": profile.get("version"),
        }
        if extra:
            event.update(extra)
        with self.paths.audit_log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True) + "\n")

    @classmethod
    def validate_registry(cls, data: dict[str, Any]) -> None:
        if "profiles" not in data or not isinstance(data["profiles"], list):
            raise ValueError("Registry must contain a profiles list.")
        seen: set[str] = set()
        for profile in data["profiles"]:
            cls.validate_profile(profile)
            if profile["id"] in seen:
                raise ValueError(f"Duplicate profile id: {profile['id']}")
            seen.add(profile["id"])

    @classmethod
    def validate_profile(cls, profile: dict[str, Any]) -> None:
        missing = sorted(REQUIRED_PROFILE_FIELDS - set(profile))
        if missing:
            raise ValueError(f"Profile {profile.get('id', '<unknown>')} missing fields: {', '.join(missing)}")
        if profile["type"] not in PROFILE_TYPES:
            raise ValueError(f"Unsupported profile type: {profile['type']}")
        if not isinstance(profile.get("version"), int) or profile["version"] < 1:
            raise ValueError("Profile version must be a positive integer.")
        governance = profile.get("governance", {})
        if not isinstance(governance, dict):
            raise ValueError("Profile governance must be an object.")
        for reference in profile.get("references", []):
            reference_type = reference.get("type")
            if reference_type not in REFERENCE_TYPES:
                raise ValueError(f"Unsupported reference type: {reference_type}")


def summarize_profiles(profiles: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "id": profile["id"],
            "name": profile["name"],
            "type": profile["type"],
            "status": profile["status"],
            "version": profile["version"],
            "tags": profile.get("tags", []),
        }
        for profile in profiles
    ]
