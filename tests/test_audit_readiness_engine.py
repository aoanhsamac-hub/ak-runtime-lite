"""Test Audit Readiness Engine."""

import pytest


def test_import_audit_readiness_engine():
    import services.audit_readiness_engine as are
    assert hasattr(are, "evaluate_audit_readiness")


def test_evaluate_audit_readiness():
    from services.audit_readiness_engine import evaluate_audit_readiness
    result = evaluate_audit_readiness()
    assert isinstance(result, dict)
    assert "overall_score" in result
    assert "scores" in result


def test_readiness_scores_fields():
    from services.audit_readiness_engine import evaluate_audit_readiness
    result = evaluate_audit_readiness()
    scores = result.get("scores", {})
    assert "governance" in scores
    assert "treasury" in scores
    assert "agents" in scores


def test_scores_range():
    from services.audit_readiness_engine import evaluate_audit_readiness
    result = evaluate_audit_readiness()
    for domain, score in result["scores"].items():
        assert 0 <= score <= 100


def test_overall_score_range():
    from services.audit_readiness_engine import evaluate_audit_readiness
    result = evaluate_audit_readiness()
    assert 0 <= result["overall_score"] <= 100


def test_registry_exists():
    from pathlib import Path
    path = Path("docs/registries/KINGDOM_AUDIT_READINESS_REGISTRY.yaml")
    assert path.exists()


def test_timestamp_format():
    from services.audit_readiness_engine import evaluate_audit_readiness
    result = evaluate_audit_readiness()
    assert "timestamp" in result


def test_readiness_id_format():
    from services.audit_readiness_engine import evaluate_audit_readiness
    result = evaluate_audit_readiness()
    assert "readiness_id" in result
    assert "READINESS-" in result["readiness_id"]


def test_all_domains_evaluated():
    from services.audit_readiness_engine import evaluate_audit_readiness
    result = evaluate_audit_readiness()
    domains = ["governance", "treasury", "operations", "evidence", "capabilities", "agents", "knowledge", "security"]
    for d in domains:
        assert d in result["scores"]