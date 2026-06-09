"""Verify capabilities connect to usage, ROI, performance, evidence, and adoption."""

from memory.lancedb_adapter import LanceDBAdapter
from memory.kingdom_memory_platform import KingdomMemoryPlatform
from memory.capability_roi_registry import CapabilityROIRegistry
from tests.test_lancedb_adapter import FakeBackend


def _mp():
    return KingdomMemoryPlatform(db_path=":memory:", adapter=LanceDBAdapter(":memory:", backend=FakeBackend()))


def _roi():
    return CapabilityROIRegistry(_mp())


def test_capability_usage_can_be_recorded():
    mp = _mp()
    record = mp.record_capability_usage({"capability_name": "test_cap", "agent_id": "iris", "success": True})
    assert record["capability_name"] == "test_cap"
    results = mp.get_capability_usage("test_cap")
    assert len(results) >= 1


def test_capability_roi_can_be_recorded():
    reg = _roi()
    record = reg.record_roi("test_cap_roi", value=100.0, cost=50.0)
    assert record["roi"] == 2.0
    results = reg.get_roi("test_cap_roi")
    assert len(results) >= 1


def test_capability_roi_calculated_from_usage():
    reg = _roi()
    reg.record_roi("economy_cap", value=200.0, cost=100.0)
    reg.record_usage("economy_cap", agent_id="sage", success=True)
    result = reg.calculate_roi("economy_cap")
    assert result["roi"] == 2.0
    assert result["usage_count"] >= 0


def test_agent_performance_can_be_recorded():
    mp = _mp()
    record = mp.record_agent_performance({"agent_id": "hermes", "task": "test", "success": True})
    assert "retention_class" in record
    results = mp.get_agent_performance("hermes")
    assert len(results) >= 1


def test_evidence_can_be_recorded():
    mp = _mp()
    record = mp.record_evidence({"evidence_id": "ev-conn-001", "source_agent": "iris"})
    assert record["evidence_id"] == "ev-conn-001"
    results = mp.get_evidence("ev-conn-001")
    assert len(results) >= 1


def test_lesson_candidate_can_be_recorded():
    mp = _mp()
    record = mp.record_lesson_candidate({"lesson_id": "lesson-conn-001"})
    assert record["lesson_id"] == "lesson-conn-001"
    record["status"] = "APPROVED"
    promoted = mp.promote_lesson_candidate("lesson-conn-001")
    assert promoted is not None


def test_capability_summary_includes_all_registries():
    mp = _mp()
    mp.record_capability_usage({"capability_name": "cap_sum", "agent_id": "iris", "success": True})
    mp.record_capability_roi({"capability_name": "cap_sum", "total_value": 50.0, "total_cost": 25.0})
    mp.record_agent_performance({"agent_id": "iris", "task": "test", "success": True})
    summary = mp.summary()
    assert "capability_usage" in summary
    assert "roi_records" in summary
    assert "agent_performance" in summary
    assert "evidence_count" in summary


def test_capability_roi_registry_summary():
    reg = _roi()
    reg.record_roi("cap_a", value=10.0, cost=5.0)
    reg.record_usage("cap_a", agent_id="janus", success=True)
    summary = reg.summary()
    assert summary["total_roi_records"] >= 1
    assert summary["capabilities_tracked"] >= 1
