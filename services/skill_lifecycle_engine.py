from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from memory.lancedb_adapter import LanceDBAdapter
from memory.schemas.records import SKILL_LIFECYCLE_STAGES, make_id, utc_now


LIFECYCLE_TRANSITIONS = {
    "PROPOSED": {"DISCOVERED"},
    "DISCOVERED": {"SANDBOXED", "PROPOSED"},
    "SANDBOXED": {"VALIDATED", "DISCOVERED", "PROPOSED"},
    "VALIDATED": {"APPROVED", "SANDBOXED", "NEEDS_REVIEW"},
    "APPROVED": {"ACTIVE", "VALIDATED", "SUSPENDED"},
    "ACTIVE": {"SUSPENDED", "DEPRECATED", "APPROVED"},
    "SUSPENDED": {"ACTIVE", "DEPRECATED", "RETIRED"},
    "DEPRECATED": {"RETIRED", "SUSPENDED", "ACTIVE"},
    "RETIRED": {"ARCHIVED"},
    "ARCHIVED": set(),
}

GOVERNANCE_GATES = {
    ("PROPOSED", "DISCOVERED"): "auto",
    ("DISCOVERED", "SANDBOXED"): "sage_review",
    ("SANDBOXED", "VALIDATED"): "validation_engine",
    ("VALIDATED", "APPROVED"): "independent_review_gate",
    ("APPROVED", "ACTIVE"): "human_sovereignty_gate",
    ("ACTIVE", "SUSPENDED"): "risk_kernel",
    ("SUSPENDED", "ACTIVE"): "remediation_review",
    ("ACTIVE", "DEPRECATED"): "owner_or_sage",
    ("DEPRECATED", "RETIRED"): "retirement_conditions",
    ("RETIRED", "ARCHIVED"): "auto",
}


@dataclass(frozen=True)
class SkillLifecycleEventRecord:
    event_id: str = field(default_factory=lambda: make_id("LSE"))
    skill_id: str = ""
    from_stage: str = ""
    to_stage: str = ""
    triggered_by: str = ""
    reason: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)
    governance_approval_ref: str = ""
    timestamp: str = field(default_factory=utc_now)

    def __post_init__(self):
        for name in ("skill_id", "from_stage", "to_stage", "triggered_by"):
            if not getattr(self, name):
                raise ValueError(f"{name} is required")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SkillLifecycleEngine:
    def __init__(
        self,
        adapter: LanceDBAdapter,
        skill_registry: Any,
        validation_engine: Any = None,
        governance_gate: Any = None,
    ):
        self.adapter = adapter
        self.skill_registry = skill_registry
        self.validation_engine = validation_engine
        self.governance_gate = governance_gate
        self._events: list[SkillLifecycleEventRecord] = []
        self._hydrate()

    def _hydrate(self) -> None:
        rows = self.adapter.all("ak_skill_lifecycle")
        for row in rows:
            try:
                filtered = {k: v for k, v in row.items() if k in SkillLifecycleEventRecord.__dataclass_fields__}
                event = SkillLifecycleEventRecord(**filtered)
                self._events.append(event)
            except (TypeError, ValueError):
                continue

    def can_transition(self, from_stage: str, to_stage: str) -> bool:
        if from_stage not in SKILL_LIFECYCLE_STAGES or to_stage not in SKILL_LIFECYCLE_STAGES:
            return False
        return to_stage in LIFECYCLE_TRANSITIONS.get(from_stage, set())

    def get_required_gate(self, from_stage: str, to_stage: str) -> str | None:
        return GOVERNANCE_GATES.get((from_stage, to_stage))

    def transition(
        self,
        skill_id: str,
        to_stage: str,
        triggered_by: str,
        reason: str = "",
        evidence: dict[str, Any] | None = None,
        governance_approval_ref: str = "",
    ) -> SkillLifecycleEventRecord:
        skill = self.skill_registry.get(skill_id)
        from_stage = skill.lifecycle_stage

        if not self.can_transition(from_stage, to_stage):
            raise ValueError(f"invalid transition: {from_stage} -> {to_stage}")

        required_gate = self.get_required_gate(from_stage, to_stage)
        if required_gate and required_gate != "auto" and not governance_approval_ref:
            raise ValueError(f"transition requires {required_gate} approval")

        if required_gate == "validation_engine" and self.validation_engine:
            result = self.validation_engine.validate_skill(skill_id)
            if not result.passed:
                raise ValueError(f"validation failed: {result.blocking_issues}")

        if required_gate == "independent_review_gate" and self.governance_gate:
            pass

        if required_gate == "human_sovereignty_gate":
            if not governance_approval_ref:
                raise ValueError("human sovereignty gate approval required")

        updated_skill = self.skill_registry.transition_lifecycle(skill_id, to_stage, triggered_by)

        event = SkillLifecycleEventRecord(
            skill_id=skill_id,
            from_stage=from_stage,
            to_stage=to_stage,
            triggered_by=triggered_by,
            reason=reason,
            evidence=evidence or {},
            governance_approval_ref=governance_approval_ref,
        )
        self._save_event(event)
        return event

    def get_history(self, skill_id: str) -> list[SkillLifecycleEventRecord]:
        return [e for e in self._events if e.skill_id == skill_id]

    def get_skills_by_stage(self, stage: str) -> list[str]:
        return [e.skill_id for e in self._events if e.to_stage == stage]

    def _save_event(self, event: SkillLifecycleEventRecord) -> None:
        self._events.append(event)
        self.adapter.insert("ak_skill_lifecycle", [event.to_dict()])