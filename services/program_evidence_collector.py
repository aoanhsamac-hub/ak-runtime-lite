from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _load_registry():
    import yaml
    path = REGISTRIES_DIR / "PROGRAM_EVIDENCE_REGISTRY.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry):
    import yaml
    path = REGISTRIES_DIR / "PROGRAM_EVIDENCE_REGISTRY.yaml"
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_evidence_id():
    registry = _load_registry()
    inner = registry.get("program_evidence_registry", registry)
    counter = len(inner.get("evidence_records", [])) + 1
    return f"PROG-EVID-{counter:04d}"


def collect_program_evidence():
    evidence_id = _generate_evidence_id()
    timestamp = _utc_now()
    goal_data = {}
    program_data = {}
    try:
        from services.kingdom_goal_manager import get_goal_summary, list_goals
        goal_data = get_goal_summary()
        goals = list_goals()
        goal_data["total_goals"] = len(goals)
        goal_data["completed"] = len([g for g in goals if g["status"] == "COMPLETED"])
        goal_data["active"] = len([g for g in goals if g["status"] == "ACTIVE"])
    except Exception:
        goal_data = {"total": 0}
    try:
        from services.kingdom_program_manager import get_program_summary, list_programs
        program_data = get_program_summary()
        programs = list_programs()
        program_data["total_programs"] = len(programs)
        program_data["completed"] = len([p for p in programs if p["status"] == "COMPLETED"])
        program_data["active"] = len([p for p in programs if p["status"] == "ACTIVE"])
    except Exception:
        program_data = {"total": 0}
    registry = _load_registry()
    inner = registry.get("program_evidence_registry", registry)
    record = {
        "evidence_id": evidence_id,
        "goal_summary": goal_data,
        "program_summary": program_data,
        "recorded_at": timestamp,
    }
    if "evidence_records" not in inner:
        inner["evidence_records"] = []
    inner["evidence_records"].append(record)
    inner["last_evidence_id"] = evidence_id
    inner["last_updated"] = timestamp
    if inner.get("status") == "INITIALIZED":
        inner["status"] = "ACTIVE"
    registry["program_evidence_registry"] = inner
    _save_registry(registry)
    return record


def get_all_evidence():
    registry = _load_registry()
    inner = registry.get("program_evidence_registry", registry)
    return list(inner.get("evidence_records", []))


def get_evidence_summary():
    records = get_all_evidence()
    return {
        "total_records": len(records),
        "generated_at": _utc_now(),
    }
