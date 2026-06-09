from memory.lancedb_adapter import LanceDBAdapter
from memory.lesson_registry import LessonRegistry
from memory.skill_registry import SkillRegistry
from services.skill_validation_engine import SkillValidationEngine, VALIDATION_TYPES
from tests.test_lancedb_adapter import FakeBackend


def _setup_skill(tmp_path, **overrides):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    lessons = LessonRegistry(adapter)
    lesson = lessons.create_candidate(
        title="Approved lesson", summary="Summary", content="Content",
        source="review", owner_agent="Hermes", reviewer_agent="Sage",
        risk_level="LEVEL_1_MODERATE", tags=[],
    )
    lessons.mark_reviewed(lesson.lesson_id, "Sage")
    lessons.approve(lesson.lesson_id, "Sage")
    skills = SkillRegistry(adapter, lessons)
    params = dict(
        name="test-skill", description="Test description",
        source_lessons=[lesson.lesson_id], owner_agent="Hermes",
        allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE",
        test_cases=["test1"],
        stop_conditions={"risk_threshold": 0.9},
        governance_requirements={"approval_chain": ["Sage", "Hung Vuong"]},
        audit_requirements={"audit_level": "standard", "retention_days": 365},
    )
    params.update(overrides)
    skill = skills.create_candidate(**params)
    return adapter, skills, skill


def test_validation_unit_passes(tmp_path):
    adapter, skills, skill = _setup_skill(tmp_path)
    engine = SkillValidationEngine(adapter, skills)
    result = engine._unit_validation(skill)
    assert result.passed is True
    assert result.validation_type == "unit"


def test_validation_unit_fails_on_invalid_lifecycle_stage(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    lessons = LessonRegistry(adapter)
    lesson = lessons.create_candidate(
        title="L", summary="S", content="C", source="review",
        owner_agent="Hermes", reviewer_agent="Sage",
        risk_level="LEVEL_1_MODERATE", tags=[],
    )
    lessons.mark_reviewed(lesson.lesson_id, "Sage")
    lessons.approve(lesson.lesson_id, "Sage")
    skills = SkillRegistry(adapter, lessons)
    try:
        skills.create_candidate(
            name="validation-test", description="Test.",
            source_lessons=[lesson.lesson_id], owner_agent="Hermes",
            allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE", test_cases=[],
            lifecycle_stage="INVALID",
        )
    except ValueError as exc:
        assert "lifecycle_stage" in str(exc).lower()
    else:
        raise AssertionError("invalid lifecycle_stage should fail during creation")


def test_validation_integration_passes(tmp_path):
    adapter, skills, skill = _setup_skill(tmp_path)
    engine = SkillValidationEngine(adapter, skills)
    result = engine._integration_validation(skill)
    assert result.passed is True


def test_validation_risk_passes(tmp_path):
    adapter, skills, skill = _setup_skill(tmp_path)
    engine = SkillValidationEngine(adapter, skills)
    result = engine._risk_validation(skill)
    assert result.passed is True


def test_validation_risk_fails_without_stop_conditions(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    lessons = LessonRegistry(adapter)
    lesson = lessons.create_candidate(
        title="L", summary="S", content="C", source="review",
        owner_agent="Hermes", reviewer_agent="Sage",
        risk_level="LEVEL_1_MODERATE", tags=[],
    )
    lessons.mark_reviewed(lesson.lesson_id, "Sage")
    lessons.approve(lesson.lesson_id, "Sage")
    skills = SkillRegistry(adapter, lessons)
    skill = skills.create_candidate(
        name="risk-test", description="Risk test.",
        source_lessons=[lesson.lesson_id], owner_agent="Hermes",
        allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE", test_cases=[],
        stop_conditions={},
    )
    engine = SkillValidationEngine(adapter, skills)
    result = engine._risk_validation(skill)
    assert result.passed is False


def test_validation_governance_passes(tmp_path):
    adapter, skills, skill = _setup_skill(tmp_path)
    engine = SkillValidationEngine(adapter, skills)
    result = engine._governance_validation(skill)
    assert result.passed is True


def test_validation_performance_passes(tmp_path):
    adapter, skills, skill = _setup_skill(tmp_path)
    engine = SkillValidationEngine(adapter, skills)
    result = engine._performance_validation(skill)
    assert result.passed is True


def test_validation_audit_passes(tmp_path):
    adapter, skills, skill = _setup_skill(tmp_path)
    engine = SkillValidationEngine(adapter, skills)
    result = engine._audit_validation(skill)
    assert result.passed is True


def test_validation_audit_fails_without_audit_requirements(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    lessons = LessonRegistry(adapter)
    lesson = lessons.create_candidate(
        title="L", summary="S", content="C", source="review",
        owner_agent="Hermes", reviewer_agent="Sage",
        risk_level="LEVEL_1_MODERATE", tags=[],
    )
    lessons.mark_reviewed(lesson.lesson_id, "Sage")
    lessons.approve(lesson.lesson_id, "Sage")
    skills = SkillRegistry(adapter, lessons)
    skill = skills.create_candidate(
        name="audit-test", description="Audit test.",
        source_lessons=[lesson.lesson_id], owner_agent="Hermes",
        allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE", test_cases=[],
        audit_requirements={},
    )
    engine = SkillValidationEngine(adapter, skills)
    result = engine._audit_validation(skill)
    assert result.passed is False


def test_validation_full_validate(tmp_path):
    adapter, skills, skill = _setup_skill(tmp_path)
    engine = SkillValidationEngine(adapter, skills)
    result = engine.validate_skill(skill.skill_id)
    assert result.passed is True
    assert result.validation_type == "full"
    assert result.score >= 0


def test_validation_report(tmp_path):
    adapter, skills, skill = _setup_skill(tmp_path)
    engine = SkillValidationEngine(adapter, skills)
    report = engine.report(skill.skill_id)
    assert report["skill_id"] == skill.skill_id
    assert "passed" in report
    assert "score" in report
    assert "validated_at" in report


def test_validation_types_enum():
    assert "unit" in VALIDATION_TYPES
    assert "integration" in VALIDATION_TYPES
    assert "governance" in VALIDATION_TYPES
    assert "risk" in VALIDATION_TYPES
    assert "performance" in VALIDATION_TYPES
    assert "audit" in VALIDATION_TYPES
    assert len(VALIDATION_TYPES) == 6


def test_validation_forbidden_owner_governance_fails(tmp_path):
    adapter, skills, skill = _setup_skill(tmp_path)
    skills.update_ownership(skill.skill_id, forbidden_users=["YetKieu"])
    skill2 = skills.get(skill.skill_id)
    engine = SkillValidationEngine(adapter, skills)
    result = engine._governance_validation(skill2)
    assert result.passed is True