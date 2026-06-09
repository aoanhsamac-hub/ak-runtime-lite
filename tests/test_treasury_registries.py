"""Tests for PSOP-01 treasury registries."""

import yaml
from pathlib import Path


REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
REGISTRY_FILES = [
    "TREASURY_STATUS_REGISTRY.yaml",
    "TREASURY_ACCOUNT_REGISTRY.yaml",
    "TREASURY_TRANSACTION_REGISTRY.yaml",
    "TREASURY_REPORT_REGISTRY.yaml",
    "TREASURY_HEALTH_REGISTRY.yaml",
]

REQUIRED_METADATA = ["status", "version", "created_at", "owner"]


def test_all_registry_files_exist():
    for fname in REGISTRY_FILES:
        path = REGISTRIES_DIR / fname
        assert path.exists(), f"Missing registry: {path}"


def test_registry_has_required_metadata():
    for fname in REGISTRY_FILES:
        path = REGISTRIES_DIR / fname
        registry = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert registry is not None, f"{fname}: empty registry"

        key = list(registry.keys())[0]
        record = registry[key]
        for field in REQUIRED_METADATA:
            assert field in record, f"{fname}: missing metadata field '{field}'"


def test_registry_version_format():
    for fname in REGISTRY_FILES:
        path = REGISTRIES_DIR / fname
        registry = yaml.safe_load(path.read_text(encoding="utf-8"))
        key = list(registry.keys())[0]
        version = registry[key]["version"]
        assert version.startswith("1."), f"{fname}: version must be 1.x"


def test_account_registry_has_accounts():
    path = REGISTRIES_DIR / "TREASURY_ACCOUNT_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    accounts = registry.get("accounts", [])
    assert len(accounts) >= 5, f"Expected at least 5 accounts, got {len(accounts)}"
    for acc in accounts:
        assert "account_id" in acc, "Account missing account_id"
        assert "name" in acc, "Account missing name"
        assert "status" in acc, "Account missing status"


def test_health_registry_has_categories():
    path = REGISTRIES_DIR / "TREASURY_HEALTH_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    inner = registry.get("treasury_health_registry", registry)
    categories = inner.get("health_categories", {})
    assert len(categories) >= 5, f"Expected at least 5 health categories, got {len(categories)}"
    expected = ["revenue_health", "treasury_health", "budget_health", "reserve_health", "audit_health"]
    for cat in expected:
        assert cat in categories, f"Missing health category: {cat}"
        assert "status" in categories[cat], f"{cat}: missing status"


def test_status_registry_has_accounts():
    path = REGISTRIES_DIR / "TREASURY_STATUS_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    accounts = registry.get("accounts", [])
    assert len(accounts) >= 5, f"Expected at least 5 accounts, got {len(accounts)}"
