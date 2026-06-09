from __future__ import annotations

from pathlib import Path
from typing import Any

from memory.capability_registry import CapabilityRegistry
from memory.dataset_registry import DatasetRegistry
from memory.decision_trace_registry import DecisionTraceRegistry
from memory.lancedb_adapter import LanceDBAdapter
from memory.learning_loop import LearningLoop
from memory.lesson_registry import LessonRegistry
from memory.quarantine_policy import QuarantinePolicy
from memory.skill_registry import SkillRegistry
from memory.schemas.records import stable_hash


AGENT_ALIASES = {
    "janus": "Janus",
    "sage": "Sage",
    "hermes": "Hermes",
    "iris": "Iris",
    "helen": "Helen",
    "langlieu": "LangLieu",
    "lang lieu": "LangLieu",
    "lang liêu": "LangLieu",
    "lang_lieu": "LangLieu",
    "yetkieu": "YetKieu",
    "yet kieu": "YetKieu",
    "yết kiêu": "YetKieu",
    "yet_kieu": "YetKieu",
}
ALLOWED_AGENTS = set(AGENT_ALIASES.values())


class MemoryInterface:
    def __init__(self, db_path: str | Path = "memory/lancedb", adapter: LanceDBAdapter | None = None):
        self.adapter = adapter or LanceDBAdapter(db_path)
        self.lessons = LessonRegistry(self.adapter)
        self.skills = SkillRegistry(self.adapter, self.lessons)
        self.capabilities = CapabilityRegistry(self.adapter)
        self.datasets = DatasetRegistry(self.adapter)
        self.decision_traces = DecisionTraceRegistry(self.adapter)
        self.learning_loop = LearningLoop(self.lessons, self.skills)
        self.quarantine_policy = QuarantinePolicy()

    def search_memory(self, query: str, filters: dict[str, Any] | None = None, limit: int = 10):
        filters = filters or {}
        table = filters.get("table", "lessons")
        return self.adapter.search(table, query, limit)

    def create_lesson_candidate(self, payload: dict[str, Any]):
        self._validate_agent(payload.get("owner_agent"))
        return self.lessons.create_candidate(**payload)

    def submit_for_review(self, record_id: str, reviewer_agent: str):
        self._validate_agent(reviewer_agent)
        return self.lessons.mark_reviewed(record_id, reviewer_agent)

    def get_approved_skills(self, agent_id: str | None = None):
        if agent_id is not None:
            self._validate_agent(agent_id)
        return self.skills.approved_for_agent(agent_id)

    def record_decision_trace(self, payload: dict[str, Any]):
        self._validate_agent(payload.get("agent"))
        return self.decision_traces.record(**payload)

    def quarantine_record(self, record_id: str | dict[str, Any], reason: str):
        if isinstance(record_id, dict):
            record = dict(record_id)
            record.setdefault("record_id", record.get("lesson_id") or record.get("skill_id") or record.get("trace_id"))
        else:
            record = {
                "record_id": record_id,
                "owner_agent": "UNKNOWN",
                "reviewer_agent": "UNKNOWN",
                "source_hash": stable_hash(record_id),
                "status": "QUARANTINE",
                "version": 1,
            }
        checked = self.quarantine_policy.evaluate(record, governance_valid=False)
        checked["record"]["quarantine_reason"] = reason
        return checked["record"]

    def _validate_agent(self, agent: str | None) -> None:
        if not agent or self.normalize_agent(agent) not in ALLOWED_AGENTS:
            raise ValueError(f"agent is not authorized for memory interface: {agent}")

    def normalize_agent(self, agent: str) -> str:
        return AGENT_ALIASES.get(agent.strip().lower(), agent)
