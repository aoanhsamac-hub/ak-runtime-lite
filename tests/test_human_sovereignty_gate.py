from agents.runtime_models import ActivationState


def test_opencode_can_set_ready_for_sandbox():
    allowed = {ActivationState.LOCKED, ActivationState.READY_FOR_SANDBOX}
    assert ActivationState.READY_FOR_SANDBOX in allowed
    assert ActivationState.SANDBOX_ACTIVE not in allowed


def test_opencode_cannot_set_sandbox_active():
    from agents.runtime_models import ActivationState
    allowed = {ActivationState.LOCKED, ActivationState.READY_FOR_SANDBOX}
    assert ActivationState.SANDBOX_ACTIVE not in allowed


def test_opencode_cannot_set_pilot_active():
    allowed = {ActivationState.LOCKED, ActivationState.READY_FOR_SANDBOX}
    assert ActivationState.PILOT_ACTIVE not in allowed


def test_opencode_cannot_set_operational_limited():
    allowed = {ActivationState.LOCKED, ActivationState.READY_FOR_SANDBOX}
    assert ActivationState.OPERATIONAL_LIMITED not in allowed


def test_opencode_cannot_set_operational_approved():
    allowed = {ActivationState.LOCKED, ActivationState.READY_FOR_SANDBOX}
    assert ActivationState.OPERATIONAL_APPROVED not in allowed


def test_human_approval_required_for_sandbox_active():
    from agents.base import BaseAgent
    from agents.identity import get_identity
    from agents.role_boundary import get_role_boundary
    agent = BaseAgent(get_identity("iris"), get_role_boundary("iris"))
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    assert agent.activation_state == ActivationState.SANDBOX_ACTIVE


def test_locked_is_default():
    from agents.base import BaseAgent
    from agents.identity import get_identity
    from agents.role_boundary import get_role_boundary
    for agent_id in ["janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"]:
        agent = BaseAgent(get_identity(agent_id), get_role_boundary(agent_id))
        assert agent.activation_state == ActivationState.LOCKED, f"{agent_id} should start LOCKED"


def test_sovereignty_gate_blocks_execution_when_locked():
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
    assert report.status == "LOCKED" or "cannot accept" in report.summary.lower()


def test_readiness_check_requires_data():
    from memory.kingdom_memory_platform import KingdomMemoryPlatform
    mp = KingdomMemoryPlatform()
    result = mp.check_activation_readiness()
    assert isinstance(result, dict)
    assert "ready" in result
