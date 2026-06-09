from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

PROMOTION_OUTCOMES = {"PROMOTION_READY", "NEEDS_EVIDENCE", "NEEDS_REVIEW", "NOT_READY", "ARCHIVE_ONLY"}


@dataclass
class PromotionReadiness:
    capability_id: str
    capability_name: str
    domain: str = ""
    decision: str = "NOT_READY"
    reason: str = ""
    evidence_score: float = 0.0
    validation_score: float = 0.0
    skill_support_score: float = 0.0
    trace_support_score: float = 0.0
    governance_score: float = 0.0
    risk_score: float = 0.0
    maturity_score: float = 0.0
    reuse_score: float = 0.0
    hermes_outcome: str = ""
    hermes_reviewer: str = ""
    sage_outcome: str = ""
    sage_reviewer: str = ""


class CapabilityPromotionReadinessEngine:
    """Reassesses promotion readiness with evidence and validation results."""

    def __init__(self, capability_registry, canonical_registry,
                 promotion_registry, evidence_registry=None):
        self.capability_registry = capability_registry
        self.canonical_registry = canonical_registry
        self.promotion_registry = promotion_registry
        self.evidence_registry = evidence_registry

    def assess(self, canonical_capability: Any,
               maturity_reassessment: Any = None,
               evidence_sufficiency: dict[str, Any] | None = None,
               hermes_review: Any = None,
               sage_review: Any = None,
               recommender: str = "Hermes",
               reviewer: str = "Hung Vuong") -> PromotionReadiness:
        cap_id = getattr(canonical_capability, 'canonical_id', '')
        name = getattr(canonical_capability, 'name', '')
        domain = getattr(canonical_capability, 'domain', '')
        conf = getattr(canonical_capability, 'confidence_score', 0.0)
        risk_level = getattr(canonical_capability, 'risk_level', 'LEVEL_1_MODERATE')
        source_caps = getattr(canonical_capability, 'source_capability_ids', [])

        ev_score = evidence_sufficiency.get("avg_confidence", 0.0) if evidence_sufficiency and evidence_sufficiency.get("has_evidence") else 0.0
        val_score = evidence_sufficiency.get("avg_metric", 0.0) if evidence_sufficiency and evidence_sufficiency.get("has_evidence") else 0.0
        skill_score = min(conf + 0.1, 1.0)
        trace_score = min(len(source_caps) * 0.15, 1.0)
        gov_score = maturity_reassessment.governance_confidence if maturity_reassessment else conf
        risk_map = {"LEVEL_0_SOVEREIGN": 1.0, "LEVEL_1_MODERATE": 0.8, "LEVEL_2_HIGH": 0.4, "LEVEL_3_CRITICAL": 0.1}
        risk_score = risk_map.get(risk_level, 0.5)
        mat_score = maturity_reassessment.maturity_score if maturity_reassessment else 0.3
        reuse_score = maturity_reassessment.reuse_value if maturity_reassessment else 0.3

        hermes_outcome = getattr(hermes_review, 'outcome', '') if hermes_review else ""
        sage_outcome = getattr(sage_review, 'outcome', '') if sage_review else ""

        decision, reason = self._decide(
            ev_score=ev_score, val_score=val_score, skill_score=skill_score,
            gov_score=gov_score, risk_score=risk_score, mat_score=mat_score,
            hermes_outcome=hermes_outcome, sage_outcome=sage_outcome,
        )

        return PromotionReadiness(
            capability_id=cap_id,
            capability_name=name,
            domain=domain,
            decision=decision,
            reason=reason,
            evidence_score=round(ev_score, 2),
            validation_score=round(val_score, 2),
            skill_support_score=round(skill_score, 2),
            trace_support_score=round(trace_score, 2),
            governance_score=round(gov_score, 2),
            risk_score=round(risk_score, 2),
            maturity_score=round(mat_score, 2),
            reuse_score=round(reuse_score, 2),
            hermes_outcome=hermes_outcome,
            hermes_reviewer=getattr(hermes_review, 'reviewer', '') if hermes_review else "",
            sage_outcome=sage_outcome,
            sage_reviewer=getattr(sage_review, 'reviewer', '') if sage_review else "",
        )

    def assess_all(self, maturity_results: list | None = None,
                   evidence_map: dict[str, dict[str, Any]] | None = None,
                   hermes_reviews: dict[str, Any] | None = None,
                   sage_reviews: dict[str, Any] | None = None,
                   recommender: str = "Hermes",
                   reviewer: str = "Hung Vuong") -> list[PromotionReadiness]:
        canonicals = self.canonical_registry.list_all(classification="CANONICAL")
        evidence_map = evidence_map or {}
        hermes_reviews = hermes_reviews or {}
        sage_reviews = sage_reviews or {}
        mat_map = {}
        if maturity_results:
            mat_map = {m.capability_id: m for m in maturity_results}
        results = []
        for cc in canonicals:
            cap_id = cc.canonical_id
            mat = mat_map.get(cap_id)
            ev = evidence_map.get(cap_id, {"has_evidence": False, "avg_confidence": 0.0, "avg_metric": 0.0})
            hr = hermes_reviews.get(cap_id)
            sr = sage_reviews.get(cap_id)
            pr = self.assess(cc, maturity_reassessment=mat, evidence_sufficiency=ev,
                             hermes_review=hr, sage_review=sr,
                             recommender=recommender, reviewer=reviewer)
            results.append(pr)
        return results

    @staticmethod
    def _decide(ev_score: float, val_score: float, skill_score: float,
                gov_score: float, risk_score: float, mat_score: float,
                hermes_outcome: str = "", sage_outcome: str = "") -> tuple[str, str]:
        if hermes_outcome == "RECOMMEND_REJECT":
            return "NOT_READY", "Rejected by Hermes quality review"
        if hermes_outcome == "RECOMMEND_ARCHIVE":
            return "ARCHIVE_ONLY", "Recommended for archive by Hermes"
        if sage_outcome == "GOVERNANCE_REJECT":
            return "NOT_READY", "Rejected by Sage governance review"
        if sage_outcome == "GOVERNANCE_ARCHIVE":
            return "ARCHIVE_ONLY", "Recommended for archive by Sage"

        if skill_score >= 0.7 and ev_score >= 0.6 and val_score >= 0.6 and risk_score >= 0.5 and mat_score >= 0.5:
            if hermes_outcome in ("RECOMMEND_PROMOTION", "") and sage_outcome in ("GOVERNANCE_APPROVED_FOR_PROMOTION", ""):
                return "PROMOTION_READY", "All readiness criteria met"
            if hermes_outcome == "NEEDS_MORE_EVIDENCE":
                return "NEEDS_EVIDENCE", "Hermes requires more evidence"
            return "NEEDS_REVIEW", "Awaiting Hermes/Sage review outcomes"

        if skill_score >= 0.5 and ev_score >= 0.3:
            return "NEEDS_REVIEW", f"Partial readiness — skill={skill_score}, evidence={ev_score}"
        if ev_score >= 0.3:
            return "NEEDS_EVIDENCE", f"Evidence={ev_score} — needs more validation evidence"
        return "NOT_READY", f"Evidence={ev_score}, maturity={mat_score} — not ready for promotion"
