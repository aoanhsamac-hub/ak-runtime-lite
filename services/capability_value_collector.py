from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _load_registry():
    import yaml
    path = REGISTRIES_DIR / "CAPABILITY_VALUE_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry):
    import yaml
    path = REGISTRIES_DIR / "CAPABILITY_VALUE_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_evidence_id():
    registry = _load_registry()
    inner = registry.get("capability_value_registry", registry)
    counter = len(inner.get("evidence_records", [])) + 1
    return f"VALUE-EVID-{counter:04d}"


def collect_value(capability_name, measurable_outcome, supporting_evidence=None):
    if not capability_name:
        raise ValueError("capability_name is required")
    if not measurable_outcome:
        raise ValueError("measurable_outcome is required")
    evidence_id = _generate_evidence_id()
    timestamp = _utc_now()
    try:
        from services.capability_value_engine import assess_capability_value
        value_result = assess_capability_value(capability_name)
    except Exception:
        value_result = {}
    registry = _load_registry()
    inner = registry.get("capability_value_registry", registry)
    record = {
        "evidence_id": evidence_id,
        "capability_name": capability_name,
        "value_created": value_result.get("total_value", 0),
        "measurable_outcome": measurable_outcome,
        "supporting_evidence": supporting_evidence or [],
        "value_assessment": value_result,
        "recorded_at": timestamp,
    }
    if "evidence_records" not in inner:
        inner["evidence_records"] = []
    inner["evidence_records"].append(record)
    inner["last_evidence_id"] = evidence_id
    inner["last_updated"] = timestamp
    if inner.get("status") == "INITIALIZED":
        inner["status"] = "ACTIVE"
    registry["capability_value_registry"] = inner
    _save_registry(registry)
    return record


def get_all_evidence():
    registry = _load_registry()
    inner = registry.get("capability_value_registry", registry)
    return list(inner.get("evidence_records", []))


def get_value_summary():
    records = get_all_evidence()
    total_value = sum(r.get("value_created", 0) for r in records)
    return {
        "total_records": len(records),
        "total_value_created": total_value,
        "unique_capabilities": len(set(r.get("capability_name", "") for r in records)),
        "generated_at": _utc_now(),
    }
