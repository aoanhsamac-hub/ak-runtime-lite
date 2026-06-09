from memory.learning_loop import LearningLoop
from memory.lesson_registry import LessonRegistry
from memory.skill_registry import SkillRegistry
from memory.lancedb_adapter import LanceDBAdapter

from tests.test_lancedb_adapter import FakeBackend


def test_learning_loop_creates_lesson_candidate_but_does_not_auto_promote(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    lessons = LessonRegistry(adapter)
    skills = SkillRegistry(adapter, lessons)
    loop = LearningLoop(lessons, skills)

    lesson = loop.observe(
        title="Debug finding",
        summary="A failing test exposed a missing guard.",
        content="Evidence and analysis stay as lesson candidate.",
        source="test-run",
        owner_agent="LangLieu",
        reviewer_agent="Sage",
        risk_level="LEVEL_1_MODERATE",
        tags=["debug"],
    )

    assert lesson.status == "DRAFT"
    assert skills.list_records() == []


def test_learning_loop_requires_approved_lesson_before_skill_candidate(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    lessons = LessonRegistry(adapter)
    skills = SkillRegistry(adapter, lessons)
    loop = LearningLoop(lessons, skills)
    lesson = loop.observe(
        title="Architecture rule",
        summary="Use interface before direct backend access.",
        content="Agents must write through MemoryInterface.",
        source="architecture-review",
        owner_agent="LangLieu",
        reviewer_agent="Sage",
        risk_level="LEVEL_2_HIGH",
        tags=["architecture"],
    )

    try:
        loop.create_skill_candidate(
            name="memory-interface-only",
            description="Use MemoryInterface for memory access.",
            source_lessons=[lesson.lesson_id],
            owner_agent="LangLieu",
            allowed_agents=["LangLieu"],
            risk_level="LEVEL_2_HIGH",
            test_cases=["reject direct backend write"],
        )
    except ValueError as exc:
        assert "approved" in str(exc).lower()
    else:
        raise AssertionError("unapproved lessons must not create skills")
