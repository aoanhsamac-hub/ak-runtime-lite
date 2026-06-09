from dataclasses import dataclass
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class AuditRecord:
    event_id: str
    timestamp: str
    actor: str
    action: str
    target: str
    result: str
    issue_id: str = ""

    @classmethod
    def create(cls, event_id: str, actor: str, action: str, target: str, result: str, issue_id: str = ""):
        return cls(event_id=event_id, timestamp=utc_now(), actor=actor, action=action, target=target, result=result, issue_id=issue_id)

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "actor": self.actor,
            "action": self.action,
            "target": self.target,
            "result": self.result,
            "issue_id": self.issue_id,
        }
