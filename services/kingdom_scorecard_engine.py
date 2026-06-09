"""Kingdom Scorecard Engine - Unified evaluation across all domains."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def generate_kingdom_scorecard() -> dict[str, Any]:
    """Generate unified kingdom scorecard."""
    from services.kingdom_health_aggregator import aggregate_health
    from services.capability_economy_engine import evaluate_capability_economy
    from services.audit_readiness_engine import evaluate_audit_readiness

    health = aggregate_health()
    economy = evaluate_capability_economy()
    readiness = evaluate_audit_readiness()

    return {
        "scorecard_id": f"SCORECARD-{datetime.now().strftime('%Y%m%d')}",
        "timestamp": _utc_now(),
        "kingdom_health_score": health.get("overall_score", 0),
        "kingdom_audit_score": readiness.get("overall_score", 0),
        "kingdom_capability_score": economy.get("capability_economy_level", 0) * 25,
        "kingdom_agent_score": _calculate_agent_score(),
        "domains": {
            "governance": health.get("domains", {}).get("governance_health", {}).get("score", 0),
            "treasury": health.get("domains", {}).get("treasury_health", {}).get("score", 0),
            "agents": health.get("domains", {}).get("agents_health", {}).get("score", 0),
            "capabilities": health.get("domains", {}).get("capability_health", {}).get("score", 0),
            "knowledge": health.get("domains", {}).get("knowledge_health", {}).get("score", 0),
            "evidence": readiness.get("scores", {}).get("evidence", 0),
            "audit_readiness": readiness.get("overall_score", 0),
        },
    }


def _calculate_agent_score() -> int:
    from services.agent_status_monitor import check
    status = check()
    return status.get("score", 0)


def get_scorecard_by_category(category: str) -> dict:
    scorecard = generate_kingdom_scorecard()
    if category == "health":
        return {"kingdom_health_score": scorecard["kingdom_health_score"]}
    if category == "audit":
        return {"kingdom_audit_score": scorecard["kingdom_audit_score"]}
    if category == "capability":
        return {"kingdom_capability_score": scorecard["kingdom_capability_score"]}
    if category == "agent":
        return {"kingdom_agent_score": scorecard["kingdom_agent_score"]}
    return {"error": "Unknown category", "valid": ["health", "audit", "capability", "agent"]}


__all__ = ["generate_kingdom_scorecard", "get_scorecard_by_category"]