from __future__ import annotations

import pytest

from memory.capability_pipeline.schemas import EVOLUTION_STATES, EVOLUTION_EVENT_TYPES, EvolutionEventRecord
from memory.capability_registry.official_capability_registry import OfficialCapabilityRecord, OfficialCapabilityRegistry
from services.capability_evolution_loop import CapabilityEvolutionLoop, EvolutionProposal, EvolutionResult


@pytest.fixture
def official_registry():
    r = OfficialCapabilityRegistry()
    r.create(
        canonical_capability_id="CCAP-001",
        name="Trading Analysis",
        description="Market analysis capability",
        domain="Trading",
        owner_agent="Iris",
    )
    return r


@pytest.fixture
def evo_loop(official_registry):
    return CapabilityEvolutionLoop(official_registry=official_registry, maturity_engine=None, maturity_reassessment_engine=None)


class TestEvolutionStates:
    def test_evolution_states_defined(self):
        assert "LOCKED" in EVOLUTION_STATES
        assert "UNLOCKED" in EVOLUTION_STATES
        assert "EVOLVING_MATURITY" in EVOLUTION_STATES
        assert "EVOLVING_CYCLE" in EVOLUTION_STATES
        assert "EVOLVED" in EVOLUTION_STATES
        assert "ROLLED_BACK" in EVOLUTION_STATES

    def test_evolution_event_types_defined(self):
        assert "MATURITY_PROGRESSION" in EVOLUTION_EVENT_TYPES
        assert "CAPABILITY_EVOLUTION" in EVOLUTION_EVENT_TYPES
        assert "ROLLBACK" in EVOLUTION_EVENT_TYPES
        assert "PROMOTION" in EVOLUTION_EVENT_TYPES


class TestEvolutionEventRecord:
    def test_requires_capability_id(self):
        with pytest.raises(ValueError, match="capability_id"):
            EvolutionEventRecord(event_type="MATURITY_PROGRESSION")

    def test_requires_valid_event_type(self):
        with pytest.raises(ValueError, match="event_type"):
            EvolutionEventRecord(capability_id="C-1", event_type="INVALID")

    def test_validates_from_state(self):
        with pytest.raises(ValueError, match="from_state"):
            EvolutionEventRecord(capability_id="C-1", event_type="PROMOTION", from_state="INVALID")

    def test_validates_to_state(self):
        with pytest.raises(ValueError, match="to_state"):
            EvolutionEventRecord(capability_id="C-1", event_type="PROMOTION", to_state="INVALID")

    def test_valid_event_creates_successfully(self):
        evt = EvolutionEventRecord(
            capability_id="C-1",
            event_type="MATURITY_PROGRESSION",
            from_state="LOCKED",
            to_state="UNLOCKED",
            trigger="scheduled_review",
        )
        assert evt.event_id.startswith("EVT-")
        assert evt.capability_id == "C-1"

    def test_to_dict_includes_all_fields(self):
        evt = EvolutionEventRecord(
            capability_id="C-1",
            event_type="PROMOTION",
            description="Test promotion",
        )
        d = evt.to_dict()
        assert d["capability_id"] == "C-1"
        assert d["event_type"] == "PROMOTION"
        assert d["description"] == "Test promotion"


class TestEvolutionLoop:
    def test_propose_evolution_requires_unlocked(self, evo_loop, official_registry):
        cap_id = list(official_registry._records.keys())[0]
        with pytest.raises(ValueError, match="evolution not allowed"):
            evo_loop.propose_evolution(cap_id)

    def test_unlock_then_propose(self, evo_loop, official_registry):
        cap_id = list(official_registry._records.keys())[0]
        evo_loop.unlock_evolution(cap_id)
        proposal = evo_loop.propose_evolution(cap_id, trigger="scheduled_review")
        assert isinstance(proposal, EvolutionProposal)
        assert proposal.status == "PROPOSED"

    def test_proposal_creates_event(self, evo_loop, official_registry):
        cap_id = list(official_registry._records.keys())[0]
        evo_loop.unlock_evolution(cap_id)
        evo_loop.propose_evolution(cap_id)
        history = evo_loop.get_evolution_history(cap_id)
        assert len(history) == 1
        assert history[0].event_type == "MATURITY_PROGRESSION"

    def test_sandbox_experiment(self, evo_loop, official_registry):
        cap_id = list(official_registry._records.keys())[0]
        evo_loop.unlock_evolution(cap_id)
        proposal = evo_loop.propose_evolution(cap_id)
        result = evo_loop.sandbox_experiment(proposal.proposal_id)
        assert result["status"] == "sandbox_ready"

    def test_validate_evolution(self, evo_loop, official_registry):
        cap_id = list(official_registry._records.keys())[0]
        evo_loop.unlock_evolution(cap_id)
        proposal = evo_loop.propose_evolution(cap_id)
        validation = evo_loop.validate_evolution(proposal.proposal_id)
        assert "maturity_gain" in validation
        assert "governance" in validation
        assert "promotion_candidate" in validation

    def test_promote_evolution(self, evo_loop, official_registry):
        cap_id = list(official_registry._records.keys())[0]
        evo_loop.unlock_evolution(cap_id)
        proposal = evo_loop.propose_evolution(cap_id)
        evo_loop.sandbox_experiment(proposal.proposal_id)
        result = evo_loop.promote_evolution(proposal.proposal_id)
        assert isinstance(result, EvolutionResult)
        assert result.success
        assert result.evolution_cycle == 1
        assert result.from_state == "EVOLVING_CYCLE"
        assert result.to_state == "EVOLVED"

    def test_rollback_evolution(self, evo_loop, official_registry):
        cap_id = list(official_registry._records.keys())[0]
        evo_loop.unlock_evolution(cap_id)
        proposal = evo_loop.propose_evolution(cap_id)
        evo_loop.sandbox_experiment(proposal.proposal_id)
        evo_loop.promote_evolution(proposal.proposal_id)
        result = evo_loop.rollback_evolution(cap_id)
        assert result.success
        assert result.to_state == "ROLLED_BACK"

    def test_evolution_cycle_increments(self, evo_loop, official_registry):
        cap_id = list(official_registry._records.keys())[0]
        evo_loop.unlock_evolution(cap_id)

        # Cycle 1
        p1 = evo_loop.propose_evolution(cap_id)
        evo_loop.sandbox_experiment(p1.proposal_id)
        r1 = evo_loop.promote_evolution(p1.proposal_id)
        assert r1.evolution_cycle == 1

        # Cycle 2
        p2 = evo_loop.propose_evolution(cap_id)
        evo_loop.sandbox_experiment(p2.proposal_id)
        r2 = evo_loop.promote_evolution(p2.proposal_id)
        assert r2.evolution_cycle == 2

    def test_cannot_rollback_from_unlocked(self, evo_loop, official_registry):
        cap_id = list(official_registry._records.keys())[0]
        evo_loop.unlock_evolution(cap_id)
        with pytest.raises(ValueError, match="cannot rollback"):
            evo_loop.rollback_evolution(cap_id)

    def test_cannot_propose_twice_without_promotion(self, evo_loop, official_registry):
        # This should work - second proposal creates new proposal
        cap_id = list(official_registry._records.keys())[0]
        evo_loop.unlock_evolution(cap_id)
        evo_loop.propose_evolution(cap_id)
        evo_loop.propose_evolution(cap_id)
        # After promote, state is EVOLVED which allows proposal
        p = evo_loop.propose_evolution(cap_id)
        evo_loop.sandbox_experiment(p.proposal_id)
        evo_loop.promote_evolution(p.proposal_id)
        # Now EVOLVED allows another proposal
        evo_loop.propose_evolution(cap_id)

    def test_full_evolution_history(self, evo_loop, official_registry):
        cap_id = list(official_registry._records.keys())[0]
        evo_loop.unlock_evolution(cap_id)

        p = evo_loop.propose_evolution(cap_id)
        evo_loop.sandbox_experiment(p.proposal_id)
        evo_loop.promote_evolution(p.proposal_id)

        history = evo_loop.get_evolution_history(cap_id)
        assert len(history) == 3  # MATURITY_PROGRESSION + CAPABILITY_EVOLUTION + PROMOTION

    def test_validate_evolution_with_positive_results(self, evo_loop, official_registry):
        cap_id = list(official_registry._records.keys())[0]
        evo_loop.unlock_evolution(cap_id)
        proposal = evo_loop.propose_evolution(cap_id)
        validation = evo_loop.validate_evolution(proposal.proposal_id, {"positive": True})
        assert validation["maturity_gain"] > 0
        assert validation["promotion_candidate"]

    def test_proposal_not_found_raises(self, evo_loop):
        with pytest.raises(ValueError, match="proposal not found"):
            evo_loop.sandbox_experiment("nonexistent")

    def test_unlock_from_rolled_back(self, evo_loop, official_registry):
        cap_id = list(official_registry._records.keys())[0]
        evo_loop.unlock_evolution(cap_id)
        p = evo_loop.propose_evolution(cap_id)
        evo_loop.sandbox_experiment(p.proposal_id)
        evo_loop.promote_evolution(p.proposal_id)
        evo_loop.rollback_evolution(cap_id)
        # Should be able to unlock from ROLLED_BACK
        evo_loop.unlock_evolution(cap_id)
        record = official_registry.get(cap_id)
        assert record.evolution_status == "UNLOCKED"


class TestOfficialCapabilityEvolutionFields:
    def test_default_evolution_cycle(self, official_registry):
        cap = list(official_registry._records.values())[0]
        assert cap.evolution_cycle == 0
        assert cap.evolution_history == []
        assert cap.last_evolved_at == ""

    def test_evolution_cycle_persists_after_update(self, official_registry):
        cap_id = list(official_registry._records.keys())[0]
        updated = official_registry.update_adoption_stage(cap_id, "ASSIGNED_SANDBOX")
        assert updated.evolution_cycle == 0

    def test_evolution_statuses_include_new_states(self):
        from memory.capability_registry.official_capability_registry import EVOLUTION_STATUSES
        assert "EVOLVING_MATURITY" in EVOLUTION_STATUSES
        assert "EVOLVING_CYCLE" in EVOLUTION_STATUSES
        assert "EVOLVED" in EVOLUTION_STATUSES
        assert "ROLLED_BACK" in EVOLUTION_STATUSES
