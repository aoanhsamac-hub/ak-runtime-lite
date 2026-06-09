from services.capability_readiness_engine import CapabilityReadinessEngine
from services.capability_family_engine import CapabilityFamilyEngine
from services.canonical_capability_engine import CanonicalCapabilityEngine
from services.capability_maturity_engine import CapabilityMaturityEngine
from memory.capability_pipeline.schemas import READINESS_LEVELS


def test_readiness_promotion_ready(cap_candidate_registry, cap_family_registry,
                                    cap_canonical_registry, cap_promotion_registry):
    cap_candidate_registry.create(
        name="Trading Capability", description="T",
        domain="Trading", owner_agent="Sage", confidence_score=0.85,
        tags=["trading"], evidence={"a": 1, "b": 2},
    )
    CapabilityFamilyEngine(cap_candidate_registry, cap_family_registry).discover_families()
    CanonicalCapabilityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry).classify_all()
    mat = CapabilityMaturityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry).assess_all()
    engine = CapabilityReadinessEngine(cap_candidate_registry, cap_canonical_registry,
                                        cap_promotion_registry, mat)
    results = engine.assess_all()
    assert len(results) >= 1


def test_readiness_classifications_valid(cap_candidate_registry, cap_family_registry,
                                          cap_canonical_registry, cap_promotion_registry):
    cap_candidate_registry.create(
        name="Test Capability", description="T",
        domain="Engineering", owner_agent="Sage", confidence_score=0.75,
        tags=["engineering"], evidence={"a": 1},
    )
    CapabilityFamilyEngine(cap_candidate_registry, cap_family_registry).discover_families()
    CanonicalCapabilityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry).classify_all()
    mat = CapabilityMaturityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry).assess_all()
    engine = CapabilityReadinessEngine(cap_candidate_registry, cap_canonical_registry,
                                        cap_promotion_registry, mat)
    results = engine.assess_all()
    for r in results:
        assert r.decision in READINESS_LEVELS


def test_readiness_creates_recommendations(cap_candidate_registry, cap_family_registry,
                                            cap_canonical_registry, cap_promotion_registry):
    cap_candidate_registry.create(
        name="Agent Capability", description="A",
        domain="Agent", owner_agent="Sage", confidence_score=0.82,
        tags=["agent"], evidence={"x": 1, "y": 2},
    )
    CapabilityFamilyEngine(cap_candidate_registry, cap_family_registry).discover_families()
    CanonicalCapabilityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry).classify_all()
    mat = CapabilityMaturityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry).assess_all()
    engine = CapabilityReadinessEngine(cap_candidate_registry, cap_canonical_registry,
                                        cap_promotion_registry, mat)
    engine.assess_all()
    recs = cap_promotion_registry.list_all()
    assert len(recs) >= 1
