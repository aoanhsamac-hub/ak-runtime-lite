"""Build Validation Runtime - Validate implementations before sandbox deployment."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class BuildValidationRuntime:
    """Validates code builds for sandbox deployment."""

    FORBIDDEN_PATTERNS = ["import os.system", "subprocess.call", "eval(", "exec(", "order_send"]

    def __init__(self):
        self.validation_results: dict[str, dict] = {}

    def validate_code(self, code: str, capability_id: str) -> dict:
        """Check code for forbidden patterns and basic structure."""
        violations = []

        for pattern in self.FORBIDDEN_PATTERNS:
            if pattern in code:
                violations.append(f"Forbidden pattern detected: {pattern}")

        is_valid = len(violations) == 0

        result = {
            "capability_id": capability_id,
            "is_valid": is_valid,
            "violations": violations,
            "validated_at": _utc_now(),
        }

        self.validation_results[capability_id] = result
        return result

    def validate_tests(self, test_code: str, capability_id: str) -> dict:
        """Validate test structure."""
        has_tests = "def test_" in test_code
        return {
            "capability_id": capability_id,
            "test_coverage": "PRESENT" if has_tests else "MISSING",
            "validated_at": _utc_now(),
        }


def validate_implementation(code: str, test_code: str, capability_id: str) -> dict:
    """Full validation for capability implementation."""
    validator = BuildValidationRuntime()
    code_result = validator.validate_code(code, capability_id)
    test_result = validator.validate_tests(test_code, capability_id)

    return {
        "capability_id": capability_id,
        "code_validation": code_result,
        "test_validation": test_result,
        "status": "VALIDATION_COMPLETE",
        "generated_at": _utc_now(),
    }


__all__ = ["BuildValidationRuntime", "validate_implementation"]