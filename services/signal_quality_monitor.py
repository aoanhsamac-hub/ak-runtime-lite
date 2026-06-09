from datetime import datetime, timezone
from pathlib import Path

SERVICES_DIR = Path(__file__).resolve().parent.parent / "services"
FORBIDDEN_MODES = ["LIVE", "PRODUCTION", "EXECUTION", "ORDER_PLACEMENT", "STRATEGY_MODIFICATION"]


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def check():
    signal_pipelines_found = []
    try:
        import importlib
        for name in ["learning_signal_engine", "signal_clustering_engine", "insight_discovery_engine"]:
            try:
                mod = importlib.import_module(f"services.{name}")
                signal_pipelines_found.append(name)
            except (ImportError, Exception):
                pass
    except Exception:
        pass
    return {
        "status": "INITIALIZED",
        "score": 0,
        "signal_pipelines_found": signal_pipelines_found,
        "signal_count": 0,
        "detail": "Signal quality not calculable — no real signals to evaluate.",
        "generated_at": _utc_now(),
    }
