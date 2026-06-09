import pytest

from learning.skill_evidence_policy import (
    GovernanceGateStatus,
    RiskClassification,
    SkillEvidencePolicy,
    SkillEvidencePolicyConfig,
    SkillEvidencePolicyError,
    SkillEvidenceResult,
)


GOVERNANCE = {
    "issue_id": "ISSUE-2026-0003",
    "actor": "Hermes",
    "reviewer": "Sage",
    "governance_valid": True,
    "source": "AgentMemoryClient",
    "timestamp": "2026-06-07T00:00:00Z",
}


def sample_lessons(count=3):
    contexts = ["planning", "incident response", "code review", "audit", "budget"]
    reviewers = ["Sage", "Hermes", "Janus", "Lang Lieu", "Yet Kieu"]
    sources = ["MemoryInterface", "AgentMemoryClient", "HermesAnalytics", "JanusCoordination", "SageAudit"]
    dataset_sets = [["DS-1", "DS-2"], ["DS-3", "DS-4"], ["DS-5"], ["DS-6", "DS-7"], ["DS-8"]]
    return [
        {
            "lesson_id": f"LESSON-{i:03d}",
            "source": sources[i % len(sources)],
            "author": "Hermes",
            "reviewer": reviewers[i % len(reviewers)],
            "status": "APPROVED",
            "context": contexts[i % len(contexts)],
            "outcome": "safe recommendation",
            "evidence": [
                {"evidence_id": f"EV-{i:03d}-01", "confidence": 0.9, "success": True, "dataset_refs": dataset_sets[i % len(dataset_sets)]},
                {"evidence_id": f"EV-{i:03d}-02", "confidence": 0.8, "success": True, "dataset_refs": dataset_sets[(i + 1) % len(dataset_sets)]},
            ],
        }
        for i in range(count)
    ]


def test_risk_classification_enum_values():
    assert RiskClassification.LOW.value == "LOW"
    assert RiskClassification.MEDIUM.value == "MEDIUM"
    assert RiskClassification.HIGH.value == "HIGH"
    assert RiskClassification.SOVEREIGN.value == "SOVEREIGN"


def test_governance_gate_status_enum_values():
    assert GovernanceGateStatus.NOT_READY.value == "NOT_READY"
    assert GovernanceGateStatus.EVIDENCE_REVIEW.value == "EVIDENCE_REVIEW"
    assert GovernanceGateStatus.SAGE_RISK_REVIEW.value == "SAGE_RISK_REVIEW"
    assert GovernanceGateStatus.JANUS_COORDINATION.value == "JANUS_COORDINATION"
    assert GovernanceGateStatus.HUNG_VUONG_APPROVAL.value == "HUNG_VUONG_APPROVAL"
    assert GovernanceGateStatus.APPROVED.value == "APPROVED"
    assert GovernanceGateStatus.BLOCKED.value == "BLOCKED"


def test_evaluates_skill_evidence_with_advisory_result():
    policy = SkillEvidencePolicy()
    result = policy.evaluate(sample_lessons(3), GOVERNANCE)

    assert isinstance(result, SkillEvidenceResult)
    assert result.evidence_met is True
    assert result.lesson_count == 3
    assert result.source_diversity > 0
    assert result.dataset_diversity > 0
    assert result.context_diversity > 0
    assert result.reviewer_diversity > 0
    assert result.outcome_consistency > 0
    assert result.evidence_weight > 0
    assert result.confidence_score > 0
    assert result.risk_classification in RiskClassification
    assert result.governance_gate_status in GovernanceGateStatus
    assert result.promotion_trace_id != ""
    assert len(result.source_lessons) == 3
    assert result.evaluated_by == "Hermes"
    assert result.review_path in ("NORMAL", "SOVEREIGN")
    assert result.authority_basis != ""


def test_evidence_model_fields_present():
    policy = SkillEvidencePolicy()
    result = policy.evaluate(sample_lessons(3), GOVERNANCE)

    assert hasattr(result, "lesson_count")
    assert hasattr(result, "source_diversity")
    assert hasattr(result, "dataset_diversity")
    assert hasattr(result, "context_diversity")
    assert hasattr(result, "reviewer_diversity")
    assert hasattr(result, "outcome_consistency")
    assert hasattr(result, "evidence_weight")
    assert hasattr(result, "sovereign_asset_impact")


def test_promotion_audit_trail_fields_present():
    policy = SkillEvidencePolicy()
    result = policy.evaluate(sample_lessons(3), GOVERNANCE)

    assert hasattr(result, "promotion_trace_id")
    assert hasattr(result, "source_lessons")
    assert hasattr(result, "evidence_snapshot")
    assert hasattr(result, "decision_reason")
    assert hasattr(result, "evaluated_by")
    assert hasattr(result, "evaluated_at")
    assert hasattr(result, "review_path")
    assert hasattr(result, "authority_basis")

    assert isinstance(result.promotion_trace_id, str)
    assert isinstance(result.source_lessons, list)
    assert isinstance(result.evidence_snapshot, dict)
    assert isinstance(result.decision_reason, str)
    assert isinstance(result.evaluated_by, str)
    assert isinstance(result.evaluated_at, str)
    assert isinstance(result.review_path, str)
    assert isinstance(result.authority_basis, str)


def test_rejects_missing_governance_context():
    with pytest.raises(SkillEvidencePolicyError, match="governance context is required"):
        SkillEvidencePolicy().evaluate(sample_lessons(3), {})


def test_rejects_invalid_governance_context():
    governance = dict(GOVERNANCE)
    governance["governance_valid"] = False
    with pytest.raises(SkillEvidencePolicyError, match="governance context is invalid"):
        SkillEvidencePolicy().evaluate(sample_lessons(3), governance)


def test_rejects_missing_issue_id():
    governance = dict(GOVERNANCE)
    governance["issue_id"] = ""
    with pytest.raises(SkillEvidencePolicyError, match="issue_id is required"):
        SkillEvidencePolicy().evaluate(sample_lessons(3), governance)


def test_rejects_empty_lessons():
    with pytest.raises(SkillEvidencePolicyError, match="at least one approved lesson is required"):
        SkillEvidencePolicy().evaluate([], GOVERNANCE)


def test_rejects_non_approved_lesson():
    lessons = sample_lessons(1)
    lessons[0]["status"] = "DRAFT"
    with pytest.raises(SkillEvidencePolicyError, match="status must be APPROVED"):
        SkillEvidencePolicy().evaluate(lessons, GOVERNANCE)


def test_blocked_result_is_structured():
    result = SkillEvidencePolicy().blocked_result("SKILL-999", "Sage review required")

    assert result.evidence_met is False
    assert result.governance_gate_status == GovernanceGateStatus.BLOCKED
    assert result.confidence_score == 0.0
    assert result.review_path == "BLOCKED"
    assert result.decision_reason == "Sage review required"


def test_meets_threshold_returns_true_for_valid():
    policy = SkillEvidencePolicy()
    result = policy.evaluate(sample_lessons(3), GOVERNANCE)
    assert policy.meets_threshold(result) is True


def test_meets_threshold_returns_false_for_blocked():
    result = SkillEvidencePolicy().blocked_result("SKILL-999", "blocked")
    assert SkillEvidencePolicy().meets_threshold(result) is False


def test_get_governance_gate_for_low_risk():
    gate = SkillEvidencePolicy().get_governance_gate(RiskClassification.LOW)
    assert gate == GovernanceGateStatus.EVIDENCE_REVIEW


def test_get_governance_gate_for_medium_risk():
    gate = SkillEvidencePolicy().get_governance_gate(RiskClassification.MEDIUM)
    assert gate == GovernanceGateStatus.JANUS_COORDINATION


def test_get_governance_gate_for_high_risk():
    gate = SkillEvidencePolicy().get_governance_gate(RiskClassification.HIGH)
    assert gate == GovernanceGateStatus.JANUS_COORDINATION


def test_get_governance_gate_for_sovereign_risk():
    gate = SkillEvidencePolicy().get_governance_gate(RiskClassification.SOVEREIGN)
    assert gate == GovernanceGateStatus.HUNG_VUONG_APPROVAL


def test_sovereign_asset_impact_triggers_sovereign_risk():
    lessons = sample_lessons(5)
    lessons[0]["context"] = "constitutional review of risk kernel"
    result = SkillEvidencePolicy().evaluate(lessons, GOVERNANCE)

    assert result.sovereign_asset_impact is True
    assert result.risk_classification == RiskClassification.SOVEREIGN
    assert result.review_path == "SOVEREIGN"
    assert result.governance_gate_status == GovernanceGateStatus.HUNG_VUONG_APPROVAL


def test_to_dict_serializes_all_fields():
    result = SkillEvidencePolicy().evaluate(sample_lessons(3), GOVERNANCE)
    d = result.to_dict()

    assert isinstance(d, dict)
    assert d["skill_candidate_id"] == result.skill_candidate_id
    assert d["evidence_met"] == result.evidence_met
    assert d["risk_classification"] == result.risk_classification.value
    assert d["governance_gate_status"] == result.governance_gate_status.value
    assert d["promotion_trace_id"] == result.promotion_trace_id
    assert d["decision_reason"] == result.decision_reason
    assert d["review_path"] == result.review_path


def test_insufficient_lessons_fails_threshold():
    policy = SkillEvidencePolicy(SkillEvidencePolicyConfig(minimum_lessons=5))
    result = policy.evaluate(sample_lessons(3), GOVERNANCE)

    assert result.evidence_met is False
    assert result.governance_gate_status == GovernanceGateStatus.NOT_READY
    assert result.review_path == "BLOCKED"


def test_source_diversity_increases_with_more_sources():
    low_diversity = sample_lessons(3)
    for lesson in low_diversity:
        lesson["source"] = "SameSource"

    high_diversity = sample_lessons(3)

    low_result = SkillEvidencePolicy().evaluate(low_diversity, GOVERNANCE)
    high_result = SkillEvidencePolicy().evaluate(high_diversity, GOVERNANCE)

    assert high_result.source_diversity > low_result.source_diversity


def test_outcome_consistency_reflects_evidence_success():
    lessons = sample_lessons(3)
    for lesson in lessons:
        for ev in lesson["evidence"]:
            ev["success"] = True

    consistent = SkillEvidencePolicy().evaluate(lessons, GOVERNANCE)

    for lesson in lessons:
        for ev in lesson["evidence"]:
            ev["success"] = False
    inconsistent = SkillEvidencePolicy().evaluate(lessons, GOVERNANCE)

    assert consistent.outcome_consistency > inconsistent.outcome_consistency


def test_coverage_gaps_detected_when_threshold_not_met():
    lessons = sample_lessons(3)
    for lesson in lessons:
        lesson["source"] = "SameSource"
        lesson["reviewer"] = "SameReviewer"
        lesson["context"] = "SameContext"

    result = SkillEvidencePolicy().evaluate(lessons, GOVERNANCE)
    assert len(result.coverage_gaps) > 0


def test_evidence_weight_formula():
    policy = SkillEvidencePolicy()
    result = policy.evaluate(sample_lessons(3), GOVERNANCE)

    assert 0.0 <= result.evidence_weight <= 5.0
    assert result.evidence_weight == result.confidence_score


def test_custom_config_affects_minimum_lessons():
    config = SkillEvidencePolicyConfig(minimum_lessons=10, high_risk_minimum_lessons=15)
    policy = SkillEvidencePolicy(config)
    result = policy.evaluate(sample_lessons(3), GOVERNANCE)

    assert result.evidence_met is False
    assert "lessons=" in result.decision_reason
