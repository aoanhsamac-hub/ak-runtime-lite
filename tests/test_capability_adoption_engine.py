import pytest

from agents.identity import AGENT_IDENTITIES
from agents.runtime_models import EvidenceRecord, EvidenceClassification
from memory.adoption_registry import (
    CapabilityAdoptionRegistry,
    AdoptionRecord,
    ADOPTION_LIFECYCLE_STAGES,
    ADOPTION_TRANSITIONS,
)
from memory.capability_registry.official_capability_registry import (
    OfficialCapabilityRegistry,
    ADOPTION_STAGES,
)
from memory.capability_roi_registry import CapabilityROIRegistry
from memory.usage_registry import CapabilityUsageRegistry
from services.capability_adoption_engine import (
    CapabilityAdoptionEngine,
    CapabilityAssignmentPolicy,
)


# ---------------------------------------------------------------------------
# AdoptionRecord schema tests
# ---------------------------------------------------------------------------

class TestAdoptionRecord:
    def test_create_minimal(self):
        r = AdoptionRecord(
            official_capability_id="OCAP-001",
            assigned_agent="lang_lieu",
        )
        assert r.adoption_id.startswith("ADOPT-")
        assert r.lifecycle_stage == "PROPOSED"
        assert r.risk_level == "LEVEL_1_MODERATE"
        assert r.allowed_scope == "sandbox"

    def test_requires_official_capability_id(self):
        with pytest.raises(ValueError, match="official_capability_id is required"):
            AdoptionRecord(assigned_agent="lang_lieu")

    def test_requires_assigned_agent(self):
        with pytest.raises(ValueError, match="assigned_agent is required"):
            AdoptionRecord(official_capability_id="OCAP-001")

    def test_invalid_lifecycle_stage(self):
        with pytest.raises(ValueError, match="invalid lifecycle_stage"):
            AdoptionRecord(
                official_capability_id="OCAP-001",
                assigned_agent="lang_lieu",
                lifecycle_stage="INVALID",
            )

    def test_invalid_risk_level(self):
        with pytest.raises(ValueError, match="invalid risk_level"):
            AdoptionRecord(
                official_capability_id="OCAP-001",
                assigned_agent="lang_lieu",
                risk_level="LEVEL_99",
            )

    def test_adoption_lifecycle_stages_constant(self):
        assert ADOPTION_LIFECYCLE_STAGES == {
            "PROPOSED", "ASSIGNED_SANDBOX", "IN_USE_SANDBOX",
            "REVIEW_REQUIRED", "SUSPENDED", "RETIRED",
        }

    def test_official_capability_record_has_adoption_stage(self, official_registry):
        rec = official_registry.create(
            canonical_capability_id="CCAP-T1",
            name="Test Cap", description="Test",
            domain="Engineering",
            hermes_recommendation="RECOMMEND_PROMOTION",
            hermes_reviewer="Hermes",
            sage_recommendation="GOVERNANCE_APPROVED_FOR_PROMOTION",
            sage_reviewer="Sage",
            hung_vuong_decision="APPROVE_AS_OFFICIAL_CAPABILITY",
            owner_agent="Sage", reviewer_agent="Hung Vuong",
        )
        assert rec.adoption_stage == "PROPOSED"
        d = rec.to_dict()
        assert "adoption_stage" in d
        assert d["adoption_stage"] == "PROPOSED"

    def test_adoption_stage_validation(self, official_registry):
        with pytest.raises(ValueError, match="invalid adoption_stage"):
            official_registry.create(
                canonical_capability_id="CCAP-T2",
                name="Test", description="Test",
                domain="Engineering",
                adoption_stage="BAD_STAGE",
                hermes_recommendation="RECOMMEND_PROMOTION",
                hermes_reviewer="Hermes",
                sage_recommendation="GOVERNANCE_APPROVED_FOR_PROMOTION",
                sage_reviewer="Sage",
                hung_vuong_decision="APPROVE_AS_OFFICIAL_CAPABILITY",
                owner_agent="Sage", reviewer_agent="Hung Vuong",
            )

    def test_no_activation_enforces_proposed(self, official_registry):
        with pytest.raises(ValueError, match="adoption_stage must be PROPOSED"):
            official_registry.create(
                canonical_capability_id="CCAP-T3",
                name="Test", description="Test",
                domain="Engineering",
                adoption_stage="ASSIGNED_SANDBOX",
                hermes_recommendation="RECOMMEND_PROMOTION",
                hermes_reviewer="Hermes",
                sage_recommendation="GOVERNANCE_APPROVED_FOR_PROMOTION",
                sage_reviewer="Sage",
                hung_vuong_decision="APPROVE_AS_OFFICIAL_CAPABILITY",
                owner_agent="Sage", reviewer_agent="Hung Vuong",
            )

    def test_with_stage_creates_new_record(self):
        r1 = AdoptionRecord(
            official_capability_id="OCAP-001",
            assigned_agent="lang_lieu",
        )
        r2 = r1.with_stage("ASSIGNED_SANDBOX")
        assert r2.lifecycle_stage == "ASSIGNED_SANDBOX"
        assert r2.adoption_id == r1.adoption_id
        assert r2.assigned_agent == r1.assigned_agent
        assert r1.lifecycle_stage == "PROPOSED"

    def test_to_dict_contains_all_fields(self):
        r = AdoptionRecord(
            official_capability_id="OCAP-001",
            assigned_agent="lang_lieu",
            rollback_condition="failure_rate > 0.3",
            roi_metric="success_rate > 0.8",
        )
        d = r.to_dict()
        assert d["adoption_id"] == r.adoption_id
        assert d["official_capability_id"] == "OCAP-001"
        assert d["assigned_agent"] == "lang_lieu"
        assert d["rollback_condition"] == "failure_rate > 0.3"
        assert d["roi_metric"] == "success_rate > 0.8"

    def test_adoption_stage_constants_match(self):
        assert ADOPTION_LIFECYCLE_STAGES == ADOPTION_STAGES

    def test_transitions_from_proposed(self):
        assert ADOPTION_TRANSITIONS["PROPOSED"] == {"ASSIGNED_SANDBOX", "SUSPENDED", "RETIRED"}

    def test_transitions_from_assigned_sandbox(self):
        assert ADOPTION_TRANSITIONS["ASSIGNED_SANDBOX"] == {"IN_USE_SANDBOX", "SUSPENDED", "RETIRED"}

    def test_transitions_from_in_use_sandbox(self):
        assert ADOPTION_TRANSITIONS["IN_USE_SANDBOX"] == {"REVIEW_REQUIRED", "SUSPENDED", "RETIRED"}

    def test_transitions_from_review_required(self):
        assert ADOPTION_TRANSITIONS["REVIEW_REQUIRED"] == {"ASSIGNED_SANDBOX", "IN_USE_SANDBOX", "SUSPENDED", "RETIRED"}

    def test_transitions_from_suspended(self):
        assert ADOPTION_TRANSITIONS["SUSPENDED"] == {"ASSIGNED_SANDBOX", "RETIRED"}

    def test_transitions_from_retired(self):
        assert ADOPTION_TRANSITIONS["RETIRED"] == set()


# ---------------------------------------------------------------------------
# CapabilityAdoptionRegistry tests
# ---------------------------------------------------------------------------

class TestCapabilityAdoptionRegistry:
    def test_create_and_get(self, adoption_registry):
        r = adoption_registry.create(
            official_capability_id="OCAP-001",
            assigned_agent="lang_lieu",
        )
        assert r.adoption_id.startswith("ADOPT-")
        fetched = adoption_registry.get(r.adoption_id)
        assert fetched.assigned_agent == "lang_lieu"

    def test_get_not_found(self, adoption_registry):
        with pytest.raises(KeyError):
            adoption_registry.get("NONEXISTENT")

    def test_list_all(self, adoption_registry):
        adoption_registry.create(official_capability_id="OCAP-001", assigned_agent="lang_lieu")
        adoption_registry.create(official_capability_id="OCAP-002", assigned_agent="iris")
        assert len(adoption_registry.list_all()) == 2

    def test_list_by_agent(self, adoption_registry):
        adoption_registry.create(official_capability_id="OCAP-001", assigned_agent="lang_lieu")
        adoption_registry.create(official_capability_id="OCAP-002", assigned_agent="iris")
        lang = adoption_registry.list_by_agent("lang_lieu")
        assert len(lang) == 1
        assert lang[0].official_capability_id == "OCAP-001"

    def test_list_by_capability(self, adoption_registry):
        adoption_registry.create(official_capability_id="OCAP-001", assigned_agent="lang_lieu")
        adoption_registry.create(official_capability_id="OCAP-001", assigned_agent="iris")
        caps = adoption_registry.list_by_capability("OCAP-001")
        assert len(caps) == 2

    def test_list_by_stage(self, adoption_registry):
        adoption_registry.create(official_capability_id="OCAP-001", assigned_agent="lang_lieu")
        a2 = adoption_registry.create(
            official_capability_id="OCAP-002", assigned_agent="iris",
            lifecycle_stage="SUSPENDED",
        )
        proposed = adoption_registry.list_all(lifecycle_stage="PROPOSED")
        assert len(proposed) == 1
        suspended = adoption_registry.list_all(lifecycle_stage="SUSPENDED")
        assert len(suspended) == 1
        assert suspended[0].adoption_id == a2.adoption_id

    def test_update_stage(self, adoption_registry):
        r = adoption_registry.create(
            official_capability_id="OCAP-001",
            assigned_agent="lang_lieu",
        )
        updated = adoption_registry.update_stage(r.adoption_id, "ASSIGNED_SANDBOX")
        assert updated.lifecycle_stage == "ASSIGNED_SANDBOX"
        fetched = adoption_registry.get(r.adoption_id)
        assert fetched.lifecycle_stage == "ASSIGNED_SANDBOX"


# ---------------------------------------------------------------------------
# CapabilityAssignmentPolicy tests
# ---------------------------------------------------------------------------

class TestCapabilityAssignmentPolicy:
    def test_unknown_agent(self, official_registry):
        policy = CapabilityAssignmentPolicy(official_registry)
        result = policy.can_assign("unknown_agent", "OCAP-001")
        assert not result["allowed"]

    def test_unknown_capability(self, official_registry):
        policy = CapabilityAssignmentPolicy(official_registry)
        result = policy.can_assign("lang_lieu", "NONEXISTENT")
        assert not result["allowed"]

    def test_not_approved_capability(self, official_registry):
        cap = official_registry.create(
            canonical_capability_id="CCAP-T1",
            name="Pending Cap", description="Test",
            domain="Engineering",
            status="HOLD_FOR_EVIDENCE",
            hermes_recommendation="NEEDS_MORE_EVIDENCE",
            hermes_reviewer="Hermes",
            sage_recommendation="GOVERNANCE_HOLD",
            sage_reviewer="Sage",
            hung_vuong_decision="HOLD_FOR_EVIDENCE",
            owner_agent="Sage", reviewer_agent="Hung Vuong",
        )
        policy = CapabilityAssignmentPolicy(official_registry)
        result = policy.can_assign("lang_lieu", cap.official_capability_id)
        assert not result["allowed"]

    def test_approved_capability_allows_assignment(self, official_registry):
        cap = setup_approved_capability(official_registry, "APP-1", "Trading Cap")
        policy = CapabilityAssignmentPolicy(official_registry)
        result = policy.can_assign("lang_lieu", cap.official_capability_id)
        assert result["allowed"]

    def test_allowed_agents_for_low_risk(self, official_registry):
        policy = CapabilityAssignmentPolicy(official_registry)
        agents = policy.allowed_agents_for_risk("LEVEL_0_LOW")
        assert len(agents) == len(AGENT_IDENTITIES)

    def test_no_agents_for_high_risk(self, official_registry):
        policy = CapabilityAssignmentPolicy(official_registry)
        agents = policy.allowed_agents_for_risk("LEVEL_2_HIGH")
        assert agents == []

    def test_no_agents_for_critical_risk(self, official_registry):
        policy = CapabilityAssignmentPolicy(official_registry)
        agents = policy.allowed_agents_for_risk("LEVEL_3_CRITICAL")
        assert agents == []

    def test_no_agents_for_constitutional_risk(self, official_registry):
        policy = CapabilityAssignmentPolicy(official_registry)
        agents = policy.allowed_agents_for_risk("LEVEL_4_CONSTITUTIONAL")
        assert agents == []


# ---------------------------------------------------------------------------
# CapabilityAdoptionEngine integration tests
# ---------------------------------------------------------------------------

class TestCapabilityAdoptionEngine:
    def test_propose_adoption_success(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = setup_approved_capability(official_registry, "CCAP-E1", "Adoptable Cap")

        result = engine.propose_adoption(
            official_capability_id=cap.official_capability_id,
            assigned_agent="lang_lieu",
            owner="Janus",
        )
        assert result["success"]
        assert result["adoption"]["lifecycle_stage"] == "PROPOSED"
        assert result["adoption"]["assigned_agent"] == "lang_lieu"
        assert result["gate"]["decision"] == "ALLOW"

    def test_propose_adoption_not_approved(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = official_registry.create(
            canonical_capability_id="CCAP-E2",
            name="Not Approved", description="Test",
            domain="Engineering",
            status="HOLD_FOR_EVIDENCE",
            hermes_recommendation="NEEDS_MORE_EVIDENCE",
            hermes_reviewer="Hermes",
            sage_recommendation="GOVERNANCE_HOLD",
            sage_reviewer="Sage",
            hung_vuong_decision="HOLD_FOR_EVIDENCE",
            owner_agent="Sage", reviewer_agent="Hung Vuong",
        )
        result = engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="lang_lieu")
        assert not result["success"]

    def test_propose_adoption_unknown_agent(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = setup_approved_capability(official_registry, "CCAP-E3", "Unreachable")
        result = engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="ghost")
        assert not result["success"]

    def test_transition_proposed_to_assigned_sandbox(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = setup_approved_capability(official_registry, "CCAP-E4", "Transition Cap")
        proposal = engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="lang_lieu", owner="Janus")
        adoption_id = proposal["adoption"]["adoption_id"]

        result = engine.transition(adoption_id, "ASSIGNED_SANDBOX")
        assert result["success"]
        assert result["adoption"]["lifecycle_stage"] == "ASSIGNED_SANDBOX"
        assert result["transition"] == "PROPOSED -> ASSIGNED_SANDBOX"

    def test_transition_assigned_to_in_use_sandbox(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = setup_approved_capability(official_registry, "CCAP-E5", "InUse Test")
        proposal = engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="iris")
        adoption_id = proposal["adoption"]["adoption_id"]
        engine.transition(adoption_id, "ASSIGNED_SANDBOX")

        result = engine.transition(adoption_id, "IN_USE_SANDBOX")
        assert result["success"]
        assert result["adoption"]["lifecycle_stage"] == "IN_USE_SANDBOX"

    def test_transition_in_use_to_review_required(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = setup_approved_capability(official_registry, "CCAP-E6", "ReviewReq")
        proposal = engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="hermes")
        adoption_id = proposal["adoption"]["adoption_id"]
        engine.transition(adoption_id, "ASSIGNED_SANDBOX")
        engine.transition(adoption_id, "IN_USE_SANDBOX")

        result = engine.transition(adoption_id, "REVIEW_REQUIRED")
        assert result["success"]
        assert result["adoption"]["lifecycle_stage"] == "REVIEW_REQUIRED"

    def test_transition_invalid(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = setup_approved_capability(official_registry, "CCAP-E7", "Invalid Trans")
        proposal = engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="lang_lieu")
        adoption_id = proposal["adoption"]["adoption_id"]

        result = engine.transition(adoption_id, "IN_USE_SANDBOX")
        assert not result["success"]
        assert "cannot transition" in result["error"]

    def test_transition_suspend_and_retire(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = setup_approved_capability(official_registry, "CCAP-E8", "SuspendRetire")
        proposal = engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="lang_lieu")
        adoption_id = proposal["adoption"]["adoption_id"]

        r1 = engine.transition(adoption_id, "SUSPENDED")
        assert r1["success"]
        assert r1["adoption"]["lifecycle_stage"] == "SUSPENDED"

        r2 = engine.transition(adoption_id, "RETIRED")
        assert r2["success"]
        assert r2["adoption"]["lifecycle_stage"] == "RETIRED"

    def test_suspend_back_to_sandbox(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = setup_approved_capability(official_registry, "CCAP-E9", "Reinstate")
        proposal = engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="lang_lieu")
        adoption_id = proposal["adoption"]["adoption_id"]
        engine.transition(adoption_id, "SUSPENDED")

        r = engine.transition(adoption_id, "ASSIGNED_SANDBOX")
        assert r["success"]
        assert r["adoption"]["lifecycle_stage"] == "ASSIGNED_SANDBOX"

    def test_governance_blocks_high_risk(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = setup_approved_capability(official_registry, "CCAP-E10", "HighRisk")

        result = engine.propose_adoption(
            official_capability_id=cap.official_capability_id,
            assigned_agent="lang_lieu",
            risk_level="LEVEL_2_HIGH",
            owner="Janus",
        )
        assert not result["success"]
        assert "governance gate blocked" in result["error"]

    def test_record_usage_success(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = setup_approved_capability(official_registry, "CCAP-E11", "UsageTest")
        proposal = engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="lang_lieu")
        adoption_id = proposal["adoption"]["adoption_id"]

        result = engine.record_usage(adoption_id, success=True, value=5.0, cost=1.0)
        assert result["success"]
        assert result["usage"]["success"] is True

    def test_record_usage_failure_tracking(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = setup_approved_capability(official_registry, "CCAP-E12", "FailTrack")
        proposal = engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="lang_lieu")
        adoption_id = proposal["adoption"]["adoption_id"]

        for _ in range(3):
            engine.record_usage(adoption_id, success=False)

        adoption = adoption_registry.get(adoption_id)
        assert adoption.failure_count == 3
        assert adoption.lifecycle_stage == "SUSPENDED"

    def test_get_agent_adoptions(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = setup_approved_capability(official_registry, "CCAP-E13", "AgentAdopt")
        engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="lang_lieu")

        result = engine.get_agent_adoptions("lang_lieu")
        assert len(result) == 1
        assert result[0]["assigned_agent"] == "lang_lieu"
        assert result[0]["capability_name"] == "AgentAdopt"

    def test_get_capability_adoptions(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = setup_approved_capability(official_registry, "CCAP-E14", "CapAdopt")
        engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="lang_lieu")
        engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="iris")

        result = engine.get_capability_adoptions(cap.official_capability_id)
        assert len(result) == 2

    def test_summary(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = setup_approved_capability(official_registry, "CCAP-E15", "Summary")
        engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="lang_lieu")

        s = engine.summary()
        assert s["total_adoptions"] == 1
        assert s["by_stage"].get("PROPOSED", 0) == 1

    def test_official_registry_list_by_adoption_stage(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = setup_approved_capability(official_registry, "CCAP-E16", "StageFilter")
        engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="lang_lieu")

        proposed = official_registry.list_by_adoption_stage("PROPOSED")
        assert any(r.official_capability_id == cap.official_capability_id for r in proposed)

    def test_official_registry_update_adoption_stage(self, official_registry):
        cap = setup_approved_capability(official_registry, "CCAP-E17", "StageUpdate")
        updated = official_registry.update_adoption_stage(cap.official_capability_id, "ASSIGNED_SANDBOX")
        assert updated.adoption_stage == "ASSIGNED_SANDBOX"
        fetched = official_registry.get(cap.official_capability_id)
        assert fetched.adoption_stage == "ASSIGNED_SANDBOX"

    def test_engine_with_roi_integration(self, official_registry, adoption_registry, tmp_path):
        class FakeMemory:
            def record_capability_roi(self, record):
                return record
            def get_capability_roi(self, capability_name=None):
                return []
            def record_capability_usage(self, record):
                return record

        roi_reg = CapabilityROIRegistry(FakeMemory())
        usage_reg = CapabilityUsageRegistry(path=tmp_path / "test_usage.jsonl")
        engine = CapabilityAdoptionEngine(
            official_registry, adoption_registry,
            usage_registry=usage_reg, roi_registry=roi_reg,
        )
        cap = setup_approved_capability(official_registry, "CCAP-E18", "ROIAdopt")
        proposal = engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="lang_lieu")
        adoption_id = proposal["adoption"]["adoption_id"]

        for i in range(5):
            engine.record_usage(adoption_id, success=True, value=10.0, cost=2.0)

        assert len(usage_reg.get_all()) == 5

    def test_full_lifecycle(self, official_registry, adoption_registry):
        engine = make_engine(official_registry, adoption_registry)
        cap = setup_approved_capability(official_registry, "CCAP-E19", "FullCycle")

        proposal = engine.propose_adoption(official_capability_id=cap.official_capability_id, assigned_agent="iris")
        adoption_id = proposal["adoption"]["adoption_id"]

        path = [
            ("PROPOSED", "ASSIGNED_SANDBOX"),
            ("ASSIGNED_SANDBOX", "IN_USE_SANDBOX"),
            ("IN_USE_SANDBOX", "REVIEW_REQUIRED"),
            ("REVIEW_REQUIRED", "ASSIGNED_SANDBOX"),
            ("ASSIGNED_SANDBOX", "IN_USE_SANDBOX"),
            ("IN_USE_SANDBOX", "REVIEW_REQUIRED"),
            ("REVIEW_REQUIRED", "SUSPENDED"),
            ("SUSPENDED", "RETIRED"),
        ]
        for src, tgt in path:
            result = engine.transition(adoption_id, tgt)
            assert result["success"], f"transition {src} -> {tgt} failed: {result.get('error', 'unknown')}"

        adoption = adoption_registry.get(adoption_id)
        assert adoption.lifecycle_stage == "RETIRED"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def setup_approved_capability(registry: OfficialCapabilityRegistry, ccap_id_suffix: str, name: str):
    return registry.create(
        canonical_capability_id=f"CCAP-{ccap_id_suffix}",
        name=name,
        description=f"{name} description",
        domain="Engineering",
        status="APPROVED_AS_OFFICIAL",
        hermes_recommendation="RECOMMEND_PROMOTION",
        hermes_reviewer="Hermes",
        sage_recommendation="GOVERNANCE_APPROVED_FOR_PROMOTION",
        sage_reviewer="Sage",
        hung_vuong_decision="APPROVE_AS_OFFICIAL_CAPABILITY",
        owner_agent="Sage",
        reviewer_agent="Hung Vuong",
    )


def make_engine(official_registry, adoption_registry):
    return CapabilityAdoptionEngine(
        official_registry=official_registry,
        adoption_registry=adoption_registry,
    )
