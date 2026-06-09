from pathlib import Path

from governance.approval_engine import approval_requirements, highest_risk, validate_approvers
from governance.audit_engine import append_audit_record
from governance.governance_gate import evaluate_proposal
from governance.issue_registry import create_issue, validate_issue
from governance.policy_engine import classify_change, is_protected_module


def test_issue_creation(tmp_path):
    registry = tmp_path / "issue_registry.yaml"
    issue = create_issue("Test issue", "Description", "LEVEL_0_LOW", "LangLieu", path=registry)
    assert issue["issue_id"].startswith("ISSUE-2026-")
    assert validate_issue(issue)["valid"] is True


def test_approval_routing():
    requirements = approval_requirements("LEVEL_3_CRITICAL")
    assert requirements["approvers"] == ["Janus", "Sage"]
    assert validate_approvers("LEVEL_3_CRITICAL", ["Janus", "Sage"])["valid"] is True


def test_risk_classification():
    result = classify_change({"path": "governance/policy_engine.py"})
    assert result["risk_level"] == "LEVEL_3_CRITICAL"


def test_protected_module_detection():
    assert is_protected_module("sovereign/state_corpus/example.md") is True
    assert is_protected_module("docs/report.md") is False


def test_governance_blocking_for_missing_approver():
    result = evaluate_proposal({"target_path": "execution/gateway.py", "approvers": ["Janus"]})
    assert result["decision"] == "BLOCK"
    assert "Sage" in result["required_approvers"]


def test_audit_append(tmp_path):
    log = tmp_path / "audit.jsonl"
    first = append_audit_record("LangLieu", "test", "target", "OK", "ISSUE-2026-0001", log)
    second = append_audit_record("LangLieu", "test", "target", "OK", "ISSUE-2026-0001", log)
    lines = log.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert first["event_id"] != second["event_id"]


def test_highest_risk_wins():
    assert highest_risk("LEVEL_1_MODERATE", "LEVEL_4_CONSTITUTIONAL", "LEVEL_2_HIGH") == "LEVEL_4_CONSTITUTIONAL"
