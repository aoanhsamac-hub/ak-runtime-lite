from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class AuditEvent:
    event_id: str = ""
    timestamp: str = ""
    agent: str = ""
    action: str = ""
    record_type: str = ""
    record_id: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    status: str = "recorded"

    def __post_init__(self):
        if not self.event_id:
            from uuid import uuid4
            object.__setattr__(self, "event_id", f"AUDIT-{uuid4().hex[:12].upper()}")
        if not self.timestamp:
            object.__setattr__(self, "timestamp", datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "agent": self.agent,
            "action": self.action,
            "record_type": self.record_type,
            "record_id": self.record_id,
            "details": self.details,
            "status": self.status,
        }


AUDIT_ACTIONS = {
    "SIGNAL_EXTRACTED",
    "INSIGHT_CREATED",
    "SKILL_CANDIDATE_CREATED",
    "GOVERNANCE_CHECK",
    "GOVERNANCE_PASS",
    "GOVERNANCE_FAIL",
    "PIPELINE_RUN",
    "DRY_RUN",
    "CLUSTER_CREATED",
    "INSIGHT_DISCOVERED",
    "SKILL_DISCOVERED",
    "DUPLICATE_DETECTED",
    "MERGE_SUGGESTED",
    "DISCOVERY_PIPELINE_RUN",
    "FAMILY_CREATED",
    "CANONICAL_CLASSIFIED",
    "GRAPH_EDGE_CREATED",
    "MATURITY_ASSESSED",
    "CONSOLIDATION_RECOMMENDED",
    "PROMOTION_READINESS_ASSESSED",
    "CANONICALIZATION_PIPELINE_RUN",
    "PROMOTION_RECOMMENDED",
    "PROMOTION_REVIEWED",
    "SKILL_APPROVED",
    "SKILL_REJECTED",
    "SKILL_NEEDS_REVIEW",
    "SKILL_NEEDS_EVIDENCE",
    "SKILL_ARCHIVED",
    "SKILL_PROMOTION_DECISION",
    "PROMOTION_PIPELINE_RUN",
    "CAPABILITY_DISCOVERED",
    "CAPABILITY_FAMILY_CREATED",
    "CAPABILITY_CANONICAL_CLASSIFIED",
    "CAPABILITY_GRAPH_EDGE_CREATED",
    "CAPABILITY_MATURITY_ASSESSED",
    "CAPABILITY_READINESS_ASSESSED",
    "CAPABILITY_PROMOTION_RECOMMENDED",
    "CAPABILITY_PIPELINE_RUN",
    "SCENARIO_CREATED",
    "VALIDATION_RUN",
    "EVIDENCE_RECORDED",
    "MATURITY_REASSESSED",
    "READINESS_REASSESSED",
    "HERMES_REVIEW_COMPLETED",
    "SAGE_REVIEW_COMPLETED",
    "DECISION_PACKAGE_CREATED",
    "OFFICIAL_CAPABILITY_RECORD_PREPARED",
}


class LearningAuditLayer:
    """Records audit events for learning intelligence operations."""

    def __init__(self):
        self._events: list[AuditEvent] = []

    def record(self, agent: str, action: str, record_type: str,
               record_id: str = "", details: dict[str, Any] | None = None) -> AuditEvent:
        if action not in AUDIT_ACTIONS:
            raise ValueError(f"Unknown audit action: {action}. Allowed: {sorted(AUDIT_ACTIONS)}")
        event = AuditEvent(
            agent=agent,
            action=action,
            record_type=record_type,
            record_id=record_id,
            details=details or {},
        )
        self._events.append(event)
        return event

    def list_events(self, limit: int = 0, offset: int = 0,
                    agent: str | None = None,
                    action: str | None = None,
                    record_type: str | None = None) -> list[AuditEvent]:
        events = list(self._events)
        if agent:
            events = [e for e in events if e.agent == agent]
        if action:
            events = [e for e in events if e.action == action]
        if record_type:
            events = [e for e in events if e.record_type == record_type]
        if limit > 0:
            events = events[offset:offset + limit]
        elif offset > 0:
            events = events[offset:]
        return events

    def get_trail(self, record_id: str) -> list[AuditEvent]:
        return [e for e in self._events if e.record_id == record_id]

    def export(self) -> list[dict[str, Any]]:
        return [e.to_dict() for e in self._events]

    def clear(self) -> None:
        self._events.clear()
