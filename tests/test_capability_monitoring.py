"""Tests for PSOP-02 capability and knowledge monitoring."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def test_capability_health_monitor_imports():
    import importlib
    mod = importlib.import_module("services.capability_health_monitor")
    assert hasattr(mod, "check"), "check() not found"


def test_knowledge_health_monitor_imports():
    import importlib
    mod = importlib.import_module("services.knowledge_health_monitor")
    assert hasattr(mod, "check"), "check() not found"


def test_capability_check_returns_valid():
    from services.capability_health_monitor import check
    result = check()
    assert "status" in result
    assert "score" in result
    assert "detail" in result
    assert isinstance(result["score"], (int, float))
    assert 0 <= result["score"] <= 100


def test_knowledge_check_returns_valid():
    from services.knowledge_health_monitor import check
    result = check()
    assert "status" in result
    assert "score" in result
    assert "detail" in result
    assert isinstance(result["score"], (int, float))
    assert 0 <= result["score"] <= 100


def test_capability_has_registries_found():
    from services.capability_health_monitor import check
    result = check()
    assert "registries_present" in result
    assert result["registries_present"] >= 1, "No capability registries found"


def test_knowledge_has_registry_count():
    from services.knowledge_health_monitor import check
    result = check()
    assert "registries_ok" in result
    assert "total_registries" in result
    assert result["registries_ok"] >= 1, "No knowledge registries found"


def test_knowledge_integrity_rate():
    from services.knowledge_health_monitor import check
    result = check()
    assert 0 <= result["score"] <= 100


def test_capability_check_mentions_registries():
    from services.capability_health_monitor import check
    result = check()
    assert "registries_found" in result
    assert len(result["registries_found"]) >= 1
