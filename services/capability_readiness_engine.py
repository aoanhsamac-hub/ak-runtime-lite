from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from memory.capability_pipeline.schemas import READINESS_LEVELS


@dataclass
class ReadinessAssessment:
    capability_id: str
    capability_name: str
    decision: str
    reason: str
    evidence_score: float = 0.0
    confidence_score: float = 0.0
    governance_score: float = 0.0
    risk_score: float = 0.0
    maturity_score: float = 0.0
    reuse_score: float = 0.0


class CapabilityReadinessEngine:
    """Assesses promotion readiness of canonical capabilities."""

    def __init__(self, capability_registry, canonical_registry,
                 promotion_registry, maturity_assessments=None):
        self.capability_registry = capability_registry
        self.canonical_registry = canonical_registry
        self.promotion_registry = promotion_registry
        self.maturity_assessments = maturity_assessments or []

    def assess_all(self, recommender: str = "Hermes",
                   reviewer: str = "Hung Vuong",
                   owner_agent: str = "Sage") -> list:
        canonicals = self.canonical_registry.list_all(classification="CANONICAL")
        maturity_map = {a.capability_id: a for a in self.maturity_assessments}
        results = []

        for cc in canonicals:
            mat = maturity_map.get(cc.canonical_id)
            ev_score = min(len(cc.source_capability_ids) * 0.25, 1.0)
            conf_score = cc.confidence_score
            gov_score = mat.governance_confidence if mat else cc.confidence_score
            risk_map = {"LEVEL_0_SOVEREIGN": 0, "LEVEL_1_MODERATE": 1, "LEVEL_2_HIGH": 2, "LEVEL_3_CRITICAL": 3}
            risk_score = risk_map.get(cc.risk_level, 1)
            mat_score = mat.maturity_score if mat else 0.5
            reuse_score = mat.reuse_value if mat else 0.3

            decision, reason = self._decide(ev_score, conf_score, risk_score, mat_score)

            rec = self.promotion_registry.create(
                capability_id=cc.canonical_id,
                capability_name=cc.name,
                canonical_id=cc.canonical_id,
                recommender=recommender,
                reviewer=reviewer,
                decision=decision,
                reason=reason,
                evidence={
                    "evidence_score": ev_score,
                    "confidence_score": conf_score,
                    "governance_score": gov_score,
                    "risk_score": risk_score,
                    "maturity_score": mat_score,
                    "reuse_score": reuse_score,
                },
                risk_score=risk_score,
                governance_score=round(gov_score, 2),
                owner_agent=owner_agent,
            )
            results.append(ReadinessAssessment(
                capability_id=cc.canonical_id,
                capability_name=cc.name,
                decision=decision,
                reason=reason,
                evidence_score=ev_score,
                confidence_score=conf_score,
                governance_score=gov_score,
                risk_score=risk_score,
                maturity_score=mat_score,
                reuse_score=reuse_score,
            ))
        return results

    @staticmethod
    def _decide(ev_score: float, conf_score: float,
                risk_score: float, mat_score: float):
        if conf_score >= 0.70 and ev_score >= 0.5 and risk_score <= 2 and mat_score >= 0.5:
            return "PROMOTION_READY", "All readiness criteria met"
        if conf_score >= 0.50 and ev_score >= 0.3:
            return "NEEDS_REVIEW", f"Confidence={conf_score}, evidence={ev_score} — needs governance review"
        if ev_score >= 0.3:
            return "NEEDS_EVIDENCE", f"Evidence={ev_score}, confidence={conf_score} — needs more evidence"
        return "NOT_READY", f"Evidence={ev_score}, confidence={conf_score} — not ready"
