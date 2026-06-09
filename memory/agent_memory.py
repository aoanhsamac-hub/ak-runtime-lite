from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from memory.memory_interface import MemoryInterface


@dataclass(frozen=True)
class AgentMemoryClient:
    agent_id: str
    interface: MemoryInterface

    def search(self, query: str, table: str = "lessons", limit: int = 10):
        return self.interface.search_memory(query, filters={"table": table}, limit=limit)

    def create_lesson(self, **payload):
        payload = dict(payload)
        payload.setdefault("owner_agent", self.agent_id)
        return self.interface.create_lesson_candidate(payload)

    def approved_skills(self):
        return self.interface.get_approved_skills(self.agent_id)

    def record_decision(
        self,
        decision: str,
        reasoning: str,
        evidence: list[str],
        outcome: str,
        lesson_generated: str | None = None,
        **extra: Any,
    ):
        payload = {
            "agent": self.agent_id,
            "decision": decision,
            "reasoning": reasoning,
            "evidence": evidence,
            "outcome": outcome,
            "lesson_generated": lesson_generated,
        }
        payload.update(extra)
        return self.interface.record_decision_trace(payload)


def agent_memory_client(agent_id: str, interface: MemoryInterface) -> AgentMemoryClient:
    canonical = interface.normalize_agent(agent_id)
    interface._validate_agent(canonical)
    return AgentMemoryClient(agent_id=canonical, interface=interface)
