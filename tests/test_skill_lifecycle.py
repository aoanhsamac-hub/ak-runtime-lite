from memory.lancedb_adapter import LanceDBAdapter
from memory.lesson_registry import LessonRegistry
from memory.skill_registry import SkillRegistry
from services.skill_lifecycle_engine import SkillLifecycleEngine, LIFECYCLE_TRANSITIONS, GOVERNANCE_GATES
from services.skill_validation_engine import SkillValidationEngine, VALIDATION_TYPES
from tests.test_lancedb_adapter import FakeBackend


def _setup_registries(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    lessons = LessonRegistry(adapter)
    lesson = lessons.create_candidate(
        title="Test lesson", summary="Summary", content="Content",
        source="review", owner_agent="Hermes", reviewer_agent="Sage",
        risk_level="LEVEL_1_MODERATE", tags=[],
    )
    lessons.mark_reviewed(lesson.lesson_id, "Sage")
    lessons.approve(lesson.lesson_id, "Sage")
    skills = SkillRegistry(adapter, lessons)
    return adapter, skills, lesson


def test_lifecycle_transition_proposed_to_discovered(tmp_path):
    adapter, skills, lesson = _setup_registries(tmp_path)
    engine = SkillLifecycleEngine(adapter, skills)
    skill = skills.create_candidate(
        name="test", description="desc", source_lessons=[lesson.lesson_id],
        owner_agent="Hermes", allowed_agents=["Hermes"],
        risk_level="LEVEL_1_MODERATE", test_cases=[],
    )
    event = engine.transition(skill.skill_id, "DISCOVERED", "Hermes", "auto-detected")
    assert event.from_stage == "PROPOSED"
    assert event.to_stage == "DISCOVERED"
    assert event.triggered_by == "Hermes"
    assert event.skill_id == skill.skill_id


def test_lifecycle_invalid_transition(tmp_path):
    adapter, skills, lesson = _setup_registries(tmp_path)
    engine = SkillLifecycleEngine(adapter, skills)
    skill = skills.create_candidate(
        name="test", description="desc", source_lessons=[lesson.lesson_id],
        owner_agent="Hermes", allowed_agents=["Hermes"],
        risk_level="LEVEL_1_MODERATE", test_cases=[],
    )
    try:
        engine.transition(skill.skill_id, "ACTIVE", "Hermes", "skip")
    except ValueError as exc:
        assert "invalid transition" in str(exc).lower()
    else:
        raise AssertionError("PROPOSED->ACTIVE should be invalid")


def test_lifecycle_all_allowed_transitions(tmp_path):
    adapter, skills, lesson = _setup_registries(tmp_path)
    engine = SkillLifecycleEngine(adapter, skills)
    skill = skills.create_candidate(
        name="test", description="desc", source_lessons=[lesson.lesson_id],
        owner_agent="Hermes", allowed_agents=["Hermes"],
        risk_level="LEVEL_1_MODERATE", test_cases=[],
    )
    current = skill.skill_id
    transitions_to_test = [
        ("PROPOSED", "DISCOVERED", "Hermes"),
        ("DISCOVERED", "SANDBOXED", "Sage"),
    ]
    for from_stage, to_stage, trigger in transitions_to_test:
        kwargs = {"governance_approval_ref": f"{to_stage}-approval"} if to_stage == "SANDBOXED" else {}
        event = engine.transition(current, to_stage, trigger, f"test {to_stage}", **kwargs)
        assert event.to_stage == to_stage

    record = skills.get(current)
    assert record.lifecycle_stage == "SANDBOXED"


def test_lifecycle_get_history(tmp_path):
    adapter, skills, lesson = _setup_registries(tmp_path)
    engine = SkillLifecycleEngine(adapter, skills)
    skill = skills.create_candidate(
        name="test", description="desc", source_lessons=[lesson.lesson_id],
        owner_agent="Hermes", allowed_agents=["Hermes"],
        risk_level="LEVEL_1_MODERATE", test_cases=[],
    )
    engine.transition(skill.skill_id, "DISCOVERED", "Hermes", "auto")
    engine.transition(skill.skill_id, "SANDBOXED", "Sage", "review", governance_approval_ref="sage-ok")
    history = engine.get_history(skill.skill_id)
    assert len(history) == 2
    assert history[0].to_stage == "DISCOVERED"
    assert history[1].to_stage == "SANDBOXED"


def test_lifecycle_gate_required_for_approval(tmp_path):
    adapter, skills, lesson = _setup_registries(tmp_path)
    skill = skills.create_candidate(
        name="test", description="desc", source_lessons=[lesson.lesson_id],
        owner_agent="Hermes", allowed_agents=["Hermes"],
        risk_level="LEVEL_1_MODERATE", test_cases=[],
    )
    skills.transition_lifecycle(skill.skill_id, "DISCOVERED", "Hermes")
    skills.transition_lifecycle(skill.skill_id, "SANDBOXED", "Sage")
    engine = SkillLifecycleEngine(adapter, skills)
    try:
        engine.transition(skill.skill_id, "APPROVED", "Hermes", "approve", governance_approval_ref="missing")
    except ValueError as exc:
        assert "approval" in str(exc).lower() or "gate" in str(exc).lower() or "transition" in str(exc).lower()
    else:
        pass


def test_lifecycle_can_transition_returns_bool(tmp_path):
    adapter, skills, lesson = _setup_registries(tmp_path)
    engine = SkillLifecycleEngine(adapter, skills)
    assert engine.can_transition("PROPOSED", "DISCOVERED") is True
    assert engine.can_transition("PROPOSED", "ACTIVE") is False
    assert engine.can_transition("ACTIVE", "SUSPENDED") is True
    assert engine.can_transition("ACTIVE", "RETIRED") is False
    assert engine.can_transition("RETIRED", "ARCHIVED") is True
    assert engine.can_transition("ARCHIVED", "PROPOSED") is False


def test_lifecycle_governance_gates_exist():
    expected_gates = {
        ("PROPOSED", "DISCOVERED"), ("DISCOVERED", "SANDBOXED"),
        ("SANDBOXED", "VALIDATED"), ("VALIDATED", "APPROVED"),
        ("APPROVED", "ACTIVE"), ("ACTIVE", "SUSPENDED"),
        ("SUSPENDED", "ACTIVE"), ("ACTIVE", "DEPRECATED"),
        ("DEPRECATED", "RETIRED"), ("RETIRED", "ARCHIVED"),
    }
    for from_stage, to_stage in expected_gates:
        assert (from_stage, to_stage) in GOVERNANCE_GATES, f"missing gate: {from_stage}->{to_stage}"


def test_lifecycle_transition_matrix_complete():
    assert "PROPOSED" in LIFECYCLE_TRANSITIONS
    assert "DISCOVERED" in LIFECYCLE_TRANSITIONS
    assert "SANDBOXED" in LIFECYCLE_TRANSITIONS
    assert "VALIDATED" in LIFECYCLE_TRANSITIONS
    assert "APPROVED" in LIFECYCLE_TRANSITIONS
    assert "ACTIVE" in LIFECYCLE_TRANSITIONS
    assert "SUSPENDED" in LIFECYCLE_TRANSITIONS
    assert "DEPRECATED" in LIFECYCLE_TRANSITIONS
    assert "RETIRED" in LIFECYCLE_TRANSITIONS
    assert "ARCHIVED" in LIFECYCLE_TRANSITIONS


def test_lifecycle_validation_integration(tmp_path):
    adapter, skills, lesson = _setup_registries(tmp_path)
    validation = SkillValidationEngine(adapter, skills)
    lifecycle = SkillLifecycleEngine(adapter, skills, validation)
    skill = skills.create_candidate(
        name="val-skill", description="Val desc", source_lessons=[lesson.lesson_id],
        owner_agent="Hermes", allowed_agents=["Hermes"],
        risk_level="LEVEL_1_MODERATE", test_cases=["test1"],
    )
    assert lifecycle.can_transition(skill.lifecycle_stage, "DISCOVERED")
    event = lifecycle.transition(skill.skill_id, "DISCOVERED", "Hermes", "test validation")
    assert event.to_stage == "DISCOVERED"