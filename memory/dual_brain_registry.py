"""NEURON T4 Dual Brain Architecture Registries - OBSERVE_ONLY."""

from __future__ import annotations

from datetime import datetime, timezone


class FastBrainRegistry:
    def __init__(self):
        self._decisions = {}

    def record(self, decision_id: str, prompt: str, response: str, confidence: float, owner_agent: str) -> dict:
        self._decisions[decision_id] = {"decision_id": decision_id, "prompt": prompt, "response": response, "confidence": confidence, "owner_agent": owner_agent, "mode": "OBSERVE_ONLY"}
        return self._decisions[decision_id]


class SlowBrainRegistry:
    def __init__(self):
        self._decisions = {}

    def record(self, decision_id: str, prompt: str, response: str, confidence: float, owner_agent: str) -> dict:
        self._decisions[decision_id] = {"decision_id": decision_id, "prompt": prompt, "response": response, "confidence": confidence, "owner_agent": owner_agent, "mode": "OBSERVE_ONLY"}
        return self._decisions[decision_id]


class RoutingLayer:
    def __init__(self):
        self._routes = []

    def route(self, prompt: str, fast_available: bool, confidence: float) -> dict:
        mode = "FAST" if fast_available and confidence > 0.8 else "SLOW"
        return {"prompt_hash": hash(prompt), "selected_mode": mode, "confidence": confidence}


class EscalationLayer:
    def __init__(self):
        self._escalations = {}

    def escalate(self, decision_id: str, reason: str, owner_agent: str) -> dict:
        self._escalations[decision_id] = {"decision_id": decision_id, "reason": reason, "owner_agent": owner_agent, "escalated_at": datetime.now(timezone.utc).isoformat()}
        return self._escalations[decision_id]


FAST_BRAIN = FastBrainRegistry()
SLOW_BRAIN = SlowBrainRegistry()
ROUTING = RoutingLayer()
ESCALATION = EscalationLayer()

__all__ = ["FastBrainRegistry", "SlowBrainRegistry", "RoutingLayer", "EscalationLayer", "FAST_BRAIN", "SLOW_BRAIN", "ROUTING", "ESCALATION"]