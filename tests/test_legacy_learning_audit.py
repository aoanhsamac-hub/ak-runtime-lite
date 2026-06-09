"""Verify legacy learning audit logic without touching real legacy files."""

from pathlib import Path
from scripts.audit_legacy_learning import (
    _classify_path,
    _risk_level,
    _contains_code,
    _contains_secret,
    _migration_status,
    _target_registry,
    audit_legacy,
    BLOCKED_DIRECTORIES,
)


def test_classify_governance():
    p = Path("governance/production_standards_sage.md")
    assert _classify_path(p) == "GOVERNANCE"


def test_classify_skill():
    p = Path("approved/skills/langgraph_skill_template.json")
    assert _classify_path(p) == "SKILL"


def test_classify_capability():
    p = Path("evolution/week5_activation.json")
    assert _classify_path(p) == "CAPABILITY"


def test_classify_market_intelligence():
    p = Path("cognitive_market_intelligence.py")
    assert _classify_path(p) == "MARKET_INTELLIGENCE"


def test_classify_trading_knowledge():
    p = Path("execution_adaptation/execution_adapter.py")
    assert _classify_path(p) == "TRADING_STRATEGY_KNOWLEDGE"


def test_risk_low_for_markdown():
    p = Path("report.md")
    assert _risk_level(p, "LESSON") == "LOW"


def test_risk_medium_for_code():
    p = Path("script.py")
    assert _risk_level(p, "ENGINEERING_KNOWLEDGE") == "MEDIUM"


def test_contains_code_py():
    assert _contains_code(Path("test.py")) is True


def test_contains_code_md():
    assert _contains_code(Path("test.md")) is False


def test_contains_secret_clean():
    p = Path(__file__)
    assert _contains_secret(p) is False


def test_migration_status_approved():
    assert _migration_status("LESSON", "LOW", False, False) == "APPROVED_FOR_REVIEW"


def test_migration_status_quarantine():
    assert _migration_status("ENGINEERING_KNOWLEDGE", "MEDIUM", True, False) == "QUARANTINE_IMPORT"


def test_migration_status_sage():
    assert _migration_status("UNKNOWN", "LOW", False, False) == "REQUIRES_SAGE_REVIEW"


def test_migration_status_do_not_import():
    assert _migration_status("REJECTED", "REJECTED", False, True) == "DO_NOT_IMPORT"


def test_target_registry_memory():
    assert "quarantine" in _target_registry("MEMORY")


def test_target_registry_skill():
    assert "skill" in _target_registry("SKILL")


def test_blocked_directories():
    assert "__pycache__" in BLOCKED_DIRECTORIES


def test_audit_legacy_runs_without_error():
    result = audit_legacy(dry_run=True)
    assert "inventory" in result
    assert "summary" in result
    assert result["dry_run"] is True
