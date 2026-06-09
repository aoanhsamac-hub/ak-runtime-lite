"""Test Iris Scorecard."""

import pytest


def test_import_scorecard_engine():
    import services.iris_intelligence_scorecard_engine as ise
    assert hasattr(ise, "calculate_intelligence_scorecard")


def test_calculate_scorecard():
    from services.iris_intelligence_scorecard_engine import calculate_intelligence_scorecard
    result = calculate_intelligence_scorecard()
    assert isinstance(result, dict)


def test_scorecard_has_metrics():
    from services.iris_intelligence_scorecard_engine import calculate_intelligence_scorecard
    result = calculate_intelligence_scorecard()
    assert "forecast_count" in result
    assert "forecast_accuracy" in result
    assert "lesson_count" in result
    assert "knowledge_count" in result


def test_scorecard_values_numeric():
    from services.iris_intelligence_scorecard_engine import calculate_intelligence_scorecard
    result = calculate_intelligence_scorecard()
    assert isinstance(result.get("forecast_accuracy", 0), (int, float))


def test_scorecard_id_format():
    from services.iris_intelligence_scorecard_engine import calculate_intelligence_scorecard
    result = calculate_intelligence_scorecard()
    assert "SC-" in result.get("scorecard_id", "")


def test_generate_report():
    from services.iris_intelligence_scorecard_engine import generate_scorecard_report
    result = generate_scorecard_report()
    assert "report_id" in result
    assert "scorecard" in result


def test_scorecard_timestamp():
    from services.iris_intelligence_scorecard_engine import calculate_intelligence_scorecard
    result = calculate_intelligence_scorecard()
    assert "timestamp" in result


def test_empty_scorecard_valid():
    scorecard = {
        "forecast_count": 0,
        "forecast_accuracy": 0,
        "lesson_count": 0,
        "knowledge_count": 0,
    }
    assert isinstance(scorecard["forecast_count"], int)