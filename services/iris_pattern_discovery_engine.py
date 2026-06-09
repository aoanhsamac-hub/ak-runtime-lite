"""Iris Pattern Discovery Engine - Discover market patterns."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_pattern_registry() -> dict:
    import yaml
    path = REGISTRIES_DIR / "IRIS_PATTERN_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_pattern_registry(registry: dict) -> None:
    import yaml
    path = REGISTRIES_DIR / "IRIS_PATTERN_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def discover_patterns(features: dict, symbol: str) -> list[dict]:
    """Discover patterns from market features."""
    patterns = []

    if features.get("trend") == "bullish" and features.get("momentum", 0) > 0:
        patterns.append({
            "pattern_id": f"PATTERN-{symbol}-BULL-001",
            "symbol": symbol,
            "type": "trend_continuation",
            "confidence": 0.8,
            "timestamp": _utc_now(),
        })

    if features.get("volatility", 0) > 0.01:
        patterns.append({
            "pattern_id": f"PATTERN-{symbol}-VOL-001",
            "symbol": symbol,
            "type": "high_volatility",
            "confidence": 0.7,
            "timestamp": _utc_now(),
        })

    if features.get("momentum", 0) > 0.02:
        patterns.append({
            "pattern_id": f"PATTERN-{symbol}-MOM-001",
            "symbol": symbol,
            "type": "strong_momentum",
            "confidence": 0.85,
            "timestamp": _utc_now(),
        })

    registry = _load_pattern_registry()
    inner = registry.get("iris_pattern_registry", {})
    inner.setdefault("patterns", []).extend(patterns)
    inner["last_updated"] = _utc_now()
    registry["iris_pattern_registry"] = inner
    _save_pattern_registry(registry)

    return patterns


def get_patterns() -> list[dict]:
    return _load_pattern_registry().get("iris_pattern_registry", {}).get("patterns", [])


__all__ = ["discover_patterns", "get_patterns"]