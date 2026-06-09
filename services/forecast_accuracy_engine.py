"""Forecast Accuracy Engine - Compare forecasts against reality."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_forecast_registry() -> dict:
    import yaml
    path = REGISTRIES_DIR / "KINGDOM_MARKET_FORECAST_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_accuracy_registry() -> dict:
    import yaml
    path = REGISTRIES_DIR / "KINGDOM_FORECAST_ACCURACY_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_accuracy_registry(registry: dict) -> None:
    import yaml
    path = REGISTRIES_DIR / "KINGDOM_FORECAST_ACCURACY_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_accuracy_id() -> str:
    registry = _load_accuracy_registry()
    inner = registry.get("kingdom_forecast_accuracy_registry", registry)
    counter = len(inner.get("accuracy_records", [])) + 1
    return f"ACCU-{counter:04d}"


def _calculate_direction_accuracy(forecast: dict, price_path: list[float]) -> tuple[bool, float]:
    if not price_path:
        return (False, 0.0)
    direction = forecast.get("forecast_direction", "neutral")
    if direction == "neutral":
        return (True, 0.5)
    start = price_path[0] if price_path else 0
    end = price_path[-1] if price_path else 0
    actual_direction = "long" if end > start * 1.0001 else "short" if end < start * 0.9999 else "neutral"
    return (actual_direction == direction, 0.0 if actual_direction != direction else 0.5)


def _calculate_zone_accuracy(forecast: dict, price_path: list[float]) -> bool:
    zone_low = forecast.get("zone_low", 0)
    zone_high = forecast.get("zone_high", 0)
    if zone_low == 0 and zone_high == 0:
        return False
    touched = any(zone_low <= p <= zone_high for p in price_path)
    return touched


def calculate_accuracy(forecast_id: str, hours_waited: int = 1) -> dict[str, Any]:
    inner = _load_forecast_registry().get("kingdom_market_forecast_registry", {})
    forecast = None
    for f in inner.get("forecast_records", []):
        if f.get("forecast_id") == forecast_id:
            forecast = f
            break

    if not forecast:
        return {}

    symbol = forecast.get("symbol", "XAUUSDm")
    try:
        from connectors.mt5.mt5_demo_observer import MT5DemoObserver
        observer = MT5DemoObserver(symbol)
        ohlcv = observer.get_ohlcv(symbol, count=100).get("ohlcv", [])
    except Exception:
        ohlcv = []
    price_path = [c.get("close", 0) for c in ohlcv] if ohlcv else []

    dir_acc, dir_score = _calculate_direction_accuracy(forecast, price_path)
    zone_touched = _calculate_zone_accuracy(forecast, price_path)

    actual_result = "zone_hit" if zone_touched else "zone_miss"
    accuracy_score = (dir_score + (0.5 if zone_touched else 0.0)) / 2

    accuracy = {
        "accuracy_id": _generate_accuracy_id(),
        "forecast_id": forecast_id,
        "actual_result": actual_result,
        "accuracy_score": accuracy_score,
        "direction_accuracy": dir_acc,
        "zone_accuracy": zone_touched,
        "outcome": "success" if zone_touched else "miss",
        "reviewed_at": _utc_now(),
    }

    registry = _load_accuracy_registry()
    acc_inner = registry.get("kingdom_forecast_accuracy_registry", {})
    acc_inner.setdefault("accuracy_records", []).append(accuracy)
    acc_inner["last_accuracy_id"] = accuracy["accuracy_id"]
    acc_inner["last_updated"] = _utc_now()
    registry["kingdom_forecast_accuracy_registry"] = acc_inner
    _save_accuracy_registry(registry)

    return accuracy


def list_all_accuracies() -> list[dict]:
    registry = _load_accuracy_registry()
    inner = registry.get("kingdom_forecast_accuracy_registry", {})
    return inner.get("accuracy_records", [])


def get_accuracy_by_forecast(forecast_id: str) -> dict | None:
    for acc in list_all_accuracies():
        if acc.get("forecast_id") == forecast_id:
            return acc
    return None


__all__ = ["calculate_accuracy", "list_all_accuracies", "get_accuracy_by_forecast"]