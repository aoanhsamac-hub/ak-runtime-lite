# Kingdom Report Compiler
# Generates executive reports from directive/task completion

from datetime import datetime, timezone
from pathlib import Path
import yaml

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "docs" / "reports"


class ReportError(Exception):
    pass


def generate_executive_report(directive_id):
    """Generate executive report for a directive."""
    from services import reh_directive_manager as dm
    from services import kingdom_task_manager as tm
    
    directive_registry = dm._load_registry()
    directives = directive_registry.get("kingdom_directive_registry", {}).get("directives", [])
    directive = next((d for d in directives if d.get("directive_id") == directive_id), None)
    
    task_registry = tm._load_registry()
    tasks = task_registry.get("kingdom_task_registry", {}).get("tasks", [])
    directive_tasks = [t for t in tasks if t.get("directive_id") == directive_id]
    
    progress = sum(t.get("progress", 0) for t in directive_tasks) / len(directive_tasks) if directive_tasks else 0
    
    report = {
        "report_id": f"RPT-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{directive_id}",
        "directive_id": directive_id,
        "author": "Janus",
        "reviewer": "Sage",
        "status": "DRAFT",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sections": {
            "summary": f"Directive: {directive.get('title', 'N/A') if directive else directive_id}",
            "status": directive.get("status") if directive else "UNKNOWN",
            "progress": f"{progress:.1f}% complete",
            "risks": "None identified",
            "blockers": "None",
            "recommendations": "Continue execution",
            "next_actions": "Monitor task completion",
        },
    }
    
    return report


def generate_weekly_report():
    """Generate weekly kingdom status report."""
    from services import kingdom_progress_tracker as pt
    
    kingdom = pt.get_kingdom_progress()
    
    report = {
        "report_type": "WEEKLY_PRESIDENTIAL_BRIEFING",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "kingdom_status": kingdom,
        "agent_status": pt.get_agent_progress("all"),
    }
    
    return report


def save_report(report, filename):
    """Save report to file."""
    import yaml as y
    path = REPORTS_DIR / filename
    path.write_text(y.dump(report, default_flow_style=False, allow_unicode=True), encoding="utf-8")
    return {"saved": True, "path": str(path)}