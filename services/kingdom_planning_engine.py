from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
SERVICES_DIR = Path(__file__).resolve().parent.parent / "services"

MAX_PLANNING_LEVEL = 4
CAP_VIOLATION = "PSOP-03 CAP: Kingdom Planning capped at Level 4."


class PlanningError(Exception):
    pass


def _load_registry(name):
    import yaml
    path = REGISTRIES_DIR / name
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _import_service(name):
    import importlib
    return importlib.import_module(f"services.{name}")


def create_kingdom_plan(name, description, goal_ids, program_ids=None):
    gm = _import_service("kingdom_goal_manager")
    pm = _import_service("kingdom_program_manager")
    for gid in goal_ids:
        goal = gm.get_goal(gid)
        if not goal:
            raise PlanningError(f"Goal not found: {gid}")
    if program_ids:
        for pid in program_ids:
            prog = pm.get_program(pid)
            if not prog:
                raise PlanningError(f"Program not found: {pid}")
    timestamp = datetime.now(timezone.utc).isoformat()
    plan = {
        "plan_id": f"PLAN-{timestamp[:10]}",
        "name": name,
        "description": description,
        "goal_ids": goal_ids,
        "program_ids": program_ids or [],
        "created_at": timestamp,
        "updated_at": timestamp,
        "status": "PROPOSED",
        "progress": 0.0,
        "planning_level": 0,
    }
    return plan


def get_planning_summary():
    gm = _import_service("kingdom_goal_manager")
    pm = _import_service("kingdom_program_manager")
    goal_summary = gm.get_goal_summary()
    program_summary = pm.get_program_summary()
    goal_progress = goal_summary.get("average_progress", 0)
    program_progress = program_summary.get("average_progress", 0)
    planning_efficiency = round((goal_progress + program_progress) / 2, 2) if (goal_progress or program_progress) else 0.0
    level = _determine_planning_level(goal_summary, program_summary)
    return {
        "goal_summary": goal_summary,
        "program_summary": program_summary,
        "planning_efficiency": planning_efficiency,
        "planning_level": level,
        "planning_level_cap": MAX_PLANNING_LEVEL,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def _determine_planning_level(goal_summary, program_summary):
    if goal_summary["total"] == 0:
        return 0
    has_progress = any(g.get("progress", 0) > 0 for g in _import_service("kingdom_goal_manager").list_goals())
    if not has_progress:
        return 1
    has_programs = program_summary["total"] > 0
    if not has_programs:
        return 2
    has_linked = any(
        len(g.get("linked_programs", [])) > 0
        for g in _import_service("kingdom_goal_manager").list_goals()
    )
    if not has_linked:
        return 2
    has_completed = program_summary["by_status"].get("COMPLETED", 0) > 0
    if not has_completed:
        return 3
    return min(4, MAX_PLANNING_LEVEL)


def check_planning_compliance():
    gm = _import_service("kingdom_goal_manager")
    pm = _import_service("kingdom_program_manager")
    findings = []
    goals = gm.list_goals()
    for g in goals:
        if g["progress"] >= 100 and g["status"] != "COMPLETED":
            findings.append({
                "goal_id": g["goal_id"],
                "issue": "Goal at 100% progress but not COMPLETED",
                "severity": "LOW",
            })
    programs = pm.list_programs()
    for p in programs:
        if p["progress"] >= 100 and p["status"] != "COMPLETED":
            findings.append({
                "program_id": p["program_id"],
                "issue": "Program at 100% progress but not COMPLETED",
                "severity": "LOW",
            })
    return {"findings": findings, "total_findings": len(findings)}
