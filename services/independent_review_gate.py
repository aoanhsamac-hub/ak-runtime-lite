from __future__ import annotations

from typing import Any


REVIEWER_ROLES = {
    "Hermes": "strategic_owner",
    "Sage": "governance_owner",
    "Hung Vuong": "approval_authority",
}


class IndependentReviewGate:
    """Ensures promotion recommendation source != final promotion reviewer."""

    def __init__(self):
        self._allowed_final_reviewers = {"Hung Vuong", "Sage"}
        self._allowed_recommenders = {"Hermes", "Sage"}

    def validate(self, recommendation: dict[str, Any]) -> dict[str, Any]:
        recommender = recommendation.get("recommender", "")
        reviewer = recommendation.get("reviewer", "")

        if recommender not in self._allowed_recommenders:
            return {
                "passed": False,
                "reason": f"Recommender '{recommender}' not authorized. Allowed: {sorted(self._allowed_recommenders)}",
                "recommender": recommender,
                "reviewer": reviewer,
            }

        if reviewer not in self._allowed_final_reviewers:
            return {
                "passed": False,
                "reason": f"Reviewer '{reviewer}' not authorized. Allowed: {sorted(self._allowed_final_reviewers)}",
                "recommender": recommender,
                "reviewer": reviewer,
            }

        if recommender == reviewer:
            return {
                "passed": False,
                "reason": f"Recommender '{recommender}' cannot also be the final reviewer. Must be independent.",
                "recommender": recommender,
                "reviewer": reviewer,
            }

        if recommender == "Hermes":
            return {
                "passed": True,
                "reason": f"Hermes recommendation independently validated by {reviewer}",
                "recommender": recommender,
                "reviewer": reviewer,
            }

        return {
            "passed": True,
            "reason": f"Recommendation by {recommender} independently reviewed by {reviewer}",
            "recommender": recommender,
            "reviewer": reviewer,
        }

    def validate_batch(self, recommendations: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [self.validate(r) for r in recommendations]
