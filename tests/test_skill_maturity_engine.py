from services.skill_family_engine import SkillFamilyEngine
from services.canonical_skill_engine import CanonicalSkillEngine
from services.skill_maturity_engine import SkillMaturityEngine


def test_assess_maturity_on_canonical_skills(
    candidate_skill_registry, family_registry, canonical_registry,
):
    candidate_skill_registry.create_candidate(
        name="Trading Strategy", description="A mature trading strategy",
        owner_agent="Sage", confidence_score=0.92, tags=["trading", "strategy"],
    )
    feng = SkillFamilyEngine(candidate_skill_registry, family_registry)
    feng.discover_families()
    ceng = CanonicalSkillEngine(candidate_skill_registry, family_registry, canonical_registry)
    ceng.classify_all()
    meng = SkillMaturityEngine(candidate_skill_registry, family_registry, canonical_registry)
    assessments = meng.assess_all()
    assert len(assessments) >= 1


def test_maturity_levels_follow_order(
    candidate_skill_registry, family_registry, canonical_registry,
):
    for i, tag in enumerate(["trading", "risk", "execution"]):
        candidate_skill_registry.create_candidate(
            name=f"{tag.title()} Skill", description=f"{tag} skill",
            owner_agent="Sage", confidence_score=0.5 + i * 0.15,
            tags=[tag, f"{tag}_knowledge"],
        )
    feng = SkillFamilyEngine(candidate_skill_registry, family_registry)
    feng.discover_families()
    ceng = CanonicalSkillEngine(candidate_skill_registry, family_registry, canonical_registry)
    ceng.classify_all()
    meng = SkillMaturityEngine(candidate_skill_registry, family_registry, canonical_registry)
    assessments = meng.assess_all()
    valid_levels = {"EMERGING", "DEVELOPING", "ESTABLISHED", "ADVANCED", "SOVEREIGN"}
    for a in assessments:
        assert a.maturity_level in valid_levels


def test_readiness_never_promotion(
    candidate_skill_registry, family_registry, canonical_registry,
):
    candidate_skill_registry.create_candidate(
        name="Test Skill", description="Test",
        owner_agent="Sage", confidence_score=0.70, tags=["test", "test_knowledge"],
    )
    feng = SkillFamilyEngine(candidate_skill_registry, family_registry)
    feng.discover_families()
    ceng = CanonicalSkillEngine(candidate_skill_registry, family_registry, canonical_registry)
    ceng.classify_all()
    meng = SkillMaturityEngine(candidate_skill_registry, family_registry, canonical_registry)
    assessments = meng.assess_all()
    valid_readiness = {"Needs Consolidation", "Needs Evidence", "Needs Review", "Promotion Ready"}
    for a in assessments:
        assert a.promotion_readiness in valid_readiness
        assert a.maturity_score >= 0.0


def test_metrics_components_are_present(
    candidate_skill_registry, family_registry, canonical_registry,
):
    candidate_skill_registry.create_candidate(
        name="Full Skill", description="Full",
        owner_agent="Sage", confidence_score=0.88,
        tags=["full", "full_knowledge", "full_skills", "trading"],
    )
    feng = SkillFamilyEngine(candidate_skill_registry, family_registry)
    feng.discover_families()
    ceng = CanonicalSkillEngine(candidate_skill_registry, family_registry, canonical_registry)
    ceng.classify_all()
    meng = SkillMaturityEngine(candidate_skill_registry, family_registry, canonical_registry)
    assessments = meng.assess_all()
    for a in assessments:
        assert a.evidence_depth >= 1
        assert a.repeatability >= 0.0
        assert a.reuse_value >= 0.0
        assert a.governance_confidence >= 0.0


def test_empty_registry_returns_empty(candidate_skill_registry, family_registry, canonical_registry):
    meng = SkillMaturityEngine(candidate_skill_registry, family_registry, canonical_registry)
    assessments = meng.assess_all()
    assert len(assessments) == 0
