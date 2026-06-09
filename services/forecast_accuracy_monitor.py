from datetime import datetime, timezone
from pathlib import Path

SERVICES_DIR = Path(__file__).resolve().parent.parent / "services"
FORBIDDEN_MODES = ["LIVE", "PRODUCTION", "EXECUTION", "ORDER_PLACEMENT", "STRATEGY_MODIFICATION"]


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def check():
    forecast_available = False
    forecast_count = 0
    try:
        from services.iris.zone_validation_engine import MarketForecast
        forecast_available = True
    except (ImportError, Exception):
        pass
    return {
        "status": "INITIALIZED",
        "score": 0,
        "forecast_available": forecast_available,
        "forecast_count": forecast_count,
        "accuracy": None,
        "detail": "Forecast accuracy not calculable — no actual trades to validate against.",
        "generated_at": _utc_now(),
    }
