"""Audit Evidence Engine - Consolidate evidence from all kingdom domains."""

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


def _save_yaml(name: str, registry: dict) -> None:
    import yaml
    path = REGISTRIES_DIR / name
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def consolidate_all_evidence() -> dict[str, Any]:
    """Consolidate evidence from all kingdom domains."""
    evidence_sources = {
        "reh_evidence": _count_evidence("KINGDOM_REPORT_REGISTRY.yaml", "kingdom_report_registry", "evidence_records"),
        "treasury_evidence": _count_evidence("TREASURY_EVIDENCE_REGISTRY.yaml", "treasury_evidence_registry", "evidence_records"),
        "trading_evidence": _count_evidence("TRADING_EVIDENCE_REGISTRY.yaml", "trading_evidence_registry", "evidence_records"),
        "capability_evidence": _count_evidence("CAPABILITY_USAGE_REGISTRY.yaml", "capability_usage_registry", "records"),
        "agent_evidence": _count_evidence("PROGRAM_EVIDENCE_REGISTRY.yaml", "program_evidence_registry", "evidence_records"),
        "planning_evidence": _count_evidence("PROGRAM_EVIDENCE_REGISTRY.yaml", "program_evidence_registry", "evidence_records"),
        "situation_room_evidence": _count_evidence("KINGDOM_HEALTH_REGISTRY.yaml", "kingdom_health_registry", "health_checks"),
    }

    total = sum(evidence_sources.values())

    return {
        "consolidation_id": f"EVID-CONSOL-{datetime.now().strftime('%Y%m%d%H%M')}",
        "timestamp": _utc_now(),
        "evidence_sources": evidence_sources,
        "total_evidence": total,
        "consolidated_at": _utc_now(),
    }


def _count_evidence(registry_name: str, wrapper_key: str, record_key: str) -> int:
    reg = _load_yaml(registry_name)
    inner = reg.get(wrapper_key, reg) if wrapper_key else reg
    return len(inner.get(record_key, []))


def update_audit_index() -> dict:
    """Update the audit evidence index."""
    consolidated = consolidate_all_evidence()

    reg = _load_yaml("KINGDOM_AUDIT_EVIDENCE_INDEX.yaml")
    inner = reg.get("kingdom_audit_evidence_index", {})

    inner["evidence_sources"] = consolidated["evidence_sources"]
    inner["last_updated"] = _utc_now()
    reg["kingdom_audit_evidence_index"] = inner
    _save_yaml("KINGDOM_AUDIT_EVIDENCE_INDEX.yaml", reg)

    return consolidated


__all__ = ["consolidate_all_evidence", "update_audit_index"]