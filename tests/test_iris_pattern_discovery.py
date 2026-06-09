"""Test Iris Pattern Discovery."""

import pytest


def test_import_pattern_engine():
    import services.iris_pattern_discovery_engine as pde
    assert hasattr(pde, "discover_patterns")


def test_discover_patterns_empty():
    from services.iris_pattern_discovery_engine import discover_patterns
    result = discover_patterns({}, "XAUUSDm")
    assert isinstance(result, list)


def test_discover_patterns_bullish():
    from services.iris_pattern_discovery_engine import discover_patterns
    features = {"trend": "bullish", "momentum": 0.05}
    patterns = discover_patterns(features, "XAUUSDm")
    assert len(patterns) >= 1


def test_discover_patterns_volatility():
    from services.iris_pattern_discovery_engine import discover_patterns
    features = {"trend": "neutral", "volatility": 0.05}
    patterns = discover_patterns(features, "XAUUSDm")
    types = [p.get("type") for p in patterns]
    assert "high_volatility" in types


def test_pattern_has_type():
    from services.iris_pattern_discovery_engine import discover_patterns
    features = {"trend": "bullish", "momentum": 0.05}
    patterns = discover_patterns(features, "XAUUSDm")
    for p in patterns:
        assert "type" in p


def test_pattern_confidence():
    from services.iris_pattern_discovery_engine import discover_patterns
    features = {"trend": "bullish", "momentum": 0.05}
    patterns = discover_patterns(features, "XAUUSDm")
    for p in patterns:
        assert "confidence" in p


def test_pattern_registry():
    from services.iris_pattern_discovery_engine import discover_patterns, get_patterns
    discover_patterns({"trend": "bullish"}, "EURUSDm")
    all_patterns = get_patterns()
    assert len(all_patterns) >= 1