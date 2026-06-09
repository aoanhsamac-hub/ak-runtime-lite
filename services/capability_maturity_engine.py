from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


MATURITY_ORDER = ["EMERGING", "DEVELOPING", "ESTABLISHED", "ADVANCED", "SOVEREIGN"]


@dataclass
class CapabilityMaturityAssessment:
    capability_id: str
    capability_name: str
    domain: str
    maturity_level: str
    maturity_score: float
    evidence_depth: int = 0
    cross_domain_adoption: int = 0
    skill_support: float = 0.0
    governance_confidence: float = 0.0
    reuse_value: float = 0.0
    evolution_cycle: int = 0
    evolution_bonus: float = 0.0


class CapabilityMaturityEngine:
    """Assesses maturity of canonical capabilities."""

    def __init__(self, capability_registry, family_registry, canonical_registry):
        self.capability_registry = capability_registry
        self.family_registry = family_registry
        self.canonical_registry = canonical_registry

    def assess_all(self) -> list[CapabilityMaturityAssessment]:
        canonicals = self.canonical_registry.list_all()
        caps = {c.capability_id: c for c in self.capability_registry.list_all()}
        assessments = []

        for cc in canonicals:
            if cc.classification != "CANONICAL":
                continue
            source = [caps[s] for s in cc.source_capability_ids if s in caps]

            ev_depth = min(len(source) + 1, 5)
            cross = self._calc_cross_domain(cc, source)
            skill_sup = self._calc_skill_support(cc, source)
            gov_conf = max(cc.confidence_score, 0.5)
            reuse = self._calc_reuse(cc, source)
            evolution_cycle = self._get_evolution_cycle(cc)
            evolution_bonus = min(evolution_cycle * 0.05, 0.2)

            score = round((ev_depth * 0.2 + cross * 0.2 + skill_sup * 0.25 + gov_conf * 0.25 + reuse * 0.1 + evolution_bonus), 2)
            level = self._score_to_level(score)

            assessments.append(CapabilityMaturityAssessment(
                capability_id=cc.canonical_id,
                capability_name=cc.name,
                domain=cc.domain,
                maturity_level=level,
                maturity_score=score,
                evidence_depth=ev_depth,
                cross_domain_adoption=cross,
                skill_support=skill_sup,
                governance_confidence=gov_conf,
                reuse_value=reuse,
                evolution_cycle=evolution_cycle,
                evolution_bonus=round(evolution_bonus, 2),
            ))
        return assessments

    @staticmethod
    def _get_evolution_cycle(cc) -> int:
        meta = getattr(cc, 'metadata', {}) or {}
        if isinstance(meta, dict):
            return int(meta.get("evolution_cycle", 0))
        return 0

    @staticmethod
    def _calc_cross_domain(cc, source) -> int:
        domains = set()
        domains.add(cc.domain)
        for s in source:
            for tag in s.tags:
                for d in ["trading", "risk", "execution", "governance", "memory", "engineering", "agent"]:
                    if d in tag.lower():
                        domains.add(d.capitalize())
        return min(len(domains), 5)

    @staticmethod
    def _calc_skill_support(cc, source) -> float:
        count = len(source)
        return min(count / 3.0, 1.0)

    @staticmethod
    def _calc_reuse(cc, source) -> float:
        unique_tags = set()
        for s in source:
            unique_tags.update(s.tags)
        return min(len(unique_tags) * 0.15, 1.0)

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
