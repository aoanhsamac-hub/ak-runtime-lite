# Kingdom Assignment Manager
# Assigns tasks to agents based on authority and capacity

from datetime import datetime, timezone
from pathlib import Path
import yaml

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"

# Agent names as they appear in charter files
AGENT_NAMES = ["janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"]


class AssignmentError(Exception):
    pass


def _load_assignment_registry():
    path = REGISTRIES_DIR / "KINGDOM_ASSIGNMENT_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_task_registry():
    path = REGISTRIES_DIR / "KINGDOM_TASK_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_assignment_registry(registry):
    path = REGISTRIES_DIR / "KINGDOM_ASSIGNMENT_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def assign_task_to_agent(task_id, agent):
    """Assign task to agent if within authority bounds."""
    from services import kingdom_task_manager as tm
    
    agent = agent.lower().strip()
    
    # Verify agent exists in registry
    assignment_registry = _load_assignment_registry()
    inner = assignment_registry.get("kingdom_assignment_registry", assignment_registry)
    
    if agent not in inner.get("agent_capacity", {}):
        raise AssignmentError(f"Agent not recognized: {agent}. Valid: {AGENT_NAMES}")
    
    # Check capacity
    assignments = inner.get("assignments", [])
    current_assignments = [a for a in assignments if a.get("agent") == agent and a.get("status") == "ACTIVE"]
    
    if len(current_assignments) >= inner["agent_capacity"][agent]:
        raise AssignmentError(f"Agent {agent} at capacity ({len(current_assignments)}/{inner['agent_capacity'][agent]})")
    
    # Assign task
    task = tm.assign_task(task_id, agent)
    
    # Record assignment
    assignment = {
        "task_id": task_id,
        "agent": agent,
        "assigned_at": datetime.now(timezone.utc).isoformat(),
        "status": "ACTIVE",
        "audit_trail": [f"ASSIGNED:{agent}"],
    }
    
    assignments.append(assignment)
    inner["assignments"] = assignments
    inner["updated_at"] = assignment["assigned_at"]
    _save_assignment_registry(assignment_registry)
    
    return task


def complete_assignment(task_id, agent):
    """Mark assignment as complete."""
    assignment_registry = _load_assignment_registry()
    inner = assignment_registry.get("kingdom_assignment_registry", assignment_registry)
    
    for a in inner.get("assignments", []):
        if a.get("task_id") == task_id and a.get("agent") == agent:
            a["status"] = "COMPLETED"
            a["completed_at"] = datetime.now(timezone.utc).isoformat()
            a["audit_trail"].append("COMPLETED")
            break
    
    _save_assignment_registry(assignment_registry)
    return {"task_id": task_id, "agent": agent, "status": "completed"}


def get_agent_load(agent):
    """Get current task load for agent."""
    assignment_registry = _load_assignment_registry()
    inner = assignment_registry.get("kingdom_assignment_registry", assignment_registry)
    
    active = [a for a in inner.get("assignments", []) if a.get("agent") == agent and a.get("status") == "ACTIVE"]
    return len(active)