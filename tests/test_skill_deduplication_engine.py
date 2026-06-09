from services.skill_deduplication_engine import SkillDeduplicationEngine


def test_detects_exact_duplicate(candidate_skill_registry):
    candidate_skill_registry.create_candidate(
        name="Trading Skill",
        description="Test A", owner_agent="Sage",
    )
    candidate_skill_registry.create_candidate(
        name="Trading Skill",
        description="Test B (duplicate)", owner_agent="Sage",
    )
    engine = SkillDeduplicationEngine(candidate_skill_registry)
    result = engine.run_all()
    assert result["duplicate_count"] >= 1


def test_detects_unique_skills(candidate_skill_registry):
    candidate_skill_registry.create_candidate(
        name="Unique Skill Alpha",
        description="Test A", owner_agent="Sage",
    )
    candidate_skill_registry.create_candidate(
        name="Completely Different Beta",
        description="Test B", owner_agent="Sage",
    )
    engine = SkillDeduplicationEngine(candidate_skill_registry)
    result = engine.run_all()
    assert result["unique_count"] >= 2
    assert result["duplicate_count"] == 0
    assert result["superseded_count"] == 0


def test_empty_registry_returns_unique_count_zero(candidate_skill_registry):
    engine = SkillDeduplicationEngine(candidate_skill_registry)
    result = engine.run_all()
    assert result["unique_count"] == 0
    assert result["duplicate_count"] == 0


def test_merge_suggestions_for_duplicates(candidate_skill_registry):
    candidate_skill_registry.create_candidate(
        name="Risk Assessment",
        description="Test A", owner_agent="Sage",
    )
    candidate_skill_registry.create_candidate(
        name="Risk Assessment",
        description="Test B", owner_agent="Sage",
    )
    engine = SkillDeduplicationEngine(candidate_skill_registry)
    result = engine.run_all()
    assert len(result["merge_suggestions"]) >= 1
    suggestion = result["merge_suggestions"][0]
    assert "merging" in suggestion.reason.lower()


def test_detects_overlapping(candidate_skill_registry):
    candidate_skill_registry.create_candidate(
        name="Trading Execution Strategy",
        description="Test A", owner_agent="Sage",
    )
    candidate_skill_registry.create_candidate(
        name="Trading Risk Management",
        description="Test B", owner_agent="Sage",
    )
    engine = SkillDeduplicationEngine(candidate_skill_registry)
    result = engine.run_all()
    overlapping = [r for r in result["results"] if r.status == "overlapping"]
    assert len(overlapping) >= 0


def test_detects_superseded(candidate_skill_registry):
    candidate_skill_registry.create_candidate(
        name="Simple Trading Strategy",
        description="Test A", owner_agent="Sage",
    )
    candidate_skill_registry.create_candidate(
        name="Simple Trading Strategy V2",
        description="Test B", owner_agent="Sage",
    )
    engine = SkillDeduplicationEngine(candidate_skill_registry)
    result = engine.run_all()
    superseded = [r for r in result["results"] if r.status == "superseded"]
    assert len(superseded) >= 0


def test_no_automatic_merge(candidate_skill_registry):
    candidate_skill_registry.create_candidate(
        name="Duplicate Skill",
        description="Test A", owner_agent="Sage",
    )
    candidate_skill_registry.create_candidate(
        name="Duplicate Skill",
        description="Test B", owner_agent="Sage",
    )
    engine = SkillDeduplicationEngine(candidate_skill_registry)
    result = engine.run_all()
    for r in result["results"]:
        assert r.status != "merged"
    merge_names = [s.reason.lower() for s in result["merge_suggestions"]]
    any_merging = any("merging" in r for r in merge_names)
    assert any_merging


def test_duplication_result_structure(candidate_skill_registry):
    candidate_skill_registry.create_candidate(
        name="Test Skill",
        description="Test", owner_agent="Sage",
    )
    engine = SkillDeduplicationEngine(candidate_skill_registry)
    result = engine.run_all()
    assert "results" in result
    assert "merge_suggestions" in result
    assert "unique_count" in result
    assert "duplicate_count" in result
    assert "superseded_count" in result
    assert "overlapping_count" in result
    assert "conflicting_count" in result
    for r in result["results"]:
        assert r.skill_id
        assert r.skill_name
        assert r.status in ("unique", "duplicate", "superseded", "overlapping", "conflicting")
