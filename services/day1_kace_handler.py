from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
KACE_REGISTRY_FILE = "KINGDOM_SCORECARD.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_registry() -> dict:
    import json
    path = REGISTRIES_DIR / KACE_REGISTRY_FILE
    if not path.exists():
        return {"kingdom_scorecard_registry": {"scorecard_records": [], "last_updated": "", "status": "INITIALIZED"}}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_registry(registry: dict) -> None:
    import json
    path = REGISTRIES_DIR / KACE_REGISTRY_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")


def _generate_scorecard_id() -> str:
    registry = _load_registry()
    inner = registry.get("kingdom_scorecard_registry", {})
    counter = len(inner.get("scorecard_records", [])) + 1
    return f"KACE-{datetime.now().strftime('%Y%m%d')}-{counter:04d}"


def _aggregate_forecast_data() -> dict[str, Any]:
    try:
        from services.day1_forecast_handler import get_forecast_summary
        return get_forecast_summary()
    except Exception:
        return {"total_forecasts": 0}


def _aggregate_reality_data() -> dict[str, Any]:
    try:
        from services.day1_reality_handler import get_benchmark_summary
        return get_benchmark_summary()
    except Exception:
        return {"total_benchmarks": 0}


def _aggregate_lesson_data() -> dict[str, Any]:
    try:
        from services.day1_lesson_handler import get_lesson_summary
        return get_lesson_summary()
    except Exception:
        return {"total_lessons": 0}


def _aggregate_evidence_data() -> dict[str, Any]:
    try:
        from services.day1_evidence_handler import get_evidence_summary
        return get_evidence_summary()
    except Exception:
        return {"total_evidence_records": 0}


def _aggregate_runtime_health() -> dict[str, Any]:
    try:
        from services.runtime_supervisor import RuntimeSupervisor
        sup = RuntimeSupervisor()
        report = sup.status_report()
        return {
            "all_healthy": report.get("all_healthy", False),
            "component_count": len(report.get("components", {})),
            "restart_count": report.get("restart_count", 0),
        }
    except Exception:
        return {"all_healthy": False, "error": "runtime_supervisor_not_available"}


def run_kace_handler() -> dict[str, Any]:
    forecast_data = _aggregate_forecast_data()
    reality_data = _aggregate_reality_data()
    lesson_data = _aggregate_lesson_data()
    evidence_data = _aggregate_evidence_data()
    runtime_health = _aggregate_runtime_health()
    scorecard = {
        "scorecard_id": _generate_scorecard_id(),
        "timestamp": _utc_now(),
        "forecast_count": forecast_data.get("total_forecasts", 0),
        "reality_count": reality_data.get("total_benchmarks", 0),
        "lesson_count": lesson_data.get("total_lessons", 0),
        "evidence_count": evidence_data.get("total_evidence_records", 0),
        "runtime_healthy": runtime_health.get("all_healthy", False),
        "runtime_component_count": runtime_health.get("component_count", 0),
        "runtime_restart_count": runtime_health.get("restart_count", 0),
        "handler_type": "day1_kace_handler",
    }
    registry = _load_registry()
    if "kingdom_scorecard_registry" not in registry:
        registry["kingdom_scorecard_registry"] = {}
    inner = registry["kingdom_scorecard_registry"]
    inner.setdefault("scorecard_records", []).append(scorecard)
    inner["last_run"] = _utc_now()
    inner["scorecard_count"] = len(inner["scorecard_records"])
    inner["status"] = "ACTIVE"
    _save_registry(registry)
    return {
        "status": "OK",
        "handler": "day1_kace_handler",
        "scorecard_id": scorecard["scorecard_id"],
        "timestamp": _utc_now(),
    }


def get_scorecards() -> list[dict]:
    reg = _load_registry()
    return reg.get("kingdom_scorecard_registry", {}).get("scorecard_records", [])


def get_latest_scorecard() -> dict | None:
    records = get_scorecards()
    return records[-1] if records else None


__all__ = ["run_kace_handler", "get_scorecards", "get_latest_scorecard"]
