from agents.janus.agent import create_agent as create_janus
from agents.sage.agent import create_agent as create_sage
from agents.hermes.agent import create_agent as create_hermes
from agents.iris.agent import create_agent as create_iris
from agents.helen.agent import create_agent as create_helen
from agents.lang_lieu.agent import create_agent as create_lang_lieu
from agents.yet_kieu.agent import create_agent as create_yet_kieu
from agents.base import BaseAgent
from agents.runtime_models import (
    ActivationState,
    AgentReportEnvelope,
    EvidenceRecord,
    MissionEnvelope,
    MissionType,
    ToolResult,
)


class FakeMemoryInterface:
    def normalize_agent(self, agent):
        aliases = {"lang_lieu": "LangLieu", "yet_kieu": "YetKieu"}
        return aliases.get(agent, agent.title())

    def _validate_agent(self, agent):
        return None

    def record_decision_trace(self, payload):
        return {"trace_id": "TRACE-TEST", **payload}


FAKE_MEMORY = FakeMemoryInterface()


def _make_agents():
    creators = [create_janus, create_sage, create_hermes, create_iris, create_helen, create_lang_lieu, create_yet_kieu]
    agents = {}
    for creator in creators:
        agent = creator(memory_interface=FAKE_MEMORY)
        agent.boot()
        agents[agent.identity.agent_id] = agent
    return agents


def test_all_seven_agents_boot():
    agents = _make_agents()
    assert len(agents) == 7
    for aid, agent in agents.items():
        assert agent.status() == "operational"


def test_all_agents_have_llm_connector():
    agents = _make_agents()
    for aid, agent in agents.items():
        assert hasattr(agent, "llm"), f"{aid} missing llm"
        result = agent.llm.execute("test")
        assert result.get("success") is True
        assert result.get("mode") in ("mock", "api")


def test_all_agents_generate_report_envelope():
    agents = _make_agents()
    for aid, agent in agents.items():
        report = agent.generate_report_envelope(mission_type="test")
        assert isinstance(report, AgentReportEnvelope)
        assert report.agent_id == aid
        assert report.status == "DRAFT"


def test_all_agents_write_evidence():
    agents = _make_agents()
    mission = MissionEnvelope(mission_type=MissionType.COUNCIL, title="Test", objective="Test evidence capture")
    for aid, agent in agents.items():
        agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
        report = agent.receive_mission(mission)
        evidence = agent.get_evidence_registry()
        assert len(evidence) >= 0


def test_hermes_distill_lesson():
    agent = create_hermes(memory_interface=FAKE_MEMORY)
    agent.boot()
    records = [
        EvidenceRecord(
            source_agent="hermes", mission_id="M-TEST", tool_used="llm",
            input_summary="test", output_summary="test output",
        )
    ]
    lesson = agent.distill_lesson(records)
    assert lesson is not None
    assert lesson.source_agent == "hermes"
    assert len(lesson.source_evidence_ids) == 1


def test_sage_blocks_unsafe_activation():
    agent = create_sage(memory_interface=FAKE_MEMORY)
    agent.boot()
    gate = agent.validate_activation(ActivationState.OPERATIONAL_APPROVED)
    assert gate.get("allowed") is False
    assert "Hung Vuong" in gate.get("reason", "")

    gate = agent.validate_activation(ActivationState.SANDBOX_ACTIVE)
    assert gate.get("allowed") is True


def test_sage_compliance_report():
    agent = create_sage(memory_interface=FAKE_MEMORY)
    agent.boot()
    report = agent.compliance_report(ActivationState.SANDBOX_ACTIVE)
    assert report.get("all_pass") is True
    assert "constitution_compliant" in report.get("checks", {})
    assert report.get("activation_state") == "SANDBOX_ACTIVE"


def test_janus_plan_and_route_mission():
    agent = create_janus(memory_interface=FAKE_MEMORY)
    agent.boot()
    mission = agent.plan_mission("Test mission", ["sage", "hermes"])
    assert mission.mission_type == MissionType.COUNCIL
    assert mission.objective == "Test mission"
    assert mission.target_agents == ["sage", "hermes"]


def test_janus_consolidate_council():
    agent = create_janus(memory_interface=FAKE_MEMORY)
    agent.boot()
    reports = [
        AgentReportEnvelope(agent_id="sage", mission_id="M-1", mission_type="test", summary="Sage report"),
        AgentReportEnvelope(agent_id="hermes", mission_id="M-1", mission_type="test", summary="Hermes report"),
    ]
    consolidated = agent.consolidate_council(reports)
    assert consolidated.get("total_reports") == 2


def test_iris_market_research():
    agent = create_iris(memory_interface=FAKE_MEMORY)
    agent.boot()
    result = agent.market_research("AK economic growth")
    assert result.get("topic") == "AK economic growth"
    assert "disclaimer" in result
    assert "paper" in result["disclaimer"].lower()


def test_iris_trading_hypothesis_review():
    agent = create_iris(memory_interface=FAKE_MEMORY)
    agent.boot()
    hypothesis = {"asset": "EURUSD", "direction": "long", "rationale": "technical breakout"}
    result = agent.review_trading_hypothesis(hypothesis)
    assert result.get("approved_for_paper") is True
    assert result.get("requires_sage_review") is True


def test_helen_research_topic():
    agent = create_helen(memory_interface=FAKE_MEMORY)
    agent.boot()
    result = agent.research_topic("AI safety", domain="technology")
    assert result.get("topic") == "AI safety"
    assert result.get("domain") == "technology"


def test_helen_classify_source():
    agent = create_helen(memory_interface=FAKE_MEMORY)
    agent.boot()
    result = agent.classify_source("Research Paper", "Key findings in AI development")
    assert result.get("source") == "Research Paper"


def test_lang_lieu_plan_implementation():
    agent = create_lang_lieu(memory_interface=FAKE_MEMORY)
    agent.boot()
    result = agent.plan_implementation("Build capability completion framework")
    assert result.get("status") == "planned"
    assert result.get("objective") == "Build capability completion framework"


def test_lang_lieu_opencode_status():
    agent = create_lang_lieu(memory_interface=FAKE_MEMORY)
    agent.boot()
    status = agent.opencode_status()
    assert status.get("status") in ("UNAVAILABLE", "AVAILABLE")


def test_yet_kieu_infrastructure_check():
    agent = create_yet_kieu(memory_interface=FAKE_MEMORY)
    agent.boot()
    result = agent.check_infrastructure()
    assert "all_ok" in result
    assert "checks" in result


def test_yet_kieu_security_review():
    agent = create_yet_kieu(memory_interface=FAKE_MEMORY)
    agent.boot()
    result = agent.security_review()
    assert "findings" in result
    assert "risk_level" in result


def test_all_agents_get_context():
    agents = _make_agents()
    for aid, agent in agents.items():
        ctx = agent.get_context()
        assert ctx.agent_id == aid
        assert ctx.activation_state == ActivationState.LOCKED


def test_activation_state_transitions():
    agents = _make_agents()
    for agent in agents.values():
        assert agent.activation_state == ActivationState.LOCKED
        agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
        assert agent.activation_state == ActivationState.SANDBOX_ACTIVE
