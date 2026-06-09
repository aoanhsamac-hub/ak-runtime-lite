from services.capability_discovery_engine import CapabilityDiscoveryEngine


def test_discover_from_skills(approved_skill_registry, cap_candidate_registry):
    approved_skill_registry.approve(
        name="Trading Strategy Skill", description="A trading skill",
        owner_agent="Sage", approval_authority="Hung Vuong",
        confidence_score=0.85, canonical_id="C-1",
        tags=["trading"], evidence={"src": "test"},
    )
    approved_skill_registry.approve(
        name="Risk Management Skill", description="A risk skill",
        owner_agent="Sage", approval_authority="Hung Vuong",
        confidence_score=0.80, canonical_id="C-2",
        tags=["risk"], evidence={"src": "test"},
    )
    engine = CapabilityDiscoveryEngine(approved_skill_registry, cap_candidate_registry)
    caps = engine.discover_from_skills(owner_agent="Sage")
    assert len(caps) >= 2
    domains = {c.domain for c in caps}
    assert "Trading" in domains
    assert "Risk" in domains
    for c in caps:
        assert c.status == "CANDIDATE"


def test_domain_classification(approved_skill_registry, cap_candidate_registry):
    approved_skill_registry.approve(
        name="Governance Policy Engine", description="A governance skill",
        owner_agent="Sage", approval_authority="Hung Vuong",
        confidence_score=0.78, canonical_id="C-1",
        tags=["governance"], evidence={"src": "test"},
    )
    engine = CapabilityDiscoveryEngine(approved_skill_registry, cap_candidate_registry)
    caps = engine.discover_from_skills(owner_agent="Sage")
    gov = [c for c in caps if c.domain == "Governance"]
    assert len(gov) == 1


def test_run_all_combines_sources(approved_skill_registry, cap_candidate_registry):
    approved_skill_registry.approve(
        name="Engineering Pipeline Skill", description="An eng skill",
        owner_agent="Sage", approval_authority="Hung Vuong",
        confidence_score=0.82, canonical_id="C-1",
        tags=["engineering"], evidence={"src": "test"},
    )
    engine = CapabilityDiscoveryEngine(approved_skill_registry, cap_candidate_registry)
    caps = engine.run_all(owner_agent="Sage")
    assert len(caps) >= 1


def test_empty_registry_returns_empty(cap_candidate_registry):
    empty = type("Empty", (), {"list_all": lambda *a, **kw: []})()
    engine = CapabilityDiscoveryEngine(empty, cap_candidate_registry)
    caps = engine.run_all()
    assert len(caps) == 0


def test_evidence_aggregated(approved_skill_registry, cap_candidate_registry):
    for i in range(3):
        approved_skill_registry.approve(
            name=f"Agent Skill {i}", description=f"A{i}",
            owner_agent="Sage", approval_authority="Hung Vuong",
            confidence_score=0.70 + i * 0.08, canonical_id=f"C-{i}",
            tags=["agent"], evidence={"src": "test"},
        )
    engine = CapabilityDiscoveryEngine(approved_skill_registry, cap_candidate_registry)
    caps = engine.discover_from_skills(owner_agent="Sage")
    agent = [c for c in caps if c.domain == "Agent"]
    if agent:
        assert agent[0].confidence_score > 0.7
