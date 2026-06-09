import pytest
from services.learning_governance_gate import LearningGovernanceGate, GOVERNANCE_GATES


class TestCapabilityValidationGovernance:
    def test_governance_gates_list_includes_new_gates(self):
        assert "evidence_gate" in GOVERNANCE_GATES
        assert "validation_gate" in GOVERNANCE_GATES
        assert "maturity_gate" in GOVERNANCE_GATES
        assert "hermes_review_gate" in GOVERNANCE_GATES
        assert "sage_review_gate" in GOVERNANCE_GATES
        assert "no_agent_adoption_gate" in GOVERNANCE_GATES
        assert "no_evolution_gate" in GOVERNANCE_GATES

    def test_evaluate_validation_all_passed(self):
        gate = LearningGovernanceGate()
        record = {
            "canonical_id": "CCAP-001",
            "capability_id": "CCAP-001",
            "domain": "Trading",
            "confidence_score": 0.85,
            "evidence": {"evidence_score": 0.7, "avg_confidence": 0.7},
            "has_evidence": True,
            "validation_score": 0.7,
            "maturity_level": "ESTABLISHED",
            "maturity_score": 0.65,
            "owner_agent": "Sage",
            "reviewer_agent": "Hung Vuong",
            "risk_level": "LEVEL_1_MODERATE",
            "classification": "CANONICAL",
            "status": "CANDIDATE",
            "agent_adoption_status": "NOT_ASSIGNED",
            "evolution_status": "LOCKED",
            "source_capability_ids": ["CAPC-001"],
            "metadata": {},
        }
        report = gate.evaluate_validation(record)
        assert report.all_passed

    def test_no_agent_adoption_gate(self):
        gate = LearningGovernanceGate()
        record = {
            "canonical_id": "CCAP-001",
            "domain": "Trading",
            "confidence_score": 0.8,
            "evidence": {},
            "owner_agent": "Sage",
            "reviewer_agent": "Hung Vuong",
            "risk_level": "LEVEL_1_MODERATE",
            "classification": "CANONICAL",
            "status": "CANDIDATE",
            "agent_adoption_status": "NOT_ASSIGNED",
            "evolution_status": "LOCKED",
            "source_capability_ids": [],
            "metadata": {},
        }
        report = gate.evaluate_validation(record)
        no_agent = [g for g in report.gates if g.gate == "no_agent_adoption_gate"]
        assert no_agent
        assert no_agent[0].passed

    def test_no_evolution_gate(self):
        gate = LearningGovernanceGate()
        record = {
            "canonical_id": "CCAP-001",
            "domain": "Trading",
            "confidence_score": 0.8,
            "evidence": {},
            "owner_agent": "Sage",
            "reviewer_agent": "Hung Vuong",
            "risk_level": "LEVEL_1_MODERATE",
            "classification": "CANONICAL",
            "status": "CANDIDATE",
            "agent_adoption_status": "NOT_ASSIGNED",
            "evolution_status": "LOCKED",
            "source_capability_ids": [],
            "metadata": {},
        }
        report = gate.evaluate_validation(record)
        no_evol = [g for g in report.gates if g.gate == "no_evolution_gate"]
        assert no_evol
        assert no_evol[0].passed

    def test_evidence_gate_fails_without_evidence(self):
        gate = LearningGovernanceGate()
        record = {
            "canonical_id": "CCAP-001",
            "domain": "Trading",
            "confidence_score": 0.8,
            "evidence": {},
            "has_evidence": False,
            "owner_agent": "Sage",
            "reviewer_agent": "Hung Vuong",
            "risk_level": "LEVEL_1_MODERATE",
            "classification": "CANONICAL",
            "status": "CANDIDATE",
            "agent_adoption_status": "NOT_ASSIGNED",
            "evolution_status": "LOCKED",
            "source_capability_ids": [],
            "metadata": {},
        }
        report = gate.evaluate_validation(record)
        ev_gate = [g for g in report.gates if g.gate == "evidence_gate"]
        assert ev_gate
        assert not ev_gate[0].passed

    def test_governance_rejects_missing_fields(self):
        gate = LearningGovernanceGate()
        record = {"canonical_id": "CCAP-001", "domain": "Trading"}
        report = gate.evaluate_validation(record)
        assert not report.all_passed
