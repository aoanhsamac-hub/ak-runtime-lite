from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

MATURITY_LEVELS = ["EMERGING", "DEVELOPING", "ESTABLISHED", "ADVANCED", "SOVEREIGN"]


@dataclass
class MaturityReassessment:
    capability_id: str
    capability_name: str
    domain: str
    evidence_depth: float = 0.0
    skill_support: float = 0.0
    trace_support: float = 0.0
    validation_results: float = 0.0
    risk_profile: float = 0.0
    reuse_value: float = 0.0
    governance_confidence: float = 0.0
    maturity_level: str = "EMERGING"
    maturity_score: float = 0.0
    previous_maturity: str = ""
    evolution_cycle: int = 0
    evolution_trace_count: int = 0


class CapabilityMaturityReassessmentEngine:
    """Reassesses maturity of capabilities based on validation evidence."""

    def __init__(self, capability_registry, canonical_registry,
                 evidence_registry=None, maturity_engine=None):
        self.capability_registry = capability_registry
        self.canonical_registry = canonical_registry
        self.evidence_registry = evidence_registry
        self.maturity_engine = maturity_engine

    def reassess(self, canonical_capability: Any,
                 evidence_sufficiency: dict[str, Any] | None = None,
                 previous_maturity: str = "",
                 evolution_cycle: int = 0,
                 evolution_trace_ids: list[str] | None = None) -> MaturityReassessment:
        cap_id = getattr(canonical_capability, 'canonical_id', '')
        name = getattr(canonical_capability, 'name', '')
        domain = getattr(canonical_capability, 'domain', '')
        conf = getattr(canonical_capability, 'confidence_score', 0.0)
        source_caps = getattr(canonical_capability, 'source_capability_ids', [])

        ev_depth = 0.0
        if evidence_sufficiency:
            ev_depth = evidence_sufficiency.get("avg_confidence", 0.0) if evidence_sufficiency.get("has_evidence") else 0.0
        skill_support = min(conf + 0.1, 1.0)
        trace_support = min(len(source_caps) * 0.15, 1.0)
        validation = evidence_sufficiency.get("avg_metric", 0.0) if evidence_sufficiency and evidence_sufficiency.get("has_evidence") else 0.0
        risk_profile = 1.0 - (getattr(canonical_capability, 'risk_level', 'LEVEL_1_MODERATE').count("_") * 0.15)
        reuse_value = min(trace_support + 0.2, 1.0)
        gov_conf = min((skill_support + trace_support + validation) / 3 + 0.1, 1.0)
        evolution_trace_count = len(evolution_trace_ids or [])
        evolution_bonus = min(evolution_cycle * 0.03, 0.15)

        score = round((ev_depth * 0.20 + skill_support * 0.20 + trace_support * 0.15 +
                       validation * 0.20 + risk_profile * 0.10 + reuse_value * 0.10 +
                       gov_conf * 0.05 + evolution_bonus), 2)

        level = self._score_to_level(score)
        if previous_maturity and MATURITY_LEVELS.index(level) < MATURITY_LEVELS.index(previous_maturity):
            level = previous_maturity

        return MaturityReassessment(
            capability_id=cap_id,
            capability_name=name,
            domain=domain,
            evidence_depth=round(ev_depth, 2),
            skill_support=round(skill_support, 2),
            trace_support=round(trace_support, 2),
            validation_results=round(validation, 2),
            risk_profile=round(risk_profile, 2),
            reuse_value=round(reuse_value, 2),
            governance_confidence=round(gov_conf, 2),
            maturity_level=level,
            maturity_score=score,
            previous_maturity=previous_maturity,
            evolution_cycle=evolution_cycle,
            evolution_trace_count=evolution_trace_count,
        )

    def reassess_all(self, evidence_map: dict[str, dict[str, Any]] | None = None) -> list[MaturityReassessment]:
        canonicals = self.canonical_registry.list_all(classification="CANONICAL")
        evidence_map = evidence_map or {}
        results = []
        for cc in canonicals:
            cap_id = cc.canonical_id
            ev = evidence_map.get(cap_id, {"has_evidence": False, "avg_confidence": 0.0, "avg_metric": 0.0})
            prev = cc.maturity_level if hasattr(cc, 'maturity_level') else ""
            assessment = self.reassess(cc, evidence_sufficiency=ev, previous_maturity=prev)
            results.append(assessment)
        return results

    @staticmethod
    def _score_to_level(score: float) -> str:
        if score >= 0.9:
            return "SOVEREIGN"
        elif score >= 0.7:
            return "ADVANCED"
        elif score >= 0.5:
            return "ESTABLISHED"
        elif score >= 0.3:
            return "DEVELOPING"
        else:
            return "EMERGING"
