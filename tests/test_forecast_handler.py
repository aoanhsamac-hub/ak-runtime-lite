import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from services.day1_forecast_handler import (
    run_forecast_handler,
    get_forecasts,
    get_forecast_summary,
)


def test_run_forecast_handler_returns_dict():
    result = run_forecast_handler()
    assert isinstance(result, dict)
    assert result.get("status") == "OK"


def test_run_forecast_handler_returns_handler_name():
    result = run_forecast_handler()
    assert result.get("handler") == "day1_forecast_handler"


def test_run_forecast_handler_generates_forecasts():
    result = run_forecast_handler()
    assert result.get("forecasts_generated", 0) > 0


def test_run_forecast_handler_has_timestamp():
    result = run_forecast_handler()
    assert result.get("timestamp", "").startswith("202")


def test_get_forecasts_returns_list():
    forecasts = get_forecasts()
    assert isinstance(forecasts, list)


def test_get_forecasts_contains_dicts():
    forecasts = get_forecasts()
    if forecasts:
        assert isinstance(forecasts[0], dict)


def test_get_forecast_summary_returns_dict():
    summary = get_forecast_summary()
    assert isinstance(summary, dict)


def test_get_forecast_summary_has_total():
    summary = get_forecast_summary()
    assert "total_forecasts" in summary


def test_forecast_has_required_fields():
    forecasts = get_forecasts()
    if forecasts:
        f = forecasts[0]
        assert "forecast_id" in f
        assert "symbol" in f
        assert "timeframe" in f
        assert "timestamp" in f


def test_forecast_has_no_trading_fields():
    forecasts = get_forecasts()
    for f in forecasts:
        assert "order_send" not in str(f)
        assert "order_modify" not in str(f)
        assert "order_close" not in str(f)


def test_forecast_summary_by_status():
    summary = get_forecast_summary()
    assert "by_status" in summary
    assert isinstance(summary["by_status"], dict)

def test_forecast_summary_by_symbol():
    summary = get_forecast_summary()
    assert "by_symbol" in summary

def test_multiple_runs_dont_crash():
    for _ in range(3):
        r = run_forecast_handler()
        assert r["status"] == "OK"

def test_forecast_count_increases():
    before = len(get_forecasts())
    run_forecast_handler()
    after = len(get_forecasts())
    assert after >= before
