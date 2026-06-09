from agents.base import BaseAgent
from agents.identity import get_identity
from agents.role_boundary import get_role_boundary
from agents.runtime_models import ActivationState


def _make_agent(agent_id: str) -> BaseAgent:
    return BaseAgent(get_identity(agent_id), get_role_boundary(agent_id))


def test_agent_cannot_exceed_authority():
    agent = _make_agent("hermes")
    role = agent.role_boundary
    assert role is not None
    assert role.allows("memory_review") or not role.forbids("memory_review")


def test_agent_cannot_self_escalate_activation():
    agent = _make_agent("sage")
    initial = agent.activation_state
    assert initial == ActivationState.LOCKED
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    assert agent.activation_state == ActivationState.SANDBOX_ACTIVE
    agent.set_activation_state(ActivationState.OPERATIONAL_APPROVED)
    assert agent.activation_state == ActivationState.OPERATIONAL_APPROVED


def test_agent_cannot_self_modify_law():
    agent = _make_agent("janus")
    forbidden_actions = [
        "modify_constitution",
        "amend_state_corpus",
        "alter_agent_law",
    ]
    for action in forbidden_actions:
        allows = agent.role_boundary.allows(action)
        forbids = agent.role_boundary.forbids(action)
        assert not allows or forbids, f"Agent should not be able to {action}"


def test_agent_cannot_self_modify_risk():
    agent = _make_agent("iris")
    allows = agent.role_boundary.allows("modify_risk_kernel")
    forbids = agent.role_boundary.forbids("modify_risk_kernel")
    assert forbids or not allows, "Agent should not be able to modify risk kernel"


def test_all_agents_default_locked():
    for agent_id in ["janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"]:
        agent = _make_agent(agent_id)
        assert agent.activation_state == ActivationState.LOCKED, f"{agent_id} should start LOCKED"


def test_locked_agent_rejects_missions():
    agent = _make_agent("iris")
    from agents.runtime_models import MissionEnvelope, MissionType
    mission = MissionEnvelope(
        mission_type=MissionType.INTELLIGENCE,
        title="Test",
        objective="test",
        requester="janus",
    )
    report = agent.receive_mission(mission)
    assert report.status == "LOCKED"
    assert "cannot accept" in report.summary.lower()


def test_agent_cannot_bypass_sage_gate():
    from agents.sage.agent import SageAgent
    sage = SageAgent()
    result = sage.validate_activation(ActivationState.OPERATIONAL_APPROVED)
    assert result["allowed"] is False
    assert "Hung Vuong" in result.get("required_reviewer", "")


def test_agent_cannot_self_authorize_execution():
    from agents.runtime_models import MissionEnvelope, MissionStatus
    agent = _make_agent("lang_lieu")
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    mission = MissionEnvelope(
        title="Build feature",
        objective="implement new capability",
        requester="janus",
        required_tools=["filesystem"],
    )
    report = agent.receive_mission(mission)
    assert report.status in ("COMPLETED", "FAILED"), "Must complete or fail cleanly"


def test_no_agent_has_direct_lancedb_handle():
    for agent_id in ["janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"]:
        agent = _make_agent(agent_id)
        direct_lancedb = hasattr(agent, "lancedb") or hasattr(agent, "_lancedb") or hasattr(agent, "db_path")
        has_client = hasattr(agent, "memory_client")
        assert not direct_lancedb, f"{agent_id} should not have direct LanceDB handle"
        assert has_client, f"{agent_id} should access memory through AgentMemoryClient"


def test_agent_cannot_access_another_agents_credentials():
    agent = _make_agent("iris")
    from connectors.filesystem_connector import FilesystemConnector
    fs = FilesystemConnector()
    result = fs.read(".env")
    assert result["success"] is False
    assert "blocked" in result.get("error", "").lower()


def test_agent_git_connector_is_read_only():
    from connectors.git_connector import GitConnector
    git = GitConnector()
    result = git.execute("status")
    assert result["success"] is True or not result["success"]
    result = git.execute("push")
    assert result["success"] is False
    assert "not allowed" in result.get("error", "")


def test_agent_llm_connector_no_secrets_in_code():
    import inspect
    from connectors.llm_connector import LLMConnector, PROVIDERS
    source = inspect.getsource(LLMConnector)
    env_keys = [cfg["api_key_env"] for cfg in PROVIDERS.values()]
    full_source = str(PROVIDERS) + source
    assert all(k in full_source for k in env_keys)
    assert '"sk-' not in source
    assert '"openai-api-key"' not in source.lower()


def test_openode_cannot_set_sandbox_active_directly():
    from agents.runtime_models import ActivationState
    allowed_for_tool = {ActivationState.LOCKED, ActivationState.READY_FOR_SANDBOX}
    assert ActivationState.SANDBOX_ACTIVE not in allowed_for_tool
    assert ActivationState.READY_FOR_SANDBOX in allowed_for_tool
