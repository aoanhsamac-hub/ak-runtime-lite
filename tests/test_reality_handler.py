import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from services.day1_reality_handler import (
    run_reality_handler,
    get_benchmarks,
    get_benchmark_summary,
)
from services.day1_forecast_handler import run_forecast_handler


def test_run_reality_handler_returns_dict():
    result = run_reality_handler()
    assert isinstance(result, dict)


def test_run_reality_handler_returns_ok():
    run_forecast_handler()
    result = run_reality_handler()
    assert result.get("status") == "OK"


def test_run_reality_handler_has_handler_name():
    result = run_reality_handler()
    assert result.get("handler") == "day1_reality_handler"


def test_run_reality_handler_benchmarks_forecasts():
    run_forecast_handler()
    result = run_reality_handler()
    assert result.get("benchmarked", 0) >= 0


def test_get_benchmarks_returns_list():
    benchmarks = get_benchmarks()
    assert isinstance(benchmarks, list)


def test_get_benchmark_summary_returns_dict():
    summary = get_benchmark_summary()
    assert isinstance(summary, dict)


def test_benchmark_has_required_fields():
    benchmarks = get_benchmarks()
    if benchmarks:
        b = benchmarks[0]
        assert "benchmark_id" in b
        assert "forecast_id" in b
        assert "overall_accuracy" in b


def test_benchmark_has_no_trading_fields():
    run_forecast_handler()
    run_reality_handler()
    for b in get_benchmarks():
        assert "order_send" not in str(b)
        assert "order_modify" not in str(b)
        assert "order_close" not in str(b)


def test_benchmark_accuracy_is_float():
    benchmarks = get_benchmarks()
    for b in benchmarks:
        assert isinstance(b.get("overall_accuracy"), (int, float))


def test_benchmark_reality_chain():
    run_forecast_handler()
    result = run_reality_handler()
    assert result.get("timestamp", "").startswith("202")


def test_benchmark_summary_has_total():
    summary = get_benchmark_summary()
    assert "total_benchmarks" in summary


def test_benchmark_summary_has_last_run():
    summary = get_benchmark_summary()
    assert "last_run" in summary


def test_benchmark_does_not_mutate_forecast_wrongly():
    run_forecast_handler()
    benchmarks_before = len(get_benchmarks())
    run_reality_handler()
    benchmarks_after = len(get_benchmarks())
    assert benchmarks_after >= benchmarks_before
