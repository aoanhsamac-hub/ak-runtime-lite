import pytest
from services.capability_promotion_readiness_engine import (
    CapabilityPromotionReadinessEngine, PromotionReadiness,
)


class TestCapabilityPromotionReadinessEngine:
    def test_assess_not_ready_no_evidence(self, cap_canonical_registry, cap_promotion_registry,
                                           cap_candidate_registry):
        cc = cap_canonical_registry.create(
            name="Test Cap", description="Test",
            classification="CANONICAL", domain="Engineering",
            owner_agent="Sage", confidence_score=0.5,
            source_capability_ids=[],
        )
        engine = CapabilityPromotionReadinessEngine(
            cap_candidate_registry, cap_canonical_registry, cap_promotion_registry,
        )
        pr = engine.assess(cc)
        assert pr.decision in ("NOT_READY", "NEEDS_EVIDENCE")

    def test_assess_promotion_ready(self, cap_canonical_registry, cap_promotion_registry,
                                     cap_candidate_registry):
        cc = cap_canonical_registry.create(
            name="Trading Cap", description="Test",
            classification="CANONICAL", domain="Trading",
            owner_agent="Sage", confidence_score=0.85,
            source_capability_ids=["CAPC-001", "CAPC-002", "CAPC-003"],
        )
        from services.capability_maturity_reassessment_engine import MaturityReassessment
        mat = MaturityReassessment(
            capability_id=cc.canonical_id, capability_name="Trading Cap",
            domain="Trading", maturity_level="ESTABLISHED",
            maturity_score=0.65, evidence_depth=0.7, skill_support=0.85,
            trace_support=0.6, validation_results=0.7, risk_profile=0.8,
            reuse_value=0.6, governance_confidence=0.75,
        )
        ev = {"has_evidence": True, "avg_confidence": 0.7, "avg_metric": 0.7, "evidence_count": 3}
        engine = CapabilityPromotionReadinessEngine(
            cap_candidate_registry, cap_canonical_registry, cap_promotion_registry,
        )
        pr = engine.assess(cc, maturity_reassessment=mat, evidence_sufficiency=ev)
        assert pr.decision == "PROMOTION_READY"

    def test_assess_hermes_reject(self, cap_canonical_registry, cap_promotion_registry,
                                   cap_candidate_registry):
        cc = cap_canonical_registry.create(
            name="Test Cap", description="Test",
            classification="CANONICAL", domain="Engineering",
            owner_agent="Sage", confidence_score=0.85,
            source_capability_ids=["CAPC-001"],
        )
        hr = type("HermesReview", (), {"outcome": "RECOMMEND_REJECT", "reviewer": "Hermes"})()
        engine = CapabilityPromotionReadinessEngine(
            cap_candidate_registry, cap_canonical_registry, cap_promotion_registry,
        )
        pr = engine.assess(cc, hermes_review=hr)
        assert pr.decision == "NOT_READY"

    def test_assess_all(self, cap_canonical_registry, cap_promotion_registry,
                         cap_candidate_registry):
        cap_canonical_registry.create(
            name="Cap A", description="Test",
            classification="CANONICAL", domain="Trading",
            owner_agent="Sage", confidence_score=0.9,
            source_capability_ids=["CAPC-001", "CAPC-002"],
        )
        cap_canonical_registry.create(
            name="Cap B", description="Test",
            classification="CANONICAL", domain="Risk",
            owner_agent="Sage", confidence_score=0.4,
            source_capability_ids=[],
        )
        engine = CapabilityPromotionReadinessEngine(
            cap_candidate_registry, cap_canonical_registry, cap_promotion_registry,
        )
        results = engine.assess_all()
        assert len(results) == 2
        decisions = {r.decision for r in results}
        assert decisions.issubset({"PROMOTION_READY", "NEEDS_EVIDENCE", "NEEDS_REVIEW", "NOT_READY", "ARCHIVE_ONLY"})
