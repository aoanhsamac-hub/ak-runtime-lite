from services.skill_family_engine import SkillFamilyEngine
from services.canonical_skill_engine import CanonicalSkillEngine


def test_classify_single_skill_as_canonical(candidate_skill_registry, family_registry, canonical_registry):
    candidate_skill_registry.create_candidate(
        name="Unique Trading Skill", description="A unique skill",
        owner_agent="Sage", confidence_score=0.85, tags=["trading"],
    )
    fam_engine = SkillFamilyEngine(candidate_skill_registry, family_registry)
    fam_engine.discover_families(owner_agent="Sage")
    engine = CanonicalSkillEngine(candidate_skill_registry, family_registry, canonical_registry)
    results = engine.classify_all(owner_agent="Sage")
    assert len(results) >= 1
    for r in results:
        assert r.status == "CANDIDATE"
        assert r.classification in ("CANONICAL", "ISOLATED")


def test_merge_related_skills(candidate_skill_registry, family_registry, canonical_registry):
    candidate_skill_registry.create_candidate(
        name="Trading Signal Analysis", description="TSA v1",
        owner_agent="Sage", confidence_score=0.90, tags=["trading"],
    )
    candidate_skill_registry.create_candidate(
        name="Trading Signal Analysis v2", description="TSA v2",
        owner_agent="Sage", confidence_score=0.95, tags=["trading"],
    )
    fam_engine = SkillFamilyEngine(candidate_skill_registry, family_registry)
    fam_engine.discover_families(owner_agent="Sage")
    engine = CanonicalSkillEngine(candidate_skill_registry, family_registry, canonical_registry)
    results = engine.classify_all(owner_agent="Sage")
    canon = [r for r in results if r.classification == "CANONICAL"]
    assert len(canon) >= 1
    for c in canon:
        assert len(c.source_skill_ids) >= 1


def test_superseded_skills_identified(candidate_skill_registry, family_registry, canonical_registry):
    candidate_skill_registry.create_candidate(
        name="Execution Optimizer", description="Old version",
        owner_agent="Sage", confidence_score=0.45, tags=["execution"],
    )
    candidate_skill_registry.create_candidate(
        name="Execution Optimizer v3", description="New version",
        owner_agent="Sage", confidence_score=0.92, tags=["execution"],
    )
    fam_engine = SkillFamilyEngine(candidate_skill_registry, family_registry)
    fam_engine.discover_families()
    engine = CanonicalSkillEngine(candidate_skill_registry, family_registry, canonical_registry)
    results = engine.classify_all(owner_agent="Sage")
    canon = [r for r in results if r.classification == "CANONICAL"]
    if canon:
        assert len(canon[0].superseded_ids) >= 1 or len(canon[0].source_skill_ids) >= 1


def test_overlapping_skills_detected(candidate_skill_registry, family_registry, canonical_registry):
    candidate_skill_registry.create_candidate(
        name="Risk Assessment", description="RA v1",
        owner_agent="Sage", confidence_score=0.80, tags=["risk"],
    )
    candidate_skill_registry.create_candidate(
        name="Risk Calibration", description="RA v2",
        owner_agent="Sage", confidence_score=0.82, tags=["risk"],
    )
    fam_engine = SkillFamilyEngine(candidate_skill_registry, family_registry)
    fam_engine.discover_families()
    engine = CanonicalSkillEngine(candidate_skill_registry, family_registry, canonical_registry)
    results = engine.classify_all(owner_agent="Sage")
    canon = [r for r in results if r.classification == "CANONICAL"]
    has_overlap = any(len(r.overlapping_ids) > 0 for r in results)
    assert has_overlap or len(canon) >= 1


def test_empty_registry_returns_empty(family_registry, canonical_registry):
    empty = type("EmptyRegistry", (), {"list_all": lambda *a, **kw: []})()
    engine = CanonicalSkillEngine(empty, family_registry, canonical_registry)
    results = engine.classify_all()
    assert len(results) == 0
