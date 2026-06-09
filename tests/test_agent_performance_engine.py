"""Test Agent Performance Engine."""

import pytest


def test_import_agent_performance_engine():
    import services.agent_performance_engine as ape
    assert hasattr(ape, "evaluate_agent_performance")
    assert hasattr(ape, "get_agent_performance")


def test_evaluate_agent_performance():
    from services.agent_performance_engine import evaluate_agent_performance
    result = evaluate_agent_performance("janus")
    assert isinstance(result, dict)
    assert "performance_id" in result


def test_performance_has_required_fields():
    from services.agent_performance_engine import evaluate_agent_performance
    result = evaluate_agent_performance("hermes")
    assert "agent_name" in result
    assert "is_operational" in result
    assert "capability_growth" in result
    assert "task_completion" in result


def test_get_agent_performance():
    from services.agent_performance_engine import get_agent_performance
    result = get_agent_performance("janus")
    assert isinstance(result, dict)


def test_get_all_performance():
    from services.agent_performance_engine import get_all_performance
    result = get_all_performance()
    assert isinstance(result, list)


def test_performance_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/KINGDOM_AGENT_PERFORMANCE_REGISTRY.yaml")
    assert path.exists()


def test_all_agents_evaluated():
    from services.agent_performance_engine import evaluate_agent_performance
    for agent in ["janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"]:
        result = evaluate_agent_performance(agent)
        assert result["agent_name"] == agent


def test_performance_score_calculation():
    from services.agent_performance_engine import evaluate_agent_performance
    result = evaluate_agent_performance("janus")
    assert "operational_output" in result


def test_no_negative_metrics():
    from services.agent_performance_engine import evaluate_agent_performance
    for agent in ["janus", "hermes"]:
        result = evaluate_agent_performance(agent)
        assert result.get("capability_growth", -1) >= 0
        assert result.get("task_completion", -1) >= 0


def test_timestamp_format():
    from services.agent_performance_engine import evaluate_agent_performance
    result = evaluate_agent_performance("janus")
    assert "timestamp" in result