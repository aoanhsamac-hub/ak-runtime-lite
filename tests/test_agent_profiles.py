from __future__ import annotations

import pytest

from agents.identity import AgentIdentity, AGENT_IDENTITIES, get_identity, AgentRole, AgentDepartment, AgentAuthorityLevel
from agents.role_boundary import RoleBoundary, ROLE_BOUNDARIES, get_role_boundary, TERMINAL_AUTONOMY_LEVELS, AUTONOMY_HIERARCHY


class TestAgentIdentityCapabilities:
    def test_all_agents_have_capabilities(self):
        for agent_id, identity in AGENT_IDENTITIES.items():
            assert len(identity.capabilities) > 0, f"{agent_id} has no capabilities"

    def test_all_agents_have_skills(self):
        for agent_id, identity in AGENT_IDENTITIES.items():
            assert len(identity.skills) > 0, f"{agent_id} has no skills"

    def test_janus_capabilities(self):
        janus = AGENT_IDENTITIES["janus"]
        assert "orchestration" in janus.capabilities
        assert "council_consolidation" in janus.capabilities

    def test_sage_capabilities(self):
        sage = AGENT_IDENTITIES["sage"]
        assert "governance_review" in sage.capabilities
        assert "veto_authority" in sage.capabilities

    def test_hermes_capabilities(self):
        hermes = AGENT_IDENTITIES["hermes"]
        assert "lesson_distillation" in hermes.capabilities
        assert "evidence_review" in hermes.capabilities

    def test_to_dict_includes_capabilities_and_skills(self):
        janus = AGENT_IDENTITIES["janus"]
        d = janus.to_dict()
        assert "capabilities" in d
        assert "skills" in d
        assert isinstance(d["capabilities"], list)
        assert isinstance(d["skills"], list)

    def test_default_maturity_level_empty(self):
        janus = AGENT_IDENTITIES["janus"]
        assert janus.maturity_level == ""
        assert janus.evolution_cycle == 0

    def test_all_agents_have_default_maturity(self):
        for identity in AGENT_IDENTITIES.values():
            assert identity.maturity_level == ""
            assert identity.evolution_cycle == 0


class TestRoleBoundaryAutonomy:
    def test_autonomy_levels_defined(self):
        assert "READ_ONLY" in TERMINAL_AUTONOMY_LEVELS
        assert "SANDBOX_WRITE" in TERMINAL_AUTONOMY_LEVELS
        assert "BRANCH_WRITE" in TERMINAL_AUTONOMY_LEVELS
        assert "PROMOTION_CANDIDATE" in TERMINAL_AUTONOMY_LEVELS

    def test_autonomy_hierarchy(self):
        assert AUTONOMY_HIERARCHY["READ_ONLY"] == 0
        assert AUTONOMY_HIERARCHY["SANDBOX_WRITE"] == 1
        assert AUTONOMY_HIERARCHY["BRANCH_WRITE"] == 2
        assert AUTONOMY_HIERARCHY["PROMOTION_CANDIDATE"] == 3

    def test_all_agents_have_autonomy_level(self):
        for agent_id, boundary in ROLE_BOUNDARIES.items():
            assert boundary.autonomy_level in TERMINAL_AUTONOMY_LEVELS, f"{agent_id} missing autonomy_level"

    def test_lang_lieu_has_branch_write(self):
        ll = ROLE_BOUNDARIES["lang_lieu"]
        assert ll.autonomy_level == "BRANCH_WRITE"

    def test_iris_has_read_only(self):
        iris = ROLE_BOUNDARIES["iris"]
        assert iris.autonomy_level == "READ_ONLY"

    def test_allows_autonomy_checks_hierarchy(self):
        read_only = RoleBoundary("test", ("observe",), (), autonomy_level="READ_ONLY")
        assert read_only.allows_autonomy("READ_ONLY")
        assert not read_only.allows_autonomy("SANDBOX_WRITE")

        sandbox = RoleBoundary("test", ("observe", "write"), (), autonomy_level="SANDBOX_WRITE")
        assert sandbox.allows_autonomy("READ_ONLY")
        assert sandbox.allows_autonomy("SANDBOX_WRITE")
        assert not sandbox.allows_autonomy("BRANCH_WRITE")

    def test_invalid_autonomy_level_raises(self):
        with pytest.raises(ValueError, match="autonomy_level"):
            RoleBoundary("test", ("observe",), (), autonomy_level="INVALID")

    def test_to_dict_includes_autonomy_level(self):
        janus = ROLE_BOUNDARIES["janus"]
        d = janus.to_dict()
        assert "autonomy_level" in d
        assert d["autonomy_level"] == "SANDBOX_WRITE"
