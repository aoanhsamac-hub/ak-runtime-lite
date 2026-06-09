from agents.base import BaseAgent
from agents.hermes.agent import create_agent as create_hermes
from agents.helen.agent import create_agent as create_helen
from agents.iris.agent import create_agent as create_iris
from agents.janus.agent import create_agent as create_janus
from agents.lang_lieu.agent import create_agent as create_lang_lieu
from agents.sage.agent import create_agent as create_sage
from agents.yet_kieu.agent import create_agent as create_yet_kieu


class FakeMemoryInterface:
    def normalize_agent(self, agent):
        aliases = {"lang_lieu": "LangLieu", "yet_kieu": "YetKieu"}
        return aliases.get(agent, agent.title())

    def _validate_agent(self, agent):
        return None

    def record_decision_trace(self, payload):
        return {"trace_id": "TRACE-TEST", **payload}


def test_all_seven_agents_boot_operational():
    creators = [create_janus, create_sage, create_hermes, create_iris, create_helen, create_lang_lieu, create_yet_kieu]
    agents = [creator(memory_interface=FakeMemoryInterface()) for creator in creators]
    assert all(isinstance(agent, BaseAgent) for agent in agents)
    assert all(agent.boot()["status"] == "operational" for agent in agents)
    assert all(agent.get_identity() is not None for agent in agents)
    assert all(agent.get_role_boundary() is not None for agent in agents)


def test_lang_lieu_opencode_unavailable_safe():
    agent = create_lang_lieu(memory_interface=FakeMemoryInterface())
    status = agent.opencode_status()
    assert status.get("status") in {"UNAVAILABLE", "AVAILABLE"}
