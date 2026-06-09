from memory.capability_roi_registry import CapabilityROIRegistry
from memory.lancedb_adapter import LanceDBAdapter
from memory.kingdom_memory_platform import KingdomMemoryPlatform

from tests.test_lancedb_adapter import FakeBackend


def _registry():
    import pytest
    mp = KingdomMemoryPlatform(db_path=":memory:", adapter=LanceDBAdapter(":memory:", backend=FakeBackend()))
    return CapabilityROIRegistry(mp)


def test_record_and_get_roi():
    reg = _registry()
    record = reg.record_roi("test_cap", value=100.0, cost=50.0)
    assert record["capability_name"] == "test_cap"
    assert record["total_value"] == 100.0
    assert record["total_cost"] == 50.0
    assert record["roi"] == 2.0

    results = reg.get_roi("test_cap")
    assert len(results) >= 1
    assert results[-1]["capability_name"] == "test_cap"


def test_calculate_roi_zero_cost():
    reg = _registry()
    reg.record_roi("zero_cost_cap", value=50.0, cost=0.0)
    result = reg.calculate_roi("zero_cost_cap")
    assert result["roi"] == 0.0


def test_record_and_get_usage():
    reg = _registry()
    usage = reg.record_usage("test_cap_usage", agent_id="iris", success=True)
    assert usage["capability_name"] == "test_cap_usage"
    assert usage["agent_id"] == "iris"
    assert usage["success"] is True

    results = reg.get_usage("test_cap_usage")
    assert len(results) >= 1


def test_summary():
    reg = _registry()
    summary = reg.summary()
    assert "total_roi_records" in summary
    assert "total_usage_records" in summary
    assert "capabilities_tracked" in summary
