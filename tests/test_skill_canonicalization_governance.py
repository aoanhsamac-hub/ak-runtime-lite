from services.learning_governance_gate import LearningGovernanceGate


def test_canonical_mapping_gate_passes_on_canonical():
    gate = LearningGovernanceGate()
    record = {
        "classification": "CANONICAL",
        "family_id": "SFAM-001",
    }
    result = gate._check_canonical_mapping(record)
    assert result.passed


def test_canonical_mapping_fails_non_canonical():
    gate = LearningGovernanceGate()
    record = {
        "classification": "SUPERSEDED",
        "family_id": "",
    }
    result = gate._check_canonical_mapping(record)
    assert not result.passed


def test_canonical_mapping_passes_with_ref():
    gate = LearningGovernanceGate()
    record = {
        "classification": "OVERLAPPING",
        "supercedes_canonical_id": "CANON-001",
    }
    result = gate._check_canonical_mapping(record)
    assert result.passed


def test_graph_integrity_passes_no_edges():
    gate = LearningGovernanceGate()
    result = gate._check_graph_integrity({"metadata": {}})
    assert result.passed


def test_graph_integrity_valid_edges():
    gate = LearningGovernanceGate()
    result = gate._check_graph_integrity({
        "metadata": {"graph_edges": [{"source_id": "A", "target_id": "B"}]},
    })
    assert result.passed


def test_graph_integrity_invalid_edges():
    gate = LearningGovernanceGate()
    result = gate._check_graph_integrity({
        "metadata": {"graph_edges": [{"source_id": "A", "target_id": ""}]},
    })
    assert not result.passed


def test_evaluate_family_uses_canonical_gate():
    gate = LearningGovernanceGate()
    report = gate.evaluate_family({
        "family_id": "SFAM-001",
        "family_name": "Trading Family",
        "member_skill_ids": ["CSK-1"],
        "classification": "",
        "evidence": {"member_count": 1},
        "confidence_score": 0.80,
        "owner_agent": "Sage",
        "reviewer_agent": "Sage",
        "risk_level": "LEVEL_1_MODERATE",
    })
    assert report.record_type == "family"


def test_evaluate_canonical_includes_graph_gate():
    gate = LearningGovernanceGate()
    report = gate.evaluate_canonical({
        "canonical_id": "CANON-001",
        "classification": "CANONICAL",
        "evidence": {"group_size": 1},
        "confidence_score": 0.85,
        "owner_agent": "Sage",
        "reviewer_agent": "Sage",
        "risk_level": "LEVEL_1_MODERATE",
        "metadata": {},
    })
    assert report.record_type == "canonical"
    gate_names = {g.gate for g in report.gates}
    assert "graph_integrity" in gate_names
    assert "canonical_mapping" in gate_names


def test_governance_gates_list_updated():
    from services.learning_governance_gate import GOVERNANCE_GATES
    assert "canonical_mapping" in GOVERNANCE_GATES
    assert "graph_integrity" in GOVERNANCE_GATES
