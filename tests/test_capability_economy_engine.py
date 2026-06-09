"""Test Capability Economy Engine."""

import pytest


def test_import_capability_economy_engine():
    import services.capability_economy_engine as cee
    assert hasattr(cee, "evaluate_capability_economy")
    assert hasattr(cee, "get_capability_metrics")


def test_evaluate_capability_economy():
    from services.capability_economy_engine import evaluate_capability_economy
    result = evaluate_capability_economy()
    assert isinstance(result, dict)
    assert "capability_economy_level" in result


def test_economy_has_required_fields():
    from services.capability_economy_engine import evaluate_capability_economy
    result = evaluate_capability_economy()
    assert "total_capabilities" in result
    assert "total_usage_events" in result
    assert "total_value" in result


def test_capability_metrics():
    from services.capability_economy_engine import get_capability_metrics
    result = get_capability_metrics("test-capability")
    assert "capability_name" in result


def test_domain_economy():
    from services.capability_economy_engine import get_domain_economy
    result = get_domain_economy("governance")
    assert "domain" in result


def test_level_calculation_empty():
    from services.capability_economy_engine import _calculate_level
    assert _calculate_level(0, 0, 0) == 1


def test_level_calculation_with_usage():
    from services.capability_economy_engine import _calculate_level
    assert _calculate_level(10, 0, 0) == 2


def test_level_calculation_with_value():
    from services.capability_economy_engine import _calculate_level
    assert _calculate_level(10, 100.0, 0) == 3


def test_level_calculation_max():
    from services.capability_economy_engine import _calculate_level
    assert _calculate_level(10, 100.0, 5) == 4


def test_timestamp_in_result():
    from services.capability_economy_engine import evaluate_capability_economy
    result = evaluate_capability_economy()
    assert "timestamp" in result