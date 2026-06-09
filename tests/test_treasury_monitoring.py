"""Tests for PSOP-02 treasury and security monitoring."""

from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "treasury"
REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
SERVICES_DIR = Path(__file__).resolve().parent.parent / "services"


def test_treasury_status_monitor_imports():
    import importlib
    mod = importlib.import_module("services.treasury_status_monitor")
    assert hasattr(mod, "check"), "check() not found"


def test_security_status_monitor_imports():
    import importlib
    mod = importlib.import_module("services.security_status_monitor")
    assert hasattr(mod, "check"), "check() not found"


def test_treasury_check_returns_valid():
    from services.treasury_status_monitor import check
    result = check()
    assert "status" in result
    assert "score" in result
    assert "detail" in result
    assert isinstance(result["score"], (int, float))
    assert 0 <= result["score"] <= 100


def test_security_check_returns_valid():
    from services.security_status_monitor import check
    result = check()
    assert "status" in result
    assert "score" in result
    assert "detail" in result
    assert isinstance(result["score"], (int, float))
    assert 0 <= result["score"] <= 100


def test_treasury_has_domain_counts():
    from services.treasury_status_monitor import check
    result = check()
    assert "domains_active" in result
    assert "domains_total" in result
    assert result["domains_total"] == 5


def test_security_has_check_counts():
    from services.security_status_monitor import check
    result = check()
    assert "checks_passed" in result
    assert "checks_total" in result
    assert result["checks_total"] >= 4


def test_treasury_health_registry_exists():
    path = REGISTRIES_DIR / "TREASURY_HEALTH_REGISTRY.yaml"
    assert path.exists()


def test_security_check_findings_format():
    from services.security_status_monitor import check
    result = check()
    assert isinstance(result.get("findings", []), list)


def test_treasury_has_five_domains():
    from services.treasury_status_monitor import TREASURY_DOMAINS
    expected = ["revenue_health", "treasury_health", "budget_health", "reserve_health", "audit_health"]
    assert TREASURY_DOMAINS == expected
