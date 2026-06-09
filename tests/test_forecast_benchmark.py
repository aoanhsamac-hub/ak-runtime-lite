"""Test Forecast Benchmark Engine."""

import pytest


def test_import_benchmark_engine():
    import services.iris_forecast_benchmark_engine as fbe
    assert hasattr(fbe, "benchmark_forecast")


def test_benchmark_forecast():
    from services.iris_forecast_benchmark_engine import benchmark_forecast
    forecast = {"forecast_id": "test-001", "forecast_direction": "bullish", "confidence": 0.8}
    ohlcv = [{"open": 100, "high": 105, "low": 99, "close": 106}]
    result = benchmark_forecast(forecast, ohlcv)
    assert "overall_accuracy" in result


def test_benchmark_empty_data():
    from services.iris_forecast_benchmark_engine import benchmark_forecast
    forecast = {"forecast_id": "test-002"}
    result = benchmark_forecast(forecast, [])
    assert result["direction_accuracy"] == 0.5


def test_benchmark_calculates_direction():
    from services.iris_forecast_benchmark_engine import benchmark_forecast
    forecast = {"forecast_id": "test-003", "forecast_direction": "bullish"}
    ohlcv = [{"open": 100, "high": 110, "low": 99, "close": 106}]
    result = benchmark_forecast(forecast, ohlcv)
    assert "direction_accuracy" in result


def test_benchmark_stores_result():
    from services.iris_forecast_benchmark_engine import benchmark_forecast, get_benchmarks
    forecast = {"forecast_id": "test-004", "forecast_direction": "bullish"}
    ohlcv = [{"open": 100, "high": 110, "low": 99, "close": 106}]
    benchmark_forecast(forecast, ohlcv)
    benchmarks = get_benchmarks()
    assert len(benchmarks) >= 1


def test_benchmark_id_format():
    from services.iris_forecast_benchmark_engine import benchmark_forecast
    forecast = {"forecast_id": "test-005", "forecast_direction": "bullish"}
    result = benchmark_forecast(forecast, [{"open": 100, "high": 105, "low": 99, "close": 106}])
    assert "BENCH-" in result.get("benchmark_id", "")