"""Test Build Validation Runtime."""

import pytest


def test_import_build_validation_runtime():
    import services.build_validation_runtime as bvr
    assert hasattr(bvr, "BuildValidationRuntime")
    assert hasattr(bvr, "validate_implementation")


def test_build_validation_init():
    from services.build_validation_runtime import BuildValidationRuntime
    validator = BuildValidationRuntime()
    assert validator.validation_results == {}


def test_validate_clean_code():
    from services.build_validation_runtime import BuildValidationRuntime
    validator = BuildValidationRuntime()
    result = validator.validate_code("def test(): pass", "CAP-001")
    assert result["is_valid"] is True


def test_validate_forbidden_pattern():
    from services.build_validation_runtime import BuildValidationRuntime
    validator = BuildValidationRuntime()
    result = validator.validate_code("import os.system('rm -rf')", "CAP-002")
    assert result["is_valid"] is False


def test_validate_multiple_patterns():
    from services.build_validation_runtime import BuildValidationRuntime
    validator = BuildValidationRuntime()
    code = "eval('bad') and exec('bad') and order_send('buy')"
    result = validator.validate_code(code, "CAP-003")
    assert result["is_valid"] is False
    assert len(result["violations"]) >= 2


def test_validate_tests_present():
    from services.build_validation_runtime import BuildValidationRuntime
    validator = BuildValidationRuntime()
    result = validator.validate_tests("def test_something(): pass", "CAP-004")
    assert result["test_coverage"] == "PRESENT"


def test_validate_tests_missing():
    from services.build_validation_runtime import BuildValidationRuntime
    validator = BuildValidationRuntime()
    result = validator.validate_tests("def not_a_test(): pass", "CAP-005")
    assert result["test_coverage"] == "MISSING"


def test_validate_implementation():
    from services.build_validation_runtime import validate_implementation
    result = validate_implementation(
        "def impl(): pass",
        "def test(): pass",
        "CAP-006"
    )
    assert "code_validation" in result
    assert "test_validation" in result


def test_forbidden_patterns_list():
    from services.build_validation_runtime import BuildValidationRuntime
    validator = BuildValidationRuntime()
    assert "eval(" in validator.FORBIDDEN_PATTERNS
    assert "exec(" in validator.FORBIDDEN_PATTERNS


def test_validation_result_structure():
    from services.build_validation_runtime import BuildValidationRuntime
    validator = BuildValidationRuntime()
    result = validator.validate_code("clean code", "CAP-007")
    assert "capability_id" in result
    assert "validated_at" in result