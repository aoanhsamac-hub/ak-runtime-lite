from datetime import datetime, timezone
from pathlib import Path

SERVICES_DIR = Path(__file__).resolve().parent.parent / "services"
FORBIDDEN_MODES = ["LIVE", "PRODUCTION", "EXECUTION", "ORDER_PLACEMENT", "STRATEGY_MODIFICATION"]


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def check():
    zone_types_found = []
    try:
        from services.iris.zone_detector import ZoneDetector
        detector = ZoneDetector()
        zone_types_found = list(getattr(detector, "zone_types", {}).keys())
    except (ImportError, Exception):
        pass
    return {
        "status": "INITIALIZED",
        "score": 0,
        "zone_types_found": zone_types_found,
        "zone_count": 0,
        "detail": "Zone quality not calculable — no trading zones generated.",
        "generated_at": _utc_now(),
    }
