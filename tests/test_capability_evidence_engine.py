import pytest
from memory.capability_registry.capability_evidence_registry import (
    CapabilityEvidenceRegistry, EvidenceRecord,
)
from services.capability_evidence_engine import CapabilityEvidenceEngine


class TestCapabilityEvidenceEngine:
    def test_record_evidence(self, evidence_registry):
        engine = CapabilityEvidenceEngine(evidence_registry)
        rec = engine.record_evidence(
            capability_id="CCAP-001", scenario_id="SCEN-001",
            evidence_type="VALIDATION_RESULT", result="PASSED", metric=1.0,
            reviewer_agent="Sage",
        )
        assert rec.evidence_id.startswith("EVID-")
        assert rec.capability_id == "CCAP-001"
        assert rec.metric == 1.0

    def test_record_documentation_evidence(self, evidence_registry):
        engine = CapabilityEvidenceEngine(evidence_registry)
        rec = engine.record_documentation_evidence(
            capability_id="CCAP-001", scenario_id="SCEN-001",
            documentation_found=True, reviewer_agent="Sage",
        )
        assert rec.evidence_type == "DOCUMENTATION"
        assert rec.result == "FOUND"

    def test_record_validation_evidence(self, evidence_registry):
        engine = CapabilityEvidenceEngine(evidence_registry)
        rec = engine.record_validation_evidence(
            capability_id="CCAP-001", scenario_id="SCEN-001",
            validation_result={"status": "PASSED", "scenario_id": "SCEN-001"},
            reviewer_agent="Sage",
        )
        assert rec.evidence_type == "VALIDATION_RESULT"
        assert rec.metric == 1.0

    def test_evaluate_evidence_sufficiency_no_evidence(self, evidence_registry):
        engine = CapabilityEvidenceEngine(evidence_registry)
        result = engine.evaluate_evidence_sufficiency("CCAP-999")
        assert result["has_evidence"] is False
        assert result["sufficient"] is False
        assert "No evidence" in result["gap"]

    def test_evaluate_evidence_sufficiency_sufficient(self, evidence_registry):
        engine = CapabilityEvidenceEngine(evidence_registry)
        engine.record_evidence(
            capability_id="CCAP-001", scenario_id="SCEN-001",
            evidence_type="VALIDATION_RESULT", result="PASSED", metric=1.0,
            confidence=0.9, reviewer_agent="Sage",
        )
        engine.record_evidence(
            capability_id="CCAP-001", scenario_id="SCEN-002",
            evidence_type="DOCUMENTATION", result="FOUND", metric=1.0,
            confidence=0.8, reviewer_agent="Sage",
        )
        result = engine.evaluate_evidence_sufficiency("CCAP-001")
        assert result["has_evidence"] is True
        assert result["sufficient"] is True

    def test_evidence_registry_list(self, evidence_registry):
        evidence_registry.create(
            capability_id="CCAP-001", scenario_id="SCEN-001",
            evidence_type="VALIDATION_RESULT", result="PASSED",
        )
        assert len(evidence_registry.list_all()) == 1
        assert len(evidence_registry.list_all(capability_id="CCAP-001")) == 1
        assert len(evidence_registry.list_all(capability_id="NONE")) == 0

    def test_invalid_evidence_type_raises(self):
        with pytest.raises(ValueError, match="invalid evidence_type"):
            EvidenceRecord(
                capability_id="CCAP-001", scenario_id="SCEN-001",
                evidence_type="INVALID_TYPE", result="PASSED",
            )
