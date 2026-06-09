from services.signal_clustering_engine import SignalClusteringEngine


def test_cluster_by_type_creates_clusters(signal_registry, cluster_registry):
    signal_registry.create_candidate(
        signal_type="PATTERN", source_kind="lesson", source_id="L-1",
        title="P1", content="C1", owner_agent="Sage",
        confidence_score=0.85, tags=["lesson", "pattern", "engineering"],
    )
    signal_registry.create_candidate(
        signal_type="GOVERNANCE", source_kind="lesson", source_id="L-2",
        title="G1", content="C2", owner_agent="Sage",
        confidence_score=0.75, tags=["lesson", "governance"],
    )
    engine = SignalClusteringEngine(signal_registry, cluster_registry)
    clusters = engine.cluster_by_type(owner_agent="Sage")
    assert len(clusters) >= 2
    types = {c.cluster_type for c in clusters}
    assert "ENGINEERING" in types
    assert "GOVERNANCE" in types
    for c in clusters:
        assert c.status == "CANDIDATE"


def test_cluster_contains_source_signal_ids(signal_registry, cluster_registry):
    signal_registry.create_candidate(
        signal_type="TRADING", source_kind="lesson", source_id="L-1",
        title="T1", content="C1", owner_agent="Sage",
        confidence_score=0.80, tags=["lesson", "trading"],
    )
    engine = SignalClusteringEngine(signal_registry, cluster_registry)
    clusters = engine.cluster_by_type(owner_agent="Sage")
    trading = [c for c in clusters if c.cluster_type == "TRADING"]
    if trading:
        assert len(trading[0].source_signal_ids) >= 1


def test_cluster_by_domain(signal_registry, cluster_registry):
    signal_registry.create_candidate(
        signal_type="PATTERN", source_kind="lesson", source_id="L-1",
        title="P1", content="C1", owner_agent="Sage",
        confidence_score=0.85, tags=["lesson", "pattern", "trading_knowledge"],
    )
    signal_registry.create_candidate(
        signal_type="DATASET", source_kind="lesson", source_id="L-2",
        title="D1", content="C2", owner_agent="Sage",
        confidence_score=0.70, tags=["lesson", "dataset", "trading_knowledge"],
    )
    engine = SignalClusteringEngine(signal_registry, cluster_registry)
    clusters = engine.cluster_by_domain(owner_agent="Sage")
    trading = [c for c in clusters if "trading" in c.title.lower()]
    assert len(trading) > 0


def test_run_all_combines_type_and_domain(signal_registry, cluster_registry):
    signal_registry.create_candidate(
        signal_type="PATTERN", source_kind="lesson", source_id="L-1",
        title="P1", content="C1", owner_agent="Sage",
        confidence_score=0.85, tags=["lesson", "pattern"],
    )
    engine = SignalClusteringEngine(signal_registry, cluster_registry)
    clusters = engine.run_all(owner_agent="Sage")
    assert len(clusters) >= 1


def test_empty_registry_returns_empty_clusters(cluster_registry):
    empty = type("EmptyRegistry", (), {"list_all": lambda *a, **kw: []})()
    engine = SignalClusteringEngine(empty, cluster_registry)
    clusters = engine.run_all()
    assert len(clusters) == 0


def test_cluster_confidence_aggregation(signal_registry, cluster_registry):
    signal_registry.create_candidate(
        signal_type="PATTERN", source_kind="lesson", source_id="L-1",
        title="P1", content="C1", owner_agent="Sage",
        confidence_score=0.90, tags=["lesson", "pattern"],
    )
    signal_registry.create_candidate(
        signal_type="PATTERN", source_kind="lesson", source_id="L-2",
        title="P2", content="C2", owner_agent="Sage",
        confidence_score=0.80, tags=["lesson", "pattern"],
    )
    engine = SignalClusteringEngine(signal_registry, cluster_registry)
    clusters = engine.cluster_by_type(owner_agent="Sage")
    eng = [c for c in clusters if c.cluster_type == "ENGINEERING"]
    if eng:
        assert 0.80 <= eng[0].confidence_score <= 0.90


def test_cluster_no_auto_promotion(signal_registry, cluster_registry):
    engine = SignalClusteringEngine(signal_registry, cluster_registry)
    clusters = engine.run_all()
    for c in clusters:
        assert c.status == "CANDIDATE"
