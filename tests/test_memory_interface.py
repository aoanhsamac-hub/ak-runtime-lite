from memory.lancedb_adapter import LanceDBAdapter
from memory.memory_interface import MemoryInterface

from tests.test_lancedb_adapter import FakeBackend


def test_memory_interface_exposes_public_api_and_quarantines_by_id(tmp_path):
    interface = MemoryInterface(adapter=LanceDBAdapter(tmp_path, backend=FakeBackend()))

    record = interface.quarantine_record("LESSON-1", "missing reviewer")

    assert record["record_id"] == "LESSON-1"
    assert record["status"] == "QUARANTINE"
    assert record["quarantine_reason"] == "missing reviewer"


def test_registry_records_have_required_common_metadata(tmp_path):
    interface = MemoryInterface(adapter=LanceDBAdapter(tmp_path, backend=FakeBackend()))
    lesson = interface.create_lesson_candidate({
        "title": "Metadata lesson",
        "summary": "Metadata summary",
        "content": "Metadata content",
        "source": "metadata-test",
        "owner_agent": "LangLieu",
        "reviewer_agent": "Sage",
        "risk_level": "LEVEL_1_MODERATE",
        "tags": ["metadata"],
    })
    reviewed = interface.submit_for_review(lesson.lesson_id, "Sage")
    approved = interface.lessons.approve(reviewed.lesson_id, "Sage")
    skill = interface.skills.create_candidate(
        name="metadata-skill",
        description="Skill metadata",
        source_lessons=[approved.lesson_id],
        owner_agent="LangLieu",
        allowed_agents=["LangLieu"],
        risk_level="LEVEL_1_MODERATE",
        test_cases=["metadata present"],
    )

    for record in [lesson, skill]:
        data = record.to_dict()
        for key in ["source_hash", "owner_agent", "reviewer_agent", "status", "version", "risk_level", "created_at"]:
            assert data.get(key), f"{key} missing from {type(record).__name__}"


def test_memory_interface_accepts_canonical_ak_agent_name_variants(tmp_path):
    interface = MemoryInterface(adapter=LanceDBAdapter(tmp_path, backend=FakeBackend()))

    for agent_name in ["Lang Lieu", "LangLieu", "Lang Liêu", "lang_lieu", "yet_kieu"]:
        interface._validate_agent(agent_name)
