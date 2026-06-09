# Kingdom Escalation Manager
# Manages directive/task escalations

from datetime import datetime, timezone
from pathlib import Path
import yaml

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


class EscalationError(Exception):
    pass


def check_escalation(task_id):
    """Check if task requires escalation."""
    from services import kingdom_task_manager as tm
    
    task_registry = tm._load_registry()
    tasks = task_registry.get("kingdom_task_registry", {}).get("tasks", [])
    task = next((t for t in tasks if t["task_id"] == task_id), None)
    
    if not task:
        raise EscalationError(f"Task not found: {task_id}")
    
    # Check missed deadline
    if task.get("due_date") and task["status"] != "COMPLETE":
        due = datetime.fromisoformat(task["due_date"].replace("Z", "+00:00"))
        if datetime.now(timezone.utc) > due:
            return {"escalate": True, "reason": "missed_deadline", "task": task}
    
    # Check blocked status
    if task.get("status") == "BLOCKED":
        return {"escalate": True, "reason": "blocked_state", "task": task}
    
    return {"escalate": False}


def create_escalation(task_id, reason, level=1):
    """Create escalation entry."""
    registry = _load_escalation_registry()
    inner = registry.get("kingdom_escalation_registry", registry)
    
    escalation = {
        "escalation_id": f"ESC-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "task_id": task_id,
        "reason": reason,
        "level": level,
        "status": "TRIGGERED",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "audit_trail": [f"ESCALATION_CREATED:{reason}"],
    }
    
    if "escalations" not in inner:
        inner["escalations"] = []
    inner["escalations"].append(escalation)
    _save_escalation_registry(registry)
    
    return escalation


def resolve_escalation(escalation_id, resolution):
    """Resolve escalation."""
    registry = _load_escalation_registry()
    inner = registry.get("kingdom_escalation_registry", registry)
    
    for e in inner.get("escalations", []):
        if e["escalation_id"] == escalation_id:
            e["status"] = "RESOLVED"
            e["resolution"] = resolution
            e["resolved_at"] = datetime.now(timezone.utc).isoformat()
            e["audit_trail"].append(f"ESCALATION_RESOLVED:{resolution}")
            break
    
    _save_escalation_registry(registry)
    return {"resolved": True, "escalation_id": escalation_id}


def _load_escalation_registry():
    path = REGISTRIES_DIR / "KINGDOM_ESCALATION_REGISTRY.yaml"
    import yaml as y
    return y.safe_load(path.read_text(encoding="utf-8"))


def _save_escalation_registry(registry):
    path = REGISTRIES_DIR / "KINGDOM_ESCALATION_REGISTRY.yaml"
    import yaml as y
    path.write_text(y.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")