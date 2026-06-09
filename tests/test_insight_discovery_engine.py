from services.insight_discovery_engine import InsightDiscoveryEngine


def test_discover_from_clusters(signal_registry, cluster_registry, insight_registry):
    signal_registry.create_candidate(
        signal_type="PATTERN", source_kind="lesson", source_id="L-1",
        title="P1", content="C1", owner_agent="Sage",
        confidence_score=0.85, tags=["lesson", "pattern"],
    )
    cluster_registry.create_cluster(
        cluster_type="ENGINEERING",
        title="ENGINEERING Cluster (1 signals)",
        description="Test cluster",
        source_signal_ids=["LSIG-TEST-1"],
        signal_count=1, confidence_score=0.85,
        owner_agent="Sage",
        tags=["engineering", "cluster", "lesson"],
    )
    engine = InsightDiscoveryEngine(signal_registry, cluster_registry, insight_registry)
    insights = engine.discover_from_clusters(owner_agent="Sage")
    assert len(insights) >= 1
    for ins in insights:
        assert ins.status == "CANDIDATE"
        assert ins.insight_id.startswith("INS-")


def test_discover_from_signals_direct(signal_registry, insight_registry):
    signal_registry.create_candidate(
        signal_type="PATTERN", source_kind="lesson", source_id="L-1",
        title="P1", content="C1", owner_agent="Sage",
        confidence_score=0.85, tags=["lesson", "pattern"],
    )
    signal_registry.create_candidate(
        signal_type="PATTERN", source_kind="lesson", source_id="L-2",
        title="P2", content="C2", owner_agent="Sage",
        confidence_score=0.75, tags=["lesson", "pattern"],
    )
    empty_clusters = type("EmptyClusterReg", (), {"list_all": lambda *a, **kw: []})()
    engine = InsightDiscoveryEngine(signal_registry, empty_clusters, insight_registry)
    insights = engine.discover_from_signals_direct(owner_agent="Sage")
    assert len(insights) >= 1


def test_discover_from_signals_requires_min_2(signal_registry, insight_registry):
    signal_registry.create_candidate(
        signal_type="PATTERN", source_kind="lesson", source_id="L-1",
        title="P1", content="C1", owner_agent="Sage",
        confidence_score=0.85, tags=["lesson", "pattern"],
    )
    empty_clusters = type("EmptyClusterReg", (), {"list_all": lambda *a, **kw: []})()
    engine = InsightDiscoveryEngine(signal_registry, empty_clusters, insight_registry)
    insights = engine.discover_from_signals_direct(owner_agent="Sage")
    assert len(insights) == 0  # only 1 signal, min 2 required


def test_run_all_combines_discovery_methods(signal_registry, cluster_registry, insight_registry):
    signal_registry.create_candidate(
        signal_type="TRADING", source_kind="lesson", source_id="L-1",
        title="T1", content="C1", owner_agent="Sage",
        confidence_score=0.80, tags=["lesson", "trading"],
    )
    cluster_registry.create_cluster(
        cluster_type="TRADING", title="TRADING Cluster (1 signals)",
        description="Test", source_signal_ids=["LSIG-1"],
        signal_count=1, confidence_score=0.80,
        owner_agent="Sage", tags=["trading", "cluster"],
    )
    engine = InsightDiscoveryEngine(signal_registry, cluster_registry, insight_registry)
    all_insights = engine.run_all(owner_agent="Sage")
    assert len(all_insights) >= 1


def test_insight_traceability(signal_registry, cluster_registry, insight_registry):
    signal_registry.create_candidate(
        signal_type="GOVERNANCE", source_kind="lesson", source_id="L-1",
        title="G1", content="C1", owner_agent="Sage",
        confidence_score=0.80, tags=["lesson", "governance"],
    )
    cluster_registry.create_cluster(
        cluster_type="GOVERNANCE", title="GOVERNANCE Cluster (1 signals)",
        description="Test", source_signal_ids=["LSIG-TEST-1"],
        signal_count=1, confidence_score=0.80,
        owner_agent="Sage", tags=["governance", "cluster"],
    )
    engine = InsightDiscoveryEngine(signal_registry, cluster_registry, insight_registry)
    insights = engine.discover_from_clusters(owner_agent="Sage")
    for ins in insights:
        assert len(ins.source_signal_ids) > 0


def test_no_auto_promotion(signal_registry, cluster_registry, insight_registry):
    signal_registry.create_candidate(
        signal_type="RISK", source_kind="lesson", source_id="L-1",
        title="R1", content="C1", owner_agent="Sage",
        confidence_score=0.70, tags=["lesson", "risk"],
    )
    cluster_registry.create_cluster(
        cluster_type="RISK", title="RISK Cluster (1 signals)",
        description="Test", source_signal_ids=["LSIG-1"],
        signal_count=1, confidence_score=0.70,
        owner_agent="Sage", tags=["risk", "cluster"],
    )
    engine = InsightDiscoveryEngine(signal_registry, cluster_registry, insight_registry)
    insights = engine.run_all(owner_agent="Sage")
    for ins in insights:
        assert ins.status == "CANDIDATE"


def test_duplicate_suppression(signal_registry, cluster_registry, insight_registry):
    cluster_registry.create_cluster(
        cluster_type="MEMORY", title="MEMORY Cluster (1 signals)",
        description="Test A", source_signal_ids=["LSIG-1"],
        signal_count=1, confidence_score=0.80,
        owner_agent="Sage", tags=["memory", "cluster"],
    )
    cluster_registry.create_cluster(
        cluster_type="MEMORY", title="MEMORY Cluster (1 signals)",
        description="Test B (same title)", source_signal_ids=["LSIG-2"],
        signal_count=1, confidence_score=0.80,
        owner_agent="Sage", tags=["memory", "cluster"],
    )
    engine = InsightDiscoveryEngine(signal_registry, cluster_registry, insight_registry)
    insights = engine.discover_from_clusters(owner_agent="Sage")
    memory_insights = [i for i in insights if "MEMORY" in i.title]
    assert len(memory_insights) <= 1
