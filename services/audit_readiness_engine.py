"""Audit Readiness Engine - Evaluate kingdom audit readiness."""

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


def evaluate_audit_readiness() -> dict[str, Any]:
    """Calculate audit readiness scores across all domains."""
    scores = {
        "governance": _check_governance(),
        "treasury": _check_treasury(),
        "operations": _check_operations(),
        "evidence": _check_evidence(),
        "capabilities": _check_capabilities(),
        "agents": _check_agents(),
        "knowledge": _check_knowledge(),
        "security": _check_security(),
    }

    overall = int(sum(scores.values()) / len(scores))

    readiness = {
        "readiness_id": f"READINESS-{datetime.now().strftime('%Y%m%d')}",
        "timestamp": _utc_now(),
        "scores": scores,
        "overall_score": overall,
    }

    reg = _load_yaml("KINGDOM_AUDIT_READINESS_REGISTRY.yaml")
    inner = reg.get("kingdom_audit_readiness_registry", {})
    inner["readiness_scores"] = scores
    inner["overall_score"] = overall
    inner["last_updated"] = _utc_now()
    reg["kingdom_audit_readiness_registry"] = inner
    _save_yaml("KINGDOM_AUDIT_READINESS_REGISTRY.yaml", reg)

    return readiness


def _check_governance() -> int:
    reg = _load_yaml("KINGDOM_GOAL_REGISTRY.yaml")
    goals = reg.get("kingdom_goal_registry", {}).get("goals", [])
    return min(100, len(goals) * 20)


def _check_treasury() -> int:
    reg = _load_yaml("TREASURY_ACCOUNT_REGISTRY.yaml")
    accounts = reg.get("treasury_accounts", [])
    return min(100, len(accounts) * 20)


def _check_operations() -> int:
    reg = _load_yaml("KINGDOM_STATUS_REGISTRY.yaml")
    status = reg.get("kingdom_status_registry", {}).get("status", "INITIALIZED")
    return 100 if status != "INITIALIZED" else 50


def _check_evidence() -> int:
    from services.audit_evidence_engine import consolidate_all_evidence
    consolidated = consolidate_all_evidence()
    total = consolidated.get("total_evidence", 0)
    return min(100, total // 10)


def _check_capabilities() -> int:
    reg = _load_yaml("CAPABILITY_USAGE_REGISTRY.yaml")
    records = reg.get("capability_usage_registry", {}).get("records", [])
    return min(100, len(records) * 25)


def _check_agents() -> int:
    from services.agent_status_monitor import check
    status = check()
    return status.get("score", 0)


def _check_knowledge() -> int:
    reg = _load_yaml("PROGRAM_EVIDENCE_REGISTRY.yaml")
    records = reg.get("program_evidence_registry", {}).get("evidence_records", [])
    knowledge = [r for r in records if "knowledge" in str(r).lower()]
    return min(100, len(knowledge) * 20)


def _check_security() -> int:
    reg = _load_yaml("TRADING_EVIDENCE_REGISTRY.yaml")
    records = reg.get("trading_evidence_registry", {}).get("evidence_records", [])
    security = [r for r in records if "security" in r.get("evidence_type", "")]
    return min(100, len(security) * 50)


__all__ = ["evaluate_audit_readiness"]