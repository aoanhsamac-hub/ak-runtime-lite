import json
import uuid
from pathlib import Path

from governance.models.audit_record import AuditRecord


DEFAULT_AUDIT_LOG = Path(__file__).resolve().parent / "audit" / "audit_log.jsonl"


def append_audit_record(actor: str, action: str, target: str, result: str, issue_id: str = "", log_path: str | Path | None = None) -> dict:
    path = Path(log_path) if log_path else DEFAULT_AUDIT_LOG
    path.parent.mkdir(parents=True, exist_ok=True)
    record = AuditRecord.create(
        event_id=f"AUDIT-{uuid.uuid4().hex[:12].upper()}",
        actor=actor,
        action=action,
        target=target,
        result=result,
        issue_id=issue_id,
    )
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
    return record.to_dict()
