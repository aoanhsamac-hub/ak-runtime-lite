from services.candidate_skill_pipeline import CandidateSkillPipeline


def test_create_from_insight(signal_registry, insight_registry_with_data, candidate_skill_registry):
    pipeline = CandidateSkillPipeline(signal_registry, insight_registry_with_data, candidate_skill_registry)
    insights = insight_registry_with_data.list_all()
    assert len(insights) >= 1
    skill = pipeline.create_from_insight(insights[0].insight_id, owner_agent="Sage")
    assert skill is not None
    assert skill.name.startswith("Skill:")
    assert skill.status == "CANDIDATE"
    assert skill.approval_status == "PENDING_REVIEW"
    assert skill.activation_status == "DISABLED"


def test_create_from_insight_with_custom_name(signal_registry, insight_registry_with_data, candidate_skill_registry):
    pipeline = CandidateSkillPipeline(signal_registry, insight_registry_with_data, candidate_skill_registry)
    insights = insight_registry_with_data.list_all()
    skill = pipeline.create_from_insight(
        insights[0].insight_id,
        name="Custom Skill",
        description="Custom description",
        owner_agent="Sage",
        test_cases=["test_1", "test_2"],
        allowed_agents=["Sage", "Janus"],
    )
    assert skill is not None
    assert skill.name == "Custom Skill"
    assert skill.test_cases == ["test_1", "test_2"]
    assert skill.allowed_agents == ["Sage", "Janus"]


def test_create_from_insight_returns_none_for_missing(signal_registry, insight_registry, candidate_skill_registry):
    pipeline = CandidateSkillPipeline(signal_registry, insight_registry, candidate_skill_registry)
    skill = pipeline.create_from_insight("INS-NONEXISTENT", owner_agent="Sage")
    assert skill is None


def test_batch_create_from_insights(signal_registry, insight_registry_with_data, candidate_skill_registry):
    pipeline = CandidateSkillPipeline(signal_registry, insight_registry_with_data, candidate_skill_registry)
    insights = insight_registry_with_data.list_all()
    ids = [i.insight_id for i in insights]
    skills = pipeline.batch_create_from_insights(ids, owner_agent="Sage")
    assert len(skills) == len(ids)
    for s in skills:
        assert s.status == "CANDIDATE"


def test_create_from_insight_type(signal_registry, insight_registry_with_data, candidate_skill_registry):
    pipeline = CandidateSkillPipeline(signal_registry, insight_registry_with_data, candidate_skill_registry)
    skills = pipeline.create_from_insight_type("PATTERN", owner_agent="Sage")
    assert len(skills) >= 1
    for s in skills:
        assert s.status == "CANDIDATE"


def test_run_all_creates_skills_from_all_insights(signal_registry, insight_registry_with_data, candidate_skill_registry):
    pipeline = CandidateSkillPipeline(signal_registry, insight_registry_with_data, candidate_skill_registry)
    skills = pipeline.run_all(owner_agent="Sage")
    assert len(skills) >= 1


def test_candidate_skill_locked_status(signal_registry, insight_registry_with_data, candidate_skill_registry):
    pipeline = CandidateSkillPipeline(signal_registry, insight_registry_with_data, candidate_skill_registry)
    skills = pipeline.run_all(owner_agent="Sage")
    for s in skills:
        assert s.status == "CANDIDATE"
        assert s.approval_status == "PENDING_REVIEW"
        assert s.activation_status == "DISABLED"


def test_candidate_skill_has_traceability(signal_registry, insight_registry_with_data, candidate_skill_registry):
    pipeline = CandidateSkillPipeline(signal_registry, insight_registry_with_data, candidate_skill_registry)
    skills = pipeline.run_all(owner_agent="Sage")
    for s in skills:
        assert len(s.source_insight_ids) > 0
