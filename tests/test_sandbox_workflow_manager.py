"""Test Sandbox Workflow Manager."""

import pytest


def test_import_sandbox_workflow_manager():
    import services.sandbox_workflow_manager as swm
    assert hasattr(swm, "SandboxWorkflowManager")
    assert hasattr(swm, "run_sandbox_workflow")


def test_sandbox_workflow_init():
    from services.sandbox_workflow_manager import SandboxWorkflowManager
    mgr = SandboxWorkflowManager("CAP-001")
    assert mgr.capability_id == "CAP-001"
    assert mgr.current_state == "SANDBOX_PENDING"


def test_start_workflow():
    from services.sandbox_workflow_manager import SandboxWorkflowManager
    mgr = SandboxWorkflowManager("CAP-002")
    result = mgr.start_workflow()
    assert result["workflow_state"] == "VALIDATION"


def test_validate():
    from services.sandbox_workflow_manager import SandboxWorkflowManager
    mgr = SandboxWorkflowManager("CAP-003")
    mgr.start_workflow()
    result = mgr.validate({"is_valid": True})
    assert result["workflow_state"] == "TESTING"


def test_complete_testing():
    from services.sandbox_workflow_manager import SandboxWorkflowManager
    mgr = SandboxWorkflowManager("CAP-004")
    mgr.start_workflow()
    mgr.validate({"is_valid": True})
    result = mgr.complete_testing()
    assert result["workflow_state"] == "REVIEW"


def test_return_to_human():
    from services.sandbox_workflow_manager import SandboxWorkflowManager
    mgr = SandboxWorkflowManager("CAP-005")
    mgr.start_workflow()
    result = mgr.return_to_human("Missing tests")
    assert result["workflow_state"] == "RETURNED"


def test_run_sandbox_workflow():
    from services.sandbox_workflow_manager import run_sandbox_workflow
    result = run_sandbox_workflow("CAP-006", {"code": "test"})
    assert result["status"] == "SANDBOX_COMPLETE"
    assert result["requires_human_approval"] is True


def test_workflow_states():
    from services.sandbox_workflow_manager import SandboxWorkflowManager
    mgr = SandboxWorkflowManager("CAP-007")
    states = mgr.workflow_states
    assert "SANDBOX_PENDING" in states
    assert "VALIDATION" in states
    assert "TESTING" in states


def test_review_required():
    from services.sandbox_workflow_manager import SandboxWorkflowManager
    mgr = SandboxWorkflowManager("CAP-008")
    assert mgr.review_required is True


def test_sandbox_result_structure():
    from services.sandbox_workflow_manager import run_sandbox_workflow
    result = run_sandbox_workflow("CAP-009", {"code": "test"})
    assert "capability_id" in result
    assert "workflow" in result