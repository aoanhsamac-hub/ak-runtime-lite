import pytest

from learning.lesson_evaluator import (
    InformationClassification,
    LessonEvaluation,
    LessonEvaluationError,
    LessonEvaluator,
    LessonEvaluatorConfig,
    LessonStatus,
)


GOVERNANCE = {
    "issue_id": "ISSUE-2026-0002",
    "reviewer": "Sage",
    "governance_valid": True,
    "source": "MemoryInterface",
    "timestamp": "2026-06-07T00:00:00Z",
}


def sample_lesson():
    return {
        "lesson_id": "LESSON-001",
        "context": "protected planning",
        "outcome": "safe recommendation",
        "status": "DRAFT",
        "evidence": [
            {"evidence_id": "EV-001", "confidence": 0.9, "success": True},
            {"evidence_id": "EV-002", "confidence": 0.8, "success": True},
        ],
    }


def test_lesson_status_enum_values():
    assert LessonStatus.DRAFT.value == "DRAFT"
    assert LessonStatus.REVIEWED.value == "REVIEWED"
    assert LessonStatus.APPROVED.value == "APPROVED"
    assert LessonStatus.DEPRECATED.value == "DEPRECATED"
    assert LessonStatus.QUARANTINE.value == "QUARANTINE"


def test_evaluates_lesson_with_advisory_result():
    evaluator = LessonEvaluator()
    result = evaluator.evaluate(sample_lesson(), GOVERNANCE)

    assert isinstance(result, LessonEvaluation)
    assert result.status == LessonStatus.DRAFT
    assert result.quality_score == pytest.approx(0.85)
    assert result.evidence_count == 2
    assert result.reviewer == "Sage"


def test_rejects_missing_governance_context():
    with pytest.raises(LessonEvaluationError, match="governance context is required"):
        LessonEvaluator().evaluate(sample_lesson(), {})


def test_rejects_invalid_governance_context():
    governance = dict(GOVERNANCE)
    governance["governance_valid"] = False

    with pytest.raises(LessonEvaluationError, match="governance context is invalid"):
        LessonEvaluator().evaluate(sample_lesson(), governance)


def test_rejects_lesson_missing_fields():
    lesson = {"lesson_id": "LESSON-002"}

    with pytest.raises(LessonEvaluationError, match="lesson missing fields"):
        LessonEvaluator().evaluate(lesson, GOVERNANCE)


def test_validates_status_transition():
    evaluator = LessonEvaluator()
    lesson = {"lesson_id": "LESSON-003", "context": "c", "outcome": "o", "status": "INVALID_STATUS"}

    with pytest.raises(LessonEvaluationError, match="invalid lesson status"):
        evaluator.evaluate(lesson, GOVERNANCE)


def test_block_result_returns_quarantine_status():
    result = LessonEvaluator().block_result("LESSON-999", "Sage review required")

    assert result.status == LessonStatus.QUARANTINE
    assert result.quality_score == 0.0
    assert result.blocked is True


def test_custom_precision_affects_quality_score():
    low_precision = LessonEvaluator(LessonEvaluatorConfig(precision=2))
    high_precision = LessonEvaluator(LessonEvaluatorConfig(precision=6))

    lesson = {"lesson_id": "L1", "context": "c", "outcome": "o", "status": "DRAFT", "evidence": [{"confidence": 0.5555}]}
    r1 = low_precision.evaluate(lesson, GOVERNANCE)
    r2 = high_precision.evaluate(lesson, GOVERNANCE)

    assert r1.quality_score == pytest.approx(0.56, rel=0.01)
    assert r2.quality_score == pytest.approx(0.5555, rel=0.0001)


def test_information_classification_values():
    assert InformationClassification.I0_OFFICIAL_VERIFIED.value == "I0_OFFICIAL_VERIFIED"
    assert InformationClassification.I1_PROBABLE.value == "I1_PROBABLE"
    assert InformationClassification.I2_HYPOTHESIS.value == "I2_HYPOTHESIS"
    assert InformationClassification.I3_THEORY.value == "I3_THEORY"
    assert InformationClassification.I4_SCENARIO.value == "I4_SCENARIO"
    assert InformationClassification.I5_SPECULATIVE.value == "I5_SPECULATIVE"
    assert InformationClassification.I6_FICTION.value == "I6_FICTION"
    assert InformationClassification.I7_LEGEND.value == "I7_LEGEND"
    assert InformationClassification.I8_RUMOR.value == "I8_RUMOR"
    assert InformationClassification.I9_REJECTED.value == "I9_REJECTED"


def test_lesson_model_includes_mandatory_fields():
    result = LessonEvaluator().evaluate(sample_lesson(), GOVERNANCE)

    assert result.source is None
    assert result.author is None
    assert result.reviewer == "Sage"
    assert result.date == "2026-06-07T00:00:00Z"
    assert result.validation_result is None
    assert result.version is None
    assert result.information_classification is None


def test_block_result_includes_all_mandatory_fields():
    result = LessonEvaluator().block_result("LESSON-999", "Sage review required")

    assert result.reviewer is None
    assert result.date is None
    assert result.validation_result is None
    assert result.version is None
    assert result.information_classification is None