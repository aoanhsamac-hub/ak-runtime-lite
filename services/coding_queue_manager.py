"""Coding Queue Manager - Manage capability implementation queue."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_queue() -> dict:
    import yaml
    path = REGISTRIES_DIR / "CAPABILITY_IMPLEMENTATION_QUEUE.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_queue(queue: dict) -> None:
    import yaml
    path = REGISTRIES_DIR / "CAPABILITY_IMPLEMENTATION_QUEUE.yaml"
    path.write_text(yaml.dump(queue, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def _generate_queue_id() -> str:
    return f"QUEUE-{datetime.now().strftime('%Y%m%d')}-{len(_load_queue().get('kingdom_capability_implementation_queue', {}).get('capability_queue', [])) + 1:04d}"


def add_to_queue(capability_name: str, owner: str, priority: int = 999) -> dict:
    queue = _load_queue()
    inner = queue.get("kingdom_capability_implementation_queue", {})

    entry = {
        "capability_id": _generate_queue_id(),
        "capability_name": capability_name,
        "priority": priority,
        "roi": 0.0,
        "complexity": "UNKNOWN",
        "owner": owner,
        "reviewer": "Sage",
        "status": "PROPOSED",
        "dependencies": [],
        "recommended_phase": "TBD",
    }

    inner.setdefault("capability_queue", []).append(entry)
    inner["last_updated"] = _utc_now()
    queue["kingdom_capability_implementation_queue"] = inner
    _save_queue(queue)

    return entry


def get_queue() -> list[dict]:
    queue = _load_queue()
    inner = queue.get("kingdom_capability_implementation_queue", {})
    return inner.get("capability_queue", [])


def get_by_status(status: str) -> list[dict]:
    return [e for e in get_queue() if e.get("status") == status]


def update_status(capability_id: str, status: str) -> dict | None:
    queue = _load_queue()
    inner = queue.get("kingdom_capability_implementation_queue", {})

    for entry in inner.get("capability_queue", []):
        if entry.get("capability_id") == capability_id:
            entry["status"] = status
            entry["updated_at"] = _utc_now()
            inner["last_updated"] = _utc_now()
            queue["kingdom_capability_implementation_queue"] = inner
            _save_queue(queue)
            return entry

    return None


def list_queued() -> list[dict]:
    return [e for e in get_queue() if e.get("status") in ("PROPOSED", "QUEUED", "APPROVED")]


__all__ = ["add_to_queue", "get_queue", "get_by_status", "update_status", "list_queued"]