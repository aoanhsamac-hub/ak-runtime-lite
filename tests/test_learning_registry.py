from memory.learning_registry import (
    LearningSignalRecord,
    InsightRecord,
    CandidateSkillRecord,
    LearningSignalRegistry,
    InsightRegistry,
    CandidateSkillRegistry,
)


def test_learning_signal_record_creation():
    record = LearningSignalRecord(
        signal_type="PATTERN",
        source_kind="lesson",
        source_id="LKI-TEST",
        title="Test Pattern",
        content="Test content",
        owner_agent="Sage",
    )
    assert record.signal_id.startswith("LSIG-")
    assert record.signal_type == "PATTERN"
    assert record.source_kind == "lesson"
    assert record.source_id == "LKI-TEST"
    assert record.status == "CANDIDATE"
    assert record.version == 1
    assert record.source_hash != ""


def test_learning_signal_record_validates_type():
    try:
        LearningSignalRecord(
            signal_type="INVALID",
            source_kind="lesson",
            source_id="LKI-TEST",
            title="Test",
            content="Test",
            owner_agent="Sage",
        )
    except ValueError as exc:
        assert "invalid signal_type" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_learning_signal_record_to_dict():
    record = LearningSignalRecord(
        signal_type="ANOMALY",
        source_kind="trace",
        source_id="TRACE-1",
        title="Test Anomaly",
        content="Test",
        owner_agent="Janus",
    )
    d = record.to_dict()
    assert d["signal_type"] == "ANOMALY"
    assert d["signal_id"].startswith("LSIG-")


def test_insight_record_creation():
    record = InsightRecord(
        insight_type="PATTERN",
        title="Test Insight",
        description="A test insight",
        owner_agent="Sage",
    )
    assert record.insight_id.startswith("INS-")
    assert record.insight_type == "PATTERN"
    assert record.status == "CANDIDATE"


def test_insight_record_validates_type():
    try:
        InsightRecord(
            insight_type="INVALID",
            title="Test",
            description="Test",
            owner_agent="Sage",
        )
    except ValueError as exc:
        assert "invalid insight_type" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_candidate_skill_record_creation():
    record = CandidateSkillRecord(
        name="Test Skill",
        description="A test candidate skill",
        owner_agent="LangLieu",
    )
    assert record.candidate_skill_id.startswith("CSK-")
    assert record.status == "CANDIDATE"
    assert record.approval_status == "PENDING_REVIEW"
    assert record.activation_status == "DISABLED"


def test_candidate_skill_record_allows_valid_statuses():
    record = CandidateSkillRecord(
        name="Valid Skill",
        description="Should pass",
        owner_agent="Sage",
        status="ACTIVE",
    )
    assert record.status == "ACTIVE"
    assert record.approval_status == "PENDING_REVIEW"
    assert record.activation_status == "DISABLED"


def test_candidate_skill_registry_create_candidate_locks_status(candidate_skill_registry):
    record = candidate_skill_registry.create_candidate(
        name="Locked Skill",
        description="Should be locked",
        owner_agent="Sage",
    )
    assert record.status == "CANDIDATE"
    assert record.approval_status == "PENDING_REVIEW"
    assert record.activation_status == "DISABLED"


def test_candidate_skill_record_allows_all_activation_statuses():
    record = CandidateSkillRecord(
        name="Enabled Skill",
        description="Should pass",
        owner_agent="Sage",
        activation_status="ENABLED",
    )
    assert record.activation_status == "ENABLED"


def test_learning_signal_registry_create_and_get(signal_registry):
    record = signal_registry.create_candidate(
        signal_type="PATTERN",
        source_kind="lesson",
        source_id="LKI-1",
        title="Test",
        content="Content",
        owner_agent="Sage",
    )
    fetched = signal_registry.get(record.signal_id)
    assert fetched.signal_id == record.signal_id
    assert fetched.title == "Test"


def test_learning_signal_registry_list_all(signal_registry):
    signal_registry.create_candidate(
        signal_type="PATTERN", source_kind="lesson", source_id="LKI-1",
        title="P1", content="C1", owner_agent="Sage",
    )
    signal_registry.create_candidate(
        signal_type="ANOMALY", source_kind="trace", source_id="TR-1",
        title="A1", content="C2", owner_agent="Janus",
    )
    all_records = signal_registry.list_all()
    assert len(all_records) == 2
    patterns = signal_registry.list_all(signal_type="PATTERN")
    assert len(patterns) == 1
    janus_records = signal_registry.list_all(owner_agent="Janus")
    assert len(janus_records) == 1


def test_insight_registry_create_and_get(insight_registry):
    record = insight_registry.create_candidate(
        insight_type="TREND",
        title="Trend Insight",
        description="Test",
        owner_agent="Sage",
    )
    fetched = insight_registry.get(record.insight_id)
    assert fetched.insight_id == record.insight_id


def test_candidate_skill_registry_create_and_get(candidate_skill_registry):
    record = candidate_skill_registry.create_candidate(
        name="Test Skill",
        description="Test",
        owner_agent="Sage",
    )
    assert record.status == "CANDIDATE"
    assert record.approval_status == "PENDING_REVIEW"
    assert record.activation_status == "DISABLED"
    fetched = candidate_skill_registry.get(record.candidate_skill_id)
    assert fetched.name == "Test Skill"


def test_candidate_skill_registry_list_candidates(candidate_skill_registry):
    candidate_skill_registry.create_candidate(
        name="Skill A", description="Test", owner_agent="Sage",
    )
    candidate_skill_registry.create_candidate(
        name="Skill B", description="Test", owner_agent="Janus",
    )
    candidates = candidate_skill_registry.list_candidates()
    assert len(candidates) == 2
