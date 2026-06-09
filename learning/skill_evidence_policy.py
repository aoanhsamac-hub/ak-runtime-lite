from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Mapping, Sequence
from uuid import uuid4


class SkillEvidencePolicyError(ValueError):
    """Raised when skill evidence policy violates AK governance contracts."""


class RiskClassification(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    SOVEREIGN = "SOVEREIGN"


class GovernanceGateStatus(Enum):
    NOT_READY = "NOT_READY"
    EVIDENCE_REVIEW = "EVIDENCE_REVIEW"
    SAGE_RISK_REVIEW = "SAGE_RISK_REVIEW"
    JANUS_COORDINATION = "JANUS_COORDINATION"
    HUNG_VUONG_APPROVAL = "HUNG_VUONG_APPROVAL"
    APPROVED = "APPROVED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class SkillEvidenceResult:
    skill_candidate_id: str
    evidence_met: bool
    lesson_count: int
    source_diversity: float
    dataset_diversity: float
    context_diversity: float
    reviewer_diversity: float
    outcome_consistency: float
    evidence_weight: float
    sovereign_asset_impact: bool
    quality_threshold: float
    coverage_gaps: Sequence[str]
    risk_classification: RiskClassification
    governance_gate_status: GovernanceGateStatus
    confidence_score: float
    promotion_trace_id: str
    source_lessons: Sequence[str]
    evidence_snapshot: Mapping[str, object]
    decision_reason: str
    evaluated_by: str
    evaluated_at: str
    review_path: str
    authority_basis: str

    def to_dict(self) -> dict[str, object]:
        return {
            "skill_candidate_id": self.skill_candidate_id,
            "evidence_met": self.evidence_met,
            "lesson_count": self.lesson_count,
            "source_diversity": self.source_diversity,
            "dataset_diversity": self.dataset_diversity,
            "context_diversity": self.context_diversity,
            "reviewer_diversity": self.reviewer_diversity,
            "outcome_consistency": self.outcome_consistency,
            "evidence_weight": self.evidence_weight,
            "sovereign_asset_impact": self.sovereign_asset_impact,
            "quality_threshold": self.quality_threshold,
            "coverage_gaps": list(self.coverage_gaps),
            "risk_classification": self.risk_classification.value,
            "governance_gate_status": self.governance_gate_status.value,
            "confidence_score": self.confidence_score,
            "promotion_trace_id": self.promotion_trace_id,
            "source_lessons": list(self.source_lessons),
            "evidence_snapshot": dict(self.evidence_snapshot),
            "decision_reason": self.decision_reason,
            "evaluated_by": self.evaluated_by,
            "evaluated_at": self.evaluated_at,
            "review_path": self.review_path,
            "authority_basis": self.authority_basis,
        }


@dataclass(frozen=True)
class SkillEvidencePolicyConfig:
    precision: int = 4
    minimum_lessons: int = 3
    high_risk_minimum_lessons: int = 5
    sovereign_asset_domains: tuple[str, ...] = (
        "constitution",
        "risk_kernel",
        "security_law",
        "execution_law",
        "state_corpus",
        "governance",
    )


class SkillEvidenceValidationLayer:
    REQUIRED_LESSON_FIELDS = ("lesson_id", "source", "author", "reviewer", "status", "evidence")

    def validate_governance(self, context: Mapping[str, object]) -> None:
        if not context:
            raise SkillEvidencePolicyError("governance context is required")
        if context.get("governance_valid") is not True:
            raise SkillEvidencePolicyError("governance context is invalid")
        if not str(context.get("issue_id", "")).strip():
            raise SkillEvidencePolicyError("issue_id is required for WP3.5 skill evidence policy")
        if not str(context.get("reviewer", "")).strip():
            raise SkillEvidencePolicyError("reviewer is required for WP3.5 skill evidence policy")

    def validate_approved_lessons(self, lessons: Sequence[Mapping[str, object]]) -> None:
        if not lessons:
            raise SkillEvidencePolicyError("at least one approved lesson is required")
        for index, lesson in enumerate(lessons):
            missing = [f for f in self.REQUIRED_LESSON_FIELDS if f not in lesson]
            if missing:
                raise SkillEvidencePolicyError(f"lesson {index} missing fields: {', '.join(missing)}")
            status = str(lesson.get("status", "")).upper()
            if status != "APPROVED":
                raise SkillEvidencePolicyError(f"lesson {index} status must be APPROVED, got {status}")


class SkillEvidencePolicy:
    def __init__(self, config: SkillEvidencePolicyConfig | None = None, validator: SkillEvidenceValidationLayer | None = None):
        self.config = config or SkillEvidencePolicyConfig()
        self.validator = validator or SkillEvidenceValidationLayer()
        self._evaluated_by: str = ""

    def evaluate(
        self,
        approved_lessons: Sequence[Mapping[str, object]],
        governance: Mapping[str, object],
    ) -> SkillEvidenceResult:
        self.validator.validate_governance(governance)
        self.validator.validate_approved_lessons(approved_lessons)
        self._evaluated_by = str(governance.get("actor", "Hermes"))
        evaluated_at = str(governance.get("timestamp", datetime.now(timezone.utc).isoformat()))
        issue_id = str(governance.get("issue_id", ""))
        reviewer = str(governance.get("reviewer", ""))

        lesson_count = len(approved_lessons)
        source_diversity = self._compute_source_diversity(approved_lessons)
        dataset_diversity = self._compute_dataset_diversity(approved_lessons)
        context_diversity = self._compute_context_diversity(approved_lessons)
        reviewer_diversity = self._compute_reviewer_diversity(approved_lessons)
        outcome_consistency = self._compute_outcome_consistency(approved_lessons)
        evidence_weight = self._compute_evidence_weight(source_diversity, dataset_diversity, context_diversity, reviewer_diversity, outcome_consistency)
        sovereign_asset_impact = self._check_sovereign_assets(approved_lessons)
        risk_classification = self._classify_risk(sovereign_asset_impact, evidence_weight, lesson_count)
        coverage_gaps = self._find_coverage_gaps(approved_lessons, risk_classification)
        source_lesson_ids = [str(lesson.get("lesson_id", "")) for lesson in approved_lessons]

        quality_threshold = 3.0
        evidence_met = self._check_evidence_met(
            lesson_count, source_diversity, dataset_diversity,
            context_diversity, reviewer_diversity, outcome_consistency,
            evidence_weight, risk_classification,
        )
        confidence_score = self._round(evidence_weight)

        promotion_trace_id = str(uuid4())
        evidence_snapshot = {
            "lesson_count": lesson_count,
            "source_diversity": source_diversity,
            "dataset_diversity": dataset_diversity,
            "context_diversity": context_diversity,
            "reviewer_diversity": reviewer_diversity,
            "outcome_consistency": outcome_consistency,
            "evidence_weight": evidence_weight,
            "sovereign_asset_impact": sovereign_asset_impact,
        }

        if not evidence_met:
            governance_gate_status = GovernanceGateStatus.NOT_READY
            decision_reason = self._build_fail_reason(
                lesson_count, source_diversity, dataset_diversity, context_diversity,
                reviewer_diversity, outcome_consistency, evidence_weight, risk_classification,
            )
            review_path = "BLOCKED"
            authority_basis = "Threshold not met; refer to Evidence Policy Design and Risk Classification"
        else:
            governance_gate_status = self._resolve_gate_status(risk_classification)
            if risk_classification == RiskClassification.SOVEREIGN:
                review_path = "SOVEREIGN"
                authority_basis = "Article 27 Constitution; Security Law Article 21-23; Risk Law"
            else:
                review_path = "NORMAL"
                authority_basis = "Evidence Policy Design; Promotion Governance Model"

            decision_reason = f"Evidence threshold met for {risk_classification.value} risk: evidence_weight={evidence_weight}"

        return SkillEvidenceResult(
            skill_candidate_id=f"SKILL-{promotion_trace_id[:8].upper()}",
            evidence_met=evidence_met,
            lesson_count=lesson_count,
            source_diversity=self._round(source_diversity),
            dataset_diversity=self._round(dataset_diversity),
            context_diversity=self._round(context_diversity),
            reviewer_diversity=self._round(reviewer_diversity),
            outcome_consistency=self._round(outcome_consistency),
            evidence_weight=self._round(evidence_weight),
            sovereign_asset_impact=sovereign_asset_impact,
            quality_threshold=quality_threshold,
            coverage_gaps=coverage_gaps,
            risk_classification=risk_classification,
            governance_gate_status=governance_gate_status,
            confidence_score=confidence_score,
            promotion_trace_id=promotion_trace_id,
            source_lessons=source_lesson_ids,
            evidence_snapshot=evidence_snapshot,
            decision_reason=decision_reason,
            evaluated_by=self._evaluated_by,
            evaluated_at=evaluated_at,
            review_path=review_path,
            authority_basis=authority_basis,
        )

    def meets_threshold(self, result: SkillEvidenceResult) -> bool:
        return result.evidence_met and result.governance_gate_status != GovernanceGateStatus.BLOCKED

    def get_governance_gate(self, risk_class: RiskClassification) -> GovernanceGateStatus:
        return self._resolve_gate_status(risk_class)

    def blocked_result(self, skill_candidate_id: str, reason: str) -> SkillEvidenceResult:
        trace_id = str(uuid4())
        return SkillEvidenceResult(
            skill_candidate_id=skill_candidate_id,
            evidence_met=False,
            lesson_count=0,
            source_diversity=0.0,
            dataset_diversity=0.0,
            context_diversity=0.0,
            reviewer_diversity=0.0,
            outcome_consistency=0.0,
            evidence_weight=0.0,
            sovereign_asset_impact=False,
            quality_threshold=3.0,
            coverage_gaps=["no evidence provided"],
            risk_classification=RiskClassification.LOW,
            governance_gate_status=GovernanceGateStatus.BLOCKED,
            confidence_score=0.0,
            promotion_trace_id=trace_id,
            source_lessons=[],
            evidence_snapshot={"blocked": True, "reason": reason},
            decision_reason=reason,
            evaluated_by=self._evaluated_by or "system",
            evaluated_at=datetime.now(timezone.utc).isoformat(),
            review_path="BLOCKED",
            authority_basis="Blocked by SkillEvidencePolicy",
        )

    def _compute_source_diversity(self, lessons: Sequence[Mapping[str, object]]) -> float:
        sources = {str(lesson.get("source", "")).strip().lower() for lesson in lessons if str(lesson.get("source", "")).strip()}
        if not sources:
            return 0.0
        return len(sources) / len(lessons)

    def _compute_dataset_diversity(self, lessons: Sequence[Mapping[str, object]]) -> float:
        all_refs: set[str] = set()
        for lesson in lessons:
            evidence_list = lesson.get("evidence", [])
            if isinstance(evidence_list, list):
                for ev in evidence_list:
                    refs = ev.get("dataset_refs", []) if isinstance(ev, dict) else []
                    if isinstance(refs, list):
                        all_refs.update(str(r) for r in refs if str(r).strip())
        if not all_refs or not lessons:
            return 0.0
        return min(1.0, len(all_refs) / max(1, len(lessons)))

    def _compute_context_diversity(self, lessons: Sequence[Mapping[str, object]]) -> float:
        contexts = {str(lesson.get("context", "")).strip().lower() for lesson in lessons if str(lesson.get("context", "")).strip()}
        if not contexts:
            return 0.0
        return len(contexts) / len(lessons)

    def _compute_reviewer_diversity(self, lessons: Sequence[Mapping[str, object]]) -> float:
        reviewers = {str(lesson.get("reviewer", "")).strip().lower() for lesson in lessons if str(lesson.get("reviewer", "")).strip()}
        if not reviewers:
            return 0.0
        return len(reviewers) / len(lessons)

    def _compute_outcome_consistency(self, lessons: Sequence[Mapping[str, object]]) -> float:
        outcomes = []
        for lesson in lessons:
            evidence_list = lesson.get("evidence", [])
            if isinstance(evidence_list, list):
                for ev in evidence_list:
                    if isinstance(ev, dict) and isinstance(ev.get("success"), bool):
                        outcomes.append(ev["success"])
        if not outcomes:
            return 0.0
        positive = sum(1 for o in outcomes if o)
        return positive / len(outcomes)

    def _compute_evidence_weight(self, source_d: float, dataset_d: float, context_d: float, reviewer_d: float, outcome_c: float) -> float:
        source_score = min(5.0, source_d * 5)
        dataset_score = min(5.0, dataset_d * 5)
        context_score = min(5.0, context_d * 5)
        reviewer_score = min(5.0, reviewer_d * 5)
        outcome_score = min(5.0, outcome_c * 5)
        return self._round(
            source_score * 0.20 +
            dataset_score * 0.20 +
            context_score * 0.20 +
            reviewer_score * 0.20 +
            outcome_score * 0.20
        )

    def _check_sovereign_assets(self, lessons: Sequence[Mapping[str, object]]) -> bool:
        for lesson in lessons:
            context = str(lesson.get("context", "")).strip().lower()
            for domain in self.config.sovereign_asset_domains:
                if domain in context:
                    return True
            outcome = str(lesson.get("outcome", "")).strip().lower()
            for domain in self.config.sovereign_asset_domains:
                if domain in outcome:
                    return True
        return False

    def _classify_risk(self, sovereign_asset_impact: bool, evidence_weight: float, lesson_count: int) -> RiskClassification:
        if sovereign_asset_impact:
            return RiskClassification.SOVEREIGN
        if evidence_weight >= 4.0 and lesson_count >= self.config.high_risk_minimum_lessons:
            return RiskClassification.HIGH
        if evidence_weight >= 3.5:
            return RiskClassification.MEDIUM
        if evidence_weight >= 3.0:
            return RiskClassification.MEDIUM
        if evidence_weight >= 2.5:
            return RiskClassification.LOW
        return RiskClassification.LOW

    def _find_coverage_gaps(self, lessons: Sequence[Mapping[str, object]], risk_class: RiskClassification) -> list[str]:
        gaps: list[str] = []
        source_d = self._compute_source_diversity(lessons)
        dataset_d = self._compute_dataset_diversity(lessons)
        context_d = self._compute_context_diversity(lessons)
        reviewer_d = self._compute_reviewer_diversity(lessons)
        outcome_c = self._compute_outcome_consistency(lessons)

        thresholds = self._get_thresholds(risk_class)
        if source_d < thresholds["source_diversity"]:
            gaps.append(f"source_diversity ({source_d}) < threshold ({thresholds['source_diversity']})")
        if dataset_d < thresholds["dataset_diversity"]:
            gaps.append(f"dataset_diversity ({dataset_d}) < threshold ({thresholds['dataset_diversity']})")
        if context_d < thresholds["context_diversity"]:
            gaps.append(f"context_diversity ({context_d}) < threshold ({thresholds['context_diversity']})")
        if reviewer_d < thresholds["reviewer_diversity"]:
            gaps.append(f"reviewer_diversity ({reviewer_d}) < threshold ({thresholds['reviewer_diversity']})")
        if outcome_c < thresholds["outcome_consistency"]:
            gaps.append(f"outcome_consistency ({outcome_c}) < threshold ({thresholds['outcome_consistency']})")
        return gaps

    def _get_thresholds(self, risk_class: RiskClassification) -> dict[str, float]:
        thresholds = {
            RiskClassification.LOW: {"source_diversity": 0.3, "dataset_diversity": 0.3, "context_diversity": 0.4, "reviewer_diversity": 0.3, "outcome_consistency": 0.7},
            RiskClassification.MEDIUM: {"source_diversity": 0.4, "dataset_diversity": 0.4, "context_diversity": 0.5, "reviewer_diversity": 0.4, "outcome_consistency": 0.8},
            RiskClassification.HIGH: {"source_diversity": 0.5, "dataset_diversity": 0.5, "context_diversity": 0.6, "reviewer_diversity": 0.5, "outcome_consistency": 0.85},
            RiskClassification.SOVEREIGN: {"source_diversity": 0.6, "dataset_diversity": 0.6, "context_diversity": 0.7, "reviewer_diversity": 0.6, "outcome_consistency": 0.9},
        }
        return thresholds.get(risk_class, thresholds[RiskClassification.LOW])

    def _check_evidence_met(self, lesson_count: int, source_d: float, dataset_d: float, context_d: float, reviewer_d: float, outcome_c: float, evidence_weight: float, risk_class: RiskClassification) -> bool:
        thresholds = self._get_thresholds(risk_class)
        min_lessons = self.config.high_risk_minimum_lessons if risk_class in (RiskClassification.HIGH, RiskClassification.SOVEREIGN) else self.config.minimum_lessons
        if lesson_count < min_lessons:
            return False
        if source_d < thresholds["source_diversity"]:
            return False
        if dataset_d < thresholds["dataset_diversity"]:
            return False
        if context_d < thresholds["context_diversity"]:
            return False
        if reviewer_d < thresholds["reviewer_diversity"]:
            return False
        if outcome_c < thresholds["outcome_consistency"]:
            return False
        if evidence_weight < 2.5:
            return False
        return True

    def _resolve_gate_status(self, risk_class: RiskClassification) -> GovernanceGateStatus:
        if risk_class == RiskClassification.SOVEREIGN:
            return GovernanceGateStatus.HUNG_VUONG_APPROVAL
        if risk_class == RiskClassification.HIGH:
            return GovernanceGateStatus.JANUS_COORDINATION
        if risk_class == RiskClassification.MEDIUM:
            return GovernanceGateStatus.JANUS_COORDINATION
        return GovernanceGateStatus.EVIDENCE_REVIEW

    def _build_fail_reason(self, lesson_count: int, source_d: float, dataset_d: float, context_d: float, reviewer_d: float, outcome_c: float, evidence_weight: float, risk_class: RiskClassification) -> str:
        parts = [f"risk={risk_class.value}"]
        min_lessons = self.config.high_risk_minimum_lessons if risk_class in (RiskClassification.HIGH, RiskClassification.SOVEREIGN) else self.config.minimum_lessons
        if lesson_count < min_lessons:
            parts.append(f"lessons={lesson_count}<{min_lessons}")
        thresholds = self._get_thresholds(risk_class)
        if source_d < thresholds["source_diversity"]:
            parts.append(f"source_diversity={source_d}")
        if dataset_d < thresholds["dataset_diversity"]:
            parts.append(f"dataset_diversity={dataset_d}")
        if context_d < thresholds["context_diversity"]:
            parts.append(f"context_diversity={context_d}")
        if reviewer_d < thresholds["reviewer_diversity"]:
            parts.append(f"reviewer_diversity={reviewer_d}")
        if outcome_c < thresholds["outcome_consistency"]:
            parts.append(f"outcome_consistency={outcome_c}")
        if evidence_weight < 2.5:
            parts.append(f"evidence_weight={evidence_weight}<2.5")
        return f"Evidence threshold not met: {'; '.join(parts)}"

    def _round(self, value: float) -> float:
        return round(float(value), self.config.precision)
