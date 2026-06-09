"""Tests for PSOP-02 Kingdom Health Registry."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"

REQUIRED_HEALTH_DOMAINS = [
    "governance_health", "treasury_health", "agents_health",
    "capability_health", "knowledge_health", "dataset_health",
    "security_health", "trading_health",
]

REQUIRED_STATUS_DOMAINS = [
    "governance", "treasury", "agents", "capabilities",
    "knowledge", "datasets", "security", "trading",
]

VALID_STATUSES = ["HEALTHY", "WATCH", "WARNING", "CRITICAL", "INITIALIZED"]


def test_health_registry_exists():
    path = REGISTRIES_DIR / "KINGDOM_HEALTH_REGISTRY.yaml"
    assert path.exists(), "KINGDOM_HEALTH_REGISTRY.yaml not found"


def test_status_registry_exists():
    path = REGISTRIES_DIR / "KINGDOM_STATUS_REGISTRY.yaml"
    assert path.exists(), "KINGDOM_STATUS_REGISTRY.yaml not found"


def test_health_registry_has_all_domains():
    path = REGISTRIES_DIR / "KINGDOM_HEALTH_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    domains = registry.get("kingdom_health_registry", {}).get("health_domains", {})
    for domain in REQUIRED_HEALTH_DOMAINS:
        assert domain in domains, f"Missing health domain: {domain}"


def test_health_domains_have_metadata():
    path = REGISTRIES_DIR / "KINGDOM_HEALTH_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    domains = registry.get("kingdom_health_registry", {}).get("health_domains", {})
    for name, data in domains.items():
        assert "status" in data, f"{name}: missing status"
        assert "score" in data, f"{name}: missing score"
        assert "last_checked" in data, f"{name}: missing last_checked"
        assert "metrics" in data, f"{name}: missing metrics"


def test_health_registry_has_status_levels():
    path = REGISTRIES_DIR / "KINGDOM_HEALTH_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    levels = registry.get("kingdom_health_registry", {}).get("status_levels", [])
    level_names = [l["level"] for l in levels]
    for s in ["HEALTHY", "WATCH", "WARNING", "CRITICAL"]:
        assert s in level_names, f"Missing status level: {s}"


def test_status_registry_has_all_domains():
    path = REGISTRIES_DIR / "KINGDOM_STATUS_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    domains = registry.get("kingdom_status_registry", {}).get("domains", {})
    for domain in REQUIRED_STATUS_DOMAINS:
        assert domain in domains, f"Missing status domain: {domain}"


def test_status_domains_have_metadata():
    path = REGISTRIES_DIR / "KINGDOM_STATUS_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    domains = registry.get("kingdom_status_registry", {}).get("domains", {})
    for name, data in domains.items():
        assert "status" in data, f"{name}: missing status"
        assert "description" in data, f"{name}: missing description"
        assert "last_updated" in data, f"{name}: missing last_updated"


def test_status_registry_has_current_phase():
    path = REGISTRIES_DIR / "KINGDOM_STATUS_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    phase = registry.get("kingdom_status_registry", {}).get("current_phase")
    assert phase == "PSOP-02", f"Expected PSOP-02, got {phase}"
