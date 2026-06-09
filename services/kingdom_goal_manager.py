import json
from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
GOAL_LIFECYCLE = ["PROPOSED", "APPROVED", "ACTIVE", "COMPLETED", "ARCHIVED"]


class GoalError(Exception):
    pass


def _load_registry():
    path = REGISTRIES_DIR / "KINGDOM_GOAL_REGISTRY.yaml"
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry):
    path = REGISTRIES_DIR / "KINGDOM_GOAL_REGISTRY.yaml"
    import yaml
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_goal_id():
    registry = _load_registry()
    inner = registry.get("kingdom_goal_registry", registry)
    goals = inner.get("goals", [])
    return f"GOAL-{len(goals) + 1:04d}"


def create_goal(name, description, vision_link, parent_goal_id=None):
    registry = _load_registry()
    inner = registry.get("kingdom_goal_registry", registry)
    goal_id = _generate_goal_id()
    timestamp = datetime.now(timezone.utc).isoformat()
    goal = {
        "goal_id": goal_id,
        "name": name,
        "description": description,
        "vision_link": vision_link,
        "parent_goal_id": parent_goal_id,
        "status": "PROPOSED",
        "created_at": timestamp,
        "updated_at": timestamp,
        "progress": 0.0,
        "completion_criteria": [],
        "linked_programs": [],
    }
    if "goals" not in inner:
        inner["goals"] = []
    inner["goals"].append(goal)
    inner["last_goal_id"] = goal_id
    inner["last_updated"] = timestamp
    if "status" in inner and inner["status"] == "INITIALIZED":
        inner["status"] = "ACTIVE"
    registry["kingdom_goal_registry"] = inner
    _save_registry(registry)
    return goal


def get_goal(goal_id):
    registry = _load_registry()
    inner = registry.get("kingdom_goal_registry", registry)
    for g in inner.get("goals", []):
        if g["goal_id"] == goal_id:
            return g
    return None


def list_goals(status=None):
    registry = _load_registry()
    inner = registry.get("kingdom_goal_registry", registry)
    goals = inner.get("goals", [])
    if status:
        return [g for g in goals if g["status"] == status]
    return list(goals)


def transition_goal(goal_id, new_status):
    if new_status not in GOAL_LIFECYCLE:
        raise GoalError(f"Invalid goal status: {new_status}")
    registry = _load_registry()
    inner = registry.get("kingdom_goal_registry", registry)
    for g in inner.get("goals", []):
        if g["goal_id"] == goal_id:
            current_idx = GOAL_LIFECYCLE.index(g["status"])
            new_idx = GOAL_LIFECYCLE.index(new_status)
            if new_idx < current_idx:
                raise GoalError(f"Cannot transition {g['status']} backwards to {new_status}")
            g["status"] = new_status
            g["updated_at"] = datetime.now(timezone.utc).isoformat()
            inner["last_updated"] = g["updated_at"]
            registry["kingdom_goal_registry"] = inner
            _save_registry(registry)
            return g
    raise GoalError(f"Goal not found: {goal_id}")


def update_progress(goal_id, progress, completion_criteria=None):
    if not (0.0 <= progress <= 100.0):
        raise GoalError("Progress must be between 0 and 100")
    registry = _load_registry()
    inner = registry.get("kingdom_goal_registry", registry)
    for g in inner.get("goals", []):
        if g["goal_id"] == goal_id:
            g["progress"] = progress
            if completion_criteria is not None:
                g["completion_criteria"] = completion_criteria
            g["updated_at"] = datetime.now(timezone.utc).isoformat()
            inner["last_updated"] = g["updated_at"]
            registry["kingdom_goal_registry"] = inner
            _save_registry(registry)
            return g
    raise GoalError(f"Goal not found: {goal_id}")


def link_program(goal_id, program_id):
    registry = _load_registry()
    inner = registry.get("kingdom_goal_registry", registry)
    for g in inner.get("goals", []):
        if g["goal_id"] == goal_id:
            if "linked_programs" not in g:
                g["linked_programs"] = []
            if program_id not in g["linked_programs"]:
                g["linked_programs"].append(program_id)
            g["updated_at"] = datetime.now(timezone.utc).isoformat()
            inner["last_updated"] = g["updated_at"]
            registry["kingdom_goal_registry"] = inner
            _save_registry(registry)
            return g
    raise GoalError(f"Goal not found: {goal_id}")


def get_goal_summary():
    registry = _load_registry()
    inner = registry.get("kingdom_goal_registry", registry)
    goals = inner.get("goals", [])
    summary = {"total": len(goals), "by_status": {}, "average_progress": 0.0}
    if goals:
        for s in GOAL_LIFECYCLE:
            count = len([g for g in goals if g["status"] == s])
            if count > 0:
                summary["by_status"][s] = count
        summary["average_progress"] = round(sum(g["progress"] for g in goals) / len(goals), 2)
    return summary
