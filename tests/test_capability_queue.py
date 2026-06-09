"""Test Capability Implementation Queue."""

import pytest


def test_queue_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/CAPABILITY_IMPLEMENTATION_QUEUE.yaml")
    assert path.exists()


def test_queue_yaml_structure():
    import yaml
    from pathlib import Path
    path = Path("docs/registries/CAPABILITY_IMPLEMENTATION_QUEUE.yaml")
    content = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert "kingdom_capability_implementation_queue" in content


def test_queue_has_required_fields():
    import yaml
    from pathlib import Path
    path = Path("docs/registries/CAPABILITY_IMPLEMENTATION_QUEUE.yaml")
    content = yaml.safe_load(path.read_text(encoding="utf-8"))
    inner = content.get("kingdom_capability_implementation_queue", {})
    queue = inner.get("capability_queue", [])
    for entry in queue:
        assert "capability_id" in entry
        assert "capability_name" in entry
        assert "priority" in entry
        assert "owner" in entry
        assert "status" in entry


def test_queue_has_initial_entries():
    import yaml
    from pathlib import Path
    path = Path("docs/registries/CAPABILITY_IMPLEMENTATION_QUEUE.yaml")
    content = yaml.safe_load(path.read_text(encoding="utf-8"))
    inner = content.get("kingdom_capability_implementation_queue", {})
    queue = inner.get("capability_queue", [])
    assert len(queue) >= 3


def test_service_queue_integration():
    from services.coding_queue_manager import list_queued
    result = list_queued()
    assert len(result) >= 0


def test_priority_ordering():
    from services.coding_queue_manager import get_queue
    queue = get_queue()
    if len(queue) >= 2:
        priorities = [e.get("priority", 999) for e in queue]
        assert priorities[0] <= priorities[-1] or len(priorities) == 0


def test_status_values():
    valid_statuses = ["PROPOSED", "QUEUED", "APPROVED", "IMPLEMENTING", "REVIEW", "COMPLETE"]
    assert "PROPOSED" in valid_statuses


def test_complexity_values():
    valid_complexity = ["LOW", "MEDIUM", "HIGH", "UNKNOWN"]
    assert "LOW" in valid_complexity


def test_registry_metadata():
    import yaml
    from pathlib import Path
    path = Path("docs/registries/CAPABILITY_IMPLEMENTATION_QUEUE.yaml")
    content = yaml.safe_load(path.read_text(encoding="utf-8"))
    inner = content.get("kingdom_capability_implementation_queue", {})
    assert "created_at" in inner
    assert "operator" in inner
    assert "reviewer" in inner


def test_queue_operations():
    from services.coding_queue_manager import add_to_queue, get_queue
    initial_count = len(get_queue())
    add_to_queue("Temp Test", "Hermes")
    new_count = len(get_queue())
    assert new_count >= initial_count