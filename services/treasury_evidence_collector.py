from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"

EVIDENCE_TYPES = ["revenue", "expense", "reserve", "treasury"]


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _load_registry():
    import yaml
    path = REGISTRIES_DIR / "TREASURY_EVIDENCE_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry):
    import yaml
    path = REGISTRIES_DIR / "TREASURY_EVIDENCE_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_evidence_id():
    registry = _load_registry()
    inner = registry.get("treasury_evidence_registry", registry)
    counter = len(inner.get("evidence_records", [])) + 1
    return f"TREASURY-EVID-{counter:04d}"


def collect_treasury_evidence(event_type, event_data=None):
    if event_type not in EVIDENCE_TYPES:
        raise ValueError(f"Invalid event_type: {event_type}. Must be one of {EVIDENCE_TYPES}")
    evidence_id = _generate_evidence_id()
    timestamp = _utc_now()
    try:
        from services.treasury_impact_tracker import record_program_impact
        recorded = record_program_impact(
            program_id="TREASURY-EVIDENCE",
            program_name=f"Treasury {event_type}",
            treasury_contribution=0.0,
        )
        reference_id = recorded.get("impact_id", "")
    except Exception:
        reference_id = ""
    registry = _load_registry()
    inner = registry.get("treasury_evidence_registry", registry)
    record = {
        "evidence_id": evidence_id,
        "event_type": event_type,
        "event_data": event_data or {},
        "treasury_impact_id": reference_id,
        "recorded_at": timestamp,
    }
    if "evidence_records" not in inner:
        inner["evidence_records"] = []
    inner["evidence_records"].append(record)
    inner["last_evidence_id"] = evidence_id
    inner["last_updated"] = timestamp
    if inner.get("status") == "INITIALIZED":
        inner["status"] = "ACTIVE"
    registry["treasury_evidence_registry"] = inner
    _save_registry(registry)
    return record


def collect_revenue_event(revenue_data=None):
    return collect_treasury_evidence("revenue", revenue_data)


def collect_expense_event(expense_data=None):
    return collect_treasury_evidence("expense", expense_data)


def collect_reserve_event(reserve_data=None):
    return collect_treasury_evidence("reserve", reserve_data)


def collect_treasury_event(treasury_data=None):
    return collect_treasury_evidence("treasury", treasury_data)


def get_all_evidence():
    registry = _load_registry()
    inner = registry.get("treasury_evidence_registry", registry)
    return list(inner.get("evidence_records", []))


def get_evidence_summary():
    records = get_all_evidence()
    by_type = {}
    for r in records:
        et = r.get("event_type", "unknown")
        by_type[et] = by_type.get(et, 0) + 1
    return {
        "total_records": len(records),
        "by_event_type": by_type,
        "generated_at": _utc_now(),
    }
