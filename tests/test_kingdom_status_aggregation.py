"""Tests for PSOP-02 national status and health aggregation."""

from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
SERVICES_DIR = Path(__file__).resolve().parent.parent / "services"


def test_kingdom_status_aggregator_imports():
    import importlib
    mod = importlib.import_module("services.kingdom_status_aggregator")
    assert hasattr(mod, "aggregate_all"), "aggregate_all not found"


def test_kingdom_health_aggregator_imports():
    import importlib
    mod = importlib.import_module("services.kingdom_health_aggregator")
    assert hasattr(mod, "aggregate_health"), "aggregate_health not found"


def test_status_aggregator_returns_8_domains():
    from services.kingdom_status_aggregator import DOMAIN_MONITORS
    assert len(DOMAIN_MONITORS) == 8, f"Expected 8 domains, got {len(DOMAIN_MONITORS)}"


def test_health_aggregator_returns_8_domains():
    from services.kingdom_health_aggregator import HEALTH_MONITORS
    assert len(HEALTH_MONITORS) == 8, f"Expected 8 domains, got {len(HEALTH_MONITORS)}"


def test_status_aggregator_maps_all_domains():
    from services.kingdom_status_aggregator import DOMAIN_MONITORS
    expected = ["governance", "treasury", "agents", "capabilities", "knowledge", "datasets", "security", "trading"]
    for domain in expected:
        assert domain in DOMAIN_MONITORS, f"Domain {domain} not in DOMAIN_MONITORS"


def test_health_aggregator_maps_all_domains():
    from services.kingdom_health_aggregator import HEALTH_MONITORS
    expected = ["governance_health", "treasury_health", "agents_health", "capability_health",
                "knowledge_health", "dataset_health", "security_health", "trading_health"]
    for domain in expected:
        assert domain in HEALTH_MONITORS, f"Domain {domain} not in HEALTH_MONITORS"


def test_status_aggregate_all_returns_dict():
    import importlib
    mod = importlib.import_module("services.kingdom_status_aggregator")
    result = mod.aggregate_all()
    assert isinstance(result, dict)
    assert "timestamp" in result
    assert "domains" in result
    assert "overall_status" in result


def test_health_aggregate_returns_dict():
    import importlib
    mod = importlib.import_module("services.kingdom_health_aggregator")
    result = mod.aggregate_health()
    assert isinstance(result, dict)
    assert "timestamp" in result
    assert "domains" in result
    assert "overall_status" in result
    assert "overall_score" in result


def test_status_aggregation_updates_registry():
    import importlib
    mod = importlib.import_module("services.kingdom_status_aggregator")
    mod.aggregate_all()
    path = REGISTRIES_DIR / "KINGDOM_STATUS_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert registry.get("kingdom_status_registry", {}).get("last_aggregated") is not None


def test_health_aggregation_updates_registry():
    import importlib
    mod = importlib.import_module("services.kingdom_health_aggregator")
    mod.aggregate_health()
    path = REGISTRIES_DIR / "KINGDOM_HEALTH_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert registry.get("kingdom_health_registry", {}).get("last_health_check") is not None
