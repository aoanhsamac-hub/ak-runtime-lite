from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
AUDIT_DIR = Path(__file__).resolve().parent.parent / "docs" / "audit"


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _load_yaml(name):
    import yaml
    path = REGISTRIES_DIR / name
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _get_records(registry, wrapper_key):
    inner = registry.get(wrapper_key, registry) if wrapper_key else registry
    return list(inner.get("evidence_records", []))


def compile_treasury_audit():
    registry = _load_yaml("TREASURY_EVIDENCE_REGISTRY.yaml")
    records = _get_records(registry, "treasury_evidence_registry")
    by_type = {}
    for r in records:
        et = r.get("event_type", "unknown")
        by_type.setdefault(et, []).append(r["evidence_id"])
    return {
        "audit_type": "Treasury Evidence",
        "total_records": len(records),
        "by_event_type": {k: len(v) for k, v in by_type.items()},
        "evidence_ids": [r["evidence_id"] for r in records],
        "compiled_at": _utc_now(),
    }


def compile_capability_audit():
    usage = _get_records(_load_yaml("CAPABILITY_USAGE_REGISTRY.yaml"), "capability_usage_registry")
    value = _get_records(_load_yaml("CAPABILITY_VALUE_REGISTRY.yaml"), "capability_value_registry")
    roi = _get_records(_load_yaml("CAPABILITY_ROI_REGISTRY.yaml"), "capability_roi_registry")
    return {
        "audit_type": "Capability Evidence",
        "usage_records": len(usage),
        "value_records": len(value),
        "roi_records": len(roi),
        "total_evidence": len(usage) + len(value) + len(roi),
        "compiled_at": _utc_now(),
    }


def compile_program_audit():
    registry = _load_yaml("PROGRAM_EVIDENCE_REGISTRY.yaml")
    records = _get_records(registry, "program_evidence_registry")
    return {
        "audit_type": "Program Evidence",
        "total_records": len(records),
        "evidence_ids": [r["evidence_id"] for r in records],
        "compiled_at": _utc_now(),
    }


def compile_governance_audit():
    findings = []
    required_registries = [
        "CAPABILITY_USAGE_REGISTRY.yaml",
        "CAPABILITY_VALUE_REGISTRY.yaml",
        "CAPABILITY_ROI_REGISTRY.yaml",
        "TREASURY_EVIDENCE_REGISTRY.yaml",
        "TRADING_EVIDENCE_REGISTRY.yaml",
        "PROGRAM_EVIDENCE_REGISTRY.yaml",
    ]
    for name in required_registries:
        path = REGISTRIES_DIR / name
        findings.append({
            "registry": name,
            "exists": path.exists(),
            "has_records": _get_records(_load_yaml(name), None) != [],
        })
    return {
        "audit_type": "Governance Evidence",
        "registries_checked": len(required_registries),
        "all_present": all(f["exists"] for f in findings),
        "findings": findings,
        "compiled_at": _utc_now(),
    }


def compile_all():
    return {
        "treasury": compile_treasury_audit(),
        "capability": compile_capability_audit(),
        "program": compile_program_audit(),
        "governance": compile_governance_audit(),
        "compiled_at": _utc_now(),
    }
