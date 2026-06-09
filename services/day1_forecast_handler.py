from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
FORECAST_REGISTRY_FILE = "FORECAST_REGISTRY.json"
SYMBOLS = ["XAUUSDm", "EURUSDm", "GBPUSDm", "USDJPYm", "USDCADm", "EURGBPm"]
TIMEFRAMES = ["H1", "H4", "D1"]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_registry() -> dict:
    import json
    path = REGISTRIES_DIR / FORECAST_REGISTRY_FILE
    if not path.exists():
        return {"forecast_registry": {"forecast_records": [], "last_updated": "", "status": "INITIALIZED"}}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_registry(registry: dict) -> None:
    import json
    path = REGISTRIES_DIR / FORECAST_REGISTRY_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")


def _generate_forecast_id() -> str:
    registry = _load_registry()
    inner = registry.get("forecast_registry", {})
    counter = len(inner.get("forecast_records", [])) + 1
    return f"DAY1-FCST-{counter:04d}"


def run_forecast_handler() -> dict[str, Any]:
    registry = _load_registry()
    if "forecast_registry" not in registry:
        registry["forecast_registry"] = {}
    inner = registry["forecast_registry"]
    forecasts = []
    for symbol in SYMBOLS:
        for tf in TIMEFRAMES:
            try:
                forecast = {
                    "forecast_id": _generate_forecast_id(),
                    "timestamp": _utc_now(),
                    "symbol": symbol,
                    "timeframe": tf,
                    "market_state": "neutral",
                    "forecast_direction": "neutral",
                    "confidence": 0.5,
                    "forecast_reason": "DAY-1 activation — operational evidence collection",
                    "forecast_horizon": f"1-{tf}",
                    "zone_low": 0.0,
                    "zone_high": 0.0,
                    "regime": "normal",
                    "status": "PENDING_VALIDATION",
                    "handler_type": "day1_forecast_handler",
                }
                inner.setdefault("forecast_records", []).append(forecast)
                forecasts.append(forecast)
            except Exception as e:
                forecasts.append({"symbol": symbol, "timeframe": tf, "error": str(e)})
    inner["last_run"] = _utc_now()
    inner["forecast_count"] = len(forecasts)
    inner["status"] = "ACTIVE"
    _save_registry(registry)
    return {
        "status": "OK",
        "handler": "day1_forecast_handler",
        "forecasts_generated": len(forecasts),
        "timestamp": _utc_now(),
        "registry": str(REGISTRIES_DIR / FORECAST_REGISTRY_FILE),
    }


def get_forecasts() -> list[dict]:
    registry = _load_registry()
    return registry.get("forecast_registry", {}).get("forecast_records", [])


def get_forecast_summary() -> dict[str, Any]:
    records = get_forecasts()
    return {
        "total_forecasts": len(records),
        "by_status": _count_by(records, "status"),
        "by_symbol": _count_by(records, "symbol"),
        "last_run": _load_registry().get("forecast_registry", {}).get("last_run", ""),
    }


def _count_by(records: list[dict], key: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for r in records:
        k = str(r.get(key, "unknown"))
        result[k] = result.get(k, 0) + 1
    return result


__all__ = ["run_forecast_handler", "get_forecasts", "get_forecast_summary"]
