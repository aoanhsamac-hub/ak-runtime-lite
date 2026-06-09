"""Iris Data Import Engine - Validate and register market datasets."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_dataset_registry() -> dict:
    import yaml
    path = REGISTRIES_DIR / "IRIS_DATASET_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_dataset_registry(registry: dict) -> None:
    import yaml
    path = REGISTRIES_DIR / "IRIS_DATASET_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_dataset_id(symbol: str, tf: str) -> str:
    return f"IRIS-DATASET-{symbol}-{tf}-{datetime.now().strftime('%Y%m%d')}"


def validate_dataset(ohlcv: list[dict], symbol: str, timeframe: str) -> dict[str, Any]:
    """Validate OHLCV data integrity."""
    issues = []
    valid = True

    if not ohlcv:
        issues.append("Empty dataset")
        valid = False

    for i, bar in enumerate(ohlcv):
        if bar.get("high", 0) < bar.get("low", 0):
            issues.append(f"OHLC integrity error at index {i}")
            valid = False

    quality = {
        "dataset_id": _generate_dataset_id(symbol, timeframe),
        "symbol": symbol,
        "timeframe": timeframe,
        "record_count": len(ohlcv),
        "is_valid": valid,
        "issues": issues,
        "quality_score": 100 if valid else max(0, 100 - len(issues) * 10),
        "validated_at": _utc_now(),
    }

    registry = _load_dataset_registry()
    inner = registry.get("iris_dataset_registry", {})
    inner.setdefault("datasets", []).append(quality)
    inner["last_updated"] = _utc_now()
    registry["iris_dataset_registry"] = inner
    _save_dataset_registry(registry)

    return quality


def get_dataset_register() -> list[dict]:
    return _load_dataset_registry().get("iris_dataset_registry", {}).get("datasets", [])


def get_market_snapshot() -> dict:
    from connectors.mt5.mt5_demo_observer import MT5DemoObserver
    from services.iris.market_snapshot import MarketSnapshotCollector

    try:
        observer = MT5DemoObserver("XAUUSDm")
        collector = MarketSnapshotCollector(observer)
        snapshot = collector.collect("XAUUSDm", "H1", count=100)
        return {
            "symbol": snapshot.symbol,
            "ohlcv_count": len(snapshot.ohlcv),
            "session": snapshot.session,
            "timestamp": snapshot.timestamp,
        }
    except Exception:
        return {"symbol": "XAUUSDm", "ohlcv_count": 0, "session": "unknown"}


__all__ = ["validate_dataset", "get_dataset_register", "get_market_snapshot"]