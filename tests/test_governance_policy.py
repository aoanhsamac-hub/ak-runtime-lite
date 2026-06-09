from governance.policy_engine import classify_change, is_protected_module, requires_approval


def test_constitution_change_is_level_4():
    result = classify_change({"path": "sovereign/constitution/example.md"})
    assert result["risk_level"] == "LEVEL_4_CONSTITUTIONAL"


def test_execution_change_is_at_least_level_3():
    result = classify_change({"path": "execution/gateway.py"})
    assert result["risk_level"] in {"LEVEL_3_CRITICAL", "LEVEL_4_CONSTITUTIONAL"}


def test_docs_change_can_be_level_0():
    result = classify_change({"path": "docs/readme.md"})
    assert result["risk_level"] == "LEVEL_0_LOW"
    assert result["blocked"] is False


def test_invalid_governance_blocks_execution():
    result = requires_approval({
        "path": "execution/gateway.py",
        "governance_valid": False,
        "execution_requested": True,
    })
    assert result["blocked"] is True


def test_protected_module_detection():
    assert is_protected_module("sovereign/constitution/example.md") is True
    assert is_protected_module("docs/readme.md") is False
