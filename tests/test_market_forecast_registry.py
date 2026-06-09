"""Test Market Forecast Registry."""

from memory.market_forecast_registry import FORECASTS, MarketForecastRegistry


def test_record_forecast():
    forecast = {"forecast_id": "test-fcst-1", "symbol": "XAUUSDm", "confidence_score": 0.8}
    result = FORECASTS.record(forecast)
    assert result["forecast_id"] == "test-fcst-1"


def test_get_forecast():
    fore = FORECASTS.get("test-fcst-1")
    assert fore is not None


def test_update_validation():
    validation = {"zone_touched": True, "final_score": 0.9}
    result = FORECASTS.update_validation("test-fcst-1", validation)
    assert result["status"] == "VALIDATED"


def test_registry_isolation():
    reg = MarketForecastRegistry()
    assert reg is not FORECASTS