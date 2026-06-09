import pytest

from memory.learning_registry import (
    LearningSignalRegistry,
    InsightRegistry,
    CandidateSkillRegistry,
    SignalClusterRegistry,
    SkillFamilyRegistry,
    CanonicalSkillRegistry,
    ApprovedSkillRegistry,
)
from memory.capability_pipeline import (
    CapabilityCandidateRegistry,
    CapabilityFamilyRegistry,
    CanonicalCapabilityRegistry,
    PromotionRecommendationRegistry,
)
from memory.capability_registry import (
    CapabilityEvidenceRegistry,
    OfficialCapabilityRegistry,
)
from memory.adoption_registry import CapabilityAdoptionRegistry


@pytest.fixture
def signal_registry():
    return LearningSignalRegistry()


@pytest.fixture
def insight_registry():
    return InsightRegistry()


@pytest.fixture
def candidate_skill_registry():
    return CandidateSkillRegistry()


@pytest.fixture
def cluster_registry():
    return SignalClusterRegistry()


@pytest.fixture
def signal_registry_with_data(signal_registry):
    signal_registry.create_candidate(
        signal_type="PATTERN", source_kind="lesson", source_id="LKI-1",
        title="Pattern 1", content="Content 1", owner_agent="Sage",
        confidence_score=0.85,
        tags=["lesson", "pattern"],
    )
    signal_registry.create_candidate(
        signal_type="ANOMALY", source_kind="trace", source_id="TR-1",
        title="Anomaly 1", content="Content 2", owner_agent="Janus",
        confidence_score=0.40,
        tags=["trace", "anomaly"],
    )
    signal_registry.create_candidate(
        signal_type="GOVERNANCE", source_kind="lesson", source_id="LKI-2",
        title="Governance 1", content="Content 3", owner_agent="Sage",
        confidence_score=0.75,
        tags=["lesson", "governance"],
    )
    return signal_registry


@pytest.fixture
def family_registry():
    return SkillFamilyRegistry()


@pytest.fixture
def canonical_registry():
    return CanonicalSkillRegistry()


@pytest.fixture
def approved_skill_registry():
    return ApprovedSkillRegistry()


@pytest.fixture
def seeded_capability_candidates(approved_skill_registry, cap_candidate_registry,
                                  cap_family_registry, cap_canonical_registry):
    from services.capability_discovery_engine import CapabilityDiscoveryEngine
    from services.capability_family_engine import CapabilityFamilyEngine
    from services.canonical_capability_engine import CanonicalCapabilityEngine

    for i, (name, conf) in enumerate([("Trading Skill", 0.82), ("Risk Skill", 0.81),
                                        ("Engineering Skill", 0.86)], 1):
        approved_skill_registry.approve(
            name=name, description=f"Seed {i}", canonical_id=f"CANON-S{i}",
            owner_agent="Sage", approval_authority="Hung Vuong",
            reviewer_agent="Hung Vuong",
            confidence_score=conf, risk_level="LEVEL_1_MODERATE",
            tags=["seed", name.lower().split()[0]],
            evidence={"source": "seed", "seed_id": i},
        )
    CapabilityDiscoveryEngine(approved_skill_registry, cap_candidate_registry).run_all(owner_agent="Sage")
    CapabilityFamilyEngine(cap_candidate_registry, cap_family_registry).discover_families(owner_agent="Sage")
    CanonicalCapabilityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry).classify_all(owner_agent="Sage")
    return cap_candidate_registry, cap_family_registry, cap_canonical_registry


@pytest.fixture
def insight_registry_with_data(insight_registry):
    insight_registry.create_candidate(
        insight_type="PATTERN", title="Pattern Insight",
        description="A pattern insight", owner_agent="Sage",
        source_signal_ids=["LSIG-1", "LSIG-2"],
        confidence_score=0.80,
        tags=["pattern", "consolidated"],
    )
    insight_registry.create_candidate(
        insight_type="TREND", title="Trend Insight",
        description="A trend", owner_agent="Janus",
        source_signal_ids=["LSIG-3"],
        confidence_score=0.60,
        tags=["trend", "emerging"],
    )
    return insight_registry


@pytest.fixture
def cap_candidate_registry():
    return CapabilityCandidateRegistry()


@pytest.fixture
def cap_family_registry():
    return CapabilityFamilyRegistry()


@pytest.fixture
def cap_canonical_registry():
    return CanonicalCapabilityRegistry()


@pytest.fixture
def cap_promotion_registry():
    return PromotionRecommendationRegistry()


@pytest.fixture
def evidence_registry():
    return CapabilityEvidenceRegistry()


@pytest.fixture
def official_registry():
    return OfficialCapabilityRegistry()


@pytest.fixture
def cap_candidate_with_skills(approved_skill_registry):
    skills = []
    for i, (name, conf) in enumerate([("Trading Domain Skill", 0.82),
                                        ("Risk Domain Skill", 0.81),
                                        ("Engineering Domain Skill", 0.86)], 1):
        s = approved_skill_registry.approve(
            name=name, description=f"Skill {i}", canonical_id=f"CSEED-{i}",
            owner_agent="Sage", approval_authority="Hung Vuong",
            reviewer_agent="Hung Vuong",
            confidence_score=conf, risk_level="LEVEL_1_MODERATE",
            tags=["test"], evidence={"source": "test", "seed_id": i},
        )
        skills.append(s)
    return skills


@pytest.fixture
def adoption_registry():
    return CapabilityAdoptionRegistry()
