from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
PROGRAM_LIFECYCLE = ["PROPOSED", "APPROVED", "ACTIVE", "COMPLETED", "ARCHIVED"]


class ProgramError(Exception):
    pass


def _load_registry():
    path = REGISTRIES_DIR / "KINGDOM_PROGRAM_REGISTRY.yaml"
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry):
    path = REGISTRIES_DIR / "KINGDOM_PROGRAM_REGISTRY.yaml"
    import yaml
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_program_id():
    registry = _load_registry()
    inner = registry.get("kingdom_program_registry", registry)
    programs = inner.get("programs", [])
    return f"PROG-{len(programs) + 1:04d}"


def create_program(name, description, objective, goal_ids=None):
    registry = _load_registry()
    inner = registry.get("kingdom_program_registry", registry)
    program_id = _generate_program_id()
    timestamp = datetime.now(timezone.utc).isoformat()
    program = {
        "program_id": program_id,
        "name": name,
        "description": description,
        "objective": objective,
        "goal_ids": goal_ids or [],
        "status": "PROPOSED",
        "created_at": timestamp,
        "updated_at": timestamp,
        "progress": 0.0,
        "deliverable_count": 0,
        "deliverables_completed": 0,
        "linked_capabilities": [],
    }
    if "programs" not in inner:
        inner["programs"] = []
    inner["programs"].append(program)
    inner["last_program_id"] = program_id
    inner["last_updated"] = timestamp
    if inner.get("status") == "INITIALIZED":
        inner["status"] = "ACTIVE"
    registry["kingdom_program_registry"] = inner
    _save_registry(registry)
    return program


def get_program(program_id):
    registry = _load_registry()
    inner = registry.get("kingdom_program_registry", registry)
    for p in inner.get("programs", []):
        if p["program_id"] == program_id:
            return p
    return None


def list_programs(status=None):
    registry = _load_registry()
    inner = registry.get("kingdom_program_registry", registry)
    programs = inner.get("programs", [])
    if status:
        return [p for p in programs if p["status"] == status]
    return list(programs)


def transition_program(program_id, new_status):
    if new_status not in PROGRAM_LIFECYCLE:
        raise ProgramError(f"Invalid program status: {new_status}")
    registry = _load_registry()
    inner = registry.get("kingdom_program_registry", registry)
    for p in inner.get("programs", []):
        if p["program_id"] == program_id:
            current_idx = PROGRAM_LIFECYCLE.index(p["status"])
            new_idx = PROGRAM_LIFECYCLE.index(new_status)
            if new_idx < current_idx:
                raise ProgramError(f"Cannot transition {p['status']} backwards to {new_status}")
            p["status"] = new_status
            p["updated_at"] = datetime.now(timezone.utc).isoformat()
            inner["last_updated"] = p["updated_at"]
            registry["kingdom_program_registry"] = inner
            _save_registry(registry)
            return p
    raise ProgramError(f"Program not found: {program_id}")


def update_progress(program_id, progress, deliverables_completed=None):
    if not (0.0 <= progress <= 100.0):
        raise ProgramError("Progress must be between 0 and 100")
    registry = _load_registry()
    inner = registry.get("kingdom_program_registry", registry)
    for p in inner.get("programs", []):
        if p["program_id"] == program_id:
            p["progress"] = progress
            if deliverables_completed is not None:
                p["deliverables_completed"] = deliverables_completed
            p["updated_at"] = datetime.now(timezone.utc).isoformat()
            inner["last_updated"] = p["updated_at"]
            registry["kingdom_program_registry"] = inner
            _save_registry(registry)
            return p
    raise ProgramError(f"Program not found: {program_id}")


def link_capability(program_id, capability_name):
    registry = _load_registry()
    inner = registry.get("kingdom_program_registry", registry)
    for p in inner.get("programs", []):
        if p["program_id"] == program_id:
            if "linked_capabilities" not in p:
                p["linked_capabilities"] = []
            if capability_name not in p["linked_capabilities"]:
                p["linked_capabilities"].append(capability_name)
            p["updated_at"] = datetime.now(timezone.utc).isoformat()
            inner["last_updated"] = p["updated_at"]
            registry["kingdom_program_registry"] = inner
            _save_registry(registry)
            return p
    raise ProgramError(f"Program not found: {program_id}")


def get_program_summary():
    registry = _load_registry()
    inner = registry.get("kingdom_program_registry", registry)
    programs = inner.get("programs", [])
    summary = {"total": len(programs), "by_status": {}, "average_progress": 0.0}
    if programs:
        for s in PROGRAM_LIFECYCLE:
            count = len([p for p in programs if p["status"] == s])
            if count > 0:
                summary["by_status"][s] = count
        summary["average_progress"] = round(sum(p["progress"] for p in programs) / len(programs), 2)
    return summary
