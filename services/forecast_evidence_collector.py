from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
SERVICES_DIR = Path(__file__).resolve().parent.parent / "services"
FORBIDDEN_MODES = ["LIVE", "PRODUCTION", "EXECUTION", "ORDER_PLACEMENT", "STRATEGY_MODIFICATION"]


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _load_registry():
    import yaml
    path = REGISTRIES_DIR / "TRADING_EVIDENCE_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry):
    import yaml
    path = REGISTRIES_DIR / "TRADING_EVIDENCE_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_evidence_id():
    registry = _load_registry()
    inner = registry.get("trading_evidence_registry", registry)
    counter = len(inner.get("evidence_records", [])) + 1
    return f"TRADING-EVID-{counter:04d}"


def _record_evidence(evidence_type, monitor_result, detail):
    evidence_id = _generate_evidence_id()
    timestamp = _utc_now()
    registry = _load_registry()
    inner = registry.get("trading_evidence_registry", registry)
    record = {
        "evidence_id": evidence_id,
        "evidence_type": evidence_type,
        "monitor_result": monitor_result,
        "detail": detail,
        "recorded_at": timestamp,
    }
    if "evidence_records" not in inner:
        inner["evidence_records"] = []
    inner["evidence_records"].append(record)
    inner["last_evidence_id"] = evidence_id
    inner["last_updated"] = timestamp
    if inner.get("status") == "INITIALIZED":
        inner["status"] = "ACTIVE"
    registry["trading_evidence_registry"] = inner
    _save_registry(registry)
    return record


def collect_forecast_evidence():
    try:
        from services.forecast_accuracy_monitor import check
        result = check()
    except Exception:
        result = {"status": "INITIALIZED", "score": 0}
    return _record_evidence("forecast_accuracy", result, result.get("detail", ""))


def collect_signal_evidence():
    try:
        from services.signal_quality_monitor import check
        result = check()
    except Exception:
        result = {"status": "INITIALIZED", "score": 0}
    return _record_evidence("signal_quality", result, result.get("detail", ""))


def collect_zone_evidence():
    try:
        from services.zone_quality_monitor import check
        result = check()
    except Exception:
        result = {"status": "INITIALIZED", "score": 0}
    return _record_evidence("zone_quality", result, result.get("detail", ""))


def collect_trading_health_evidence():
    try:
        from services.trading_health_monitor import check
        result = check()
    except Exception:
        result = {"status": "INITIALIZED", "score": 0}
    return _record_evidence("trading_health", result, result.get("status", ""))


def collect_all():
    return {
        "forecast": collect_forecast_evidence(),
        "signal": collect_signal_evidence(),
        "zone": collect_zone_evidence(),
        "health": collect_trading_health_evidence(),
    }


def get_all_evidence():
    registry = _load_registry()
    inner = registry.get("trading_evidence_registry", registry)
    return list(inner.get("evidence_records", []))


def get_evidence_summary():
    records = get_all_evidence()
    by_type = {}
    for r in records:
        et = r.get("evidence_type", "unknown")
        by_type[et] = by_type.get(et, 0) + 1
    return {
        "total_records": len(records),
        "by_evidence_type": by_type,
        "generated_at": _utc_now(),
    }
