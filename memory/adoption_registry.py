from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from memory.schemas.records import make_id, utc_now


ADOPTION_LIFECYCLE_STAGES = {
    "PROPOSED", "ASSIGNED_SANDBOX", "IN_USE_SANDBOX",
    "REVIEW_REQUIRED", "SUSPENDED", "RETIRED",
}

ADOPTION_TRANSITIONS: dict[str, set[str]] = {
    "PROPOSED": {"ASSIGNED_SANDBOX", "SUSPENDED", "RETIRED"},
    "ASSIGNED_SANDBOX": {"IN_USE_SANDBOX", "SUSPENDED", "RETIRED"},
    "IN_USE_SANDBOX": {"REVIEW_REQUIRED", "SUSPENDED", "RETIRED"},
    "REVIEW_REQUIRED": {"ASSIGNED_SANDBOX", "IN_USE_SANDBOX", "SUSPENDED", "RETIRED"},
    "SUSPENDED": {"ASSIGNED_SANDBOX", "RETIRED"},
    "RETIRED": set(),
}

RISK_LEVELS = {"LEVEL_0_LOW", "LEVEL_1_MODERATE", "LEVEL_2_HIGH", "LEVEL_3_CRITICAL", "LEVEL_4_CONSTITUTIONAL"}


@dataclass(frozen=True)
class AdoptionRecord:
    adoption_id: str = field(default_factory=lambda: make_id("ADOPT"))
    official_capability_id: str = ""
    owner: str = ""
    assigned_agent: str = ""
    allowed_scope: str = "sandbox"
    risk_level: str = "LEVEL_1_MODERATE"
    lifecycle_stage: str = "PROPOSED"
    validation_refs: list[str] = field(default_factory=list)
    rollback_condition: str = ""
    roi_metric: str = ""
    assigned_at: str = ""
    evidence_ids: list[str] = field(default_factory=list)
    failure_count: int = 0
    total_value: float = 0.0
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def __post_init__(self):
        if not self.official_capability_id:
            raise ValueError("official_capability_id is required")
        if not self.assigned_agent:
            raise ValueError("assigned_agent is required")
        if self.lifecycle_stage not in ADOPTION_LIFECYCLE_STAGES:
            raise ValueError(f"invalid lifecycle_stage: {self.lifecycle_stage}")
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(f"invalid risk_level: {self.risk_level}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def with_stage(self, stage: str, **extra: Any) -> AdoptionRecord:
        return AdoptionRecord(
            adoption_id=self.adoption_id,
            official_capability_id=self.official_capability_id,
            owner=extra.get("owner", self.owner),
            assigned_agent=extra.get("assigned_agent", self.assigned_agent),
            allowed_scope=extra.get("allowed_scope", self.allowed_scope),
            risk_level=extra.get("risk_level", self.risk_level),
            lifecycle_stage=stage,
            validation_refs=list(extra.get("validation_refs", self.validation_refs)),
            rollback_condition=extra.get("rollback_condition", self.rollback_condition),
            roi_metric=extra.get("roi_metric", self.roi_metric),
            assigned_at=extra.get("assigned_at", self.assigned_at),
            evidence_ids=list(extra.get("evidence_ids", self.evidence_ids)),
            failure_count=extra.get("failure_count", self.failure_count),
            total_value=extra.get("total_value", self.total_value),
            created_at=self.created_at,
            updated_at=utc_now(),
        )


class CapabilityAdoptionRegistry:
    table_name = "ak_capability_adoptions"

    def __init__(self, adapter=None):
        self.adapter = adapter
        self._records: dict[str, AdoptionRecord] = {}

    def create(self, **payload) -> AdoptionRecord:
        record = AdoptionRecord(**payload)
        self._records[record.adoption_id] = record
        if self.adapter:
            self.adapter.insert(self.table_name, [record.to_dict()])
        return record

    def get(self, adoption_id: str) -> AdoptionRecord:
        try:
            return self._records[adoption_id]
        except KeyError as exc:
            raise KeyError(f"adoption not found: {adoption_id}") from exc

    def list_all(self, lifecycle_stage: str | None = None) -> list[AdoptionRecord]:
        records = list(self._records.values())
        if lifecycle_stage:
            records = [r for r in records if r.lifecycle_stage == lifecycle_stage]
        return records

    def list_by_agent(self, agent_id: str) -> list[AdoptionRecord]:
        return [r for r in self._records.values() if r.assigned_agent == agent_id]

    def list_by_capability(self, official_capability_id: str) -> list[AdoptionRecord]:
        return [r for r in self._records.values() if r.official_capability_id == official_capability_id]

    def update_stage(self, adoption_id: str, new_stage: str, **extra: Any) -> AdoptionRecord:
        record = self.get(adoption_id)
        updated = record.with_stage(new_stage, **extra)
        self._records[adoption_id] = updated
        return updated
