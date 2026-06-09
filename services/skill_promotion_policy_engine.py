from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


PROMOTION_OUTCOMES = {"APPROVED", "REJECTED", "NEEDS_REVIEW", "NEEDS_EVIDENCE", "ARCHIVED"}


@dataclass
class PolicyResult:
    decision: str
    reason: str
    risk_score: float = 0.0
    governance_score: float = 0.0
    passed_gates: list[str] = field(default_factory=list)
    failed_gates: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "reason": self.reason,
            "risk_score": self.risk_score,
            "governance_score": self.governance_score,
            "passed_gates": self.passed_gates,
            "failed_gates": self.failed_gates,
        }


class SkillPromotionPolicyEngine:
    """Evaluates a canonical skill against promotion policy rules."""

    MIN_CONFIDENCE = 0.70
    MIN_MATURITY_SCORE = 0.5
    MAX_RISK_SCORE = 2.0
    MIN_EVIDENCE_DEPTH = 2

    def evaluate(self, canonical: dict[str, Any], maturity: dict[str, Any] | None = None) -> PolicyResult:
        passed = []
        failed = []
        risk_score = 0.0

        conf = canonical.get("confidence_score", 0)
        if conf >= self.MIN_CONFIDENCE:
            passed.append("confidence_threshold")
        else:
            failed.append(f"confidence_threshold: {conf} < {self.MIN_CONFIDENCE}")

        risk_str = canonical.get("risk_level", "")
        risk_map = {"LEVEL_0_SOVEREIGN": 0, "LEVEL_1_MODERATE": 1, "LEVEL_2_HIGH": 2, "LEVEL_3_CRITICAL": 3}
        risk_score = risk_map.get(risk_str, 1)
        if risk_score <= self.MAX_RISK_SCORE:
            passed.append("risk_threshold")
        else:
            failed.append(f"risk_threshold: level={risk_str}, score={risk_score}")

        evidence = canonical.get("evidence", {}) or {}
        ev_depth = len(evidence) if isinstance(evidence, dict) else (1 if evidence else 0)
        if ev_depth >= self.MIN_EVIDENCE_DEPTH:
            passed.append("evidence_depth")
        else:
            failed.append(f"evidence_depth: {ev_depth} < {self.MIN_EVIDENCE_DEPTH}")

        classification = canonical.get("classification", "")
        if classification == "CANONICAL":
            passed.append("canonical_status")
        else:
            failed.append(f"canonical_status: {classification}")

        status = canonical.get("status", "")
        if status == "CANDIDATE":
            passed.append("candidate_status")
        else:
            failed.append(f"candidate_status: {status}")

        gov_score = 0.0
        if maturity:
            ms = maturity.get("maturity_score", 0)
            gov_score = maturity.get("governance_confidence", ms)
            if ms >= self.MIN_MATURITY_SCORE:
                passed.append("maturity_threshold")
            else:
                failed.append(f"maturity_threshold: {ms} < {self.MIN_MATURITY_SCORE}")
        else:
            passed.append("maturity_threshold")

        gov_score = max(gov_score, conf)
        all_pass = len(failed) == 0

        if all_pass:
            return PolicyResult(
                decision="APPROVED",
                reason="All promotion policy gates passed",
                risk_score=risk_score,
                governance_score=round(gov_score, 2),
                passed_gates=passed,
            )
        has_confidence = conf >= 0.5
        has_evidence = ev_depth >= 1
        if has_confidence and has_evidence:
            return PolicyResult(
                decision="NEEDS_REVIEW",
                reason=f"Failed gates: {'; '.join(failed)}",
                risk_score=risk_score,
                governance_score=round(gov_score, 2),
                passed_gates=passed,
                failed_gates=failed,
            )
        if has_evidence:
            return PolicyResult(
                decision="NEEDS_EVIDENCE",
                reason=f"Insufficient confidence/risk profile: {'; '.join(failed)}",
                risk_score=risk_score,
                governance_score=round(gov_score, 2),
                passed_gates=passed,
                failed_gates=failed,
            )
        return PolicyResult(
            decision="REJECTED",
            reason=f"Critical gates failed: {'; '.join(failed)}",
            risk_score=risk_score,
            governance_score=round(gov_score, 2),
            failed_gates=failed,
        )

    def evaluate_archival(self, canonical: dict[str, Any]) -> PolicyResult:
        classification = canonical.get("classification", "")
        conf = canonical.get("confidence_score", 0)
        if classification == "ISOLATED" and conf < 0.3:
            return PolicyResult(
                decision="ARCHIVED",
                reason="Isolated skill with very low confidence",
                risk_score=0, governance_score=0,
            )
        if classification in ("SUPERSEDED", "DUPLICATE"):
            return PolicyResult(
                decision="ARCHIVED",
                reason=f"Skill classified as {classification}",
                risk_score=0, governance_score=0,
            )
        return PolicyResult(decision="NEEDS_REVIEW", reason="Not eligible for archival")
