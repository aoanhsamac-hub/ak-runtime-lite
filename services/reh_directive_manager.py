# REH Directive Manager
# Manages directives from Hung Vuong through Royal Executive House

import json
from datetime import datetime, timezone
from pathlib import Path

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"

DIRECTIVE_LIFECYCLE = ["PROPOSED", "APPROVED", "IN_PROGRESS", "BLOCKED", "REVIEW", "CLOSED"]


class DirectiveError(Exception):
    pass


def _load_registry():
    path = REGISTRIES_DIR / "KINGDOM_DIRECTIVE_REGISTRY.yaml"
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_registry(registry):
    path = REGISTRIES_DIR / "KINGDOM_DIRECTIVE_REGISTRY.yaml"
    import yaml
    path.write_text(yaml.dump(registry, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_directive_id():
    registry = _load_registry()
    inner = registry.get("kingdom_directive_registry", registry)
    directives = inner.get("directives", [])
    return f"DIR-{len(directives) + 1:04d}"


def create_directive(title, authority, priority, deadline, objective, deliverables=None, category="OPERATIONAL"):
    """Create a new directive from Hung Vuong through REH."""
    registry = _load_registry()
    inner = registry.get("kingdom_directive_registry", registry)
    
    directive_id = _generate_directive_id()
    timestamp = datetime.now(timezone.utc).isoformat()
    
    directive = {
        "directive_id": directive_id,
        "title": title,
        "authority": authority,
        "priority": priority,
        "status": "PROPOSED",
        "created_at": timestamp,
        "updated_at": timestamp,
        "deadline": deadline,
        "objective": objective,
        "deliverables": deliverables or [],
        "category": category,
        "tasks_generated": [],
        "audit_trail": [f"DIRECTIVE_CREATED:{timestamp}"],
    }
    
    if "directives" not in inner:
        inner["directives"] = []
    inner["directives"].append(directive)
    _save_registry(registry)
    return directive


def update_directive(directive_id, status=None, **updates):
    """Update directive status or fields."""
    registry = _load_registry()
    inner = registry.get("kingdom_directive_registry", registry)
    directives = inner.get("directives", [])
    
    for d in directives:
        if d["directive_id"] == directive_id:
            if status:
                if status not in DIRECTIVE_LIFECYCLE:
                    raise DirectiveError(f"Invalid status: {status}")
                d["status"] = status
            for key, value in updates.items():
                d[key] = value
            d["updated_at"] = datetime.now(timezone.utc).isoformat()
            d["audit_trail"].append(f"DIRECTIVE_UPDATED:{d['status']}")
            _save_registry(registry)
            return d
    raise DirectiveError(f"Directive not found: {directive_id}")


def close_directive(directive_id):
    """Close directive and archive."""
    return update_directive(directive_id, status="CLOSED")