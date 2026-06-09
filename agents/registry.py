from __future__ import annotations

from agents.identity import AGENT_IDENTITIES, get_identity
from agents.role_boundary import ROLE_BOUNDARIES, get_role_boundary


AGENT_MODULES = {
    "janus": "agents.janus.agent",
    "sage": "agents.sage.agent",
    "hermes": "agents.hermes.agent",
    "iris": "agents.iris.agent",
    "helen": "agents.helen.agent",
    "lang_lieu": "agents.lang_lieu.agent",
    "yet_kieu": "agents.yet_kieu.agent",
}


class AgentRegistry:
    def list_agents(self) -> list[str]:
        return list(AGENT_IDENTITIES.keys())

    def get_identity(self, agent_id: str):
        return get_identity(agent_id)

    def get_role_boundary(self, agent_id: str):
        return get_role_boundary(agent_id)

    def validate_agent(self, agent_id: str) -> dict:
        return {
            "valid": agent_id in AGENT_IDENTITIES and agent_id in ROLE_BOUNDARIES,
            "agent_id": agent_id,
            "identity": agent_id in AGENT_IDENTITIES,
            "role_boundary": agent_id in ROLE_BOUNDARIES,
        }


def registry_status() -> dict:
    registry = AgentRegistry()
    return {agent_id: registry.validate_agent(agent_id) for agent_id in registry.list_agents()}
