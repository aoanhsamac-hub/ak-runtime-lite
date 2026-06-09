"""Verify LanceDB operational memory flow: Mission → Evidence → Lesson → Knowledge → Skill → Capability."""

from memory.lancedb_adapter import LanceDBAdapter
from memory.kingdom_memory_platform import KingdomMemoryPlatform
from tests.test_lancedb_adapter import FakeBackend


def _mp():
    return KingdomMemoryPlatform(db_path=":memory:", adapter=LanceDBAdapter(":memory:", backend=FakeBackend()))


def test_mission_to_evidence():
    mp = _mp()
    mission = mp.record_mission({"mission_id": "m-flow-1", "objective": "Test flow", "status": "COMPLETED"})
    assert mission["mission_id"] == "m-flow-1"
    evidence = mp.record_evidence({"evidence_id": "ev-flow-1", "source_agent": "iris", "mission_id": "m-flow-1"})
    assert evidence["mission_id"] == "m-flow-1"
    matched = mp.get_evidence_by_mission("m-flow-1")
    assert len(matched) >= 1


def test_evidence_to_lesson_candidate():
    mp = _mp()
    mp.record_evidence({"evidence_id": "ev-flow-2", "source_agent": "hermes", "mission_id": "m-flow-2"})
    candidate = mp.record_lesson_candidate({"lesson_id": "lc-flow-1", "source_evidence_ids": ["ev-flow-2"]})
    assert candidate["lesson_id"] == "lc-flow-1"
    assert candidate.get("source_evidence_ids") == ["ev-flow-2"]


def test_lesson_candidate_promotion():
    mp = _mp()
    mp.record_lesson_candidate({"lesson_id": "lc-flow-2", "status": "DRAFT"})
    promoted = mp.promote_lesson_candidate("lc-flow-2")
    assert promoted is not None
    assert promoted["status"] == "APPROVED"
    lessons = mp.get_lessons()
    assert len(lessons) >= 1


def test_lesson_to_knowledge():
    mp = _mp()
    mp.record_lesson_candidate({"lesson_id": "lc-flow-3"})
    mp.promote_lesson_candidate("lc-flow-3")
    knowledge = mp.promote_to_knowledge("lc-flow-3", {"title": "Test knowledge"})
    assert knowledge["knowledge_id"] == "KNOW-lc-flow-3"
    assert knowledge["source_lesson_id"] == "lc-flow-3"
    assert knowledge["retention_class"] == "CANONICAL"


def test_knowledge_to_skill():
    mp = _mp()
    mp.promote_to_knowledge("lc-flow-4", {"lesson_id": "lc-flow-4"})
    skill = mp.promote_to_skill("KNOW-lc-flow-4", {"name": "Test skill"})
    assert skill["skill_id"] == "SKILL-KNOW-lc-flow-4"
    assert skill["source_knowledge_id"] == "KNOW-lc-flow-4"
    assert skill["retention_class"] == "CANONICAL"


def test_skill_to_capability():
    mp = _mp()
    mp.promote_to_knowledge("lc-flow-5", {"lesson_id": "lc-flow-5"})
    mp.promote_to_skill("KNOW-lc-flow-5", {"name": "Test skill for cap"})
    capability = mp.promote_to_capability("SKILL-KNOW-lc-flow-5", {"name": "Test capability"})
    assert capability["capability_id"] == "CAP-SKILL-KNOW-lc-flow-5"
    assert capability["source_skill_id"] == "SKILL-KNOW-lc-flow-5"
    assert capability["retention_class"] == "CANONICAL"


def test_full_lifecycle_path_exists():
    mp = _mp()
    assert hasattr(mp, "record_mission")
    assert hasattr(mp, "record_evidence")
    assert hasattr(mp, "record_lesson_candidate")
    assert hasattr(mp, "promote_lesson_candidate")
    assert hasattr(mp, "get_lessons")
    assert hasattr(mp, "promote_to_knowledge")
    assert hasattr(mp, "promote_to_skill")
    assert hasattr(mp, "promote_to_capability")
    assert hasattr(mp, "record_capability_usage")
    assert hasattr(mp, "record_capability_roi")
    assert hasattr(mp, "record_agent_performance")


def test_unreviewed_records_default_to_quarantine_equivalent():
    mp = _mp()
    candidate = mp.record_lesson_candidate({"lesson_id": "lc-flow-6"})
    assert candidate.get("status") == "DRAFT"
    evidence = mp.record_evidence({"evidence_id": "ev-flow-6"})
    assert "retention_class" in evidence


def test_promotion_requires_approval():
    mp = _mp()
    candidate = mp.record_lesson_candidate({"lesson_id": "lc-flow-7", "status": "DRAFT"})
    assert candidate["status"] == "DRAFT"
    promoted = mp.promote_lesson_candidate("lc-flow-7")
    assert promoted["status"] == "APPROVED"
