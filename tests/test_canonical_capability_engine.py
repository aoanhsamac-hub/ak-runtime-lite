from services.capability_family_engine import CapabilityFamilyEngine
from services.canonical_capability_engine import CanonicalCapabilityEngine


def test_classify_single_as_canonical(cap_candidate_registry, cap_family_registry, cap_canonical_registry):
    cap_candidate_registry.create(
        name="Trading Capability", description="T",
        domain="Trading", owner_agent="Sage", confidence_score=0.85,
    )
    CapabilityFamilyEngine(cap_candidate_registry, cap_family_registry).discover_families()
    engine = CanonicalCapabilityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry)
    results = engine.classify_all(owner_agent="Sage")
    assert len(results) >= 1
    for r in results:
        assert r.classification in ("CANONICAL", "ISOLATED")
        assert r.status == "CANDIDATE"


def test_merge_related(cap_candidate_registry, cap_family_registry, cap_canonical_registry):
    cap_candidate_registry.create(
        name="Risk Analysis v1", description="RA v1",
        domain="Risk", owner_agent="Sage", confidence_score=0.60,
    )
    cap_candidate_registry.create(
        name="Risk Analysis v2", description="RA v2",
        domain="Risk", owner_agent="Sage", confidence_score=0.90,
    )
    CapabilityFamilyEngine(cap_candidate_registry, cap_family_registry).discover_families()
    engine = CanonicalCapabilityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry)
    results = engine.classify_all(owner_agent="Sage")
    canon = [r for r in results if r.classification == "CANONICAL"]
    assert len(canon) >= 1
    assert len(canon[0].source_capability_ids) >= 1


def test_empty_registry(cap_family_registry, cap_canonical_registry):
    empty = type("Empty", (), {"list_all": lambda *a, **kw: []})()
    engine = CanonicalCapabilityEngine(empty, cap_family_registry, cap_canonical_registry)
    results = engine.classify_all()
    assert len(results) == 0
