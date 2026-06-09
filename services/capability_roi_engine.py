from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
MAX_CE_LEVEL = 4
CAP_VIOLATION = "PSOP-03 CAP: Capability Economy capped at Level 4."


class CapabilityROIError(Exception):
    pass


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _get_capability_roi_registry():
    try:
        from memory.capability_roi_registry import CapabilityROIRegistry
        from memory.kingdom_memory_platform import KingdomMemoryPlatform
        mp = KingdomMemoryPlatform()
        return CapabilityROIRegistry(mp)
    except Exception:
        return None


def record_capability_roi(capability_name, value=0.0, cost=0.0, evolution_cost=0.0,
                          evolution_value=0.0, evolution_cycle=0):
    registry = _get_capability_roi_registry()
    if registry:
        return registry.record_roi(
            capability_name=capability_name,
            value=value,
            cost=cost,
            evolution_cost=evolution_cost,
            evolution_value=evolution_value,
            evolution_cycle=evolution_cycle,
        )
    timestamp = _utc_now()
    roi = round((value / cost), 4) if cost > 0 else 0.0
    return {
        "capability_name": capability_name,
        "total_value": value,
        "total_cost": cost,
        "roi": roi,
        "usage_count": 0,
        "evolution_cost": evolution_cost,
        "evolution_value": evolution_value,
        "evolution_cycle": evolution_cycle,
        "evolution_roi": round((evolution_value / evolution_cost), 4) if evolution_cost > 0 else 0.0,
        "cap_level": min(3 if roi > 0 else 0, MAX_CE_LEVEL),
        "created_at": timestamp,
    }


def get_capability_roi(capability_name=None):
    registry = _get_capability_roi_registry()
    if registry:
        return registry.get_roi(capability_name)
    return []


def calculate_program_roi(program_id, capability_names):
    if not capability_names:
        return {"program_id": program_id, "total_value": 0, "total_cost": 0, "program_roi": 0.0}
    results = [record_capability_roi(name) for name in capability_names]
    total_value = sum(r.get("total_value", 0) for r in results)
    total_cost = sum(r.get("total_cost", 0) for r in results)
    program_roi = round((total_value / total_cost), 4) if total_cost > 0 else 0.0
    return {
        "program_id": program_id,
        "total_value": total_value,
        "total_cost": total_cost,
        "program_roi": program_roi,
        "capability_count": len(capability_names),
        "generated_at": _utc_now(),
    }


def get_domain_roi_summary():
    roi_records = get_capability_roi()
    if not roi_records:
        return {"domains": {}, "total_value": 0, "total_cost": 0, "roi": 0.0}
    total_value = sum(r.get("total_value", 0) for r in roi_records)
    total_cost = sum(r.get("total_cost", 0) for r in roi_records)
    overall_roi = round((total_value / total_cost), 4) if total_cost > 0 else 0.0
    return {
        "total_value": total_value,
        "total_cost": total_cost,
        "roi": overall_roi,
        "record_count": len(roi_records),
        "generated_at": _utc_now(),
    }


def get_capability_economy_level():
    roi_records = get_capability_roi()
    if not roi_records:
        return 0
    has_usage = any(r.get("usage_count", 0) > 0 for r in roi_records)
    if not has_usage:
        return 1
    has_value = any(r.get("total_value", 0) > 0 for r in roi_records)
    if not has_value:
        return 2
    has_roi = any(r.get("roi", 0) > 0 for r in roi_records)
    if not has_roi:
        return 3
    return min(4, MAX_CE_LEVEL)
