import json

import pytest

from services.emas.audit import AppendOnlyAuditLogger, AuditEvent, AuditIntegrityError


def test_append_creates_hash_chain(tmp_path):
    log_path = tmp_path / "audit-log.jsonl"
    logger = AppendOnlyAuditLogger(log_path)

    first = logger.append(AuditEvent(actor="tester", action="one", result="success"))
    second = logger.append(AuditEvent(actor="tester", action="two", result="success"))

    assert first.previous_hash is None
    assert second.previous_hash == first.event_hash
    assert logger.verify() is True


def test_tampered_event_fails_verification(tmp_path):
    log_path = tmp_path / "audit-log.jsonl"
    logger = AppendOnlyAuditLogger(log_path)
    logger.append(AuditEvent(actor="tester", action="one", result="success"))

    line = log_path.read_text(encoding="utf-8").splitlines()[0]
    event = json.loads(line)
    event["action"] = "tampered"
    log_path.write_text(json.dumps(event) + "\n", encoding="utf-8")

    with pytest.raises(AuditIntegrityError):
        logger.verify()
