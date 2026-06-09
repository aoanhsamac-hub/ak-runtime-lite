from services.capability_family_engine import CapabilityFamilyEngine


def test_discover_families_creates_groups(cap_candidate_registry, cap_family_registry):
    cap_candidate_registry.create(
        name="Trading Capability", description="T",
        domain="Trading", owner_agent="Sage", confidence_score=0.85,
        tags=["trading", "capability"],
    )
    cap_candidate_registry.create(
        name="Risk Capability", description="R",
        domain="Risk", owner_agent="Sage", confidence_score=0.80,
        tags=["risk", "capability"],
    )
    engine = CapabilityFamilyEngine(cap_candidate_registry, cap_family_registry)
    families = engine.discover_families(owner_agent="Sage")
    assert len(families) >= 2
    for f in families:
        assert f.status == "CANDIDATE"


def test_family_contains_members(cap_candidate_registry, cap_family_registry):
    c = cap_candidate_registry.create(
        name="Execution Capability", description="E",
        domain="Execution", owner_agent="Sage", confidence_score=0.78,
        tags=["execution"],
    )
    engine = CapabilityFamilyEngine(cap_candidate_registry, cap_family_registry)
    families = engine.discover_families(owner_agent="Sage")
    exec_fams = [f for f in families if "Execution" in f.family_name]
    if exec_fams:
        assert c.capability_id in exec_fams[0].member_capability_ids


def test_empty_registry(cap_family_registry):
    empty = type("Empty", (), {"list_all": lambda *a, **kw: []})()
    engine = CapabilityFamilyEngine(empty, cap_family_registry)
    families = engine.discover_families()
    assert len(families) == 0
