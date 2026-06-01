"""Append-only audit logging for EchoMedia Ad Studio.

This module closes EMAS-008 for the production RC lane.
It writes JSONL events with a hash chain so tampering is detectable.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable
from uuid import uuid4


AuditResult = str


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: dict[str, Any]) -> str:
    """Return stable JSON for hashing."""

    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def hash_event(value: dict[str, Any]) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class AuditEvent:
    actor: str
    action: str
    result: AuditResult
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=_utc_now)
    project_name: str | None = None
    ad_name: str | None = None
    target_type: str | None = None
    target_id: str | None = None
    reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    previous_hash: str | None = None
    event_hash: str | None = None

    def to_hash_payload(self) -> dict[str, Any]:
        payload = self.to_dict()
        payload.pop("event_hash", None)
        return payload

    def to_dict(self) -> dict[str, Any]:
        return {
            "eventId": self.event_id,
            "timestamp": self.timestamp,
            "actor": self.actor,
            "action": self.action,
            "projectName": self.project_name,
            "adName": self.ad_name,
            "targetType": self.target_type,
            "targetId": self.target_id,
            "result": self.result,
            "reason": self.reason,
            "metadata": self.metadata,
            "previousHash": self.previous_hash,
            "eventHash": self.event_hash,
        }

    @staticmethod
    def from_dict(value: dict[str, Any]) -> "AuditEvent":
        return AuditEvent(
            event_id=value["eventId"],
            timestamp=value["timestamp"],
            actor=value["actor"],
            action=value["action"],
            project_name=value.get("projectName"),
            ad_name=value.get("adName"),
            target_type=value.get("targetType"),
            target_id=value.get("targetId"),
            result=value["result"],
            reason=value.get("reason"),
            metadata=value.get("metadata") or {},
            previous_hash=value.get("previousHash"),
            event_hash=value.get("eventHash"),
        )


class AuditIntegrityError(RuntimeError):
    """Raised when an audit log cannot be trusted."""


class AppendOnlyAuditLogger:
    """Append-only JSONL audit logger with hash chaining."""

    def __init__(self, log_path: str | Path):
        self.log_path = Path(log_path)
        self._ensure_safe_path(self.log_path)

    def append(self, event: AuditEvent) -> AuditEvent:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        previous_hash = self.get_last_hash()
        event_with_previous = AuditEvent(
            event_id=event.event_id,
            timestamp=event.timestamp or _utc_now(),
            actor=event.actor,
            action=event.action,
            project_name=event.project_name,
            ad_name=event.ad_name,
            target_type=event.target_type,
            target_id=event.target_id,
            result=event.result,
            reason=event.reason,
            metadata=event.metadata,
            previous_hash=previous_hash,
            event_hash=None,
        )
        final_event = AuditEvent(
            **{
                **event_with_previous.__dict__,
                "event_hash": hash_event(event_with_previous.to_hash_payload()),
            }
        )

        # Open in append-only mode. The app never rewrites prior events.
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(final_event.to_dict(), sort_keys=True, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())

        return final_event

    def iter_events(self) -> Iterable[AuditEvent]:
        if not self.log_path.exists():
            return []
        events: list[AuditEvent] = []
        with self.log_path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    events.append(AuditEvent.from_dict(json.loads(stripped)))
                except Exception as exc:  # pragma: no cover - details included in raised message
                    raise AuditIntegrityError(f"Invalid audit JSON at line {line_number}: {exc}") from exc
        return events

    def get_last_hash(self) -> str | None:
        events = list(self.iter_events())
        if not events:
            return None
        return events[-1].event_hash

    def verify(self) -> bool:
        previous_hash: str | None = None
        for index, event in enumerate(self.iter_events()):
            if event.previous_hash != previous_hash:
                raise AuditIntegrityError(
                    f"Audit hash chain break at event {index + 1}: expected previousHash {previous_hash}, got {event.previous_hash}"
                )
            if not event.event_hash:
                raise AuditIntegrityError(f"Audit event {index + 1} is missing eventHash")
            expected_hash = hash_event(event.to_hash_payload())
            if event.event_hash != expected_hash:
                raise AuditIntegrityError(
                    f"Audit event {index + 1} hash mismatch: expected {expected_hash}, got {event.event_hash}"
                )
            previous_hash = event.event_hash
        return True

    @staticmethod
    def _ensure_safe_path(path: Path) -> None:
        if any(part == ".." for part in path.parts):
            raise ValueError(f"Path traversal is not allowed for audit logs: {path}")
