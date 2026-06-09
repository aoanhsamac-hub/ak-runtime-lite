from __future__ import annotations

from typing import Any

from memory.learning_registry.schemas import CandidateSkillRecord, SKILL_CATEGORIES


SIGNAL_TO_CATEGORY: dict[str, str] = {
    "PATTERN": "Engineering Skills",
    "ANOMALY": "Risk Skills",
    "REPEATABILITY": "Memory Skills",
    "GOVERNANCE": "Governance Skills",
    "DATASET": "Engineering Skills",
    "DECISION": "Agent Skills",
    "EXECUTION": "Execution Skills",
    "RISK": "Risk Skills",
    "TRADING": "Trading Skills",
    "PERFORMANCE": "Memory Skills",
}

INSIGHT_TO_CATEGORY: dict[str, str] = {
    "PATTERN": "Engineering Skills",
    "CONSOLIDATION": "Memory Skills",
    "GAP": "Risk Skills",
    "TREND": "Trading Skills",
    "RISK": "Risk Skills",
    "PROCESS": "Agent Skills",
    "SKILL": "Engineering Skills",
    "GOVERNANCE": "Governance Skills",
    "MARKET": "Trading Skills",
    "EXECUTION": "Execution Skills",
    "PERFORMANCE": "Memory Skills",
}


class SkillDiscoveryEngine:
    """Discovers candidate skills from insights and signal clusters.

    All generated skills are locked to:
      status=CANDIDATE, approval_status=PENDING_REVIEW, activation_status=DISABLED
    """

    def __init__(self, signal_registry, cluster_registry, insight_registry, candidate_skill_registry):
        self.signal_registry = signal_registry
        self.cluster_registry = cluster_registry
        self.insight_registry = insight_registry
        self.candidate_skill_registry = candidate_skill_registry

    def discover_from_insights(self, owner_agent: str = "Sage") -> list[CandidateSkillRecord]:
        insights = self.insight_registry.list_all()
        skills: list[CandidateSkillRecord] = []

        for ins in insights:
            category = INSIGHT_TO_CATEGORY.get(ins.insight_type, "Engineering Skills")
            skill_name = f"{category} Skill: {ins.title}"
            source_lesson_ids = self._resolve_lesson_ids(ins.source_signal_ids)

            skill = self.candidate_skill_registry.create_candidate(
                name=skill_name,
                description=f"Discovered from insight {ins.insight_id}: {ins.description}",
                source_insight_ids=[ins.insight_id],
                source_signal_ids=list(ins.source_signal_ids),
                source_lesson_ids=source_lesson_ids,
                owner_agent=owner_agent,
                risk_level=ins.risk_level,
                confidence_score=ins.confidence_score,
                evidence={"discovery_method": "insight", "insight_type": ins.insight_type,
                          "category": category},
                tags=["discovered", category.lower().replace(" ", "_")] + list(ins.tags),
                allowed_agents=[owner_agent],
            )
            skills.append(skill)

        return skills

    def discover_from_clusters(self, owner_agent: str = "Sage") -> list[CandidateSkillRecord]:
        clusters = self.cluster_registry.list_all()
        skills: list[CandidateSkillRecord] = []

        for cluster in clusters:
            category = SIGNAL_TO_CATEGORY.get(
                next((st for st in SIGNAL_TO_CATEGORY if st in [s.split(" ")[0] for s in cluster.tags]), ""),
                "Engineering Skills",
            )
            skill_name = f"{category} Discovery: {cluster.title}"

            skill = self.candidate_skill_registry.create_candidate(
                name=skill_name,
                description=f"Discovered from cluster {cluster.cluster_id}: {cluster.description}",
                source_insight_ids=[],
                source_signal_ids=list(cluster.source_signal_ids),
                source_lesson_ids=self._resolve_lesson_ids(cluster.source_signal_ids),
                owner_agent=owner_agent,
                risk_level=cluster.risk_level,
                confidence_score=cluster.confidence_score,
                evidence={"discovery_method": "cluster", "cluster_type": cluster.cluster_type,
                          "category": category},
                tags=["discovered", "cluster", category.lower().replace(" ", "_")] + list(cluster.tags),
                allowed_agents=[owner_agent],
            )
            skills.append(skill)

        return skills

    def run_all(self, owner_agent: str = "Sage") -> list[CandidateSkillRecord]:
        skills = self.discover_from_insights(owner_agent)
        skills.extend(self.discover_from_clusters(owner_agent))
        return skills

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
