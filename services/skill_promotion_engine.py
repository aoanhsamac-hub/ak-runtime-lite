from __future__ import annotations

from typing import Any
from memory.learning_registry.schemas import PromotionDecisionRecord
from services.skill_promotion_policy_engine import SkillPromotionPolicyEngine, PolicyResult
from services.independent_review_gate import IndependentReviewGate


class SkillPromotionEngine:
    """Orchestrates promotion of canonical skills through policy + review + decision."""

    def __init__(self, candidate_skill_registry, canonical_registry,
                 approved_skill_registry, audit_layer, governance_gate=None):
        self.candidate_skill_registry = candidate_skill_registry
        self.canonical_registry = canonical_registry
        self.approved_skill_registry = approved_skill_registry
        self.audit_layer = audit_layer
        self.governance_gate = governance_gate
        self.policy_engine = SkillPromotionPolicyEngine()
        self.review_gate = IndependentReviewGate()
        self._decisions: list[PromotionDecisionRecord] = []

    def promote(self, canonical_id: str, recommender: str = "Hermes",
                reviewer: str = "Hung Vuong", maturity: dict[str, Any] | None = None,
                owner_agent: str = "Sage") -> dict[str, Any]:
        try:
            canon = self.canonical_registry.get(canonical_id)
        except KeyError:
            return {"error": f"canonical not found: {canonical_id}"}

        canon_dict = canon.to_dict()
        policy_result: PolicyResult = self.policy_engine.evaluate(canon_dict, maturity)
        if policy_result.decision != "APPROVED":
            return self._record_decision(canon, policy_result, recommender, reviewer, owner_agent)

        gov_pass = True
        if self.governance_gate:
            gov_report = self.governance_gate.evaluate_canonical(canon_dict)
            if not gov_report.all_passed:
                policy_result = PolicyResult(
                    decision="NEEDS_REVIEW",
                    reason=f"Governance gates failed: {gov_report.summary}",
                    risk_score=policy_result.risk_score,
                    governance_score=policy_result.governance_score,
                    passed_gates=policy_result.passed_gates,
                    failed_gates=[g.gate for g in gov_report.gates if not g.passed],
                )
                return self._record_decision(canon, policy_result, recommender, reviewer, owner_agent)

        review_rec = {
            "recommender": recommender,
            "reviewer": reviewer,
            "canonical_id": canonical_id,
            "policy_result": policy_result.to_dict(),
        }
        review_result = self.review_gate.validate(review_rec)
        if not review_result["passed"]:
            policy_result = PolicyResult(
                decision="NEEDS_REVIEW",
                reason=f"Independent review failed: {review_result['reason']}",
                risk_score=policy_result.risk_score,
                governance_score=policy_result.governance_score,
                passed_gates=policy_result.passed_gates,
                failed_gates=["independent_review"],
            )
            return self._record_decision(canon, policy_result, recommender, reviewer, owner_agent)

        drec = self._record_decision(canon, policy_result, recommender, reviewer, owner_agent)

        if drec["decision"] == "APPROVED":
            source_skills = [s for s in self.candidate_skill_registry.list_all()
                             if s.candidate_skill_id in canon.source_skill_ids]
            primary = source_skills[0] if source_skills else None
            approved = self.approved_skill_registry.approve(
                name=canon.name,
                description=canon.description,
                canonical_id=canon.canonical_id,
                candidate_skill_id=primary.candidate_skill_id if primary else "",
                family_id=canon.family_id,
                owner_agent=owner_agent,
                reviewer_agent=reviewer,
                approval_authority=reviewer,
                risk_level=canon.risk_level,
                confidence_score=canon.confidence_score,
                evidence=canon.evidence,
                tags=canon.tags,
                metadata={"recommender": recommender, "policy_version": "1.0"},
                promotion_decision_id=drec["decision_id"],
            )
            self.audit_layer.record(
                agent=owner_agent, action="SKILL_APPROVED",
                record_type="approved_skill",
                record_id=approved.approved_skill_id,
                details={"canonical_id": canonical_id, "decision_id": drec["decision_id"]},
            )

        return drec

    def _record_decision(self, canon, policy_result: PolicyResult,
                         recommender: str, reviewer: str, owner_agent: str) -> dict[str, Any]:
        drec = PromotionDecisionRecord(
            skill_id=canon.canonical_id,
            skill_name=canon.name,
            canonical_id=canon.canonical_id,
            reviewer=reviewer,
            decision=policy_result.decision,
            reason=policy_result.reason,
            evidence={
                "risk_score": policy_result.risk_score,
                "governance_score": policy_result.governance_score,
                "passed_gates": policy_result.passed_gates,
                "failed_gates": policy_result.failed_gates,
                "recommender": recommender,
            },
            risk_score=policy_result.risk_score,
            governance_score=policy_result.governance_score,
            owner_agent=owner_agent,
        )
        self._decisions.append(drec)
        self.audit_layer.record(
            agent=owner_agent, action="SKILL_PROMOTION_DECISION",
            record_type="promotion_decision",
            record_id=drec.decision_id,
            details={"canonical_id": canon.canonical_id, "decision": policy_result.decision},
        )
        return drec.to_dict()

    def promote_batch(self, canonical_ids: list[str], recommender: str = "Hermes",
                       reviewer: str = "Hung Vuong",
                       maturity_map: dict[str, dict[str, Any]] | None = None,
                       owner_agent: str = "Sage") -> list[dict[str, Any]]:
        results = []
        for cid in canonical_ids:
            mat = (maturity_map or {}).get(cid)
            results.append(self.promote(cid, recommender, reviewer, mat, owner_agent))
        return results

    def get_decisions(self) -> list[PromotionDecisionRecord]:
        return list(self._decisions)
