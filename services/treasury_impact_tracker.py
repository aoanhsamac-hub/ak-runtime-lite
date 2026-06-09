from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


class TreasuryImpactError(Exception):
    pass


def _load_registry():
    import yaml
    path = REGISTRIES_DIR / "TREASURY_IMPACT_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry):
    import yaml
    path = REGISTRIES_DIR / "TREASURY_IMPACT_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _generate_impact_id(prefix):
    registry = _load_registry()
    inner = registry.get("treasury_impact_registry", registry)
    counter = len(inner.get("program_impacts", [])) + len(inner.get("capability_impacts", [])) + 1
    return f"{prefix}-{counter:04d}"


def record_program_impact(program_id, program_name, treasury_contribution=0.0,
                          value_generated=0.0, cost_incurred=0.0):
    registry = _load_registry()
    inner = registry.get("treasury_impact_registry", registry)
    impact_id = _generate_impact_id("PI")
    timestamp = _utc_now()
    net_impact = round(value_generated - cost_incurred, 2)
    record = {
        "impact_id": impact_id,
        "program_id": program_id,
        "program_name": program_name,
        "treasury_contribution": treasury_contribution,
        "value_generated": value_generated,
        "cost_incurred": cost_incurred,
        "net_impact": net_impact,
        "recorded_at": timestamp,
    }
    if "program_impacts" not in inner:
        inner["program_impacts"] = []
    inner["program_impacts"].append(record)
    inner["last_impact_id"] = impact_id
    inner["last_updated"] = timestamp
    registry["treasury_impact_registry"] = inner
    _save_registry(registry)
    return record


def record_capability_impact(capability_name, treasury_contribution=0.0,
                             efficiency_gain=0.0, risk_reduction=0.0):
    registry = _load_registry()
    inner = registry.get("treasury_impact_registry", registry)
    impact_id = _generate_impact_id("CI")
    timestamp = _utc_now()
    record = {
        "impact_id": impact_id,
        "capability_name": capability_name,
        "treasury_contribution": treasury_contribution,
        "efficiency_gain": efficiency_gain,
        "risk_reduction": risk_reduction,
        "recorded_at": timestamp,
    }
    if "capability_impacts" not in inner:
        inner["capability_impacts"] = []
    inner["capability_impacts"].append(record)
    inner["last_impact_id"] = impact_id
    inner["last_updated"] = timestamp
    registry["treasury_impact_registry"] = inner
    _save_registry(registry)
    return record


def get_treasury_contribution_summary():
    registry = _load_registry()
    inner = registry.get("treasury_impact_registry", registry)
    program_impacts = inner.get("program_impacts", [])
    capability_impacts = inner.get("capability_impacts", [])
    total_treasury_contribution = sum(
        p.get("treasury_contribution", 0) for p in program_impacts
    ) + sum(
        c.get("treasury_contribution", 0) for c in capability_impacts
    )
    total_value = sum(p.get("value_generated", 0) for p in program_impacts)
    total_cost = sum(p.get("cost_incurred", 0) for p in program_impacts)
    return {
        "program_impact_count": len(program_impacts),
        "capability_impact_count": len(capability_impacts),
        "total_treasury_contribution": total_treasury_contribution,
        "total_value_generated": total_value,
        "total_cost_incurred": total_cost,
        "net_treasury_impact": round(total_value - total_cost, 2),
        "generated_at": _utc_now(),
    }
