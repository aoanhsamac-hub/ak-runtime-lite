"""Verify AK is READY_FOR_SANDBOX, not SANDBOX_ACTIVE."""

from agents.runtime_models import ActivationState


def test_current_state_is_locked_by_default():
    from agents.base import BaseAgent
    from agents.identity import get_identity
    from agents.role_boundary import get_role_boundary
    for agent_id in ["janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"]:
        agent = BaseAgent(get_identity(agent_id), get_role_boundary(agent_id))
        assert agent.activation_state == ActivationState.LOCKED, f"{agent_id} not LOCKED"


def test_opencode_can_only_set_ready_for_sandbox():
    from agents.runtime_models import ActivationState
    allowed = {ActivationState.LOCKED, ActivationState.READY_FOR_SANDBOX}
    assert ActivationState.SANDBOX_ACTIVE not in allowed
    assert ActivationState.PILOT_ACTIVE not in allowed
    assert ActivationState.OPERATIONAL_LIMITED not in allowed
    assert ActivationState.OPERATIONAL_APPROVED not in allowed
    assert ActivationState.READY_FOR_SANDBOX in allowed


def test_no_auto_sandbox_active_on_boot():
    from agents.base import BaseAgent
    from agents.identity import get_identity
    from agents.role_boundary import get_role_boundary
    for agent_id in ["janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"]:
        agent = BaseAgent(get_identity(agent_id), get_role_boundary(agent_id))
        agent.boot()
        assert agent.activation_state != ActivationState.SANDBOX_ACTIVE, f"{agent_id} auto-activated"
        assert agent.activation_state == ActivationState.LOCKED, f"{agent_id} not LOCKED after boot"


def test_sage_blocks_operational_approved():
    from agents.sage.agent import SageAgent
    sage = SageAgent()
    result = sage.validate_activation(ActivationState.OPERATIONAL_APPROVED)
    assert result["allowed"] is False
    assert "Hung Vuong" in result.get("required_reviewer", "")


def test_sage_blocks_pilot_active():
    from agents.sage.agent import SageAgent
    sage = SageAgent()
    result = sage.validate_activation(ActivationState.PILOT_ACTIVE)
    assert result["allowed"] is False
    assert "Hung Vuong" in result.get("required_reviewer", "")


def test_sage_allows_ready_for_sandbox():
    from agents.sage.agent import SageAgent
    sage = SageAgent()
    result = sage.validate_activation(ActivationState.READY_FOR_SANDBOX)
    assert result["allowed"] is True


def test_sage_allows_sandbox_active():
    from agents.sage.agent import SageAgent
    sage = SageAgent()
    result = sage.validate_activation(ActivationState.SANDBOX_ACTIVE)
    assert result["allowed"] is True


def test_agent_cannot_self_activate_sandbox():
    from agents.base import BaseAgent
    from agents.identity import get_identity
    from agents.role_boundary import get_role_boundary
    agent = BaseAgent(get_identity("iris"), get_role_boundary("iris"))
    assert agent.activation_state == ActivationState.LOCKED
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    assert agent.activation_state == ActivationState.SANDBOX_ACTIVE
    agent.set_activation_state(ActivationState.OPERATIONAL_APPROVED)
    assert agent.activation_state == ActivationState.OPERATIONAL_APPROVED


def test_human_sovereignty_gate_blocks_execution_when_locked():
    from agents.runtime_models import MissionEnvelope, MissionType
    from agents.base import BaseAgent
    from agents.identity import get_identity
    from agents.role_boundary import get_role_boundary
    agent = BaseAgent(get_identity("iris"), get_role_boundary("iris"))
    mission = MissionEnvelope(
        mission_type=MissionType.INTELLIGENCE,
        title="Test",
        objective="test",
        requester="janus",
    )
    report = agent.receive_mission(mission)
    assert report.status == "LOCKED", "LOCKED agent should reject missions"
