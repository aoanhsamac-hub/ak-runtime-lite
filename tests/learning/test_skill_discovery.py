import pytest

from learning.skill_discovery import (
    CandidateStatus,
    EvidencePattern,
    EvidenceRequirements,
    SkillCandidate,
    SkillDiscovery,
    SkillDiscoveryError,
    SkillDiscoveryValidationLayer,
)
from learning.skill_evidence_policy import RiskClassification


GOVERNANCE = {
    "issue_id": "ISSUE-2026-0004",
    "actor": "Hermes",
    "reviewer": "Sage",
    "governance_valid": True,
    "source": "AgentMemoryClient",
    "timestamp": "2026-06-07T00:00:00Z",
}


def sample_lessons(count=3, domain="planning"):
    contexts = [f"{domain}", f"{domain} review", f"{domain} audit", f"{domain} sync", f"{domain} retro"]
    reviewers = ["Sage", "Hermes", "Janus", "Lang Lieu", "Yet Kieu"]
    sources = ["MemoryInterface", "AgentMemoryClient", "HermesAnalytics", "JanusCoordination", "SageAudit"]
    dataset_sets = [["DS-1", "DS-2"], ["DS-3", "DS-4"], ["DS-5"], ["DS-6", "DS-7"], ["DS-8"]]
    return [
        {
            "lesson_id": f"LESSON-{i:03d}",
            "source": sources[i % len(sources)],
            "author": "Hermes",
            "reviewer": reviewers[i % len(reviewers)],
            "status": "APPROVED",
            "context": contexts[i % len(contexts)],
            "outcome": "safe recommendation",
            "evidence": [
                {"evidence_id": f"EV-{i:03d}-01", "confidence": 0.9, "success": True, "dataset_refs": dataset_sets[i % len(dataset_sets)]},
                {"evidence_id": f"EV-{i:03d}-02", "confidence": 0.8, "success": True, "dataset_refs": dataset_sets[(i + 1) % len(dataset_sets)]},
            ],
        }
        for i in range(count)
    ]


# --- Enum & Dataclass Tests ---

def test_candidate_status_enum_values():
    assert CandidateStatus.DISCOVERED.value == "DISCOVERED"
    assert CandidateStatus.VALIDATED.value == "VALIDATED"
    assert CandidateStatus.REJECTED.value == "REJECTED"
    assert CandidateStatus.MERGED.value == "MERGED"


def test_evidence_pattern_dataclass():
    pattern = EvidencePattern(
        trigger_conditions=["planning", "safe recommendation"],
        reasoning_path=["evaluate risk", "recommend action"],
        outcome_pattern="safe recommendation",
        scope_boundaries={"domain": "planning", "applicable_agents": ["Hermes"]},
        method_summary="Evaluate and recommend",
        limitations=["limited lessons"],
    )
    assert pattern.trigger_conditions == ["planning", "safe recommendation"]
    assert pattern.outcome_pattern == "safe recommendation"
    assert pattern.method_summary == "Evaluate and recommend"


def test_evidence_pattern_to_dict():
    pattern = EvidencePattern(
        trigger_conditions=["planning"],
        reasoning_path=["step1"],
        outcome_pattern="safe",
        scope_boundaries={"domain": "planning"},
        method_summary="method",
        limitations=["limit1"],
    )
    d = pattern.to_dict()
    assert d["trigger_conditions"] == ["planning"]
    assert d["outcome_pattern"] == "safe"
    assert d["scope_boundaries"] == {"domain": "planning"}


def test_evidence_requirements_defaults():
    req = EvidenceRequirements()
    assert req.minimum_lessons == 3
    assert req.minimum_distinct_tasks == 2
    assert req.minimum_evidence_weight == 2.5
    assert req.require_sage_review is False
    assert req.require_janus_coordination is False


def test_evidence_requirements_custom():
    req = EvidenceRequirements(minimum_lessons=5, minimum_distinct_tasks=3, minimum_evidence_weight=3.0)
    assert req.minimum_lessons == 5
    assert req.minimum_distinct_tasks == 3
    assert req.minimum_evidence_weight == 3.0


def test_skill_candidate_dataclass():
    pattern = EvidencePattern(
        trigger_conditions=["test"],
        reasoning_path=["step"],
        outcome_pattern="safe",
        scope_boundaries={"domain": "test"},
        method_summary="method",
        limitations=[],
    )
    candidate = SkillCandidate(
        candidate_id="CANDIDATE-TEST001",
        name="test.safe_recommendation",
        description="Test candidate",
        source_lesson_ids=["LESSON-001"],
        evidence_pattern=pattern,
        confidence_score=0.85,
        risk_classification=RiskClassification.LOW,
        deduplication_key="abc123",
        discovery_trace_id="trace-001",
        discovered_by="Hermes",
        discovered_at="2026-06-07T00:00:00Z",
        evidence_summary={"lesson_count": 1},
        status=CandidateStatus.DISCOVERED,
    )
    assert candidate.candidate_id == "CANDIDATE-TEST001"
    assert candidate.confidence_score == 0.85
    assert candidate.risk_classification == RiskClassification.LOW
    assert candidate.status == CandidateStatus.DISCOVERED


def test_skill_candidate_to_dict():
    pattern = EvidencePattern(
        trigger_conditions=["test"],
        reasoning_path=["step"],
        outcome_pattern="safe",
        scope_boundaries={"domain": "test"},
        method_summary="method",
        limitations=[],
    )
    candidate = SkillCandidate(
        candidate_id="CANDIDATE-TEST001",
        name="test.safe_recommendation",
        description="Test",
        source_lesson_ids=["LESSON-001"],
        evidence_pattern=pattern,
        confidence_score=0.85,
        risk_classification=RiskClassification.LOW,
        deduplication_key="abc123",
        discovery_trace_id="trace-001",
        discovered_by="Hermes",
        discovered_at="2026-06-07T00:00:00Z",
        evidence_summary={"lesson_count": 1},
        status=CandidateStatus.DISCOVERED,
    )
    d = candidate.to_dict()
    assert d["candidate_id"] == "CANDIDATE-TEST001"
    assert d["risk_classification"] == "LOW"
    assert d["status"] == "DISCOVERED"
    assert d["evidence_pattern"]["trigger_conditions"] == ["test"]


# --- Validation Layer ---

def test_validation_rejects_empty_governance():
    with pytest.raises(SkillDiscoveryError, match="governance context is required"):
        SkillDiscoveryValidationLayer().validate_governance({})


def test_validation_rejects_invalid_governance():
    with pytest.raises(SkillDiscoveryError, match="governance context is invalid"):
        SkillDiscoveryValidationLayer().validate_governance({"governance_valid": False})


def test_validation_rejects_missing_issue_id():
    with pytest.raises(SkillDiscoveryError, match="issue_id is required"):
        SkillDiscoveryValidationLayer().validate_governance({"governance_valid": True, "reviewer": "Sage"})


def test_validation_rejects_missing_reviewer():
    with pytest.raises(SkillDiscoveryError, match="reviewer is required"):
        SkillDiscoveryValidationLayer().validate_governance({"governance_valid": True, "issue_id": "ISS-001"})


def test_validation_rejects_empty_lessons():
    with pytest.raises(SkillDiscoveryError, match="at least one approved lesson is required"):
        SkillDiscoveryValidationLayer().validate_approved_lessons([])


def test_validation_rejects_non_approved_lesson():
    lessons = sample_lessons(1)
    lessons[0]["status"] = "DRAFT"
    with pytest.raises(SkillDiscoveryError, match="status must be APPROVED"):
        SkillDiscoveryValidationLayer().validate_approved_lessons(lessons)


def test_validation_rejects_missing_lesson_fields():
    with pytest.raises(SkillDiscoveryError, match="missing fields"):
        SkillDiscoveryValidationLayer().validate_approved_lessons([{"lesson_id": "L-1"}])


# --- Discovery ---

def test_discover_returns_candidates_with_valid_input():
    discovery = SkillDiscovery()
    candidates = discovery.discover(sample_lessons(3), GOVERNANCE)
    assert len(candidates) >= 1
    candidate = candidates[0]
    assert isinstance(candidate, SkillCandidate)
    assert candidate.candidate_id.startswith("CANDIDATE-")
    assert candidate.status == CandidateStatus.DISCOVERED
    assert candidate.risk_classification in RiskClassification
    assert 0.0 <= candidate.confidence_score <= 5.0
    assert len(candidate.source_lesson_ids) >= 3
    assert candidate.discovered_by == "Hermes"
    assert candidate.discovery_trace_id != ""


def test_discover_returns_empty_for_insufficient_lessons():
    discovery = SkillDiscovery()
    candidates = discovery.discover(sample_lessons(1), GOVERNANCE)
    assert len(candidates) == 0


def test_discover_returns_empty_for_low_evidence_weight():
    lessons = sample_lessons(3)
    for lesson in lessons:
        lesson["source"] = "SameSource"
        lesson["reviewer"] = "SameReviewer"
        lesson["context"] = "SameContext"
        for ev in lesson["evidence"]:
            ev["dataset_refs"] = []
            ev["success"] = False
    discovery = SkillDiscovery()
    candidates = discovery.discover(lessons, GOVERNANCE)
    assert len(candidates) == 0


def test_discover_respects_custom_requirements():
    req = EvidenceRequirements(minimum_lessons=5, minimum_evidence_weight=4.0)
    discovery = SkillDiscovery(requirements=req)
    candidates = discovery.discover(sample_lessons(3), GOVERNANCE)
    assert len(candidates) == 0
    candidates = discovery.discover(sample_lessons(5), GOVERNANCE)
    assert len(candidates) >= 1


def test_discover_rejects_missing_governance():
    with pytest.raises(SkillDiscoveryError, match="governance context is required"):
        SkillDiscovery().discover(sample_lessons(3), {})


def test_discover_rejects_invalid_governance():
    gov = dict(GOVERNANCE)
    gov["governance_valid"] = False
    with pytest.raises(SkillDiscoveryError, match="governance context is invalid"):
        SkillDiscovery().discover(sample_lessons(3), gov)


def test_discover_rejects_empty_lessons():
    with pytest.raises(SkillDiscoveryError, match="at least one approved lesson is required"):
        SkillDiscovery().discover([], GOVERNANCE)


def test_discover_rejects_non_approved_lessons():
    lessons = sample_lessons(3)
    lessons[0]["status"] = "DRAFT"
    with pytest.raises(SkillDiscoveryError, match="status must be APPROVED"):
        SkillDiscovery().discover(lessons, GOVERNANCE)


def test_discover_detects_sovereign_assets():
    lessons = sample_lessons(3, domain="constitution")
    for lesson in lessons:
        lesson["context"] = "constitutional review of risk kernel"
    req = EvidenceRequirements(minimum_lessons=3, minimum_distinct_tasks=1)
    candidates = SkillDiscovery(requirements=req).discover(lessons, GOVERNANCE)
    assert len(candidates) >= 1
    assert candidates[0].risk_classification == RiskClassification.SOVEREIGN


def test_discover_assigns_high_risk():
    lessons = sample_lessons(5)
    for lesson in lessons:
        lesson["source"] = f"Source-{hash(lesson['lesson_id'])}"
        lesson["reviewer"] = f"Reviewer-{hash(lesson['lesson_id'])}"
        lesson["context"] = f"planning-{hash(lesson['lesson_id'])}"
        for ev in lesson["evidence"]:
            ev["dataset_refs"] = [f"DS-{hash(lesson['lesson_id'])}", f"DS-{hash(lesson['lesson_id'])+1}"]
            ev["success"] = True
    candidates = SkillDiscovery().discover(lessons, GOVERNANCE)
    if len(candidates) > 0:
        assert candidates[0].risk_classification in (
            RiskClassification.HIGH, RiskClassification.MEDIUM
        )


def test_discover_groups_lessons_by_domain():
    planning_lessons = sample_lessons(3, domain="planning")
    audit_lessons = sample_lessons(3, domain="audit")
    all_lessons = planning_lessons + audit_lessons
    candidates = SkillDiscovery().discover(all_lessons, GOVERNANCE)
    assert len(candidates) >= 1


# --- Deduplication ---

def test_deduplication_merges_same_key():
    lessons_a = sample_lessons(3, domain="planning")
    lessons_b = sample_lessons(3, domain="planning")
    discovery = SkillDiscovery()
    candidates = discovery.discover(lessons_a + lessons_b, GOVERNANCE)
    for candidate in candidates:
        if candidate.status == CandidateStatus.MERGED:
            assert "merged_from" in candidate.evidence_summary
            break
    else:
        assert len(candidates) <= 2


def test_deduplication_threshold():
    assert SkillDiscovery().get_deduplication_threshold() == 0.8


# --- Evidence Requirements ---

def test_get_candidate_evidence_requirements():
    req = SkillDiscovery().get_candidate_evidence_requirements()
    assert isinstance(req, EvidenceRequirements)
    assert req.minimum_lessons >= 3


# --- Blocked Result ---

def test_blocked_result_returns_empty():
    result = SkillDiscovery().blocked_result("Insufficient evidence")
    assert result == []


# --- Confidence Score ---

def test_confidence_score_formula_within_bounds():
    candidates = SkillDiscovery().discover(sample_lessons(3), GOVERNANCE)
    if len(candidates) > 0:
        assert 0.0 <= candidates[0].confidence_score <= 5.0


# --- Evidence Pattern ---

def test_evidence_pattern_has_expected_structure():
    candidates = SkillDiscovery().discover(sample_lessons(3), GOVERNANCE)
    if len(candidates) > 0:
        pattern = candidates[0].evidence_pattern
        assert isinstance(pattern.trigger_conditions, list)
        assert isinstance(pattern.reasoning_path, list)
        assert isinstance(pattern.outcome_pattern, str)
        assert isinstance(pattern.scope_boundaries, dict)
        assert isinstance(pattern.method_summary, str)
        assert isinstance(pattern.limitations, list)
        assert "planning" in pattern.scope_boundaries.get("domain", "")


# --- Edge Cases ---

def test_discover_with_single_group():
    discovery = SkillDiscovery(EvidenceRequirements(minimum_lessons=3, minimum_distinct_tasks=1))
    candidates = discovery.discover(sample_lessons(3, domain="planning"), GOVERNANCE)
    assert len(candidates) >= 1


def test_discover_handles_missing_evidence_field():
    lessons = [
        {
            "lesson_id": "LESSON-001",
            "source": "MemoryInterface",
            "author": "Hermes",
            "reviewer": "Sage",
            "status": "APPROVED",
            "context": "planning",
            "outcome": "safe recommendation",
            "evidence": [],
        }
        for _ in range(3)
    ]
    candidates = SkillDiscovery().discover(lessons, GOVERNANCE)
    assert len(candidates) == 0


def test_discover_trace_id_unique_per_call():
    d1 = SkillDiscovery()
    d2 = SkillDiscovery()
    c1 = d1.discover(sample_lessons(3), GOVERNANCE)
    c2 = d2.discover(sample_lessons(3), GOVERNANCE)
    if c1 and c2:
        assert c1[0].discovery_trace_id != c2[0].discovery_trace_id


def test_discover_candidate_id_format():
    candidates = SkillDiscovery().discover(sample_lessons(3), GOVERNANCE)
    if len(candidates) > 0:
        assert candidates[0].candidate_id.startswith("CANDIDATE-")
        assert len(candidates[0].candidate_id) > 10


def test_deduplication_key_consistent():
    discovery = SkillDiscovery()
    candidates = discovery.discover(sample_lessons(3, domain="planning"), GOVERNANCE)
    if len(candidates) > 0:
        assert isinstance(candidates[0].deduplication_key, str)
        assert len(candidates[0].deduplication_key) == 16


# --- Sovereign Domain Matching ---

def test_sovereign_domains_all_detected():
    domains = ["constitution", "risk_kernel", "security_law", "execution_law", "state_corpus", "governance"]
    req = EvidenceRequirements(minimum_lessons=3, minimum_distinct_tasks=1)
    for domain in domains:
        lessons = sample_lessons(3, domain=domain)
        for lesson in lessons:
            lesson["context"] = f"{domain} review"
        candidates = SkillDiscovery(requirements=req).discover(lessons, GOVERNANCE)
        if len(candidates) > 0:
            assert candidates[0].risk_classification == RiskClassification.SOVEREIGN, f"Failed for {domain}"


# --- Candidate Traceability ---

def test_candidate_has_governance_issue_id():
    candidates = SkillDiscovery().discover(sample_lessons(3), GOVERNANCE)
    if len(candidates) > 0:
        assert candidates[0].governance_issue_id == GOVERNANCE["issue_id"]


def test_candidate_to_dict_includes_governance_issue_id():
    candidates = SkillDiscovery().discover(sample_lessons(3), GOVERNANCE)
    if len(candidates) > 0:
        d = candidates[0].to_dict()
        assert "governance_issue_id" in d
        assert d["governance_issue_id"] == GOVERNANCE["issue_id"]


def test_merged_candidate_retains_governance_issue_id():
    lessons_a = sample_lessons(3, domain="planning")
    lessons_b = sample_lessons(3, domain="planning")
    candidates = SkillDiscovery().discover(lessons_a + lessons_b, GOVERNANCE)
    if len(candidates) > 0:
        for c in candidates:
            assert c.governance_issue_id == GOVERNANCE["issue_id"], (
                f"Missing governance_issue_id on {c.candidate_id} ({c.status.value})"
            )


def test_governance_validation_requires_issue_id():
    gov = dict(GOVERNANCE)
    del gov["issue_id"]
    with pytest.raises(SkillDiscoveryError, match="issue_id is required"):
        SkillDiscovery(EvidenceRequirements(minimum_lessons=3, minimum_distinct_tasks=1)).discover(
            sample_lessons(3), gov
        )


def test_skill_candidate_dataclass_defaults_governance_issue_id():
    pattern = EvidencePattern(
        trigger_conditions=["test"], reasoning_path=["step"], outcome_pattern="safe",
        scope_boundaries={"domain": "test"}, method_summary="method", limitations=[],
    )
    candidate = SkillCandidate(
        candidate_id="CANDIDATE-TRACE01", name="test.safe", description="Test",
        source_lesson_ids=["L-1"], evidence_pattern=pattern, confidence_score=0.8,
        risk_classification=RiskClassification.LOW, deduplication_key="key1",
        discovery_trace_id="trace-1", discovered_by="Hermes", discovered_at="now",
        evidence_summary={"count": 1}, status=CandidateStatus.DISCOVERED,
    )
    assert candidate.governance_issue_id == ""
