from datetime import datetime, timezone
from pathlib import Path

SERVICES_DIR = Path(__file__).resolve().parent.parent / "services"
MAX_PLANNING_LEVEL = 4
MAX_CE_LEVEL = 4


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _import_service(name):
    import importlib
    return importlib.import_module(f"services.{name}")


def get_kingdom_performance():
    gm = _import_service("kingdom_goal_manager")
    pm = _import_service("kingdom_program_manager")
    pe = _import_service("kingdom_planning_engine")
    cve = _import_service("capability_value_engine")
    cre = _import_service("capability_roi_engine")
    kre = _import_service("knowledge_roi_engine")
    ti = _import_service("treasury_impact_tracker")

    goal_summary = gm.get_goal_summary()
    program_summary = pm.get_program_summary()
    planning_summary = pe.get_planning_summary()
    value_summary = cve.get_domain_value_summary()
    roi_summary = cre.get_domain_roi_summary()
    knowledge_summary = kre.get_knowledge_roi_summary()
    treasury_summary = ti.get_treasury_contribution_summary()

    goal_completion_rate = _calc_rate(goal_summary.get("by_status", {}).get("COMPLETED", 0),
                                      goal_summary.get("total", 0))
    program_completion_rate = _calc_rate(program_summary.get("by_status", {}).get("COMPLETED", 0),
                                         program_summary.get("total", 0))
    performance = {
        "goal_completion_rate": goal_completion_rate,
        "program_completion_rate": program_completion_rate,
        "goal_average_progress": goal_summary.get("average_progress", 0),
        "program_average_progress": program_summary.get("average_progress", 0),
        "planning_efficiency": planning_summary.get("planning_efficiency", 0),
        "planning_level": planning_summary.get("planning_level", 0),
        "capability_economy_level": cre.get_capability_economy_level(),
        "capability_roi": roi_summary.get("roi", 0),
        "knowledge_roi": knowledge_summary.get("knowledge_roi", 0),
        "average_value_score": value_summary.get("average_value_score", 0),
        "treasury_impact": treasury_summary.get("net_treasury_impact", 0),
        "total_treasury_contribution": treasury_summary.get("total_treasury_contribution", 0),
        "generated_at": _utc_now(),
        "max_planning_level": MAX_PLANNING_LEVEL,
        "max_ce_level": MAX_CE_LEVEL,
    }
    return performance


def _calc_rate(numerator, denominator):
    return round((numerator / denominator) * 100, 2) if denominator > 0 else 0.0
