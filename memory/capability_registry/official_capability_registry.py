from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from memory.schemas.records import make_id, utc_now


OFFICIAL_CAPABILITY_STATUSES = {
    "APPROVED_AS_OFFICIAL", "HOLD_FOR_EVIDENCE", "HOLD_FOR_REVIEW",
    "REJECTED", "ARCHIVE_ONLY",
}
ACTIVATION_STATUSES = {"DISABLED", "ENABLED"}
AGENT_ADOPTION_STATUSES = {"NOT_ASSIGNED", "ASSIGNED"}
ADOPTION_STAGES = {"PROPOSED", "ASSIGNED_SANDBOX", "IN_USE_SANDBOX", "REVIEW_REQUIRED", "SUSPENDED", "RETIRED"}
EVOLUTION_STATUSES = {"LOCKED", "UNLOCKED", "EVOLVING_MATURITY", "EVOLVING_CYCLE", "EVOLVED", "ROLLED_BACK"}


@dataclass(frozen=True)
class OfficialCapabilityRecord:
    official_capability_id: str = field(default_factory=lambda: make_id("OCAP"))
    canonical_capability_id: str = ""
    name: str = ""
    description: str = ""
    domain: str = ""
    source_capability_ids: list[str] = field(default_factory=list)
    hermes_recommendation: str = ""
    hermes_reviewer: str = ""
    sage_recommendation: str = ""
    sage_reviewer: str = ""
    hung_vuong_decision: str = ""
    status: str = "HOLD_FOR_REVIEW"
    activation_status: str = "DISABLED"
    agent_adoption_status: str = "NOT_ASSIGNED"
    adoption_stage: str = "PROPOSED"
    evolution_status: str = "LOCKED"
    evidence_summary: str = ""
    risk_summary: str = ""
    promotion_recommendation: str = ""
    future_activation_conditions: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    owner_agent: str = "Sage"
    reviewer_agent: str = "Hung Vuong"
    evolution_cycle: int = 0
    evolution_history: list[dict] = field(default_factory=list)
    last_evolved_at: str = ""
    evolution_trace_ids: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.name:
            raise ValueError("name is required")
        if not self.description:
            raise ValueError("description is required")
        if self.status not in OFFICIAL_CAPABILITY_STATUSES:
            raise ValueError(f"invalid status: {self.status}")
        if self.activation_status not in ACTIVATION_STATUSES:
            raise ValueError(f"invalid activation_status: {self.activation_status}")
        if self.agent_adoption_status not in AGENT_ADOPTION_STATUSES:
            raise ValueError(f"invalid agent_adoption_status: {self.agent_adoption_status}")
        if self.adoption_stage not in ADOPTION_STAGES:
            raise ValueError(f"invalid adoption_stage: {self.adoption_stage}")
        if self.evolution_status not in EVOLUTION_STATUSES:
            raise ValueError(f"invalid evolution_status: {self.evolution_status}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def with_activation(self, activation_status: str = "DISABLED",
                        agent_adoption_status: str = "NOT_ASSIGNED",
                        adoption_stage: str = "PROPOSED",
                        evolution_status: str = "LOCKED") -> OfficialCapabilityRecord:
        return OfficialCapabilityRecord(
            official_capability_id=self.official_capability_id,
            canonical_capability_id=self.canonical_capability_id,
            name=self.name,
            description=self.description,
            domain=self.domain,
            source_capability_ids=list(self.source_capability_ids),
            hermes_recommendation=self.hermes_recommendation,
            hermes_reviewer=self.hermes_reviewer,
            sage_recommendation=self.sage_recommendation,
            sage_reviewer=self.sage_reviewer,
            hung_vuong_decision=self.hung_vuong_decision,
            status=self.status,
            activation_status=activation_status,
            agent_adoption_status=agent_adoption_status,
            adoption_stage=adoption_stage,
            evolution_status=evolution_status,
            evidence_summary=self.evidence_summary,
            risk_summary=self.risk_summary,
            promotion_recommendation=self.promotion_recommendation,
            future_activation_conditions=list(self.future_activation_conditions),
            created_at=self.created_at,
            owner_agent=self.owner_agent,
            reviewer_agent=self.reviewer_agent,
            evolution_cycle=self.evolution_cycle,
            evolution_history=list(self.evolution_history),
            last_evolved_at=self.last_evolved_at,
            evolution_trace_ids=list(self.evolution_trace_ids),
        )

    def with_evolution(self, evolution_status: str = "LOCKED",
                       evolution_cycle: int = 0) -> OfficialCapabilityRecord:
        return OfficialCapabilityRecord(
            official_capability_id=self.official_capability_id,
            canonical_capability_id=self.canonical_capability_id,
            name=self.name,
            description=self.description,
            domain=self.domain,
            source_capability_ids=list(self.source_capability_ids),
            hermes_recommendation=self.hermes_recommendation,
            hermes_reviewer=self.hermes_reviewer,
            sage_recommendation=self.sage_recommendation,
            sage_reviewer=self.sage_reviewer,
            hung_vuong_decision=self.hung_vuong_decision,
            status=self.status,
            activation_status=self.activation_status,
            agent_adoption_status=self.agent_adoption_status,
            adoption_stage=self.adoption_stage,
            evolution_status=evolution_status,
            evidence_summary=self.evidence_summary,
            risk_summary=self.risk_summary,
            promotion_recommendation=self.promotion_recommendation,
            future_activation_conditions=list(self.future_activation_conditions),
            created_at=self.created_at,
            owner_agent=self.owner_agent,
            reviewer_agent=self.reviewer_agent,
            evolution_cycle=evolution_cycle if evolution_cycle else self.evolution_cycle,
            evolution_history=list(self.evolution_history),
            last_evolved_at=self.last_evolved_at,
            evolution_trace_ids=list(self.evolution_trace_ids),
        )


class OfficialCapabilityRegistry:
    table_name = "official_capabilities"

    def __init__(self, adapter=None):
        self.adapter = adapter
        self._records: dict[str, OfficialCapabilityRecord] = {}

    def create(self, **payload) -> OfficialCapabilityRecord:
        record = OfficialCapabilityRecord(**payload)
        self._validate_no_activation(record)
        self._records[record.official_capability_id] = record
        if self.adapter:
            self.adapter.insert(self.table_name, [record.to_dict()])
        return record

    def get(self, official_capability_id: str) -> OfficialCapabilityRecord:
        try:
            return self._records[official_capability_id]
        except KeyError as exc:
            raise KeyError(f"official capability not found: {official_capability_id}") from exc

    def list_all(self, status: str | None = None) -> list[OfficialCapabilityRecord]:
        records = list(self._records.values())
        if status:
            records = [r for r in records if r.status == status]
        return records

    def list_approved(self) -> list[OfficialCapabilityRecord]:
        return [r for r in self._records.values() if r.status == "APPROVED_AS_OFFICIAL"]

    def list_by_adoption_stage(self, stage: str) -> list[OfficialCapabilityRecord]:
        if stage not in ADOPTION_STAGES:
            raise ValueError(f"invalid adoption_stage: {stage}")
        return [r for r in self._records.values() if r.adoption_stage == stage]

    def update_adoption_stage(self, official_capability_id: str, new_stage: str) -> OfficialCapabilityRecord:
        if new_stage not in ADOPTION_STAGES:
            raise ValueError(f"invalid adoption_stage: {new_stage}")
        record = self.get(official_capability_id)
        updated = OfficialCapabilityRecord(
            official_capability_id=record.official_capability_id,
            canonical_capability_id=record.canonical_capability_id,
            name=record.name,
            description=record.description,
            domain=record.domain,
            source_capability_ids=list(record.source_capability_ids),
            hermes_recommendation=record.hermes_recommendation,
            hermes_reviewer=record.hermes_reviewer,
            sage_recommendation=record.sage_recommendation,
            sage_reviewer=record.sage_reviewer,
            hung_vuong_decision=record.hung_vuong_decision,
            status=record.status,
            activation_status=record.activation_status,
            agent_adoption_status=record.agent_adoption_status,
            adoption_stage=new_stage,
            evolution_status=record.evolution_status,
            evidence_summary=record.evidence_summary,
            risk_summary=record.risk_summary,
            promotion_recommendation=record.promotion_recommendation,
            future_activation_conditions=list(record.future_activation_conditions),
            created_at=record.created_at,
            owner_agent=record.owner_agent,
            reviewer_agent=record.reviewer_agent,
            evolution_cycle=record.evolution_cycle,
            evolution_history=list(record.evolution_history),
            last_evolved_at=record.last_evolved_at,
            evolution_trace_ids=list(record.evolution_trace_ids),
        )
        self._records[official_capability_id] = updated
        return updated

    @staticmethod
    def _validate_no_activation(record: OfficialCapabilityRecord) -> None:
        if record.activation_status not in ("DISABLED",):
            raise ValueError(f"activation_status must be DISABLED, got {record.activation_status}")
        if record.agent_adoption_status not in ("NOT_ASSIGNED",):
            raise ValueError(f"agent_adoption_status must be NOT_ASSIGNED, got {record.agent_adoption_status}")
        if record.adoption_stage not in ("PROPOSED",):
            raise ValueError(f"adoption_stage must be PROPOSED, got {record.adoption_stage}")
        if record.evolution_status not in ("LOCKED",):
            raise ValueError(f"evolution_status must be LOCKED, got {record.evolution_status}")
