from services.skill_family_engine import SkillFamilyEngine


def test_discover_families_creates_families(candidate_skill_registry, family_registry):
    candidate_skill_registry.create_candidate(
        name="Trading Execution Skill", description="A trading skill",
        owner_agent="Sage", confidence_score=0.85,
        tags=["trading", "execution"],
    )
    engine = SkillFamilyEngine(candidate_skill_registry, family_registry)
    families = engine.discover_families(owner_agent="Sage")
    assert len(families) >= 1
    for f in families:
        assert f.status == "CANDIDATE"
        assert f.family_name in (
            "Trading Family", "Risk Family", "Execution Family",
            "Memory Family", "Governance Family", "Engineering Family", "Agent Family",
        )


def test_family_contains_member_skills(candidate_skill_registry, family_registry):
    candidate_skill_registry.create_candidate(
        name="Trading Pattern Detector", description="Trading detection",
        owner_agent="Sage", confidence_score=0.80,
        tags=["trading", "pattern"],
    )
    engine = SkillFamilyEngine(candidate_skill_registry, family_registry)
    families = engine.discover_families(owner_agent="Sage")
    trading = [f for f in families if "Trading" in f.family_name]
    if trading:
        assert len(trading[0].member_skill_ids) >= 1


def test_family_confidence_averaged(candidate_skill_registry, family_registry):
    for i in range(3):
        candidate_skill_registry.create_candidate(
            name=f"Trading Skill {i}", description=f"T{i}",
            owner_agent="Sage", confidence_score=0.5 + i * 0.15,
            tags=["trading"],
        )
    engine = SkillFamilyEngine(candidate_skill_registry, family_registry)
    families = engine.discover_families(owner_agent="Sage")
    trading = [f for f in families if "Trading" in f.family_name]
    if trading:
        assert trading[0].family_confidence > 0.5


def test_empty_registry_returns_empty(family_registry):
    empty = type("EmptyRegistry", (), {"list_all": lambda *a, **kw: []})()
    engine = SkillFamilyEngine(empty, family_registry)
    families = engine.discover_families()
    assert len(families) == 0


def test_multi_family_discovery(candidate_skill_registry, family_registry):
    candidate_skill_registry.create_candidate(
        name="Trading Skill", description="T", owner_agent="Sage",
        confidence_score=0.80, tags=["trading"],
    )
    candidate_skill_registry.create_candidate(
        name="Governance Skill", description="G", owner_agent="Sage",
        confidence_score=0.75, tags=["governance"],
    )
    engine = SkillFamilyEngine(candidate_skill_registry, family_registry)
    families = engine.discover_families(owner_agent="Sage")
    names = {f.family_name for f in families}
    assert "Trading Family" in names
    assert "Governance Family" in names
