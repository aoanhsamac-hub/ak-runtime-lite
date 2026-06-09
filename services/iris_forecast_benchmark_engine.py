"""Iris Forecast Benchmark Engine - Compare forecasts against actual outcomes."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_benchmark_registry() -> dict:
    import yaml
    path = REGISTRIES_DIR / "IRIS_FORECAST_BENCHMARK_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_benchmark_registry(registry: dict) -> None:
    import yaml
    path = REGISTRIES_DIR / "IRIS_FORECAST_BENCHMARK_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def benchmark_forecast(forecast: dict, ohlcv: list[dict]) -> dict[str, Any]:
    """Calculate forecast accuracy metrics."""
    prices = [c.get("close", 0) for c in ohlcv] if ohlcv else []

    direction_acc = 0.5
    zone_acc = 0.5
    structure_acc = 0.5

    if prices:
        predicted = forecast.get("forecast_direction", "neutral")
        actual_direction = "bullish" if prices[-1] > prices[0] * 1.001 else "bearish" if prices[-1] < prices[0] * 0.999 else "neutral"
        direction_acc = 1.0 if predicted == actual_direction else 0.0

    benchmark = {
        "benchmark_id": f"BENCH-{forecast.get('forecast_id', 'unknown')}",
        "forecast_id": forecast.get("forecast_id", ""),
        "direction_accuracy": direction_acc,
        "zone_accuracy": zone_acc,
        "structure_accuracy": structure_acc,
        "confidence_calibration": forecast.get("confidence", 0),
        "overall_accuracy": round((direction_acc + zone_acc + structure_acc) / 3, 2),
        "benchmarked_at": _utc_now(),
    }

    registry = _load_benchmark_registry()
    inner = registry.get("iris_forecast_benchmark_registry", {})
    inner.setdefault("benchmarks", []).append(benchmark)
    inner["last_updated"] = _utc_now()
    registry["iris_forecast_benchmark_registry"] = inner
    _save_benchmark_registry(registry)

    return benchmark


def get_benchmarks() -> list[dict]:
    return _load_benchmark_registry().get("iris_forecast_benchmark_registry", {}).get("benchmarks", [])


__all__ = ["benchmark_forecast", "get_benchmarks"]