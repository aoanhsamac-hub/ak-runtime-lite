import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
BASELINE_REGISTRY_FILE = "DAY1_BASELINE_REGISTRY.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_registry() -> dict:
    import json
    path = REGISTRIES_DIR / BASELINE_REGISTRY_FILE
    if not path.exists():
        return {"day1_baseline_registry": {"baseline_records": [], "status": "INITIALIZED"}}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_registry(registry: dict) -> None:
    import json
    path = REGISTRIES_DIR / BASELINE_REGISTRY_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")


def _collect_forecast_count() -> int:
    try:
        from services.day1_forecast_handler import get_forecasts
        return len(get_forecasts())
    except Exception:
        return 0


def _collect_reality_count() -> int:
    try:
        from services.day1_reality_handler import get_benchmarks
        return len(get_benchmarks())
    except Exception:
        return 0


def _collect_lesson_count() -> int:
    try:
        from services.day1_lesson_handler import get_lessons
        return len(get_lessons())
    except Exception:
        return 0


def _collect_evidence_count() -> int:
    try:
        from services.day1_evidence_handler import get_evidence
        return len(get_evidence())
    except Exception:
        return 0


def _collect_system_metrics() -> dict[str, Any]:
    import psutil
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("C:\\")
        return {
            "cpu_percent": cpu,
            "ram_available_mb": round(mem.available / 1024 / 1024, 1),
            "ram_percent_used": mem.percent,
            "disk_free_gb": round(disk.free / 1024 / 1024 / 1024, 1),
            "disk_percent_used": disk.percent,
        }
    except Exception:
        return {"error": "psutil_not_available"}


def record_day1_baseline() -> dict[str, Any]:
    start_time = _utc_now()
    baseline = {
        "baseline_id": f"BL-DAY1-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "timestamp": start_time,
        "day1_start_time": start_time,
        "forecast_count": _collect_forecast_count(),
        "reality_count": _collect_reality_count(),
        "lesson_count": _collect_lesson_count(),
        "evidence_count": _collect_evidence_count(),
        "system_metrics": _collect_system_metrics(),
        "runtime_health": _get_runtime_health(),
        "handler_type": "day1_baseline",
    }
    registry = _load_registry()
    if "day1_baseline_registry" not in registry:
        registry["day1_baseline_registry"] = {}
    inner = registry["day1_baseline_registry"]
    inner.setdefault("baseline_records", []).append(baseline)
    inner["last_baseline_id"] = baseline["baseline_id"]
    inner["status"] = "ACTIVE"
    _save_registry(registry)
    return {
        "status": "OK",
        "handler": "day1_baseline",
        "baseline_id": baseline["baseline_id"],
        "timestamp": start_time,
    }


def _get_runtime_health() -> dict[str, Any]:
    try:
        from services.runtime_supervisor import RuntimeSupervisor
        sup = RuntimeSupervisor()
        report = sup.status_report()
        return {
            "running": report.get("running", False),
            "all_healthy": report.get("all_healthy", False),
            "component_count": len(report.get("components", {})),
        }
    except Exception:
        return {"error": "runtime_supervisor_not_available"}


def get_baselines() -> list[dict]:
    reg = _load_registry()
    return reg.get("day1_baseline_registry", {}).get("baseline_records", [])


def get_latest_baseline() -> dict | None:
    records = get_baselines()
    return records[-1] if records else None


__all__ = ["record_day1_baseline", "get_baselines", "get_latest_baseline"]
