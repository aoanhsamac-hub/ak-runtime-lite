"""Tests for PSOP-02 agent monitoring."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


AGENTS_DIR = Path(__file__).resolve().parent.parent / "agents"

AGENT_NAMES = ["janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"]


def test_agent_status_monitor_imports():
    import importlib
    mod = importlib.import_module("services.agent_status_monitor")
    assert hasattr(mod, "check"), "check() not found"


def test_all_agents_have_configs():
    for name in AGENT_NAMES:
        path = AGENTS_DIR / name / "agent.yaml"
        assert path.exists(), f"Missing agent.yaml for {name}"


def test_all_agents_have_implementations():
    for name in AGENT_NAMES:
        path = AGENTS_DIR / name / "agent.py"
        assert path.exists(), f"Missing agent.py for {name}"


def test_agent_check_returns_7_agents():
    from services.agent_status_monitor import check
    result = check()
    assert result["total_agents"] == 7, f"Expected 7, got {result['total_agents']}"
    assert len(result["agents"]) == 7, f"Expected 7 agents in list, got {len(result['agents'])}"


def test_agent_check_returns_valid_status():
    from services.agent_status_monitor import check
    result = check()
    assert result["status"] in ["HEALTHY", "WATCH", "WARNING", "CRITICAL"]


def test_agent_check_has_agent_details():
    from services.agent_status_monitor import check
    result = check()
    for agent in result["agents"]:
        assert "name" in agent
        assert "config_exists" in agent
        assert "agent_exists" in agent
        assert "agent_status" in agent


def test_all_agents_marked_operational():
    from services.agent_status_monitor import check
    result = check()
    for agent in result["agents"]:
        assert agent["agent_status"] == "OPERATIONAL", f"{agent['name']}: {agent['agent_status']}"


def test_agent_titles_all_present():
    from services.agent_status_monitor import AGENT_TITLES
    for name in AGENT_NAMES:
        assert name in AGENT_TITLES, f"Missing title for {name}"


def test_active_count_matches():
    from services.agent_status_monitor import check
    result = check()
    assert result["active_count"] == 7, f"Expected 7 active, got {result['active_count']}"
