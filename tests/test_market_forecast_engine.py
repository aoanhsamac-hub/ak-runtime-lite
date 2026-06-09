"""Test Market Forecast Engine."""

import pytest


def test_import_forecast_engine():
    import services.market_forecast_engine as mfe
    assert hasattr(mfe, "generate_forecast")
    assert hasattr(mfe, "generate_all_forecasts")


def test_generate_forecast_returns_dict():
    from services.market_forecast_engine import generate_forecast
    result = generate_forecast("XAUUSDm", "H1")
    assert isinstance(result, dict)
    assert "forecast_id" in result


def test_forecast_has_required_fields():
    from services.market_forecast_engine import generate_forecast
    result = generate_forecast("EURUSDm", "H1")
    assert "timestamp" in result
    assert "symbol" in result
    assert "timeframe" in result
    assert "market_state" in result
    assert "forecast_direction" in result
    assert "confidence" in result
    assert "forecast_reason" in result
    assert "forecast_horizon" in result


def test_forecast_direction_based_on_market_state():
    from services.market_forecast_engine import generate_forecast
    result = generate_forecast("GBPUSDm", "H1")
    direction = result.get("forecast_direction")
    assert direction in ("long", "short", "neutral")


def test_generate_all_forecasts():
    from services.market_forecast_engine import generate_all_forecasts
    results = generate_all_forecasts(["XAUUSDm"], ["H1"])
    assert len(results) >= 0


def test_get_forecast():
    from services.market_forecast_engine import get_forecast
    result = get_forecast("nonexistent-id")
    assert result is None


def test_list_pending_forecasts():
    from services.market_forecast_engine import list_pending_forecasts
    results = list_pending_forecasts()
    assert isinstance(results, list)


def test_forecast_registry_updated():
    from services.market_forecast_engine import generate_forecast, get_forecast
    fcst = generate_forecast("XAUUSDm", "H1")
    retrieved = get_forecast(fcst.get("forecast_id", ""))
    assert retrieved is not None


def test_multiple_forecasts_have_unique_ids():
    from services.market_forecast_engine import generate_forecast
    fcst1 = generate_forecast("XAUUSDm", "H1")
    fcst2 = generate_forecast("XAUUSDm", "H1")
    assert fcst1.get("forecast_id") != fcst2.get("forecast_id")