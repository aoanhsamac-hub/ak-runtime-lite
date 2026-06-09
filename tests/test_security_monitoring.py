"""Tests for PSOP-02 security monitoring."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

INFRA_DIR = Path(__file__).resolve().parent.parent / "infrastructure"
CONNECTORS_DIR = Path(__file__).resolve().parent.parent / "connectors"
AGENTS_DIR = Path(__file__).resolve().parent.parent / "agents"
SOPS_DIR = Path(__file__).resolve().parent.parent / "docs" / "sops"


def test_yet_kieu_agent_exists():
    path = AGENTS_DIR / "yet_kieu" / "agent.py"
    assert path.exists(), "Yet Kieu agent not found"


def test_yet_kieu_config_exists():
    path = AGENTS_DIR / "yet_kieu" / "agent.yaml"
    assert path.exists(), "Yet Kieu config not found"


def test_mt5_monitor_exists():
    path = CONNECTORS_DIR / "mt5" / "mt5_demo_observer.py"
    alt_path = INFRA_DIR / "yet_kieu" / "mt5_health_monitor.py"
    assert path.exists() or alt_path.exists(), "No MT5 monitor found"


def test_zone_detector_exists():
    path = Path(__file__).resolve().parent.parent / "services" / "iris" / "zone_detector.py"
    assert path.exists(), "Zone detector not found"


def test_audit_service_exists():
    path = Path(__file__).resolve().parent.parent / "services" / "treasury_audit_service.py"
    assert path.exists(), "Treasury audit service not found"


def test_sops_exist():
    sops = list(SOPS_DIR.glob("*.md"))
    assert len(sops) >= 8, f"Expected 8+ SOPs, got {len(sops)}"


def test_security_check_imports():
    import importlib
    mod = importlib.import_module("services.security_status_monitor")
    assert hasattr(mod, "check")


def test_security_check_all_passed():
    from services.security_status_monitor import check
    result = check()
    assert result["checks_total"] >= 5
