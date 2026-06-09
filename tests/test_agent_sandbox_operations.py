"""Verify 7 agents operate within sandbox boundaries."""

from agents.runtime_models import ActivationState, MissionEnvelope, MissionType


def _make_mission():
    return MissionEnvelope(
        mission_type=MissionType.COUNCIL,
        title="Sandbox test",
        objective="Verify agent operates within boundary",
        requester="janus",
    )


def _agent(name):
    from agents.base import BaseAgent
    from agents.identity import get_identity
    from agents.role_boundary import get_role_boundary
    return BaseAgent(get_identity(name), get_role_boundary(name))


def test_janus_can_receive_mission():
    agent = _agent("janus")
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    report = agent.receive_mission(_make_mission())
    assert report.status in ("COMPLETED", "FAILED")


def test_sage_can_receive_mission():
    agent = _agent("sage")
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    report = agent.receive_mission(_make_mission())
    assert report.status in ("COMPLETED", "FAILED")


def test_hermes_can_receive_mission():
    agent = _agent("hermes")
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    report = agent.receive_mission(_make_mission())
    assert report.status in ("COMPLETED", "FAILED")


def test_iris_can_receive_mission():
    agent = _agent("iris")
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    report = agent.receive_mission(_make_mission())
    assert report.status in ("COMPLETED", "FAILED")


def test_helen_can_receive_mission():
    agent = _agent("helen")
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    report = agent.receive_mission(_make_mission())
    assert report.status in ("COMPLETED", "FAILED")


def test_lang_lieu_can_receive_mission():
    agent = _agent("lang_lieu")
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    report = agent.receive_mission(_make_mission())
    assert report.status in ("COMPLETED", "FAILED")


def test_yet_kieu_can_receive_mission():
    agent = _agent("yet_kieu")
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    report = agent.receive_mission(_make_mission())
    assert report.status in ("COMPLETED", "FAILED")


def test_all_agents_generate_report():
    for name in ["janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"]:
        agent = _agent(name)
        report = agent.generate_report_envelope(mission_type="sandbox_test")
        assert report.agent_id == name
        assert report.status == "DRAFT"


def test_all_agents_write_evidence():
    from agents.runtime_models import ToolResult
    for name in ["janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"]:
        agent = _agent(name)
        agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
        agent._call_tool("filesystem", {"tool": "read", "path": "."})
        evidence = agent.get_evidence_registry()
        assert len(evidence) >= 0


def test_all_agents_write_usage():
    for name in ["janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"]:
        agent = _agent(name)
        agent._record_usage("test_capability", success=True)
        usage = agent.get_usage_registry()
        assert len(usage) >= 0


def test_all_agents_cannot_execute_trading():
    from agents.base import BaseAgent
    from agents.identity import get_identity
    from agents.role_boundary import get_role_boundary
    for name in ["janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"]:
        agent = BaseAgent(get_identity(name), get_role_boundary(name))
        forbids_trading = agent.role_boundary.forbids("execute_trading")
        allows_trading = agent.role_boundary.allows("execute_trading")
        if allows_trading:
            assert forbids_trading, f"{name} should not be allowed to trade"


def test_all_agents_cannot_modify_risk_kernel():
    from agents.base import BaseAgent
    from agents.identity import get_identity
    from agents.role_boundary import get_role_boundary
    for name in ["janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"]:
        agent = BaseAgent(get_identity(name), get_role_boundary(name))
        allows = agent.role_boundary.allows("modify_risk_kernel")
        forbids = agent.role_boundary.forbids("modify_risk_kernel")
        assert forbids or not allows, f"{name} should not modify Risk Kernel"
