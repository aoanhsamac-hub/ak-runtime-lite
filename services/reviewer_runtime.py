"""Reviewer Runtime - Automated review workflow for capability implementations."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReviewerRuntime:
    """Automated review runtime - requires human approval before completion."""

    FORBIDDEN_ACTIONS = ["self_approve", "auto_promote", "bypass_review", "skip_validation"]

    def __init__(self, capability_id: str):
        self.capability_id = capability_id
        self.review_status = "PENDING_REVIEW"
        self.governance_check = "PASS"
        self.technical_check = "PENDING"

    def request_review(self, implementation: dict) -> dict:
        """Submit implementation for review - does NOT auto-approve."""
        return {
            "capability_id": self.capability_id,
            "review_requested_at": _utc_now(),
            "implementation": implementation,
            "status": "PENDING_REVIEW",
            "requires_human_approval": True,
        }

    def evaluate_implementation(self, impl: dict) -> dict:
        """Technical evaluation only - does not approve."""
        score = 0.0
        issues = []

        if not impl.get("code"):
            issues.append("No code provided")
        if not impl.get("tests"):
            issues.append("No tests included")
        if impl.get("complexity", "LOW") == "CRITICAL":
            issues.append("Critical complexity requires elevated review")

        score = 0.5 if not issues else 0.0

        return {
            "capability_id": self.capability_id,
            "technical_score": score,
            "issues_found": issues,
            "evaluated_at": _utc_now(),
            "status": "REVIEW_COMPLETE",
        }

    def can_proceed(self) -> bool:
        """Check if human approval received - always requires approval."""
        return False  # Cannot proceed without human approval


def run_review(capability_id: str, implementation: dict) -> dict:
    """Run review process and return results for human decision."""
    runtime = ReviewerRuntime(capability_id)
    review = runtime.request_review(implementation)
    evaluation = runtime.evaluate_implementation(implementation)

    return {
        "capability_id": capability_id,
        "review": review,
        "evaluation": evaluation,
        "status": "AWAITING_HUMAN_APPROVAL",
        "generated_at": _utc_now(),
    }


def get_review_status(capability_id: str) -> str:
    """Check review status - requires human check."""
    return "PENDING_HUMAN_REVIEW"


__all__ = ["ReviewerRuntime", "run_review", "get_review_status"]