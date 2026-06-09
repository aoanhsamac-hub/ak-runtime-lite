from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _load_registry():
    import yaml
    path = REGISTRIES_DIR / "CAPABILITY_USAGE_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry):
    import yaml
    path = REGISTRIES_DIR / "CAPABILITY_USAGE_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_evidence_id():
    registry = _load_registry()
    inner = registry.get("capability_usage_registry", registry)
    counter = len(inner.get("evidence_records", [])) + 1
    return f"USAGE-EVID-{counter:04d}"


def _record_to_memory(capability_name, agent_id, operation_type, outcome):
    try:
        from memory.usage_registry import CapabilityUsageRegistry
        from agents.runtime_models import CapabilityUsageRecord
        reg = CapabilityUsageRegistry()
        record = CapabilityUsageRecord(
            agent_id=agent_id,
            capability_name=capability_name,
            operation=operation_type,
            outcome=outcome,
            timestamp=_utc_now(),
        )
        result = reg.record_usage(record)
        return result.get("usage_id", "")
    except Exception:
        return ""


def collect_usage(capability_name, agent_id, operation_type, outcome):
    if not capability_name:
        raise ValueError("capability_name is required")
    if not agent_id:
        raise ValueError("agent_id is required")
    evidence_id = _generate_evidence_id()
    timestamp = _utc_now()
    usage_record_id = _record_to_memory(capability_name, agent_id, operation_type, outcome)
    registry = _load_registry()
    inner = registry.get("capability_usage_registry", registry)
    record = {
        "evidence_id": evidence_id,
        "capability_name": capability_name,
        "agent_id": agent_id,
        "operation_type": operation_type,
        "outcome": outcome,
        "usage_record_id": usage_record_id,
        "recorded_at": timestamp,
    }
    if "evidence_records" not in inner:
        inner["evidence_records"] = []
    inner["evidence_records"].append(record)
    inner["last_evidence_id"] = evidence_id
    inner["last_updated"] = timestamp
    if inner.get("status") == "INITIALIZED":
        inner["status"] = "ACTIVE"
    registry["capability_usage_registry"] = inner
    _save_registry(registry)
    return record


def get_all_evidence():
    registry = _load_registry()
    inner = registry.get("capability_usage_registry", registry)
    return list(inner.get("evidence_records", []))


def get_evidence_summary():
    records = get_all_evidence()
    return {
        "total_records": len(records),
        "unique_capabilities": len(set(r.get("capability_name", "") for r in records)),
        "unique_agents": len(set(r.get("agent_id", "") for r in records)),
        "generated_at": _utc_now(),
    }
