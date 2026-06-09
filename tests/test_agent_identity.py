from agents.identity import AGENT_IDENTITIES, AgentIdentity


def test_all_seven_agents_have_identity():
    assert set(AGENT_IDENTITIES) == {"janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"}
    assert all(isinstance(identity, AgentIdentity) for identity in AGENT_IDENTITIES.values())
    assert all(identity.status == "operational" for identity in AGENT_IDENTITIES.values())
