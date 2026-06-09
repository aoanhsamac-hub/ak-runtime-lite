from agents.base import BaseAgent
from agents.identity import get_identity
from agents.role_boundary import get_role_boundary
from agents.runtime_models import (
    AgentReportEnvelope,
    EvidenceRecord,
    LessonRecord,
)
from connectors.llm_connector import LLMConnector


class HermesAgent(BaseAgent):
    def __init__(self, memory_interface=None, memory_client=None, llm_connector=None):
        super().__init__(get_identity("hermes"), get_role_boundary("hermes"), memory_interface, memory_client)
        self.llm = llm_connector or LLMConnector()

    def get_identity(self):
        return self.identity

    def get_role_boundary(self):
        return self.role_boundary

    def distill_lesson(self, evidence_records: list[EvidenceRecord]) -> LessonRecord | None:
        if not evidence_records:
            return None
        descriptions = [e.output_summary[:100] for e in evidence_records if e.output_summary]
        prompt = (
            f"Distill a lesson from {len(evidence_records)} evidence items:\n"
            + "\n".join(f"- {d}" for d in descriptions[:5])
            + "\n\nProvide: lesson title, description, context, outcome."
        )
        llm_result = self.llm.execute(prompt)
        return LessonRecord(
            source_evidence_ids=[e.evidence_id for e in evidence_records],
            source_agent=self.identity.agent_id,
            title=f"Distilled lesson from {len(evidence_records)} evidence items",
            description=llm_result.get("content", "Lesson distilled")[:300],
            context="memory_corpus",
            outcome="lesson_distilled",
            quality_score=0.8,
            owner=self.identity.agent_id,
            reviewer="Sage",
        )

    def review_evidence_quality(self, evidence: list[dict]) -> dict:
        if not evidence:
            return {"quality": "no_evidence", "score": 0.0, "recommendation": "collect_evidence"}
        scores = []
        for ev in evidence:
            classification = ev.get("classification", "I5_SPECULATIVE")
            score_map = {
                "I0_OFFICIAL_VERIFIED": 1.0, "I1_PROBABLE": 0.9, "I2_HYPOTHESIS": 0.8,
                "I3_THEORY": 0.7, "I4_SCENARIO": 0.6, "I5_SPECULATIVE": 0.5,
                "I6_FICTION": 0.3, "I7_LEGEND": 0.2, "I8_RUMOR": 0.1, "I9_REJECTED": 0.0,
            }
            scores.append(score_map.get(classification, 0.5))
        avg_score = sum(scores) / len(scores) if scores else 0.0
        return {
            "quality": "high" if avg_score >= 0.7 else "medium" if avg_score >= 0.4 else "low",
            "score": round(avg_score, 4),
            "total_evidence": len(evidence),
            "recommendation": "ready_for_lessons" if avg_score >= 0.7 else "needs_review",
        }

    def check_dataset_readiness(self) -> dict:
        return {
            "ready": len(self._evidence_registry) >= 3,
            "evidence_count": len(self._evidence_registry),
            "lesson_count": len(self._lesson_registry),
            "agent": self.identity.agent_id,
        }

    def generate_memory_report(self, mission_id: str) -> AgentReportEnvelope:
        return AgentReportEnvelope(
            agent_id=self.identity.agent_id,
            mission_id=mission_id,
            mission_type="memory_mission",
            summary=f"Memory mission complete: {len(self._evidence_registry)} evidence items, {len(self._lesson_registry)} lessons",
            evidence_ids=[e.evidence_id for e in self._evidence_registry],
            lesson_ids=[l.lesson_id for l in self._lesson_registry],
            status="COMPLETED",
        )


def create_agent(memory_interface=None, memory_client=None, llm_connector=None):
    return HermesAgent(memory_interface, memory_client, llm_connector)
