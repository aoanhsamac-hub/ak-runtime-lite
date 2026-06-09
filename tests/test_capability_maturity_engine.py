from services.capability_maturity_engine import CapabilityMaturityEngine
from services.capability_family_engine import CapabilityFamilyEngine
from services.canonical_capability_engine import CanonicalCapabilityEngine


def test_assess_maturity(cap_candidate_registry, cap_family_registry, cap_canonical_registry):
    cap_candidate_registry.create(
        name="Trading Capability", description="T",
        domain="Trading", owner_agent="Sage", confidence_score=0.85,
        tags=["trading", "trading_knowledge"],
    )
    CapabilityFamilyEngine(cap_candidate_registry, cap_family_registry).discover_families()
    CanonicalCapabilityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry).classify_all()
    engine = CapabilityMaturityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry)
    assessments = engine.assess_all()
    assert len(assessments) >= 1


def test_maturity_levels_valid(cap_candidate_registry, cap_family_registry, cap_canonical_registry):
    cap_candidate_registry.create(
        name="Risk Capability", description="R",
        domain="Risk", owner_agent="Sage", confidence_score=0.80,
        tags=["risk", "risk_knowledge"],
    )
    CapabilityFamilyEngine(cap_candidate_registry, cap_family_registry).discover_families()
    CanonicalCapabilityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry).classify_all()
    engine = CapabilityMaturityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry)
    assessments = engine.assess_all()
    valid = {"EMERGING", "DEVELOPING", "ESTABLISHED", "ADVANCED", "SOVEREIGN"}
    for a in assessments:
        assert a.maturity_level in valid
        assert a.maturity_score >= 0.0


def test_empty_registry(cap_candidate_registry, cap_family_registry, cap_canonical_registry):
    engine = CapabilityMaturityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry)
    assessments = engine.assess_all()
    assert len(assessments) == 0
