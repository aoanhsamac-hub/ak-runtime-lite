# Kingdom Task Manager
# Manages tasks generated from directives

import json
from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"

TASK_LIFECYCLE = ["NOT_STARTED", "IN_PROGRESS", "BLOCKED", "REVIEW", "COMPLETE", "ARCHIVED"]


class TaskError(Exception):
    pass


def _load_registry():
    path = REGISTRIES_DIR / "KINGDOM_TASK_REGISTRY.yaml"
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry):
    path = REGISTRIES_DIR / "KINGDOM_TASK_REGISTRY.yaml"
    import yaml
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_task_id():
    registry = _load_registry()
    inner = registry.get("kingdom_task_registry", registry)
    tasks = inner.get("tasks", [])
    return f"TASK-{len(tasks) + 1:04d}"


def create_task(directive_id, title, owner, priority, due_date):
    """Create a task linked to a directive."""
    registry = _load_registry()
    inner = registry.get("kingdom_task_registry", registry)
    
    task_id = _generate_task_id()
    timestamp = datetime.now(timezone.utc).isoformat()
    
    task = {
        "task_id": task_id,
        "directive_id": directive_id,
        "title": title,
        "owner": owner,
        "status": "NOT_STARTED",
        "priority": priority,
        "progress": 0.0,
        "start_date": None,
        "due_date": due_date,
        "created_at": timestamp,
        "updated_at": timestamp,
        "audit_trail": [f"TASK_CREATED:{timestamp}"],
    }
    
    if "tasks" not in inner:
        inner["tasks"] = []
    inner["tasks"].append(task)
    _save_registry(registry)
    return task


def assign_task(task_id, agent):
    """Assign task to an agent."""
    registry = _load_registry()
    inner = registry.get("kingdom_task_registry", registry)
    tasks = inner.get("tasks", [])
    
    for t in tasks:
        if t["task_id"] == task_id:
            t["assigned_to"] = agent
            t["status"] = "IN_PROGRESS"
            t["start_date"] = datetime.now(timezone.utc).isoformat()
            t["updated_at"] = t["start_date"]
            t["audit_trail"].append(f"TASK_ASSIGNED:{agent}")
            _save_registry(registry)
            return t
    raise TaskError(f"Task not found: {task_id}")


def update_task(task_id, progress=None, status=None, **updates):
    """Update task progress or status."""
    registry = _load_registry()
    inner = registry.get("kingdom_task_registry", registry)
    tasks = inner.get("tasks", [])
    
    for t in tasks:
        if t["task_id"] == task_id:
            if progress is not None:
                t["progress"] = min(100.0, max(0.0, progress))
            if status:
                if status not in TASK_LIFECYCLE:
                    raise TaskError(f"Invalid status: {status}")
                t["status"] = status
            for key, value in updates.items():
                t[key] = value
            t["updated_at"] = datetime.now(timezone.utc).isoformat()
            t["audit_trail"].append(f"TASK_UPDATED:{t['status']}")
            _save_registry(registry)
            return t
    raise TaskError(f"Task not found: {task_id}")


def close_task(task_id):
    """Close task and mark complete."""
    return update_task(task_id, status="COMPLETE", progress=100.0)