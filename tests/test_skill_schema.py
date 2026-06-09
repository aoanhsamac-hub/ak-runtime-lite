from memory.schemas.records import SkillRecord, SKILL_LIFECYCLE_STAGES, SKILL_CATEGORIES, SKILL_SOURCES


def test_skill_record_requires_name():
    try:
        SkillRecord(name="", description="desc", source_lessons=["L1"], owner_agent="Hermes",
                     allowed_agents=["Hermes"], risk_level="LEVEL_1_MODERATE", test_cases=[])
    except ValueError as exc:
        assert "required" in str(exc).lower()
    else:
        raise AssertionError("empty name should fail")


def test_skill_record_valid_lifecycle_stage():
    record = SkillRecord(name="test", description="desc", source_lessons=["L1"],
                          owner_agent="Hermes", allowed_agents=["Hermes"],
                          risk_level="LEVEL_1_MODERATE", test_cases=[],
                          lifecycle_stage="PROPOSED")
    assert record.lifecycle_stage == "PROPOSED"
    assert record.status == "DRAFT"


def test_skill_record_invalid_lifecycle_stage():
    try:
        SkillRecord(name="test", description="desc", source_lessons=["L1"],
                     owner_agent="Hermes", allowed_agents=["Hermes"],
                     risk_level="LEVEL_1_MODERATE", test_cases=[],
                     lifecycle_stage="INVALID")
    except ValueError as exc:
        assert "lifecycle_stage" in str(exc).lower()
    else:
        raise AssertionError("invalid lifecycle_stage should fail")


def test_skill_record_valid_category():
    for cat in SKILL_CATEGORIES:
        record = SkillRecord(name="test", description="desc", source_lessons=["L1"],
                              owner_agent="Hermes", allowed_agents=["Hermes"],
                              risk_level="LEVEL_1_MODERATE", test_cases=[],
                              category=cat)
        assert record.category == cat


def test_skill_record_valid_source():
    for src in SKILL_SOURCES:
        record = SkillRecord(name="test", description="desc", source_lessons=["L1"],
                              owner_agent="Hermes", allowed_agents=["Hermes"],
                              risk_level="LEVEL_1_MODERATE", test_cases=[],
                              source=src)
        assert record.source == src


def test_skill_record_forbidden_owner():
    try:
        SkillRecord(name="test", description="desc", source_lessons=["L1"],
                     owner_agent="Hermes", allowed_agents=["Hermes"],
                     risk_level="LEVEL_1_MODERATE", test_cases=[],
                     forbidden_users=["Hermes"])
    except ValueError as exc:
        assert "forbidden" in str(exc).lower()
    else:
        raise AssertionError("owner in forbidden_users should fail")


def test_skill_record_forbidden_primary():
    try:
        SkillRecord(name="test", description="desc", source_lessons=["L1"],
                     owner_agent="Hermes", allowed_agents=["Hermes", "Sage"],
                     risk_level="LEVEL_1_MODERATE", test_cases=[],
                     primary_users=["Sage"], forbidden_users=["Sage"])
    except ValueError as exc:
        assert "forbidden" in str(exc).lower()
    else:
        raise AssertionError("primary in forbidden_users should fail")


def test_skill_record_with_lifecycle_stage():
    record = SkillRecord(name="test", description="desc", source_lessons=["L1"],
                          owner_agent="Hermes", allowed_agents=["Hermes"],
                          risk_level="LEVEL_1_MODERATE", test_cases=[])
    assert record.lifecycle_stage == "PROPOSED"
    updated = record.with_lifecycle_stage("SANDBOXED", "Sage")
    assert updated.lifecycle_stage == "SANDBOXED"
    assert updated.version == record.version + 1


def test_skill_record_with_version():
    record = SkillRecord(name="test", description="desc", source_lessons=["L1"],
                          owner_agent="Hermes", allowed_agents=["Hermes"],
                          risk_level="LEVEL_1_MODERATE", test_cases=[])
    updated = record.with_version(name="new-name", risk_level="LEVEL_2_HIGH")
    assert updated.name == "new-name"
    assert updated.risk_level == "LEVEL_2_HIGH"
    assert updated.version == record.version + 1


def test_skill_record_dependency_updates():
    record = SkillRecord(name="test", description="desc", source_lessons=["L1"],
                          owner_agent="Hermes", allowed_agents=["Hermes"],
                          risk_level="LEVEL_1_MODERATE", test_cases=[])
    updated = record.with_version(dependencies=["SKILL-001", "SKILL-002"])
    assert "SKILL-001" in updated.dependencies
    assert len(updated.dependencies) == 2
    assert updated.version == 2


def test_skill_record_to_dict():
    record = SkillRecord(name="test", description="desc", source_lessons=["L1"],
                          owner_agent="Hermes", allowed_agents=["Hermes"],
                          risk_level="LEVEL_1_MODERATE", test_cases=[],
                          required_tools=["python3"], dependencies=["SKILL-001"])
    d = record.to_dict()
    assert d["name"] == "test"
    assert d["required_tools"] == ["python3"]
    assert d["dependencies"] == ["SKILL-001"]
    assert "audit_requirements" in d
    assert "governance_requirements" in d
    assert "stop_conditions" in d
    assert "retirement_conditions" in d
    assert d["lifecycle_stage"] == "PROPOSED"
    assert d["source"] == "internal"
    assert d["category"] == "core"


def test_skill_record_all_lifecycle_stages():
    for stage in SKILL_LIFECYCLE_STAGES:
        record = SkillRecord(name="test", description="desc", source_lessons=["L1"],
                              owner_agent="Hermes", allowed_agents=["Hermes"],
                              risk_level="LEVEL_1_MODERATE", test_cases=[],
                              lifecycle_stage=stage)
        assert record.lifecycle_stage == stage
        assert record.status == "DRAFT"


def test_skill_record_primary_secondary_from_allowed():
    record = SkillRecord(name="test", description="desc", source_lessons=["L1"],
                          owner_agent="Hermes", allowed_agents=["Hermes", "Sage", "LangLieu"],
                          risk_level="LEVEL_1_MODERATE", test_cases=[],
                          primary_users=[], secondary_users=[])
    # post_init should auto-derive from allowed_agents
    assert "Hermes" in record.primary_users or len(record.primary_users) > 0


def test_skill_record_hermes_source():
    record = SkillRecord(name="test", description="desc", source_lessons=["L1"],
                          owner_agent="Hermes", allowed_agents=["Hermes", "Sage"],
                          risk_level="LEVEL_1_MODERATE", test_cases=[],
                          source="hermes", category="imported")
    assert record.source == "hermes"
    assert record.category == "imported"