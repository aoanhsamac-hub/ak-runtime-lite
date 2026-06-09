import pytest
from services.capability_maturity_reassessment_engine import (
    CapabilityMaturityReassessmentEngine, MaturityReassessment,
)


class TestCapabilityMaturityReassessmentEngine:
    def test_reassess_basic(self, cap_canonical_registry, cap_candidate_registry):
        cc = cap_canonical_registry.create(
            name="Trading Domain Capability", description="Test",
            classification="CANONICAL", domain="Trading",
            owner_agent="Sage", confidence_score=0.8,
            source_capability_ids=["CAPC-001", "CAPC-002"],
        )
        engine = CapabilityMaturityReassessmentEngine(
            cap_candidate_registry, cap_canonical_registry,
        )
        mat = engine.reassess(cc)
        assert mat.capability_id == cc.canonical_id
        assert mat.maturity_level in ("EMERGING", "DEVELOPING", "ESTABLISHED")

    def test_reassess_with_evidence(self, cap_canonical_registry, cap_candidate_registry):
        cc = cap_canonical_registry.create(
            name="Risk Capability", description="Test",
            classification="CANONICAL", domain="Risk",
            owner_agent="Sage", confidence_score=0.85,
            source_capability_ids=["CAPC-001"],
        )
        engine = CapabilityMaturityReassessmentEngine(
            cap_candidate_registry, cap_canonical_registry,
        )
        ev = {"has_evidence": True, "avg_confidence": 0.8, "avg_metric": 0.9, "evidence_count": 3}
        mat = engine.reassess(cc, evidence_sufficiency=ev)
        assert mat.maturity_score >= 0.5

    def test_reassess_with_previous_maturity(self, cap_canonical_registry, cap_candidate_registry):
        cc = cap_canonical_registry.create(
            name="Memory Capability", description="Test",
            classification="CANONICAL", domain="Memory",
            owner_agent="Sage", confidence_score=0.9,
            source_capability_ids=["CAPC-001"],
        )
        engine = CapabilityMaturityReassessmentEngine(
            cap_candidate_registry, cap_canonical_registry,
        )
        mat = engine.reassess(cc, previous_maturity="ADVANCED")
        assert mat.previous_maturity == "ADVANCED"

    def test_reassess_all_empty(self, cap_canonical_registry, cap_candidate_registry):
        engine = CapabilityMaturityReassessmentEngine(
            cap_candidate_registry, cap_canonical_registry,
        )
        results = engine.reassess_all()
        assert len(results) == 0

    def test_score_to_level(self):
        assert CapabilityMaturityReassessmentEngine._score_to_level(0.95) == "SOVEREIGN"
        assert CapabilityMaturityReassessmentEngine._score_to_level(0.75) == "ADVANCED"
        assert CapabilityMaturityReassessmentEngine._score_to_level(0.55) == "ESTABLISHED"
        assert CapabilityMaturityReassessmentEngine._score_to_level(0.35) == "DEVELOPING"
        assert CapabilityMaturityReassessmentEngine._score_to_level(0.15) == "EMERGING"
