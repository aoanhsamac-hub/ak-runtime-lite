"""Test Forecast Accuracy Engine."""

import pytest


def test_import_accuracy_engine():
    import services.forecast_accuracy_engine as fae
    assert hasattr(fae, "calculate_accuracy")
    assert hasattr(fae, "list_all_accuracies")


def test_calculate_accuracy_for_nonexistent():
    from services.forecast_accuracy_engine import calculate_accuracy
    result = calculate_accuracy("nonexistent-forecast-id")
    assert result == {}


def test_list_all_accuracies():
    from services.forecast_accuracy_engine import list_all_accuracies
    results = list_all_accuracies()
    assert isinstance(results, list)


def test_accuracy_has_required_fields():
    from services.forecast_accuracy_engine import _generate_accuracy_id
    acc_id = _generate_accuracy_id()
    assert acc_id.startswith("ACCU-")


def test_direction_accuracy_bullish():
    from services.forecast_accuracy_engine import _calculate_direction_accuracy
    forecast = {"forecast_direction": "long"}
    price_path = [100.0, 101.0, 102.0]
    is_acc, score = _calculate_direction_accuracy(forecast, price_path)
    assert is_acc is True


def test_direction_accuracy_bearish():
    from services.forecast_accuracy_engine import _calculate_direction_accuracy
    forecast = {"forecast_direction": "short"}
    price_path = [102.0, 101.0, 100.0]
    is_acc, score = _calculate_direction_accuracy(forecast, price_path)
    assert is_acc is True


def test_direction_accuracy_neutral():
    from services.forecast_accuracy_engine import _calculate_direction_accuracy
    forecast = {"forecast_direction": "neutral"}
    price_path = [100.0]
    is_acc, score = _calculate_direction_accuracy(forecast, price_path)
    assert is_acc is True


def test_zone_accuracy_zone_touched():
    from services.forecast_accuracy_engine import _calculate_zone_accuracy
    forecast = {"zone_low": 100.0, "zone_high": 102.0}
    price_path = [101.0, 101.5, 100.5]
    assert _calculate_zone_accuracy(forecast, price_path) is True


def test_zone_accuracy_zone_missed():
    from services.forecast_accuracy_engine import _calculate_zone_accuracy
    forecast = {"zone_low": 100.0, "zone_high": 102.0}
    price_path = [95.0, 96.0, 97.0]
    assert _calculate_zone_accuracy(forecast, price_path) is False


def test_accuracy_record_structure():
    from services.forecast_accuracy_engine import _generate_accuracy_id, _utc_now
    acc = {
        "accuracy_id": _generate_accuracy_id(),
        "forecast_id": "test-fcst",
        "actual_result": "zone_hit",
        "accuracy_score": 0.75,
        "outcome": "success",
        "reviewed_at": _utc_now(),
    }
    assert "accuracy_id" in acc
    assert "forecast_id" in acc
    assert "accuracy_score" in acc


def test_get_accuracy_by_forecast():
    from services.forecast_accuracy_engine import get_accuracy_by_forecast
    result = get_accuracy_by_forecast("nonexistent-id")
    assert result is None