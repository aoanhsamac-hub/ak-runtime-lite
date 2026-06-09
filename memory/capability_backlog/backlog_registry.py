"""NEURON T1-4 Capability Backlog Registry."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


STATES = {
    "ACTIVE": "Production capability with full authority",
    "SANDBOX_ONLY": "Experimental capability, sandbox-restricted",
    "TRAINING_LOCKED": "Infrastructure exists, training disabled",
    "OBSERVE_ONLY": "Monitoring mode, non-authoritative",
    "BACKLOG": "Planned, not yet implemented",
    "ARCHIVED": "Deprecated capability",
}


class CapabilityBacklog:
    def __init__(self):
        self._items: dict[str, dict[str, Any]] = {}

    def register(self, capability_name: str, owner_agent: str, activation_state: str = "BACKLOG", **fields) -> dict:
        record = {
            "capability_name": capability_name,
            "owner_agent": owner_agent,
            "activation_state": activation_state,
            "dependencies": fields.get("dependencies", []),
            "risk_level": fields.get("risk_level", "LEVEL_2_HIGH"),
            "review_status": fields.get("review_status", "PENDING"),
            "activation_gate": fields.get("activation_gate", "HUNG_VUONG"),
            "created_at": datetime.now(timezone.utc).isoformat(),
            **fields,
        }
        self._items[capability_name] = record
        return record

    def update_state(self, capability_name: str, new_state: str, **updates) -> dict | None:
        if capability_name not in self._items:
            return None
        self._items[capability_name]["activation_state"] = new_state
        self._items[capability_name].update(updates)
        return self._items[capability_name]

    def get(self, capability_name: str) -> dict | None:
        return self._items.get(capability_name)

    def list_by_state(self, state: str) -> list[dict]:
        return [r for r in self._items.values() if r.get("activation_state") == state]

    def list_by_owner(self, owner: str) -> list[dict]:
        return [r for r in self._items.values() if r.get("owner_agent") == owner]

    def summary(self) -> dict:
        counts = {}
        for state in STATES:
            counts[state] = len(self.list_by_state(state))
        return {"total": len(self._items), "by_state": counts}


BACKLOG = CapabilityBacklog()


def _register_neuron_layers():
    BACKLOG.register("NEURON_T1_VectorMemory_RAG", "Hermes", "ACTIVE",
        description="LanceDB semantic retrieval with lineage",
        dependencies=["KingdomMemoryPlatform"],
        review_status="SAGE_APPROVED",
        activation_gate="READY_FOR_SANDBOX")
    BACKLOG.register("NEURON_T2_PromptEvolution", "Hermes", "SANDBOX_ONLY",
        description="Prompt registry and evolution pipeline",
        dependencies=["LLMConnector"],
        review_status="SAGE_REVIEW_REQUIRED",
        activation_gate="SANDBOX_ACTIVE")
    BACKLOG.register("NEURON_T3_FineTuning", "Hermes", "TRAINING_LOCKED",
        description="Dataset and training infrastructure",
        dependencies=["KingdomMemoryPlatform", "CapabilityBacklog"],
        review_status="SAGE_REVIEW_REQUIRED",
        activation_gate="HUNG_VUONG_APPROVAL")
    BACKLOG.register("NEURON_T4_DualBrain", "Janus", "OBSERVE_ONLY",
        description="Fast/slow brain architecture with routing",
        dependencies=["AgentRuntime", "LLMConnector"],
        review_status="SAGE_REVIEW_REQUIRED",
        activation_gate="HUNG_VUONG_APPROVAL")
    BACKLOG.register("DebateEngine", "Janus", "ACTIVE",
        description="Multi-agent challenge and counter-argument system",
        dependencies=["Sage"],
        review_status="SAGE_APPROVED",
        activation_gate="READY_FOR_SANDBOX")
    BACKLOG.register("SkillBenchmarkSystem", "Hermes", "ACTIVE",
        description="Skill evaluation and promotion pipeline",
        dependencies=["SkillRegistry"],
        review_status="SAGE_APPROVED",
        activation_gate="READY_FOR_SANDBOX")
    BACKLOG.register("ConfidenceScoringLayer", "Janus", "ACTIVE",
        description="Confidence metadata on all agent outputs",
        dependencies=["ReportEnvelope"],
        review_status="SAGE_APPROVED",
        activation_gate="READY_FOR_SANDBOX")


_register_neuron_layers()


__all__ = ["CapabilityBacklog", "BACKLOG", "STATES"]