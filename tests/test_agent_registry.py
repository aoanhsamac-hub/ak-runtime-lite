from agents.registry import AgentRegistry


def test_agent_registry_validates_all_agents():
    registry = AgentRegistry()
    assert len(registry.list_agents()) == 7
    assert all(registry.validate_agent(agent_id)["valid"] for agent_id in registry.list_agents())
