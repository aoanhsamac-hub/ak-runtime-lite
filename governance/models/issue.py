from dataclasses import dataclass, field
from datetime import datetime, timezone


ISSUE_STATUSES = (
    "Draft",
    "Submitted",
    "Reviewed",
    "Approved",
    "Implemented",
    "Verified",
    "Closed",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class Issue:
    issue_id: str
    title: str
    description: str
    status: str
    risk_level: str
    proposer: str
    reviewers: list[str] = field(default_factory=list)
    approvers: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict:
        return {
            "issue_id": self.issue_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "risk_level": self.risk_level,
            "proposer": self.proposer,
            "reviewers": list(self.reviewers),
            "approvers": list(self.approvers),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
