from services.skill_promotion_policy_engine import SkillPromotionPolicyEngine


def test_approve_high_confidence_canonical():
    engine = SkillPromotionPolicyEngine()
    result = engine.evaluate({
        "confidence_score": 0.85,
        "risk_level": "LEVEL_1_MODERATE",
        "classification": "CANONICAL",
        "status": "CANDIDATE",
        "evidence": {"source": "test", "count": 3},
    })
    assert result.decision == "APPROVED"
    assert result.risk_score <= 2.0


def test_reject_low_confidence():
    engine = SkillPromotionPolicyEngine()
    result = engine.evaluate({
        "confidence_score": 0.20,
        "risk_level": "LEVEL_2_HIGH",
        "classification": "ISOLATED",
        "status": "CANDIDATE",
        "evidence": {},
    })
    assert result.decision == "REJECTED"


def test_needs_review_medium_confidence():
    engine = SkillPromotionPolicyEngine()
    result = engine.evaluate({
        "confidence_score": 0.55,
        "risk_level": "LEVEL_2_HIGH",
        "classification": "CANONICAL",
        "status": "CANDIDATE",
        "evidence": {"source": "test"},
    })
    assert result.decision == "NEEDS_REVIEW"


def test_needs_evidence_low_confidence_some_evidence():
    engine = SkillPromotionPolicyEngine()
    result = engine.evaluate({
        "confidence_score": 0.40,
        "risk_level": "LEVEL_3_CRITICAL",
        "classification": "CANONICAL",
        "status": "CANDIDATE",
        "evidence": {"source": "test"},
    })
    assert result.decision == "NEEDS_EVIDENCE"


def test_archival_for_superseded():
    engine = SkillPromotionPolicyEngine()
    result = engine.evaluate_archival({
        "classification": "SUPERSEDED",
        "confidence_score": 0.30,
    })
    assert result.decision == "ARCHIVED"


def test_archival_for_isolated_low_confidence():
    engine = SkillPromotionPolicyEngine()
    result = engine.evaluate_archival({
        "classification": "ISOLATED",
        "confidence_score": 0.20,
    })
    assert result.decision == "ARCHIVED"


def test_archival_not_eligible():
    engine = SkillPromotionPolicyEngine()
    result = engine.evaluate_archival({
        "classification": "CANONICAL",
        "confidence_score": 0.80,
    })
    assert result.decision == "NEEDS_REVIEW"


def test_maturity_boost():
    engine = SkillPromotionPolicyEngine()
    result = engine.evaluate({
        "confidence_score": 0.85,
        "risk_level": "LEVEL_1_MODERATE",
        "classification": "CANONICAL",
        "status": "CANDIDATE",
        "evidence": {"source": "test", "count": 3},
    }, {"maturity_score": 0.92, "governance_confidence": 0.95})
    assert result.decision == "APPROVED"
    assert result.governance_score >= 0.85
