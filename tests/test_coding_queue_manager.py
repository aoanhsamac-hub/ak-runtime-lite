"""Test Coding Queue Manager."""

import pytest


def test_import_coding_queue_manager():
    import services.coding_queue_manager as cqm
    assert hasattr(cqm, "add_to_queue")
    assert hasattr(cqm, "get_queue")


def test_add_to_queue():
    from services.coding_queue_manager import add_to_queue
    result = add_to_queue("Test Capability", "Hermes", priority=1)
    assert isinstance(result, dict)
    assert "capability_id" in result
    assert result["capability_name"] == "Test Capability"


def test_get_queue_returns_list():
    from services.coding_queue_manager import get_queue
    result = get_queue()
    assert isinstance(result, list)


def test_get_by_status():
    from services.coding_queue_manager import get_by_status
    result = get_by_status("PROPOSED")
    assert isinstance(result, list)


def test_update_status():
    from services.coding_queue_manager import add_to_queue, update_status
    entry = add_to_queue("Status Test", "Hermes")
    result = update_status(entry["capability_id"], "QUEUED")
    assert result is not None
    assert result["status"] == "QUEUED"


def test_list_queued():
    from services.coding_queue_manager import list_queued
    result = list_queued()
    assert isinstance(result, list)


def test_queue_entry_has_required_fields():
    from services.coding_queue_manager import add_to_queue
    entry = add_to_queue("Field Test", "Hermes")
    assert "capability_id" in entry
    assert "capability_name" in entry
    assert "priority" in entry
    assert "owner" in entry
    assert "reviewer" in entry
    assert "status" in entry


def test_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/CAPABILITY_IMPLEMENTATION_QUEUE.yaml")
    assert path.exists()


def test_queue_id_format():
    from services.coding_queue_manager import _generate_queue_id
    queue_id = _generate_queue_id()
    assert queue_id.startswith("QUEUE-")


def test_priority_values():
    from services.coding_queue_manager import add_to_queue
    entry = add_to_queue("Priority Test", "Hermes", priority=5)
    assert entry["priority"] == 5