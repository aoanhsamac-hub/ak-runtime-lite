from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
SUMMARY_REGISTRY_FILE = "DAILY_EVIDENCE_SUMMARY_REGISTRY.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_registry() -> dict:
    import json
    path = REGISTRIES_DIR / SUMMARY_REGISTRY_FILE
    if not path.exists():
        return {"daily_evidence_summary_registry": {"summary_records": [], "status": "INITIALIZED"}}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_registry(registry: dict) -> None:
    import json
    path = REGISTRIES_DIR / SUMMARY_REGISTRY_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")


def _generate_summary_id() -> str:
    return f"DSUM-{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M')}"


def _collect_forecast_summary() -> dict[str, Any]:
    try:
        from services.day1_forecast_handler import get_forecast_summary
        return get_forecast_summary()
    except Exception as e:
        return {"error": str(e), "total_forecasts": 0}


def _collect_lesson_summary() -> dict[str, Any]:
    try:
        from services.day1_lesson_handler import get_lesson_summary
        return get_lesson_summary()
    except Exception as e:
        return {"error": str(e), "total_lessons": 0}


def _collect_knowledge_summary() -> dict[str, Any]:
    try:
        from services.day1_kace_handler import get_latest_scorecard
        scorecard = get_latest_scorecard()
        if scorecard:
            return {
                "forecast_count": scorecard.get("forecast_count", 0),
                "reality_count": scorecard.get("reality_count", 0),
                "lesson_count": scorecard.get("lesson_count", 0),
                "evidence_count": scorecard.get("evidence_count", 0),
                "runtime_healthy": scorecard.get("runtime_healthy", False),
            }
        return {"error": "no_scorecard_available"}
    except Exception as e:
        return {"error": str(e)}


def _collect_runtime_summary() -> dict[str, Any]:
    try:
        from services.runtime_supervisor import RuntimeSupervisor
        sup = RuntimeSupervisor()
        report = sup.status_report()
        return {
            "running": report.get("running", False),
            "all_healthy": report.get("all_healthy", False),
            "component_count": len(report.get("components", {})),
            "restart_count": report.get("restart_count", 0),
        }
    except Exception as e:
        return {"error": str(e)}


def _collect_audit_summary() -> dict[str, Any]:
    try:
        from services.day1_evidence_handler import get_evidence_summary
        return get_evidence_summary()
    except Exception as e:
        return {"error": str(e), "total_evidence_records": 0}


def run_daily_evidence_summary() -> dict[str, Any]:
    summary = {
        "summary_id": _generate_summary_id(),
        "timestamp": _utc_now(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "forecast_summary": _collect_forecast_summary(),
        "lesson_summary": _collect_lesson_summary(),
        "knowledge_summary": _collect_knowledge_summary(),
        "runtime_summary": _collect_runtime_summary(),
        "audit_summary": _collect_audit_summary(),
        "handler_type": "day1_evidence_summary",
    }
    registry = _load_registry()
    if "daily_evidence_summary_registry" not in registry:
        registry["daily_evidence_summary_registry"] = {}
    inner = registry["daily_evidence_summary_registry"]
    inner.setdefault("summary_records", []).append(summary)
    inner["last_run"] = _utc_now()
    inner["summary_count"] = len(inner["summary_records"])
    inner["status"] = "ACTIVE"
    _save_registry(registry)
    return {
        "status": "OK",
        "handler": "day1_evidence_summary",
        "summary_id": summary["summary_id"],
        "timestamp": _utc_now(),
    }


def get_summaries() -> list[dict]:
    reg = _load_registry()
    return reg.get("daily_evidence_summary_registry", {}).get("summary_records", [])


def get_latest_summary() -> dict | None:
    records = get_summaries()
    return records[-1] if records else None


__all__ = ["run_daily_evidence_summary", "get_summaries", "get_latest_summary"]
