from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


class TaskStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    ROUTED = "ROUTED"
    ACCEPTED = "ACCEPTED"
    BLOCKED = "BLOCKED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class TaskEnvelope:
    title: str
    objective: str
    requester: str
    target_agent: str
    risk_level: str = "LEVEL_0_LOW"
    task_id: str = field(default_factory=lambda: f"TASK-{uuid4().hex[:12].upper()}")
    issue_id: str = ""
    status: str = TaskStatus.DRAFT.value
    input_refs: list[str] = field(default_factory=list)
    allowed_tools: list[str] = field(default_factory=list)
    forbidden_tools: list[str] = field(default_factory=list)
    required_approvals: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    deadline: str = ""
    metadata: dict = field(default_factory=dict)

    def validate(self) -> dict:
        missing = []
        if not self.task_id:
            missing.append("task_id")
        if self.risk_level != "LEVEL_0_LOW" and not self.issue_id:
            missing.append("issue_id")
        return {"valid": not missing, "missing": missing}

    def to_dict(self) -> dict:
        return dict(self.__dict__)
