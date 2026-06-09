from agents.janus.agent import create_agent as create_janus
from agents.sage.agent import create_agent as create_sage
from agents.hermes.agent import create_agent as create_hermes
from agents.iris.agent import create_agent as create_iris
from agents.helen.agent import create_agent as create_helen
from agents.lang_lieu.agent import create_agent as create_lang_lieu
from agents.yet_kieu.agent import create_agent as create_yet_kieu
from agents.runtime_models import ActivationState, MissionEnvelope, MissionType
from workflows.mission_runtime import MissionRuntime
from workflows.council_review import CouncilReview
from memory.learning_runtime import LearningRuntime
from memory.evidence_registry import EvidenceRegistry
from memory.usage_registry import CapabilityUsageRegistry
from memory.learning_runtime import LessonCandidateRegistry, AgentPerformanceRegistry


class FakeMemoryInterface:
    def normalize_agent(self, agent):
        aliases = {"lang_lieu": "LangLieu", "yet_kieu": "YetKieu"}
        return aliases.get(agent, agent.title())

    def _validate_agent(self, agent):
        return None

    def record_decision_trace(self, payload):
        return {"trace_id": "TRACE-ACTIVATE", **payload}


FAKE_MEMORY = FakeMemoryInterface()


def _setup_agents():
    creators = [create_janus, create_sage, create_hermes, create_iris, create_helen, create_lang_lieu, create_yet_kieu]
    agents = {}
    for creator in creators:
        agent = creator(memory_interface=FAKE_MEMORY)
        agent.boot()
        agents[agent.identity.agent_id] = agent
    return agents


def test_default_state_is_locked():
    agents = _setup_agents()
    for aid, agent in agents.items():
        assert agent.activation_state == ActivationState.LOCKED


def test_can_set_sandbox_active():
    agents = _setup_agents()
    for agent in agents.values():
        result = agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
        assert result["activation_state"] == "SANDBOX_ACTIVE"
        assert agent.activation_state == ActivationState.SANDBOX_ACTIVE


def test_sage_controls_activation_gate():
    sage = create_sage(memory_interface=FAKE_MEMORY)
    sage.boot()

    assert sage.validate_activation(ActivationState.OPERATIONAL_APPROVED)["allowed"] is False
    assert sage.validate_activation(ActivationState.OPERATIONAL_LIMITED)["allowed"] is False
    assert sage.validate_activation(ActivationState.PILOT_ACTIVE)["allowed"] is False
    assert sage.validate_activation(ActivationState.SANDBOX_ACTIVE)["allowed"] is True
    assert sage.validate_activation(ActivationState.READY_FOR_SANDBOX)["allowed"] is True


def test_janus_checks_all_agents_ready():
    agents = _setup_agents()
    janus = agents["janus"]
    result = janus.check_all_agents_ready(agents)
    assert result["all_ready"] is False  # all LOCKED

    for agent in agents.values():
        agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)

    result = janus.check_all_agents_ready(agents)
    assert result["all_ready"] is True


def test_mission_runtime_activation_mission():
    agents = _setup_agents()
    fake_evidence = type("FakeER", (), {
        "record_evidence": lambda self, r: r,
        "get_all": lambda self: [{"evidence_id": f"EV-{i:03d}"} for i in range(7)],
        "summary": lambda self: {"total_evidence": 7, "unique_agents": 1, "classifications": []},
    })()
    fake_lessons = type("FakeLR", (), {
        "record_lesson": lambda self, r: r,
        "get_all": lambda self: [{"lesson_id": "LS-001"}],
        "summary": lambda self: {"total_lessons": 1, "unique_agents": 1},
    })()
    fake_usage = type("FakeUR", (), {
        "record_usage": lambda self, r: r,
        "get_all": lambda self: [{"agent_id": f"agent_{i}", "capability_name": "test", "success": True} for i in range(7)],
        "summary": lambda self: {"total_usages": 7, "success_count": 7, "success_rate": 1.0, "unique_agents": 7, "agents": [f"agent_{i}" for i in range(7)]},
    })()
    fake_perf = type("FakePR", (), {
        "record_performance": lambda self, r: r,
        "get_all": lambda self: [],
        "summary": lambda self: {"total_records": 0, "unique_agents": 0},
    })()

    learning = LearningRuntime(
        evidence_registry=fake_evidence,
        lesson_registry=fake_lessons,
        usage_registry=fake_usage,
        performance_registry=fake_perf,
    )
    runtime = MissionRuntime(agents, learning)

    result = runtime.run_activation_mission()
    assert result["status"] in ("SANDBOX_ACTIVE", "BLOCKED")


def test_council_review_assess_readiness():
    agents = _setup_agents()
    council = CouncilReview(agents)

    for agent in agents.values():
        agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)

    result = council.assess_readiness()
    assert "agent_readiness" in result


def test_locked_agents_cannot_receive_missions():
    agent = create_sage(memory_interface=FAKE_MEMORY)
    agent.boot()
    mission = MissionEnvelope(
        mission_type=MissionType.GOVERNANCE,
        title="Test",
        objective="Test locked state",
        target_agents=["sage"],
    )
    report = agent.receive_mission(mission)
    assert report.status == "LOCKED"


def test_sandbox_agents_can_receive_missions():
    agent = create_sage(memory_interface=FAKE_MEMORY)
    agent.boot()
    agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
    mission = MissionEnvelope(
        mission_type=MissionType.GOVERNANCE,
        title="Test",
        objective="Test sandbox state",
        target_agents=["sage"],
    )
    report = agent.receive_mission(mission)
    assert report.status == "COMPLETED"


def test_activation_gate_requires_evidence():
    agents = _setup_agents()
    learning = LearningRuntime()
    runtime = MissionRuntime(agents, learning)

    result = runtime.run_activation_mission()
    assert result["status"] == "BLOCKED"
    assert "Missing" in result.get("reason", "") or "Missing" in str(result.get("readiness", {}))


def test_sage_compliance_for_sandbox():
    sage = create_sage(memory_interface=FAKE_MEMORY)
    sage.boot()
    compliance = sage.compliance_report(ActivationState.SANDBOX_ACTIVE)
    assert compliance["all_pass"] is True
    assert compliance["activation_state"] == "SANDBOX_ACTIVE"
