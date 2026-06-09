from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from memory.capability_pipeline.schemas import (
    EVOLUTION_EVENT_TYPES,
    EVOLUTION_STATES,
    MATURITY_LEVEL_EVOLUTION_ORDER,
    EvolutionEventRecord,
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class EvolutionProposal:
    proposal_id: str
    capability_id: str
    current_maturity: str
    proposed_maturity: str
    trigger: str
    evidence: dict[str, Any]
    status: str = "PROPOSED"
    created_at: str = field(default_factory=_utc_now)


@dataclass
class EvolutionResult:
    capability_id: str
    evolution_cycle: int
    from_state: str
    to_state: str
    maturity_before: str
    maturity_after: str
    event_ids: list[str]
    success: bool
    message: str


class CapabilityEvolutionLoop:
    def __init__(self, official_registry, maturity_engine,
                 maturity_reassessment_engine, governance_gate=None,
                 audit_engine=None):
        self._official = official_registry
        self._maturity_engine = maturity_engine
        self._maturity_reassess = maturity_reassessment_engine
        self._governance_gate = governance_gate
        self._audit_engine = audit_engine
        self._proposals: dict[str, EvolutionProposal] = {}
        self._events: dict[str, EvolutionEventRecord] = {}

    def propose_evolution(self, capability_id: str, trigger: str = "scheduled_review",
                          evidence: dict[str, Any] | None = None) -> EvolutionProposal:
        record = self._official.get(capability_id)
        if record.evolution_status not in ("UNLOCKED", "EVOLVED"):
            raise ValueError(
                f"evolution not allowed from state {record.evolution_status}; "
                f"requires UNLOCKED or EVOLVED"
            )

        maturity_score = self._compute_current_score(record)
        proposed = self._propose_next_level(maturity_score)

        proposal_id = f"EVO-{capability_id}-{_utc_now()}"
        proposal = EvolutionProposal(
            proposal_id=proposal_id,
            capability_id=capability_id,
            current_maturity=record.evolution_status,
            proposed_maturity=proposed,
            trigger=trigger,
            evidence=evidence or {},
        )
        self._proposals[proposal_id] = proposal
        self._append_event(capability_id, "MATURITY_PROGRESSION",
                           record.evolution_status, "EVOLVING_MATURITY",
                           trigger, evidence or {})
        return proposal

    def sandbox_experiment(self, proposal_id: str) -> dict[str, Any]:
        proposal = self._proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f"proposal not found: {proposal_id}")

        record = self._official.get(proposal.capability_id)
        updated = record.with_evolution(evolution_status="EVOLVING_CYCLE")
        self._official._records[proposal.capability_id] = updated

        self._append_event(proposal.capability_id, "CAPABILITY_EVOLUTION",
                           "EVOLVING_MATURITY", "EVOLVING_CYCLE",
                           proposal.trigger, proposal.evidence)
        return {"status": "sandbox_ready", "proposal_id": proposal_id}

    def validate_evolution(self, proposal_id: str,
                           experiment_results: dict[str, Any] | None = None) -> dict[str, Any]:
        proposal = self._proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f"proposal not found: {proposal_id}")

        maturity_gain = self._simulate_maturity_gain(proposal, experiment_results)

        if self._governance_gate:
            gate_result = self._governance_gate.evaluate_evolution(
                proposal.capability_id, proposal.proposed_maturity
            )
        else:
            gate_result = {"passed": True, "gates": []}

        return {
            "proposal_id": proposal_id,
            "maturity_gain": maturity_gain,
            "governance": gate_result,
            "promotion_candidate": gate_result.get("passed", False) and maturity_gain > 0,
        }

    def promote_evolution(self, proposal_id: str) -> EvolutionResult:
        proposal = self._proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f"proposal not found: {proposal_id}")

        record = self._official.get(proposal.capability_id)
        new_cycle = record.evolution_cycle + 1
        from_state = record.evolution_status
        maturity_before = self._propose_next_level(self._compute_current_score(record))

        updated = record.with_evolution(
            evolution_status="EVOLVED",
            evolution_cycle=new_cycle,
        )
        self._official._records[proposal.capability_id] = updated

        event = self._append_event(proposal.capability_id, "PROMOTION",
                                   from_state, "EVOLVED",
                                   proposal.trigger, {
                                       "proposal_id": proposal_id,
                                       "maturity_before": maturity_before,
                                       "maturity_after": proposal.proposed_maturity,
                                       "cycle": new_cycle,
                                   })

        if self._audit_engine:
            self._audit_engine.append_audit_record({
                "event": "CAPABILITY_EVOLVED",
                "capability_id": proposal.capability_id,
                "cycle": new_cycle,
                "from_state": maturity_before,
                "to_state": maturity_after,
            })

        proposal.status = "PROMOTED"
        return EvolutionResult(
            capability_id=proposal.capability_id,
            evolution_cycle=new_cycle,
            from_state=from_state,
            to_state="EVOLVED",
            maturity_before=maturity_before,
            maturity_after=proposal.proposed_maturity,
            event_ids=[event.event_id],
            success=True,
            message=f"Evolved to cycle {new_cycle}: {maturity_before} -> {proposal.proposed_maturity}",
        )

    def rollback_evolution(self, capability_id: str) -> EvolutionResult:
        record = self._official.get(capability_id)
        if record.evolution_status != "EVOLVED":
            raise ValueError(f"cannot rollback from state {record.evolution_status}")

        maturity_before = record.evolution_status
        updated = record.with_evolution(evolution_status="ROLLED_BACK")
        self._official._records[capability_id] = updated

        event = self._append_event(capability_id, "ROLLBACK",
                                   "EVOLVED", "ROLLED_BACK",
                                   "manual_rollback", {})

        if self._audit_engine:
            self._audit_engine.append_audit_record({
                "event": "CAPABILITY_ROLLED_BACK",
                "capability_id": capability_id,
                "from_state": maturity_before,
                "to_state": "ROLLED_BACK",
            })

        return EvolutionResult(
            capability_id=capability_id,
            evolution_cycle=record.evolution_cycle,
            from_state="EVOLVED",
            to_state="ROLLED_BACK",
            maturity_before=maturity_before,
            maturity_after="ROLLED_BACK",
            event_ids=[event.event_id],
            success=True,
            message=f"Rolled back capability {capability_id}",
        )

    def unlock_evolution(self, capability_id: str) -> None:
        record = self._official.get(capability_id)
        if record.evolution_status not in ("LOCKED", "ROLLED_BACK"):
            raise ValueError(f"can only unlock from LOCKED or ROLLED_BACK, got {record.evolution_status}")
        updated = record.with_evolution(evolution_status="UNLOCKED")
        self._official._records[capability_id] = updated

    def get_evolution_history(self, capability_id: str) -> list[EvolutionEventRecord]:
        return [e for e in self._events.values() if e.capability_id == capability_id]

    def _compute_current_score(self, record: Any) -> float:
        return 0.5

    @staticmethod
    def _propose_next_level(current_score: float) -> str:
        if current_score >= 0.9:
            return "SOVEREIGN"
        if current_score >= 0.7:
            return "ADVANCED"
        if current_score >= 0.5:
            return "ESTABLISHED"
        if current_score >= 0.3:
            return "DEVELOPING"
        return "EMERGING"

    @staticmethod
    def _simulate_maturity_gain(proposal: EvolutionProposal,
                                results: dict[str, Any] | None = None) -> float:
        base = MATURITY_LEVEL_EVOLUTION_ORDER.get(proposal.proposed_maturity, 1) / 5.0
        return base + 0.1 if results and results.get("positive") else base

    def _append_event(self, capability_id: str, event_type: str,
                      from_state: str, to_state: str,
                      trigger: str, evidence: dict[str, Any]) -> EvolutionEventRecord:
        event = EvolutionEventRecord(
            capability_id=capability_id,
            event_type=event_type,
            from_state=from_state,
            to_state=to_state,
            trigger=trigger,
            evidence=evidence,
        )
        self._events[event.event_id] = event
        return event
