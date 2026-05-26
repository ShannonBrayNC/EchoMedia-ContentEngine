#!/usr/bin/env python3
"""Provider webhook and event normalization helpers.

This module is intentionally standard-library only so provider callback handling can
be tested in CI without live credentials or framework dependencies. A future
FastAPI/Azure Functions host can call these functions from its HTTP route layer.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_ROOT = Path(os.environ.get("CONTENT_ENGINE_STATE_ROOT", ROOT / ".content-engine" / "state"))
EVENT_FILE = STATE_ROOT / "provider-events.json"
MAX_PAYLOAD_BYTES = int(os.environ.get("CONTENT_ENGINE_WEBHOOK_MAX_BYTES", "1048576"))

REDACTED_HEADER_NAMES = {
    "authorization",
    "x-api-key",
    "api-key",
    "cookie",
    "set-cookie",
    "x-elevenlabs-signature",
    "x-webhook-signature",
}

REDACTED_PAYLOAD_KEYS = {
    "api_key",
    "apiKey",
    "authorization",
    "token",
    "secret",
    "signature",
}


def _now_ms() -> int:
    return int(time.time() * 1000)


def _load_events() -> dict[str, Any]:
    if not EVENT_FILE.exists():
        return {"events": {}, "deliveries": {}}
    return json.loads(EVENT_FILE.read_text(encoding="utf-8"))


def _save_events(state: dict[str, Any]) -> None:
    STATE_ROOT.mkdir(parents=True, exist_ok=True)
    EVENT_FILE.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def reset_provider_events() -> None:
    """Delete persisted provider events for deterministic tests."""
    if EVENT_FILE.exists():
        EVENT_FILE.unlink()


def list_provider_events(provider: str | None = None) -> dict[str, Any]:
    state = _load_events()
    events = list(state["events"].values())
    if provider:
        events = [event for event in events if event.get("provider") == provider]
    events.sort(key=lambda event: event.get("receivedAtMs", 0))
    return {"events": events, "count": len(events)}


def _redact_headers(headers: dict[str, str] | None) -> dict[str, str]:
    safe: dict[str, str] = {}
    for key, value in (headers or {}).items():
        safe[key] = "[redacted]" if key.lower() in REDACTED_HEADER_NAMES else str(value)
    return safe


def _redact_payload(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: ("[redacted]" if key in REDACTED_PAYLOAD_KEYS else _redact_payload(item)) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact_payload(item) for item in value]
    return value


def _stable_payload_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _delivery_key(provider: str, payload: dict[str, Any], headers: dict[str, str] | None) -> str:
    provider_event_id = str(payload.get("event_id") or payload.get("eventId") or payload.get("id") or "").strip()
    delivery_id = ""
    for key, value in (headers or {}).items():
        if key.lower() in {"x-elevenlabs-event-id", "x-elevenlabs-delivery-id", "x-provider-delivery-id", "x-request-id"}:
            delivery_id = str(value).strip()
            break
    if provider_event_id:
        return f"{provider}:{provider_event_id}"
    if delivery_id:
        return f"{provider}:delivery:{delivery_id}"
    return f"{provider}:sha256:{_stable_payload_hash(payload)}"


def _verify_shared_secret(headers: dict[str, str] | None, payload: dict[str, Any]) -> tuple[bool, str]:
    """Verify optional HMAC fallback when CONTENT_ENGINE_WEBHOOK_SECRET is set.

    The expected signature header is `X-Content-Engine-Signature` with a hex HMAC
    over the canonical JSON payload. This is a project-owned fallback for local
    tunnels or providers without native signatures.
    """
    secret = os.environ.get("CONTENT_ENGINE_WEBHOOK_SECRET")
    if not secret:
        return True, "not-configured"
    supplied = ""
    for key, value in (headers or {}).items():
        if key.lower() == "x-content-engine-signature":
            supplied = str(value)
            break
    if not supplied:
        return False, "missing-signature"
    expected = hmac.new(secret.encode("utf-8"), json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8"), hashlib.sha256).hexdigest()
    return hmac.compare_digest(supplied, expected), "valid" if hmac.compare_digest(supplied, expected) else "invalid-signature"


def _extract_event_type(payload: dict[str, Any]) -> str:
    return str(payload.get("type") or payload.get("event_type") or payload.get("eventType") or payload.get("event") or "unknown")


def _extract_correlation(payload: dict[str, Any]) -> dict[str, Any]:
    metadata = payload.get("webhook_metadata") or payload.get("webhookMetadata") or payload.get("metadata") or {}
    if not isinstance(metadata, dict):
        metadata = {}
    correlation = {
        "projectId": metadata.get("projectId") or metadata.get("project_id") or payload.get("projectId") or payload.get("project_id"),
        "jobId": metadata.get("jobId") or metadata.get("job_id") or payload.get("jobId") or payload.get("job_id"),
        "artifactId": metadata.get("artifactId") or metadata.get("artifact_id") or payload.get("artifactId") or payload.get("artifact_id"),
        "chapterId": metadata.get("chapterId") or metadata.get("chapter_id"),
        "sceneId": metadata.get("sceneId") or metadata.get("scene_id"),
        "audioAssetId": metadata.get("audioAssetId") or metadata.get("audio_asset_id"),
    }
    return {key: value for key, value in correlation.items() if value}


def normalize_elevenlabs_event(payload: dict[str, Any], headers: dict[str, str] | None = None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise TypeError("payload must be a JSON object")
    raw_size = len(json.dumps(payload, sort_keys=True).encode("utf-8"))
    if raw_size > MAX_PAYLOAD_BYTES:
        raise ValueError("payload exceeds configured webhook size limit")
    event_type = _extract_event_type(payload)
    correlation = _extract_correlation(payload)
    delivery_key = _delivery_key("elevenlabs", payload, headers)
    event_id = hashlib.sha256(delivery_key.encode("utf-8")).hexdigest()[:24]
    warnings = []
    if not correlation:
        warnings.append("missing-correlation-metadata")
    if event_type == "unknown":
        warnings.append("unknown-event-type")
    return {
        "eventId": f"evt-{event_id}",
        "provider": "elevenlabs",
        "providerEventType": event_type,
        "deliveryKey": delivery_key,
        "receivedAtMs": _now_ms(),
        "status": "received",
        "correlation": correlation,
        "warnings": warnings,
        "safeHeaders": _redact_headers(headers),
        "safePayload": _redact_payload(payload),
        "rawPayloadHash": _stable_payload_hash(payload),
    }


def handle_elevenlabs_webhook(payload: dict[str, Any], headers: dict[str, str] | None = None) -> dict[str, Any]:
    """Validate, normalize, and persist an ElevenLabs webhook event idempotently."""
    verified, verification_status = _verify_shared_secret(headers, payload)
    if not verified:
        return {
            "ok": False,
            "statusCode": 401,
            "error": {"code": "unauthorized_webhook", "message": "Webhook signature verification failed.", "verificationStatus": verification_status},
        }

    try:
        normalized = normalize_elevenlabs_event(payload, headers)
    except (TypeError, ValueError) as exc:
        return {"ok": False, "statusCode": 400, "error": {"code": "invalid_webhook_payload", "message": str(exc)}}

    state = _load_events()
    delivery_key = normalized["deliveryKey"]
    if delivery_key in state["deliveries"]:
        existing_id = state["deliveries"][delivery_key]
        existing = state["events"][existing_id]
        existing["duplicateDeliveries"] = int(existing.get("duplicateDeliveries", 0)) + 1
        existing["lastDuplicateAtMs"] = _now_ms()
        _save_events(state)
        return {"ok": True, "statusCode": 200, "duplicate": True, "event": existing}

    state["events"][normalized["eventId"]] = normalized
    state["deliveries"][delivery_key] = normalized["eventId"]
    _save_events(state)
    return {"ok": True, "statusCode": 202, "duplicate": False, "event": normalized}


def route_provider_event(method: str, path: str, payload: dict[str, Any], headers: dict[str, str] | None = None) -> dict[str, Any]:
    """Tiny route helper for framework adapters.

    Supported path: POST /api/webhooks/elevenlabs
    """
    clean_path = path.rstrip("/")
    if method.upper() == "POST" and clean_path == "/api/webhooks/elevenlabs":
        return handle_elevenlabs_webhook(payload, headers)
    return {"ok": False, "statusCode": 404, "error": {"code": "not_found", "message": f"No provider-event route for {method} {path}"}}
