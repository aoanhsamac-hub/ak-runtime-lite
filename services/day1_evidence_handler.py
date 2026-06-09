from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
EVIDENCE_REGISTRY_FILE = "EVIDENCE_REGISTRY.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_registry() -> dict:
    import json
    path = REGISTRIES_DIR / EVIDENCE_REGISTRY_FILE
    if not path.exists():
        return {"evidence_registry": {"evidence_records": [], "last_updated": "", "status": "INITIALIZED"}}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_registry(registry: dict) -> None:
    import json
    path = REGISTRIES_DIR / EVIDENCE_REGISTRY_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")


def _generate_evidence_id() -> str:
    registry = _load_registry()
    inner = registry.get("evidence_registry", {})
    counter = len(inner.get("evidence_records", [])) + 1
    return f"EVID-{counter:04d}"


def _capture_forecast_evidence() -> dict:
    try:
        from services.day1_forecast_handler import get_forecast_summary
        return get_forecast_summary()
    except Exception:
        return {"total_forecasts": 0, "error": "forecast_handler_not_available"}


def _capture_reality_evidence() -> dict:
    try:
        from services.day1_reality_handler import get_benchmark_summary
        return get_benchmark_summary()
    except Exception:
        return {"total_benchmarks": 0, "error": "reality_handler_not_available"}


def _capture_lesson_evidence() -> dict:
    try:
        from services.day1_lesson_handler import get_lesson_summary
        return get_lesson_summary()
    except Exception:
        return {"total_lessons": 0, "error": "lesson_handler_not_available"}


def _capture_runtime_evidence() -> dict:
    try:
        from services.runtime_supervisor import RuntimeSupervisor
        sup = RuntimeSupervisor()
        return sup.status_report()
    except Exception:
        return {"error": "runtime_supervisor_not_available"}


def run_evidence_handler() -> dict[str, Any]:
    evidence_packages = {
        "forecast_evidence": _capture_forecast_evidence(),
        "reality_evidence": _capture_reality_evidence(),
        "lesson_evidence": _capture_lesson_evidence(),
        "runtime_evidence": _capture_runtime_evidence(),
    }
    registry = _load_registry()
    if "evidence_registry" not in registry:
        registry["evidence_registry"] = {}
    inner = registry["evidence_registry"]
    record = {
        "evidence_id": _generate_evidence_id(),
        "timestamp": _utc_now(),
        "evidence_packages": evidence_packages,
        "handler_type": "day1_evidence_handler",
        "append_only": True,
        "immutable": True,
    }
    inner.setdefault("evidence_records", []).append(record)
    inner["last_run"] = _utc_now()
    inner["evidence_count"] = len(inner["evidence_records"])
    inner["status"] = "ACTIVE"
    _save_registry(registry)
    return {
        "status": "OK",
        "handler": "day1_evidence_handler",
        "evidence_id": record["evidence_id"],
        "timestamp": _utc_now(),
        "total_records": len(inner["evidence_records"]),
    }


def get_evidence() -> list[dict]:
    reg = _load_registry()
    return reg.get("evidence_registry", {}).get("evidence_records", [])


def get_evidence_summary() -> dict[str, Any]:
    records = get_evidence()
    total = len(records)
    return {
        "total_evidence_records": total,
        "last_run": _load_registry().get("evidence_registry", {}).get("last_run", ""),
        "status": "APPEND_ONLY_IMMUTABLE_AUDITABLE",
    }


__all__ = ["run_evidence_handler", "get_evidence", "get_evidence_summary"]
