from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


class ReportStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    FINAL = "FINAL"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class ReportEnvelope:
    task_id: str
    issue_id: str
    agent: str
    status: str
    summary: str
    report_id: str = field(default_factory=lambda: f"REPORT-{uuid4().hex[:12].upper()}")
    actions_taken: list[str] = field(default_factory=list)
    files_created: list[str] = field(default_factory=list)
    files_modified: list[str] = field(default_factory=list)
    files_blocked: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    test_results: list[str] = field(default_factory=list)
    memory_records_created: list[str] = field(default_factory=list)
    approval_needed: list[str] = field(default_factory=list)
    review_needed: list[str] = field(default_factory=list)
    recommendation: str = ""
    created_at: str = field(default_factory=utc_now)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return dict(self.__dict__)
