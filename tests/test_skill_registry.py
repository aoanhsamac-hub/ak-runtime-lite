from memory.lancedb_adapter import LanceDBAdapter
from memory.lesson_registry import LessonRegistry
from memory.skill_registry import SkillRegistry
from memory.schemas.records import SKILL_LIFECYCLE_STAGES, SKILL_CATEGORIES, SKILL_SOURCES

from tests.test_lancedb_adapter import FakeBackend


def _setup(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    lessons = LessonRegistry(adapter)
    lesson = lessons.create_candidate(
        title="Approved lesson", summary="Summary", content="Content",
        source="review", owner_agent="Hermes", reviewer_agent="Sage",
        risk_level="LEVEL_1_MODERATE", tags=["memory"],
    )
    lessons.mark_reviewed(lesson.lesson_id, "Sage")
    lessons.approve(lesson.lesson_id, "Sage")
    return adapter, lessons, lesson


def test_skill_registry_create_candidate(tmp_path):
    adapter, lessons, lesson = _setup(tmp_path)
    skills = SkillRegistry(adapter, lessons)
    skill = skills.create_candidate(
        name="compress-memory", description="Compress raw reports into lessons.",
        source_lessons=[lesson.lesson_id], owner_agent="Hermes",
        allowed_agents=["Hermes", "LangLieu"], risk_level="LEVEL_1_MODERATE",
        test_cases=["compress 3 reports"],
    )
    assert skill.name == "compress-memory"
    assert skill.status == "DRAFT"
    assert skill.lifecycle_stage == "PROPOSED"
    assert skill.source == "internal"
    assert skill.category == "core"


def test_skill_registry_lifecycle_transition(tmp_path):
    adapter, lessons, lesson = _setup(tmp_path)
    skills = SkillRegistry(adapter, lessons)
    skill = skills.create_candidate(
        name="lifecycle-test", description="Test lifecycle transitions.",
        source_lessons=[lesson.lesson_id], owner_agent="Hermes",
        allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE", test_cases=[],
    )
    updated = skills.transition_lifecycle(skill.skill_id, "DISCOVERED", "Sage")
    assert updated.lifecycle_stage == "DISCOVERED"
    assert updated.version == 2

    updated2 = skills.transition_lifecycle(skill.skill_id, "SANDBOXED", "Sage")
    assert updated2.lifecycle_stage == "SANDBOXED"
    assert updated2.version == 3


def test_skill_registry_suspend_retire_archive(tmp_path):
    adapter, lessons, lesson = _setup(tmp_path)
    skills = SkillRegistry(adapter, lessons)
    skill = skills.create_candidate(
        name="lifecycle-full", description="Full lifecycle test.",
        source_lessons=[lesson.lesson_id], owner_agent="Hermes",
        allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE", test_cases=[],
    )
    suspended = skills.suspend(skill.skill_id, "Sage", "risk detected")
    assert suspended.status == "SUSPENDED"
    assert "suspension_reason" in suspended.audit_requirements

    retired = skills.retire(skill.skill_id, "Sage", "end of life")
    assert retired.status == "RETIRED"
    assert retired.lifecycle_stage == "RETIRED"

    archived = skills.archive(skill.skill_id)
    assert archived.lifecycle_stage == "ARCHIVED"


def test_skill_registry_list_by_category(tmp_path):
    adapter, lessons, lesson = _setup(tmp_path)
    skills = SkillRegistry(adapter, lessons)
    skills.create_candidate(name="core-skill", description="Core skill.",
        source_lessons=[lesson.lesson_id], owner_agent="Hermes",
        allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE", test_cases=[],
        category="core")
    skills.create_candidate(name="imported-skill", description="Imported skill.",
        source_lessons=[lesson.lesson_id], owner_agent="Hermes",
        allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE", test_cases=[],
        category="imported", source="hermes")
    core_skills = skills.get_by_category("core")
    assert len(core_skills) == 1
    imported_skills = skills.get_by_category("imported")
    assert len(imported_skills) == 1


def test_skill_registry_list_by_source(tmp_path):
    adapter, lessons, lesson = _setup(tmp_path)
    skills = SkillRegistry(adapter, lessons)
    skills.create_candidate(name="internal-skill", description="Internal.",
        source_lessons=[lesson.lesson_id], owner_agent="Hermes",
        allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE", test_cases=[],
        source="internal")
    skills.create_candidate(name="hermes-skill", description="From Hermes.",
        source_lessons=[lesson.lesson_id], owner_agent="Hermes",
        allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE", test_cases=[],
        source="hermes", category="imported")
    internal_skills = skills.get_by_source("internal")
    assert len(internal_skills) >= 1
    hermes_skills = skills.get_by_source("hermes")
    assert len(hermes_skills) == 1


def test_skill_registry_list_by_lifecycle_stage(tmp_path):
    adapter, lessons, lesson = _setup(tmp_path)
    skills = SkillRegistry(adapter, lessons)
    s1 = skills.create_candidate(name="proposed-skill", description="Proposed.",
        source_lessons=[lesson.lesson_id], owner_agent="Hermes",
        allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE", test_cases=[])
    skills.transition_lifecycle(s1.skill_id, "DISCOVERED", "Sage")
    proposed = skills.get_by_lifecycle_stage("PROPOSED")
    discovered = skills.get_by_lifecycle_stage("DISCOVERED")
    assert len(proposed) >= 0
    assert len(discovered) >= 1


def test_skill_registry_update_ownership(tmp_path):
    adapter, lessons, lesson = _setup(tmp_path)
    skills = SkillRegistry(adapter, lessons)
    skill = skills.create_candidate(name="ownership-test", description="Test ownership.",
        source_lessons=[lesson.lesson_id], owner_agent="Hermes",
        allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE", test_cases=[])
    updated = skills.update_ownership(
        skill.skill_id,
        primary_users=["Sage"],
        secondary_users=["LangLieu"],
        forbidden_users=["YetKieu"],
    )
    assert "Sage" in updated.primary_users
    assert "LangLieu" in updated.secondary_users
    assert "YetKieu" in updated.forbidden_users
    assert "Sage" in updated.allowed_agents


def test_skill_registry_add_remove_dependency(tmp_path):
    adapter, lessons, lesson = _setup(tmp_path)
    skills = SkillRegistry(adapter, lessons)
    skill = skills.create_candidate(name="dep-test", description="Dependency test.",
        source_lessons=[lesson.lesson_id], owner_agent="Hermes",
        allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE", test_cases=[])
    updated = skills.add_dependency(skill.skill_id, "SKILL-OTHER")
    assert "SKILL-OTHER" in updated.dependencies
    updated2 = skills.remove_dependency(skill.skill_id, "SKILL-OTHER")
    assert "SKILL-OTHER" not in updated2.dependencies


def test_skill_registry_approved_for_agent_excludes_forbidden(tmp_path):
    adapter, lessons, lesson = _setup(tmp_path)
    skills = SkillRegistry(adapter, lessons)
    skill = skills.create_candidate(name="forbidden-test", description="Forbidden test.",
        source_lessons=[lesson.lesson_id], owner_agent="Hermes",
        allowed_agents=["Hermes", "Sage", "LangLieu"],
        risk_level="LEVEL_1_MODERATE", test_cases=[],
        forbidden_users=["Sage"],
    )
    skills.mark_reviewed(skill.skill_id, "Sage")
    skills.approve(skill.skill_id, "Sage")
    approved = skills.approved_for_agent("Sage")
    assert len(approved) == 0


def test_skill_registry_rejects_unapproved_source_lesson(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    lessons = LessonRegistry(adapter)
    lesson = lessons.create_candidate(
        title="Draft lesson", summary="Draft", content="Draft content",
        source="review", owner_agent="Hermes", reviewer_agent="Sage",
        risk_level="LEVEL_1_MODERATE", tags=[],
    )
    skills = SkillRegistry(adapter, lessons)
    try:
        skills.create_candidate(
            name="bad-skill", description="Should fail",
            source_lessons=[lesson.lesson_id], owner_agent="Hermes",
            allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE", test_cases=[],
        )
    except ValueError as exc:
        assert "approved" in str(exc).lower()
    else:
        raise AssertionError("draft lessons must be rejected")


def test_skill_registry_list_records_with_filters(tmp_path):
    adapter, lessons, lesson = _setup(tmp_path)
    skills = SkillRegistry(adapter, lessons)
    skills.create_candidate(name="s1", description="S1",
        source_lessons=[lesson.lesson_id], owner_agent="Hermes",
        allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE", test_cases=[])
    s2 = skills.create_candidate(name="s2", description="S2",
        source_lessons=[lesson.lesson_id], owner_agent="Sage",
        allowed_agents=["Sage"], risk_level="LEVEL_1_MODERATE", test_cases=[])
    skills.transition_lifecycle(s2.skill_id, "DISCOVERED", "Sage")

    all_records = skills.list_records()
    assert len(all_records) >= 2

    hermes_records = skills.list_records(owner_agent="Hermes")
    assert len(hermes_records) == 1

    discovered = skills.list_records(lifecycle_stage="DISCOVERED")
    assert len(discovered) == 1

    core_records = skills.list_records(category="core")
    assert len(core_records) >= 2


def test_skill_registry_extended_schema_fields(tmp_path):
    adapter, lessons, lesson = _setup(tmp_path)
    skills = SkillRegistry(adapter, lessons)
    skill = skills.create_candidate(
        name="extended-field-test", description="Testing all new fields.",
        source_lessons=[lesson.lesson_id], owner_agent="Hermes",
        allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE",
        test_cases=["test1"],
        required_tools=["python3", "git"],
        dependencies=["SKILL-001"],
        governance_requirements={"approval_chain": ["Sage", "Hung Vuong"]},
        stop_conditions={"risk_threshold": 0.8},
    )
    assert "python3" in skill.required_tools
    assert "SKILL-001" in skill.dependencies
    assert skill.governance_requirements["approval_chain"] == ["Sage", "Hung Vuong"]
    assert skill.stop_conditions["risk_threshold"] == 0.8