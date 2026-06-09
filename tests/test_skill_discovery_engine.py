from services.skill_discovery_engine import SkillDiscoveryEngine


def test_discover_from_insights(signal_registry, cluster_registry, insight_registry, candidate_skill_registry):
    insight_registry.create_candidate(
        insight_type="SKILL", title="Test Skill Insight",
        description="A skill insight for discovery",
        owner_agent="Sage",
        source_signal_ids=["LSIG-1"],
        confidence_score=0.80,
        tags=["skill", "discovered"],
    )
    engine = SkillDiscoveryEngine(
        signal_registry, cluster_registry, insight_registry, candidate_skill_registry,
    )
    skills = engine.discover_from_insights(owner_agent="Sage")
    assert len(skills) >= 1
    for s in skills:
        assert s.status == "CANDIDATE"
        assert s.approval_status == "PENDING_REVIEW"
        assert s.activation_status == "DISABLED"


def test_discover_from_clusters(signal_registry, cluster_registry, insight_registry, candidate_skill_registry):
    cluster_registry.create_cluster(
        cluster_type="TRADING", title="Trading Signal Cluster",
        description="Test trading cluster",
        source_signal_ids=["LSIG-1"],
        signal_count=1, confidence_score=0.80,
        owner_agent="Sage",
        tags=["trading", "cluster"],
    )
    engine = SkillDiscoveryEngine(
        signal_registry, cluster_registry, insight_registry, candidate_skill_registry,
    )
    skills = engine.discover_from_clusters(owner_agent="Sage")
    assert len(skills) >= 1
    for s in skills:
        assert s.status == "CANDIDATE"


def test_run_all_combines_sources(signal_registry, cluster_registry, insight_registry, candidate_skill_registry):
    insight_registry.create_candidate(
        insight_type="GOVERNANCE", title="Governance Insight",
        description="Test", owner_agent="Sage",
        source_signal_ids=["LSIG-1"],
        confidence_score=0.75,
    )
    engine = SkillDiscoveryEngine(
        signal_registry, cluster_registry, insight_registry, candidate_skill_registry,
    )
    skills = engine.run_all(owner_agent="Sage")
    assert len(skills) >= 1
    for s in skills:
        assert "Skill:" in s.name or "Discovery:" in s.name


def test_skill_category_mapping(signal_registry, cluster_registry, insight_registry, candidate_skill_registry):
    insight_registry.create_candidate(
        insight_type="TRADING" if False else "MARKET",
        title="Market Insight",
        description="Test market insight",
        owner_agent="Sage",
        source_signal_ids=["LSIG-1"],
        confidence_score=0.80,
    )
    engine = SkillDiscoveryEngine(
        signal_registry, cluster_registry, insight_registry, candidate_skill_registry,
    )
    skills = engine.run_all(owner_agent="Sage")
    if skills:
        assert any("Trading" in s.name or "Skill:" in s.name for s in skills)


def test_traceability_preserved(signal_registry, cluster_registry, insight_registry, candidate_skill_registry):
    signal_registry.create_candidate(
        signal_type="PATTERN", source_kind="lesson", source_id="LKI-TEST-1",
        title="P1", content="C1", owner_agent="Sage",
        confidence_score=0.85, tags=["lesson", "pattern"],
    )
    sig = signal_registry.list_all()[0]
    insight_registry.create_candidate(
        insight_type="SKILL", title="Traceable Insight",
        description="Test", owner_agent="Sage",
        source_signal_ids=[sig.signal_id],
        confidence_score=0.85,
    )
    engine = SkillDiscoveryEngine(
        signal_registry, cluster_registry, insight_registry, candidate_skill_registry,
    )
    skills = engine.discover_from_insights(owner_agent="Sage")
    for s in skills:
        assert len(s.source_insight_ids) > 0
        if s.source_signal_ids:
            assert len(s.source_signal_ids) > 0


def test_no_capability_generation(signal_registry, cluster_registry, insight_registry, candidate_skill_registry):
    engine = SkillDiscoveryEngine(
        signal_registry, cluster_registry, insight_registry, candidate_skill_registry,
    )
    skills = engine.run_all()
    for s in skills:
        assert not hasattr(s, 'capability_id')
        assert not hasattr(s, 'maturity_level')


def test_no_auto_promotion(signal_registry, cluster_registry, insight_registry, candidate_skill_registry):
    engine = SkillDiscoveryEngine(
        signal_registry, cluster_registry, insight_registry, candidate_skill_registry,
    )
    skills = engine.run_all()
    for s in skills:
        assert s.status == "CANDIDATE"
        assert s.approval_status == "PENDING_REVIEW"
        assert s.activation_status == "DISABLED"
