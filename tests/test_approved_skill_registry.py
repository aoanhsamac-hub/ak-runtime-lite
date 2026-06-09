from memory.learning_registry.schemas import ApprovedSkillRecord, PROMOTION_DECISIONS


def test_approve_creates_record(approved_skill_registry):
    rec = approved_skill_registry.approve(
        name="Test Approved Skill",
        description="A test approved skill",
        canonical_id="CANON-1",
        candidate_skill_id="CSK-1",
        family_id="SFAM-1",
        owner_agent="Sage",
        reviewer_agent="Hung Vuong",
        approval_authority="Hung Vuong",
        confidence_score=0.85,
        evidence={"source": "test"},
        tags=["test", "approved"],
    )
    assert rec.approved_skill_id.startswith("APSK")
    assert rec.status == "ACTIVE"
    assert rec.name == "Test Approved Skill"


def test_get_approved_skill(approved_skill_registry):
    rec = approved_skill_registry.approve(
        name="Get Test", description="Test",
        canonical_id="CANON-1", candidate_skill_id="CSK-1",
        owner_agent="Sage", approval_authority="Hung Vuong",
        confidence_score=0.80,
    )
    fetched = approved_skill_registry.get(rec.approved_skill_id)
    assert fetched.name == "Get Test"


def test_list_all(approved_skill_registry):
    approved_skill_registry.approve(
        name="A1", description="D1",
        canonical_id="C1", candidate_skill_id="CSK-1",
        owner_agent="Sage", approval_authority="Hung Vuong",
        confidence_score=0.80,
    )
    approved_skill_registry.approve(
        name="A2", description="D2",
        canonical_id="C2", candidate_skill_id="CSK-2",
        owner_agent="Sage", approval_authority="Hung Vuong",
        confidence_score=0.90,
    )
    all_recs = approved_skill_registry.list_all()
    assert len(all_recs) == 2


def test_list_by_status(approved_skill_registry):
    approved_skill_registry.approve(
        name="Active Skill", description="D",
        canonical_id="C1", candidate_skill_id="CSK-1",
        owner_agent="Sage", approval_authority="Hung Vuong",
        confidence_score=0.80, status="ACTIVE",
    )
    active = approved_skill_registry.list_all(status="ACTIVE")
    assert len(active) == 1


def test_export_jsonl(approved_skill_registry):
    approved_skill_registry.approve(
        name="Export Test", description="D",
        canonical_id="C1", candidate_skill_id="CSK-1",
        owner_agent="Sage", approval_authority="Hung Vuong",
        confidence_score=0.80,
    )
    exported = approved_skill_registry.export_jsonl()
    assert len(exported) == 1
    assert "approved_skill_id" in exported[0]


def test_requires_required_fields():
    import pytest
    with pytest.raises((ValueError, TypeError)):
        ApprovedSkillRecord(name="", description="", owner_agent="", approval_authority="")


def test_promotion_decision_set():
    assert "APPROVED" in PROMOTION_DECISIONS
    assert "REJECTED" in PROMOTION_DECISIONS
    assert "NEEDS_REVIEW" in PROMOTION_DECISIONS
    assert "NEEDS_EVIDENCE" in PROMOTION_DECISIONS
    assert "ARCHIVED" in PROMOTION_DECISIONS
