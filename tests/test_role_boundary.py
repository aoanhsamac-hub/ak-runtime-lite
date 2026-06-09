from agents.role_boundary import ROLE_BOUNDARIES


def test_all_seven_agents_have_role_boundary():
    assert set(ROLE_BOUNDARIES) == {"janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"}


def test_forbidden_actions_enforced():
    assert ROLE_BOUNDARIES["iris"].forbids("live_execution")
    assert ROLE_BOUNDARIES["lang_lieu"].forbids("read_env")
    assert ROLE_BOUNDARIES["sage"].forbids("direct_execution")
    assert ROLE_BOUNDARIES["janus"].forbids("bypass_sage")
    assert ROLE_BOUNDARIES["yet_kieu"].forbids("modify_law")
    assert ROLE_BOUNDARIES["hermes"].forbids("direct_lancedb_backend_access")


def test_opencode_only_for_lang_lieu():
    enabled = [agent_id for agent_id, boundary in ROLE_BOUNDARIES.items() if boundary.can_use_opencode]
    assert enabled == ["lang_lieu"]
