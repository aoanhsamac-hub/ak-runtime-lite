import pytest

from learning.learning_metrics import (
    LearningMetrics,
    LearningMetricsValidationError,
    MetricsCalculator,
    MetricsCalculatorConfig,
)


GOVERNANCE = {
    "issue_id": "ISSUE-2026-0001",
    "actor": "Hermes",
    "reviewer": "Sage",
    "risk_level": "LEVEL_1_MODERATE",
    "governance_valid": True,
    "source": "AgentMemoryClient",
}


def sample_records():
    return [
        {
            "evidence_id": "EV-001",
            "context": "protected planning",
            "outcome": "safe recommendation",
            "success": True,
            "confidence": 0.9,
            "dataset_refs": ["DS-1"],
        },
        {
            "evidence_id": "EV-002",
            "context": "protected planning",
            "outcome": "safe recommendation",
            "success": True,
            "confidence": 0.8,
            "dataset_refs": ["DS-1", "DS-2"],
        },
        {
            "evidence_id": "EV-003",
            "context": "audit planning",
            "outcome": "safe recommendation",
            "success": False,
            "confidence": 0.7,
            "dataset_refs": [],
        },
    ]


class EvidenceProviderStub:
    def evidence_records(self):
        return sample_records()


def test_calculates_learning_metrics_deterministically():
    metrics = MetricsCalculator().calculate(sample_records(), GOVERNANCE)

    assert isinstance(metrics, LearningMetrics)
    assert metrics.recurrence_count == 3
    assert metrics.evidence_count == 3
    assert metrics.success_rate == pytest.approx(0.6667)
    assert metrics.context_diversity == pytest.approx(0.6667)
    assert metrics.outcome_stability == pytest.approx(1.0)
    assert metrics.dataset_support == pytest.approx(0.6667)
    assert metrics.confidence_score == pytest.approx(0.7967)
    assert metrics.blocked is False


def test_accepts_typed_evidence_provider_interface():
    metrics = MetricsCalculator().calculate(EvidenceProviderStub(), GOVERNANCE)

    assert metrics.recurrence_count == 3
    assert metrics.metadata["source"] == "AgentMemoryClient"


def test_rejects_missing_governance_context():
    with pytest.raises(LearningMetricsValidationError, match="governance context is required"):
        MetricsCalculator().calculate(sample_records(), {})


def test_rejects_invalid_governance_context():
    governance = dict(GOVERNANCE)
    governance["governance_valid"] = False

    with pytest.raises(LearningMetricsValidationError, match="governance context is invalid"):
        MetricsCalculator().calculate(sample_records(), governance)


def test_rejects_missing_issue_id_for_non_bypass_governance():
    governance = dict(GOVERNANCE)
    governance["issue_id"] = ""

    with pytest.raises(LearningMetricsValidationError, match="issue_id is required"):
        MetricsCalculator().calculate(sample_records(), governance)


def test_rejects_invalid_record_confidence():
    records = sample_records()
    records[0]["confidence"] = 1.5

    with pytest.raises(LearningMetricsValidationError, match="between 0 and 1"):
        MetricsCalculator().calculate(records, GOVERNANCE)


def test_blocked_result_is_structured_and_non_executing():
    result = MetricsCalculator().blocked_result("Sage review required")

    assert result.blocked is True
    assert result.reason == "Sage review required"
    assert result.to_dict()["confidence_score"] == 0.0


def test_custom_minimum_evidence_affects_confidence_score():
    low_threshold = MetricsCalculator(MetricsCalculatorConfig(minimum_evidence=3)).calculate(sample_records(), GOVERNANCE)
    high_threshold = MetricsCalculator(MetricsCalculatorConfig(minimum_evidence=6)).calculate(sample_records(), GOVERNANCE)

    assert low_threshold.confidence_score > high_threshold.confidence_score
