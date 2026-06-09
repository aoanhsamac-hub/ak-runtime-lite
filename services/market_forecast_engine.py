"""Market Forecast Engine - Generate forecasts from market snapshots."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
FORBIDDEN_MODES = ["LIVE", "PRODUCTION", "EXECUTION", "ORDER_PLACEMENT", "STRATEGY_MODIFICATION"]
SYMBOLS = ["XAUUSDm", "EURUSDm", "GBPUSDm", "USDJPYm", "USDCADm", "EURGBPm"]
TIMEFRAMES = ["H1", "H4", "D1"]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_registry() -> dict:
    import yaml
    path = REGISTRIES_DIR / "KINGDOM_MARKET_FORECAST_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry: dict) -> None:
    import yaml
    path = REGISTRIES_DIR / "KINGDOM_MARKET_FORECAST_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_forecast_id(symbol: str, tf: str) -> str:
    registry = _load_registry()
    inner = registry.get("kingdom_market_forecast_registry", registry)
    counter = len(inner.get("forecast_records", [])) + 1
    return f"FCST-{symbol}-{tf}-{counter:04d}"


def _detect_market_state(ohlcv: list[dict]) -> str:
    if not ohlcv or len(ohlcv) < 2:
        return "unknown"
    closes = [c.get("close", 0) for c in ohlcv[-10:]]
    if len(closes) < 2:
        return "unknown"
    avg = sum(closes) / len(closes)
    if closes[-1] > avg * 1.002:
        return "bullish"
    if closes[-1] < avg * 0.998:
        return "bearish"
    return "neutral"


def _detect_regime(ohlcv: list[dict]) -> str:
    returns = [abs(c.get("close", 0) - c.get("open", 0)) for c in ohlcv[-20:]] if ohlcv else []
    if not returns:
        return "unknown"
    volatility = sum(returns) / len(returns) if returns else 0
    if volatility > 0.001:
        return "volatile"
    if volatility < 0.0001:
        return "quiet"
    return "normal"


def _calculate_zone_bounds(ohlcv: list[dict]) -> tuple[float, float]:
    if not ohlcv:
        return (0.0, 0.0)
    highs = [c.get("high", 0) for c in ohlcv[-20:]]
    lows = [c.get("low", 0) for c in ohlcv[-20:]]
    return (min(lows) if lows else 0.0, max(highs) if highs else 0.0)


def generate_forecast(symbol: str, timeframe: str) -> dict[str, Any]:
    ohlcv = []
    try:
        from connectors.mt5.mt5_demo_observer import MT5DemoObserver
        from services.iris.market_snapshot import MarketSnapshotCollector

        observer = MT5DemoObserver(symbol)
        collector = MarketSnapshotCollector(observer)
        snapshot = collector.collect(symbol, timeframe, count=100)

        ohlcv = snapshot.ohlcv if snapshot.ohlcv else []
    except Exception:
        pass
    zone_low, zone_high = _calculate_zone_bounds(ohlcv)
    market_state = _detect_market_state(ohlcv)
    regime = _detect_regime(ohlcv)

    forecast_id = _generate_forecast_id(symbol, timeframe)
    forecast = {
        "forecast_id": forecast_id,
        "timestamp": _utc_now(),
        "symbol": symbol,
        "timeframe": timeframe,
        "market_state": market_state,
        "forecast_direction": "long" if market_state == "bullish" else "short" if market_state == "bearish" else "neutral",
        "confidence": 0.5 if len(ohlcv) else 0.0,
        "forecast_reason": f"Zone {zone_low:.2f}-{zone_high:.2f} detected, state={market_state}",
        "forecast_horizon": f"1-{timeframe}",
        "zone_low": zone_low,
        "zone_high": zone_high,
        "regime": regime,
        "status": "PENDING_VALIDATION",
    }

    registry = _load_registry()
    inner = registry.get("kingdom_market_forecast_registry", registry)
    inner.setdefault("forecast_records", []).append(forecast)
    inner["last_forecast_id"] = forecast_id
    inner["last_updated"] = _utc_now()
    registry["kingdom_market_forecast_registry"] = inner
    _save_registry(registry)

    return forecast


def generate_all_forecasts(symbols: list[str] | None = None, timeframes: list[str] | None = None) -> list[dict]:
    symbols = symbols or SYMBOLS
    timeframes = timeframes or TIMEFRAMES
    forecasts = []
    for symbol in symbols:
        for tf in timeframes:
            try:
                f = generate_forecast(symbol, tf)
                forecasts.append(f)
            except Exception:
                continue
    return forecasts


def get_forecast(forecast_id: str) -> dict | None:
    registry = _load_registry()
    inner = registry.get("kingdom_market_forecast_registry", registry)
    for f in inner.get("forecast_records", []):
        if f.get("forecast_id") == forecast_id:
            return f
    return None


def list_pending_forecasts() -> list[dict]:
    registry = _load_registry()
    inner = registry.get("kingdom_market_forecast_registry", registry)
    return [f for f in inner.get("forecast_records", []) if f.get("status") == "PENDING_VALIDATION"]


__all__ = ["generate_forecast", "generate_all_forecasts", "get_forecast", "list_pending_forecasts"]