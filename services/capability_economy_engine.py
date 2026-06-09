"""Capability Economy Engine - Unified Level 2 evaluation for capabilities."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_yaml(name: str) -> dict:
    import yaml
    path = REGISTRIES_DIR / name
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def evaluate_capability_economy() -> dict[str, Any]:
    """Evaluate capability economy at Level 2 (usage-based)."""
    usage = _get_records("CAPABILITY_USAGE_REGISTRY.yaml", "capability_usage_registry")
    value = _get_records("CAPABILITY_VALUE_REGISTRY.yaml", "capability_value_registry")
    roi = _get_records("CAPABILITY_ROI_REGISTRY.yaml", "capability_roi_registry")

    total_usage = sum(r.get("usage_count", 0) for r in usage)
    total_value = sum(r.get("total_value", 0) for r in value)
    total_roi = len([r for r in roi if r.get("roi", 0) > 0])

    capabilities = set()
    for r in usage + value + roi:
        if r.get("capability_name"):
            capabilities.add(r.get("capability_name"))

    economy = {
        "evaluation_id": f"ECONOMY-EVAL-{datetime.now().strftime('%Y%m%d')}",
        "timestamp": _utc_now(),
        "total_capabilities": len(capabilities),
        "total_usage_events": total_usage,
        "total_value": total_value,
        "capabilities_with_roi": total_roi,
        "capability_economy_level": _calculate_level(total_usage, total_value, total_roi),
        "adoption_count": len(usage),
        "value_count": len(value),
        "roi_count": len(roi),
    }

    return economy


def _get_records(registry_name: str, wrapper_key: str) -> list:
    reg = _load_yaml(registry_name)
    return list(reg.get(wrapper_key, {}).get("records", []))


def _calculate_level(usage: int, value: float, roi: int) -> int:
    """Calculate capability economy level (1-4)."""
    if usage == 0:
        return 1
    if value == 0:
        return 2
    if roi == 0:
        return 3
    return 4


def get_capability_metrics(capability_name: str) -> dict[str, Any]:
    """Get unified metrics for a single capability."""
    usage = _find_record("CAPABILITY_USAGE_REGISTRY.yaml", "capability_usage_registry", "capability_name", capability_name)
    value = _find_record("CAPABILITY_VALUE_REGISTRY.yaml", "capability_value_registry", "capability_name", capability_name)
    roi = _find_record("CAPABILITY_ROI_REGISTRY.yaml", "capability_roi_registry", "capability_name", capability_name)

    return {
        "capability_name": capability_name,
        "usage": usage or {},
        "value": value or {},
        "roi": roi or {},
        "timestamp": _utc_now(),
    }


def _find_record(registry_name: str, wrapper_key: str, field: str, value: str) -> dict | None:
    reg = _load_yaml(registry_name)
    records = reg.get(wrapper_key, {}).get("records", [])
    for r in records:
        if r.get(field) == value:
            return r
    return None


def get_domain_economy(domain: str) -> dict[str, Any]:
    """Get economy metrics for a capability domain."""
    all_metrics = evaluate_capability_economy()
    return {
        "domain": domain,
        "total_capabilities": 0,
        "total_value": 0.0,
        "total_roi": 0.0,
        "timestamp": _utc_now(),
    }


__all__ = ["evaluate_capability_economy", "get_capability_metrics", "get_domain_economy"]