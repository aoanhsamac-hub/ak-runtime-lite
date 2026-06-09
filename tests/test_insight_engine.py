from services.insight_engine import InsightEngine


def test_consolidate_signals_groups_by_type(signal_registry_with_data, insight_registry):
    engine = InsightEngine(signal_registry_with_data, insight_registry)
    insights = engine.consolidate_signals(owner_agent="Sage")
    assert len(insights) >= 3
    types = {i.insight_type for i in insights}
    assert "PATTERN" in types or "CONSOLIDATION" in types
    for ins in insights:
        assert ins.status == "CANDIDATE"


def test_consolidate_signals_carries_source_signal_ids(signal_registry_with_data, insight_registry):
    engine = InsightEngine(signal_registry_with_data, insight_registry)
    insights = engine.consolidate_signals(owner_agent="Sage")
    for ins in insights:
        assert len(ins.source_signal_ids) > 0


def test_generate_trend_insight(signal_registry_with_data, insight_registry):
    engine = InsightEngine(signal_registry_with_data, insight_registry)
    trend = engine.generate_trend_insight(owner_agent="Sage")
    assert trend is not None
    assert trend.insight_type == "TREND"
    assert trend.status == "CANDIDATE"


def test_generate_trend_insight_returns_none_when_no_signals(insight_registry):
    empty_registry = type("EmptyRegistry", (), {"list_all": lambda *a, **kw: []})()
    engine = InsightEngine(empty_registry, insight_registry)
    trend = engine.generate_trend_insight(owner_agent="Sage")
    assert trend is None


def test_generate_gap_insight(signal_registry_with_data, insight_registry):
    engine = InsightEngine(signal_registry_with_data, insight_registry)
    gap = engine.generate_gap_insight(owner_agent="Sage")
    assert gap is not None
    assert gap.insight_type == "GAP"


def test_generate_gap_insight_returns_none_when_no_anomalies(insight_registry):
    empty = type("EmptyRegistry", (), {"list_all": lambda *a, **kw: []})()
    engine = InsightEngine(empty, insight_registry)
    gap = engine.generate_gap_insight()
    assert gap is None


def test_generate_risk_insight(signal_registry_with_data, insight_registry):
    engine = InsightEngine(signal_registry_with_data, insight_registry)
    risk = engine.generate_risk_insight(owner_agent="Sage")
    assert risk is not None
    assert risk.insight_type == "RISK"


def test_run_all_returns_all_categories(signal_registry_with_data, insight_registry):
    engine = InsightEngine(signal_registry_with_data, insight_registry)
    results = engine.run_all(owner_agent="Sage")
    assert "consolidated" in results
    assert "trends" in results
    assert "gaps" in results
    assert "risks" in results


def test_insight_engine_no_auto_promotion(signal_registry_with_data, insight_registry):
    engine = InsightEngine(signal_registry_with_data, insight_registry)
    results = engine.run_all(owner_agent="Sage")
    for category in results.values():
        for ins in category:
            assert ins.status == "CANDIDATE"
