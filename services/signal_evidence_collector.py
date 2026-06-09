from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
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


def collect_signal_evidence():
    evidence_id = _generate_evidence_id()
    timestamp = _utc_now()
    try:
        from services.signal_quality_monitor import check
        result = check()
    except Exception:
        result = {"status": "INITIALIZED", "score": 0, "signal_pipelines_found": [], "signal_count": 0}
    registry = _load_registry()
    inner = registry.get("trading_evidence_registry", registry)
    record = {
        "evidence_id": evidence_id,
        "evidence_type": "signal_quality",
        "signal_pipelines_found": result.get("signal_pipelines_found", []),
        "signal_count": result.get("signal_count", 0),
        "monitor_status": result.get("status", "INITIALIZED"),
        "detail": result.get("detail", ""),
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


def get_all_evidence():
    registry = _load_registry()
    inner = registry.get("trading_evidence_registry", registry)
    return list(inner.get("evidence_records", []))
