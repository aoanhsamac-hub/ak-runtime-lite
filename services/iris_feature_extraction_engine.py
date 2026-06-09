"""Iris Feature Extraction Engine - Extract market features from data."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_feature_registry() -> dict:
    import yaml
    path = REGISTRIES_DIR / "IRIS_FEATURE_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_feature_registry(registry: dict) -> None:
    import yaml
    path = REGISTRIES_DIR / "IRIS_FEATURE_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def extract_features(ohlcv: list[dict], symbol: str) -> dict[str, Any]:
    """Extract market features from OHLCV data."""
    features = {
        "feature_id": f"FEAT-{symbol}-{datetime.now().strftime('%Y%m%d%H%M')}",
        "symbol": symbol,
        "timestamp": _utc_now(),
    }

    if not ohlcv:
        features.update({"trend": "unknown", "volatility": 0, "error": "No data"})
        return features

    prices = [c.get("close", 0) for c in ohlcv]
    highs = [c.get("high", 0) for c in ohlcv]
    lows = [c.get("low", 0) for c in ohlcv]

    features["trend"] = "bullish" if prices[-1] > prices[0] * 1.01 else "bearish" if prices[-1] < prices[0] * 0.99 else "neutral"
    features["volatility"] = round((max(highs) - min(lows)) / min(lows) if min(lows) > 0 else 0, 6)
    features["momentum"] = round((prices[-1] - prices[0]) / prices[0] if prices[0] > 0 else 0, 6)
    features["range"] = round(max(highs) - min(lows), 2)

    registry = _load_feature_registry()
    inner = registry.get("iris_feature_registry", {})
    inner.setdefault("features", []).append(features)
    inner["last_updated"] = _utc_now()
    registry["iris_feature_registry"] = inner
    _save_feature_registry(registry)

    return features


def get_features() -> list[dict]:
    return _load_feature_registry().get("iris_feature_registry", {}).get("features", [])


__all__ = ["extract_features", "get_features"]