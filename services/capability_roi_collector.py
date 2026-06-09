from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _load_registry():
    import yaml
    path = REGISTRIES_DIR / "CAPABILITY_ROI_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry):
    import yaml
    path = REGISTRIES_DIR / "CAPABILITY_ROI_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_evidence_id():
    registry = _load_registry()
    inner = registry.get("capability_roi_registry", registry)
    counter = len(inner.get("evidence_records", [])) + 1
    return f"ROI-EVID-{counter:04d}"


def _record_to_lancedb(capability_name, value, cost):
    try:
        from services.capability_roi_engine import record_capability_roi
        result = record_capability_roi(capability_name, value=value, cost=cost)
        return result.get("capability_name", "")
    except Exception:
        return ""


def collect_roi(capability_name, value, cost, usage_ref=None, value_ref=None):
    if not capability_name:
        raise ValueError("capability_name is required")
    if value < 0 or cost < 0:
        raise ValueError("value and cost must be non-negative")
    evidence_id = _generate_evidence_id()
    timestamp = _utc_now()
    roi = round((value / cost), 4) if cost > 0 else 0.0
    reference_id = _record_to_lancedb(capability_name, value, cost)
    registry = _load_registry()
    inner = registry.get("capability_roi_registry", registry)
    record = {
        "evidence_id": evidence_id,
        "capability_name": capability_name,
        "value": value,
        "cost": cost,
        "roi": roi,
        "usage_reference": usage_ref,
        "value_reference": value_ref,
        "roi_record_id": reference_id,
        "recorded_at": timestamp,
    }
    if "evidence_records" not in inner:
        inner["evidence_records"] = []
    inner["evidence_records"].append(record)
    inner["last_evidence_id"] = evidence_id
    inner["last_updated"] = timestamp
    if inner.get("status") == "INITIALIZED":
        inner["status"] = "ACTIVE"
    registry["capability_roi_registry"] = inner
    _save_registry(registry)
    return record


def get_all_evidence():
    registry = _load_registry()
    inner = registry.get("capability_roi_registry", registry)
    return list(inner.get("evidence_records", []))


def get_roi_summary():
    records = get_all_evidence()
    total_value = sum(r.get("value", 0) for r in records)
    total_cost = sum(r.get("cost", 0) for r in records)
    overall_roi = round((total_value / total_cost), 4) if total_cost > 0 else 0.0
    return {
        "total_records": len(records),
        "total_value": total_value,
        "total_cost": total_cost,
        "overall_roi": overall_roi,
        "unique_capabilities": len(set(r.get("capability_name", "") for r in records)),
        "generated_at": _utc_now(),
    }
