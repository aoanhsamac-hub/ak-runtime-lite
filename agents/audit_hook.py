from __future__ import annotations

from pathlib import Path

from governance.audit_engine import append_audit_record


def append_agent_audit(event_type: str, agent: str, task_id: str, issue_id: str, action: str, result: str, log_path: str | Path | None = None) -> dict:
    return append_audit_record(
        actor=agent,
        action=f"{event_type}:{action}",
        target=task_id,
        result=result,
        issue_id=issue_id,
        log_path=log_path,
    )
