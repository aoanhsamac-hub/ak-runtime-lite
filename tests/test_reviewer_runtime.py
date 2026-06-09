"""Test Reviewer Runtime."""

import pytest


def test_import_reviewer_runtime():
    import services.reviewer_runtime as rr
    assert hasattr(rr, "ReviewerRuntime")
    assert hasattr(rr, "run_review")


def test_reviewer_runtime_init():
    from services.reviewer_runtime import ReviewerRuntime
    runtime = ReviewerRuntime("CAP-001")
    assert runtime.capability_id == "CAP-001"
    assert runtime.review_status == "PENDING_REVIEW"


def test_request_review():
    from services.reviewer_runtime import ReviewerRuntime
    runtime = ReviewerRuntime("CAP-002")
    result = runtime.request_review({"code": "test"})
    assert "capability_id" in result
    assert "review_requested_at" in result
    assert result["requires_human_approval"] is True


def test_evaluate_implementation():
    from services.reviewer_runtime import ReviewerRuntime
    runtime = ReviewerRuntime("CAP-003")
    result = runtime.evaluate_implementation({"code": "test", "tests": "present"})
    assert "technical_score" in result
    assert "issues_found" in result


def test_evaluate_missing_code():
    from services.reviewer_runtime import ReviewerRuntime
    runtime = ReviewerRuntime("CAP-004")
    result = runtime.evaluate_implementation({})
    assert len(result["issues_found"]) > 0


def test_can_proceed_requires_approval():
    from services.reviewer_runtime import ReviewerRuntime
    runtime = ReviewerRuntime("CAP-005")
    assert runtime.can_proceed() is False


def test_forbidden_actions():
    from services.reviewer_runtime import ReviewerRuntime
    runtime = ReviewerRuntime("CAP-006")
    assert "self_approve" in runtime.FORBIDDEN_ACTIONS
    assert "auto_promote" in runtime.FORBIDDEN_ACTIONS


def test_run_review():
    from services.reviewer_runtime import run_review
    result = run_review("CAP-007", {"code": "test"})
    assert result["status"] == "AWAITING_HUMAN_APPROVAL"


def test_get_review_status():
    from services.reviewer_runtime import get_review_status
    result = get_review_status("CAP-008")
    assert result == "PENDING_HUMAN_REVIEW"


def test_reviewer_runtime_awaiting_approval():
    from services.reviewer_runtime import ReviewerRuntime
    runtime = ReviewerRuntime("CAP-009")
    runtime.start_workflow = lambda: None
    runtime.validate_implementation = lambda x: {"is_valid": True}
    runtime.complete_testing = lambda: None
    assert runtime.review_status == "PENDING_REVIEW"