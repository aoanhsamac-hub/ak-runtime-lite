from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


MATURITY_ORDER = ["EMERGING", "DEVELOPING", "ESTABLISHED", "ADVANCED", "SOVEREIGN"]


@dataclass
class MaturityAssessment:
    skill_id: str
    skill_name: str
    maturity_level: str
    maturity_score: float
    promotion_readiness: str
    evidence_depth: int = 0
    repeatability: float = 0.0
    reuse_value: float = 0.0
    governance_confidence: float = 0.0
    cross_domain_adoption: int = 0


class SkillMaturityEngine:
    """Assesses maturity and promotion readiness of canonical skills."""

    def __init__(self, candidate_skill_registry, family_registry, canonical_registry):
        self.candidate_skill_registry = candidate_skill_registry
        self.family_registry = family_registry
        self.canonical_registry = canonical_registry

    def assess_all(self) -> list[MaturityAssessment]:
        canonical = self.canonical_registry.list_all()
        skills = self.candidate_skill_registry.list_all()
        skill_map = {s.candidate_skill_id: s for s in skills}
        assessments: list[MaturityAssessment] = []

        for c in canonical:
            if c.classification != "CANONICAL":
                continue

            source_skills = [skill_map[sid] for sid in c.source_skill_ids if sid in skill_map]
            if not source_skills:
                source_skills = [s for s in skills if s.candidate_skill_id in c.source_skill_ids]

            ev_depth = self._calc_evidence_depth(c, source_skills)
            repeat = self._calc_repeatability(c, source_skills)
            reuse = self._calc_reuse_value(c, source_skills)
            gov_conf = self._calc_governance_confidence(c, source_skills)
            cross = self._calc_cross_domain(c, source_skills)

            score = round((ev_depth * 0.25 + repeat * 0.20 + reuse * 0.20 + gov_conf * 0.25 + cross * 0.10), 2)
            level = self._score_to_level(score)
            readiness = self._calc_readiness(score, level)

            assessments.append(MaturityAssessment(
                skill_id=c.canonical_id,
                skill_name=c.name,
                maturity_level=level,
                maturity_score=score,
                promotion_readiness=readiness,
                evidence_depth=ev_depth,
                repeatability=repeat,
                reuse_value=reuse,
                governance_confidence=gov_conf,
                cross_domain_adoption=cross,
            ))

        return assessments

    @staticmethod
    def _calc_evidence_depth(canonical, source_skills) -> int:
        count = len(source_skills)
        if count >= 10:
            return 5
        if count >= 5:
            return 4
        if count >= 3:
            return 3
        if count >= 1:
            return 2
        return 1

    @staticmethod
    def _calc_repeatability(canonical, source_skills) -> float:
        scores = [s.confidence_score for s in source_skills if s]
        if not scores:
            return 0.0
        return min(sum(scores) / len(scores) * 5, 5.0) / 5.0

    @staticmethod
    def _calc_reuse_value(canonical, source_skills) -> float:
        unique_tags = set()
        for s in source_skills:
            if s:
                unique_tags.update(s.tags)
        domain_tags = {t for t in unique_tags if "_knowledge" in t or "_skills" in t or t in ("memory", "trading", "risk", "execution", "governance", "engineering", "agent")}
        score = min(len(domain_tags) * 0.5, 5.0) / 5.0
        return score

    @staticmethod
    def _calc_governance_confidence(canonical, source_skills) -> float:
        scores = [s.confidence_score for s in source_skills if s and s.confidence_score > 0]
        if not scores:
            return canonical.confidence_score
        return min((sum(scores) / len(scores)) * 1.2, 1.0)

    @staticmethod
    def _calc_cross_domain(canonical, source_skills) -> int:
        domains = set()
        for s in source_skills:
            if s:
                for tag in s.tags:
                    if "_knowledge" in tag or "_skills" in tag:
                        domains.add(tag)
        return min(len(domains), 5)

    @staticmethod
    def _score_to_level(score: float) -> str:
        if score >= 0.9:
            return "SOVEREIGN"
        if score >= 0.7:
            return "ADVANCED"
        if score >= 0.5:
            return "ESTABLISHED"
        if score >= 0.3:
            return "DEVELOPING"
        return "EMERGING"

    @staticmethod
    def _calc_readiness(score: float, level: str) -> str:
        if score >= 0.8 and level in ("ADVANCED", "SOVEREIGN"):
            return "Promotion Ready"
        if score >= 0.5:
            return "Needs Review"
        if score >= 0.3:
            return "Needs Evidence"
        return "Needs Consolidation"
