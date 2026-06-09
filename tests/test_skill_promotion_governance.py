from services.learning_governance_gate import LearningGovernanceGate


def test_promotion_eligibility_passes():
    gate = LearningGovernanceGate()
    result = gate._check_promotion_eligibility({
        "classification": "CANONICAL",
        "status": "CANDIDATE",
    })
    assert result.passed


def test_promotion_eligibility_fails_non_canonical():
    gate = LearningGovernanceGate()
    result = gate._check_promotion_eligibility({
        "classification": "ISOLATED",
        "status": "CANDIDATE",
    })
    assert not result.passed


def test_promotion_eligibility_fails_non_candidate():
    gate = LearningGovernanceGate()
    result = gate._check_promotion_eligibility({
        "classification": "CANONICAL",
        "status": "ACTIVE",
    })
    assert not result.passed


def test_independent_review_passes():
    gate = LearningGovernanceGate()
    result = gate._check_independent_review({
        "recommender": "Hermes",
        "reviewer": "Hung Vuong",
    })
    assert result.passed


def test_independent_review_fails_same():
    gate = LearningGovernanceGate()
    result = gate._check_independent_review({
        "recommender": "Sage",
        "reviewer": "Sage",
    })
    assert not result.passed


def test_independent_review_fails_missing():
    gate = LearningGovernanceGate()
    result = gate._check_independent_review({
        "recommender": "",
        "reviewer": "",
    })
    assert not result.passed


def test_evaluate_promotion_includes_all_gates():
    gate = LearningGovernanceGate()
    report = gate.evaluate_promotion({
        "decision_id": "PDEC-1",
        "canonical_id": "CANON-1",
        "skill_id": "CANON-1",
        "classification": "CANONICAL",
        "status": "CANDIDATE",
        "confidence_score": 0.85,
        "evidence": {"src": "test", "cnt": 3},
        "owner_agent": "Sage",
        "reviewer_agent": "Hung Vuong",
        "risk_level": "LEVEL_1_MODERATE",
        "recommender": "Hermes",
        "reviewer": "Hung Vuong",
        "metadata": {},
    })
    gate_names = {g.gate for g in report.gates}
    assert "traceability" in gate_names
    assert "evidence_quality" in gate_names
    assert "confidence_threshold" in gate_names
    assert "ownership" in gate_names
    assert "review_authority" in gate_names
    assert "risk_appropriate" in gate_names
    assert "canonical_mapping" in gate_names
    assert "promotion_eligibility" in gate_names
    assert "independent_review" in gate_names
    assert report.all_passed


def test_governance_gates_list_updated():
    from services.learning_governance_gate import GOVERNANCE_GATES
    assert "independent_review" in GOVERNANCE_GATES
    assert "promotion_eligibility" in GOVERNANCE_GATES
