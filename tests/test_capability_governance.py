from services.learning_governance_gate import LearningGovernanceGate


def test_no_activation_passes():
    gate = LearningGovernanceGate()
    result = gate._check_no_activation({"status": "CANDIDATE"})
    assert result.passed


def test_no_activation_fails_active():
    gate = LearningGovernanceGate()
    result = gate._check_no_activation({"status": "ACTIVE"})
    assert not result.passed


def test_no_activation_with_activation_status():
    gate = LearningGovernanceGate()
    result = gate._check_no_activation({"status": "CANDIDATE", "activation_status": "DISABLED"})
    assert result.passed


def test_no_activation_fails_enabled():
    gate = LearningGovernanceGate()
    result = gate._check_no_activation({"status": "CANDIDATE", "activation_status": "ENABLED"})
    assert not result.passed


def test_evaluate_capability_includes_all_gates():
    gate = LearningGovernanceGate()
    report = gate.evaluate_capability({
        "capability_id": "CAPC-1",
        "canonical_id": "CCAP-1",
        "source_capability_ids": ["CAPC-1"],
        "domain": "Trading",
        "classification": "CANONICAL",
        "status": "CANDIDATE",
        "confidence_score": 0.85,
        "evidence": {"src": "test", "cnt": 3},
        "owner_agent": "Sage",
        "reviewer_agent": "Sage",
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
    assert "risk_appropriate" in gate_names
    assert "canonical_mapping" in gate_names
    assert "graph_integrity" in gate_names
    assert "promotion_eligibility" in gate_names
    assert "no_activation" in gate_names


def test_governance_gates_list_updated():
    from services.learning_governance_gate import GOVERNANCE_GATES
    assert "no_activation" in GOVERNANCE_GATES
