# Kingdom Progress Tracker
# Tracks directive and task progress

from datetime import datetime, timezone
from pathlib import Path
import yaml

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def get_directive_progress(directive_id):
    """Calculate directive progress from task completion."""
    from services import kingdom_task_manager as tm
    
    task_registry = tm._load_registry()
    tasks = task_registry.get("kingdom_task_registry", {}).get("tasks", [])
    
    directive_tasks = [t for t in tasks if t.get("directive_id") == directive_id]
    
    if not directive_tasks:
        return {"progress": 0.0, "total_tasks": 0, "completed": 0}
    
    completed = sum(1 for t in directive_tasks if t.get("status") == "COMPLETE")
    avg_progress = sum(t.get("progress", 0) for t in directive_tasks) / len(directive_tasks)
    
    return {
        "progress": round(avg_progress, 2),
        "total_tasks": len(directive_tasks),
        "completed": completed,
        "status": "IN_PROGRESS" if avg_progress < 100 else "COMPLETE",
    }


def get_agent_progress(agent):
    """Get progress summary for agent."""
    from services import kingdom_task_manager as tm
    
    task_registry = tm._load_registry()
    tasks = task_registry.get("kingdom_task_registry", {}).get("tasks", [])
    
    agent_tasks = [t for t in tasks if t.get("assigned_to") == agent]
    
    return {
        "agent": agent,
        "total_tasks": len(agent_tasks),
        "in_progress": len([t for t in agent_tasks if t.get("status") == "IN_PROGRESS"]),
        "blocked": len([t for t in agent_tasks if t.get("status") == "BLOCKED"]),
        "completed": len([t for t in agent_tasks if t.get("status") == "COMPLETE"]),
    }


def get_kingdom_progress():
    """Get overall kingdom progress from all directives."""
    directive_registry = _load_directive_registry()
    directives = directive_registry.get("kingdom_directive_registry", {}).get("directives", [])
    
    total_progress = 0
    for d in directives:
        progress = get_directive_progress(d["directive_id"])
        total_progress += progress["progress"]
    
    avg = total_progress / len(directives) if directives else 0
    return {"kingdom_progress": round(avg, 2), "active_directives": len(directives)}


def _load_directive_registry():
    path = REGISTRIES_DIR / "KINGDOM_DIRECTIVE_REGISTRY.yaml"
    import yaml as y
    return y.safe_load(path.read_text(encoding="utf-8"))