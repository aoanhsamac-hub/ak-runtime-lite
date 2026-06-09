from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from memory.schemas.records import make_id, utc_now


EVIDENCE_TYPES = {
    "VALIDATION_RESULT", "DOCUMENTATION", "DRY_RUN_OUTPUT",
    "SIMULATION_RESULT", "BACKTEST_RESULT", "GOVERNANCE_AUDIT",
    "MEMORY_QUERY", "CODE_TEST", "REGISTRY_REVIEW",
}


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str = field(default_factory=lambda: make_id("EVID"))
    capability_id: str = ""
    scenario_id: str = ""
    evidence_type: str = ""
    result: str = ""
    metric: float = 0.0
    source_artifacts: list[str] = field(default_factory=list)
    source_hashes: list[str] = field(default_factory=list)
    confidence: float = 0.0
    risk_observation: str = ""
    created_at: str = field(default_factory=utc_now)
    reviewer_agent: str = ""
    audit_trace_id: str = ""

    def __post_init__(self):
        if not self.evidence_type:
            raise ValueError("evidence_type is required")
        if self.evidence_type not in EVIDENCE_TYPES:
            raise ValueError(f"invalid evidence_type: {self.evidence_type}")
        if not self.capability_id:
            raise ValueError("capability_id is required")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class CapabilityEvidenceRegistry:
    table_name = "capability_evidence"

    def __init__(self, adapter=None):
        self.adapter = adapter
        self._records: dict[str, EvidenceRecord] = {}

    def create(self, **payload) -> EvidenceRecord:
        record = EvidenceRecord(**payload)
        self._records[record.evidence_id] = record
        if self.adapter:
            self.adapter.insert(self.table_name, [record.to_dict()])
        return record

    def get(self, evidence_id: str) -> EvidenceRecord:
        try:
            return self._records[evidence_id]
        except KeyError as exc:
            raise KeyError(f"evidence not found: {evidence_id}") from exc

    def list_all(self, capability_id: str | None = None) -> list[EvidenceRecord]:
        records = list(self._records.values())
        if capability_id:
            records = [r for r in records if r.capability_id == capability_id]
        return records

    def get_evidence_for_capability(self, capability_id: str) -> list[EvidenceRecord]:
        return [r for r in self._records.values() if r.capability_id == capability_id]
