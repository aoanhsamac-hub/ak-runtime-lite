"""Agent Performance Engine - Evaluate agent performance metrics."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_registry() -> dict:
    import yaml
    path = REGISTRIES_DIR / "KINGDOM_AGENT_PERFORMANCE_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry: dict) -> None:
    import yaml
    path = REGISTRIES_DIR / "KINGDOM_AGENT_PERFORMANCE_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_perf_id(agent_name: str) -> str:
    return f"PERF-{agent_name}-{datetime.now().strftime('%Y%m%d')}"


def evaluate_agent_performance(agent_name: str) -> dict[str, Any]:
    """Calculate agent performance score from available metrics."""
    from services.agent_status_monitor import check as agent_check

    status = agent_check()
    agent_data = next((a for a in status.get("agents", []) if a.get("name") == agent_name), {})

    capability_count = _count_agent_capabilities(agent_name)
    task_count = _count_agent_tasks(agent_name)
    knowledge_contrib = _count_knowledge_contributions(agent_name)
    evidence_count = _count_evidence_contributions(agent_name)

    perf = {
        "performance_id": _generate_perf_id(agent_name),
        "agent_name": agent_name,
        "timestamp": _utc_now(),
        "is_operational": agent_data.get("agent_exists", False),
        "capability_growth": capability_count,
        "task_completion": task_count,
        "knowledge_contribution": knowledge_contrib,
        "evidence_contribution": evidence_count,
        "compliance_score": 100,
        "operational_output": task_count + knowledge_contrib + evidence_count,
        "learning_output": knowledge_contrib,
    }

    registry = _load_registry()
    inner = registry.get("kingdom_agent_performance_registry", {})
    inner.setdefault("performance_records", []).append(perf)
    inner["last_updated"] = _utc_now()
    registry["kingdom_agent_performance_registry"] = inner
    _save_registry(registry)

    return perf


def _count_agent_capabilities(agent_name: str) -> int:
    try:
        from memory.skill_registry import SkillRegistry
        from memory.lancedb_adapter import LanceDBAdapter
        adapter = LanceDBAdapter(":memory:")
        reg = SkillRegistry(adapter, None)
        return len([s for s in reg.list_records() if agent_name in s.owner_agent])
    except Exception:
        return 0


def _count_agent_tasks(agent_name: str) -> int:
    try:
        from services.kingdom_task_manager import KINGDOM_TASKS
        return len([t for t in KINGDOM_TASKS.list_all() if t.get("assigned_agent") == agent_name])
    except Exception:
        return 0


def _count_knowledge_contributions(agent_name: str) -> int:
    try:
        from services.forecast_evidence_collector import get_all_evidence
        return len([e for e in get_all_evidence() if e.get("source_agent") == agent_name])
    except Exception:
        return 0


def _count_evidence_contributions(agent_name: str) -> int:
    try:
        from services.program_evidence_collector import PROGRAM_EVIDENCE
        return len([e for e in PROGRAM_EVIDENCE.list_all() if e.get("source_agent") == agent_name])
    except Exception:
        return 0


def get_agent_performance(agent_name: str) -> dict | None:
    for record in _load_registry().get("kingdom_agent_performance_registry", {}).get("performance_records", []):
        if record.get("agent_name") == agent_name:
            return record
    return None


def get_all_performance() -> list[dict]:
    return _load_registry().get("kingdom_agent_performance_registry", {}).get("performance_records", [])


__all__ = ["evaluate_agent_performance", "get_agent_performance", "get_all_performance"]