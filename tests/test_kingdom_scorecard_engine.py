"""Test Kingdom Scorecard Engine."""

import pytest


def test_import_kingdom_scorecard_engine():
    import services.kingdom_scorecard_engine as kse
    assert hasattr(kse, "generate_kingdom_scorecard")
    assert hasattr(kse, "get_scorecard_by_category")


def test_generate_kingdom_scorecard():
    from services.kingdom_scorecard_engine import generate_kingdom_scorecard
    result = generate_kingdom_scorecard()
    assert isinstance(result, dict)
    assert "scorecard_id" in result


def test_scorecard_has_all_scores():
    from services.kingdom_scorecard_engine import generate_kingdom_scorecard
    result = generate_kingdom_scorecard()
    assert "kingdom_health_score" in result
    assert "kingdom_audit_score" in result
    assert "kingdom_capability_score" in result
    assert "kingdom_agent_score" in result


def test_scorecard_domains():
    from services.kingdom_scorecard_engine import generate_kingdom_scorecard
    result = generate_kingdom_scorecard()
    domains = result.get("domains", {})
    assert "governance" in domains
    assert "treasury" in domains
    assert "agents" in domains


def test_get_scorecard_by_category_health():
    from services.kingdom_scorecard_engine import get_scorecard_by_category
    result = get_scorecard_by_category("health")
    assert "kingdom_health_score" in result


def test_get_scorecard_by_category_audit():
    from services.kingdom_scorecard_engine import get_scorecard_by_category
    result = get_scorecard_by_category("audit")
    assert "kingdom_audit_score" in result


def test_get_scorecard_by_category_capability():
    from services.kingdom_scorecard_engine import get_scorecard_by_category
    result = get_scorecard_by_category("capability")
    assert "kingdom_capability_score" in result


def test_get_scorecard_by_category_agent():
    from services.kingdom_scorecard_engine import get_scorecard_by_category
    result = get_scorecard_by_category("agent")
    assert "kingdom_agent_score" in result


def test_invalid_category():
    from services.kingdom_scorecard_engine import get_scorecard_by_category
    result = get_scorecard_by_category("invalid")
    assert "error" in result


def test_scorecard_id_format():
    from services.kingdom_scorecard_engine import generate_kingdom_scorecard
    result = generate_kingdom_scorecard()
    assert "SCORECARD-" in result["scorecard_id"]