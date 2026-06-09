import pytest
from memory.capability_registry.official_capability_registry import (
    OfficialCapabilityRegistry, OfficialCapabilityRecord,
)


class TestOfficialCapabilityRegistry:
    def test_create_official_record(self, official_registry):
        rec = official_registry.create(
            canonical_capability_id="CCAP-001",
            name="Trading Domain Capability",
            description="Official trading capability",
            domain="Trading",
            source_capability_ids=["CAPC-001", "CAPC-002"],
            hermes_recommendation="RECOMMEND_PROMOTION",
            hermes_reviewer="Hermes",
            sage_recommendation="GOVERNANCE_APPROVED_FOR_PROMOTION",
            sage_reviewer="Sage",
            hung_vuong_decision="APPROVE_AS_OFFICIAL_CAPABILITY",
            status="APPROVED_AS_OFFICIAL",
            owner_agent="Sage", reviewer_agent="Hung Vuong",
        )
        assert rec.official_capability_id.startswith("OCAP-")
        assert rec.activation_status == "DISABLED"
        assert rec.agent_adoption_status == "NOT_ASSIGNED"
        assert rec.evolution_status == "LOCKED"

    def test_default_statuses_are_safe(self, official_registry):
        rec = official_registry.create(
            canonical_capability_id="CCAP-001",
            name="Test Capability", description="Test",
            domain="Engineering",
            hermes_recommendation="RECOMMEND_PROMOTION",
            hermes_reviewer="Hermes",
            sage_recommendation="GOVERNANCE_APPROVED_FOR_PROMOTION",
            sage_reviewer="Sage",
            hung_vuong_decision="APPROVE_AS_OFFICIAL_CAPABILITY",
            owner_agent="Sage", reviewer_agent="Hung Vuong",
        )
        assert rec.activation_status == "DISABLED"
        assert rec.agent_adoption_status == "NOT_ASSIGNED"
        assert rec.evolution_status == "LOCKED"

    def test_activation_enforcement(self, official_registry):
        with pytest.raises(ValueError, match="activation_status must be DISABLED"):
            official_registry.create(
                canonical_capability_id="CCAP-001",
                name="Test", description="Test",
                domain="Engineering",
                activation_status="ENABLED",
                hermes_recommendation="RECOMMEND_PROMOTION",
                hermes_reviewer="Hermes",
                sage_recommendation="GOVERNANCE_APPROVED_FOR_PROMOTION",
                sage_reviewer="Sage",
                hung_vuong_decision="APPROVE_AS_OFFICIAL_CAPABILITY",
                owner_agent="Sage", reviewer_agent="Hung Vuong",
            )

    def test_agent_adoption_enforcement(self, official_registry):
        with pytest.raises(ValueError, match="agent_adoption_status must be NOT_ASSIGNED"):
            official_registry.create(
                canonical_capability_id="CCAP-001",
                name="Test", description="Test",
                domain="Engineering",
                agent_adoption_status="ASSIGNED",
                hermes_recommendation="RECOMMEND_PROMOTION",
                hermes_reviewer="Hermes",
                sage_recommendation="GOVERNANCE_APPROVED_FOR_PROMOTION",
                sage_reviewer="Sage",
                hung_vuong_decision="APPROVE_AS_OFFICIAL_CAPABILITY",
                owner_agent="Sage", reviewer_agent="Hung Vuong",
            )

    def test_evolution_enforcement(self, official_registry):
        with pytest.raises(ValueError, match="evolution_status must be LOCKED"):
            official_registry.create(
                canonical_capability_id="CCAP-001",
                name="Test", description="Test",
                domain="Engineering",
                evolution_status="UNLOCKED",
                hermes_recommendation="RECOMMEND_PROMOTION",
                hermes_reviewer="Hermes",
                sage_recommendation="GOVERNANCE_APPROVED_FOR_PROMOTION",
                sage_reviewer="Sage",
                hung_vuong_decision="APPROVE_AS_OFFICIAL_CAPABILITY",
                owner_agent="Sage", reviewer_agent="Hung Vuong",
            )

    def test_list_all_and_approved(self, official_registry):
        official_registry.create(
            canonical_capability_id="CCAP-001",
            name="Cap A", description="Test",
            domain="Trading",
            status="APPROVED_AS_OFFICIAL",
            hermes_recommendation="RECOMMEND_PROMOTION",
            hermes_reviewer="Hermes",
            sage_recommendation="GOVERNANCE_APPROVED_FOR_PROMOTION",
            sage_reviewer="Sage",
            hung_vuong_decision="APPROVE_AS_OFFICIAL_CAPABILITY",
            owner_agent="Sage", reviewer_agent="Hung Vuong",
        )
        official_registry.create(
            canonical_capability_id="CCAP-002",
            name="Cap B", description="Test",
            domain="Risk",
            status="HOLD_FOR_EVIDENCE",
            hermes_recommendation="NEEDS_MORE_EVIDENCE",
            hermes_reviewer="Hermes",
            sage_recommendation="GOVERNANCE_HOLD",
            sage_reviewer="Sage",
            hung_vuong_decision="HOLD_FOR_EVIDENCE",
            owner_agent="Sage", reviewer_agent="Hung Vuong",
        )
        assert len(official_registry.list_all()) == 2
        assert len(official_registry.list_approved()) == 1

    def test_record_to_dict(self, official_registry):
        rec = official_registry.create(
            canonical_capability_id="CCAP-001",
            name="Test", description="Test",
            domain="Engineering",
            hermes_recommendation="RECOMMEND_PROMOTION",
            hermes_reviewer="Hermes",
            sage_recommendation="GOVERNANCE_APPROVED_FOR_PROMOTION",
            sage_reviewer="Sage",
            hung_vuong_decision="APPROVE_AS_OFFICIAL_CAPABILITY",
            owner_agent="Sage", reviewer_agent="Hung Vuong",
        )
        d = rec.to_dict()
        assert d["activation_status"] == "DISABLED"
        assert d["agent_adoption_status"] == "NOT_ASSIGNED"
        assert d["evolution_status"] == "LOCKED"

    def test_get_not_found(self, official_registry):
        with pytest.raises(KeyError):
            official_registry.get("NONEXISTENT")
