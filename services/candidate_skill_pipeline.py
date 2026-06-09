from __future__ import annotations

from typing import Any

from memory.learning_registry.schemas import CandidateSkillRecord


class CandidateSkillPipeline:
    """Transforms insights into candidate skill records.

    All generated skills are locked to:
      status=CANDIDATE, approval_status=PENDING_REVIEW, activation_status=DISABLED
    No autonomous promotion.
    """

    def __init__(self, signal_registry, insight_registry, candidate_skill_registry):
        self.signal_registry = signal_registry
        self.insight_registry = insight_registry
        self.candidate_skill_registry = candidate_skill_registry

    def create_from_insight(self, insight_id: str,
                            name: str | None = None,
                            description: str | None = None,
                            owner_agent: str = "Sage",
                            test_cases: list[str] | None = None,
                            allowed_agents: list[str] | None = None) -> CandidateSkillRecord | None:
        try:
            insight = self.insight_registry.get(insight_id)
        except KeyError:
            return None

        skill_name = name or f"Skill: {insight.title}"
        skill_desc = description or f"Candidate skill derived from insight {insight_id}: {insight.description}"

        source_signal_ids = list(insight.source_signal_ids)
        source_lesson_ids = self._resolve_lesson_ids(source_signal_ids)

        return self.candidate_skill_registry.create_candidate(
            name=skill_name,
            description=skill_desc,
            source_insight_ids=[insight_id],
            source_signal_ids=source_signal_ids,
            source_lesson_ids=source_lesson_ids,
            owner_agent=owner_agent,
            risk_level=insight.risk_level,
            test_cases=test_cases or [],
            allowed_agents=allowed_agents or [owner_agent],
            confidence_score=insight.confidence_score,
            evidence={"derived_from_insight": insight_id, "insight_type": insight.insight_type},
            tags=["candidate", insight.insight_type.lower()] + list(insight.tags),
        )

    def batch_create_from_insights(self, insight_ids: list[str],
                                   owner_agent: str = "Sage") -> list[CandidateSkillRecord]:
        results: list[CandidateSkillRecord] = []
        for iid in insight_ids:
            rec = self.create_from_insight(iid, owner_agent=owner_agent)
            if rec:
                results.append(rec)
        return results

    def create_from_insight_type(self, insight_type: str,
                                 owner_agent: str = "Sage") -> list[CandidateSkillRecord]:
        matching = self.insight_registry.list_all(insight_type=insight_type)
        if not matching:
            return []
        return self.batch_create_from_insights(
            [i.insight_id for i in matching],
            owner_agent=owner_agent,
        )

    def run_all(self, owner_agent: str = "Sage") -> list[CandidateSkillRecord]:
        all_insights = self.insight_registry.list_all()
        if not all_insights:
            return []
        return self.batch_create_from_insights(
            [i.insight_id for i in all_insights],
            owner_agent=owner_agent,
        )

    def _resolve_lesson_ids(self, signal_ids: list[str]) -> list[str]:
        lesson_ids: list[str] = []
        for sid in signal_ids:
            try:
                sig = self.signal_registry.get(sid)
                if sig.source_kind == "lesson":
                    lesson_ids.append(sig.source_id)
            except KeyError:
                continue
        return lesson_ids
