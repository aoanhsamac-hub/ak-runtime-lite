from services.skill_promotion_engine import SkillPromotionEngine
from services.learning_audit_layer import LearningAuditLayer


def test_promote_approved_skill(candidate_skill_registry, canonical_registry,
                                 approved_skill_registry):
    audit = LearningAuditLayer()
    csk = candidate_skill_registry.create_candidate(
        name="Approved Trading Skill", description="Test",
        owner_agent="Sage", confidence_score=0.85,
        tags=["trading"], evidence={"source": "test", "count": 3},
        source_signal_ids=["LSIG-1"],
    )
    rec = canonical_registry.create_canonical(
        name="Approved Trading Skill", description="Test",
        classification="CANONICAL", source_skill_ids=[csk.candidate_skill_id],
        family_id="SFAM-1", confidence_score=0.85,
        evidence={"source": "test", "count": 3},
        owner_agent="Sage", tags=["trading"],
        metadata={},
    )
    engine = SkillPromotionEngine(candidate_skill_registry, canonical_registry,
                                   approved_skill_registry, audit)
    result = engine.promote(rec.canonical_id, recommender="Hermes", reviewer="Hung Vuong")
    assert result["decision"] == "APPROVED"
    assert result["skill_id"] == rec.canonical_id
    assert result["reviewer"] == "Hung Vuong"


def test_needs_review_via_governance(candidate_skill_registry, canonical_registry,
                                      approved_skill_registry):
    audit = LearningAuditLayer()
    rec = canonical_registry.create_canonical(
        name="Bad Skill", description="Test",
        classification="ISOLATED", source_skill_ids=["CSK-1"],
        confidence_score=0.30, evidence={},
        owner_agent="Sage",
    )
    engine = SkillPromotionEngine(candidate_skill_registry, canonical_registry,
                                   approved_skill_registry, audit)
    result = engine.promote(rec.canonical_id)
    assert result["decision"] != "APPROVED"


def test_decision_creates_approved_record(candidate_skill_registry, canonical_registry,
                                           approved_skill_registry):
    audit = LearningAuditLayer()
    csk = candidate_skill_registry.create_candidate(
        name="Promotable Skill", description="Test",
        owner_agent="Sage", confidence_score=0.90,
        tags=["test"], evidence={"a": 1, "b": 2},
        source_signal_ids=["LSIG-1"],
    )
    rec = canonical_registry.create_canonical(
        name="Promotable Skill", description="Test",
        classification="CANONICAL", source_skill_ids=[csk.candidate_skill_id],
        family_id="SFAM-1", confidence_score=0.90,
        evidence={"a": 1, "b": 2},
        owner_agent="Sage", tags=["test"],
        metadata={},
    )
    engine = SkillPromotionEngine(candidate_skill_registry, canonical_registry,
                                   approved_skill_registry, audit)
    engine.promote(rec.canonical_id, recommender="Hermes", reviewer="Hung Vuong")
    approved = approved_skill_registry.list_all()
    assert len(approved) >= 1
    assert approved[0].canonical_id == rec.canonical_id


def test_promote_batch(candidate_skill_registry, canonical_registry,
                        approved_skill_registry):
    audit = LearningAuditLayer()
    cids = []
    for i in range(3):
        csk = candidate_skill_registry.create_candidate(
            name=f"Batch Skill {i}", description="Test",
            owner_agent="Sage", confidence_score=0.80 + i * 0.05,
            tags=["batch"], evidence={"s": "t", "c": i},
            source_signal_ids=[f"LSIG-B{i}"],
        )
        rec = canonical_registry.create_canonical(
            name=f"Batch Skill {i}", description="Test",
            classification="CANONICAL",
            source_skill_ids=[csk.candidate_skill_id],
            family_id="SFAM-1", confidence_score=0.80 + i * 0.05,
            evidence={"s": "t", "c": i},
            owner_agent="Sage", tags=["batch"],
            metadata={},
        )
        cids.append(rec.canonical_id)
    engine = SkillPromotionEngine(candidate_skill_registry, canonical_registry,
                                   approved_skill_registry, audit)
    results = engine.promote_batch(cids, recommender="Hermes", reviewer="Hung Vuong")
    assert len(results) == 3


def test_audit_trail_on_promotion(candidate_skill_registry, canonical_registry,
                                   approved_skill_registry):
    audit = LearningAuditLayer()
    csk = candidate_skill_registry.create_candidate(
        name="Audit Skill", description="Test",
        owner_agent="Sage", confidence_score=0.85,
        tags=["audit"], evidence={"src": "t", "cnt": 3},
        source_signal_ids=["LSIG-A1"],
    )
    rec = canonical_registry.create_canonical(
        name="Audit Skill", description="Test",
        classification="CANONICAL", source_skill_ids=[csk.candidate_skill_id],
        family_id="SFAM-1", confidence_score=0.85,
        evidence={"src": "t", "cnt": 3},
        owner_agent="Sage", tags=["audit"],
        metadata={},
    )
    engine = SkillPromotionEngine(candidate_skill_registry, canonical_registry,
                                   approved_skill_registry, audit)
    engine.promote(rec.canonical_id, recommender="Hermes", reviewer="Hung Vuong")
    events = audit.list_events()
    actions = [e.action for e in events]
    assert "SKILL_APPROVED" in actions
    assert "SKILL_PROMOTION_DECISION" in actions


def test_nonexistent_canonical(candidate_skill_registry, canonical_registry,
                                approved_skill_registry):
    audit = LearningAuditLayer()
    engine = SkillPromotionEngine(candidate_skill_registry, canonical_registry,
                                   approved_skill_registry, audit)
    result = engine.promote("DOES_NOT_EXIST")
    assert "error" in result
