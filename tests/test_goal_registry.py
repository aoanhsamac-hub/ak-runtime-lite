from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"


def test_goal_registry_exists():
    path = REGISTRIES_DIR / "KINGDOM_GOAL_REGISTRY.yaml"
    assert path.exists()


def test_goal_registry_has_required_metadata():
    path = REGISTRIES_DIR / "KINGDOM_GOAL_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    inner = registry.get("kingdom_goal_registry", {})
    assert "version" in inner
    assert "status" in inner
    assert "owner" in inner
    assert "goal_lifecycle" in inner
    assert "goals" in inner


def test_goal_registry_has_lifecycle_stages():
    path = REGISTRIES_DIR / "KINGDOM_GOAL_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    lifecycle = registry.get("kingdom_goal_registry", {}).get("goal_lifecycle", [])
    expected = ["PROPOSED", "APPROVED", "ACTIVE", "COMPLETED", "ARCHIVED"]
    for stage in expected:
        assert stage in lifecycle, f"Missing lifecycle stage: {stage}"


def test_goal_registry_initialized_empty():
    path = REGISTRIES_DIR / "KINGDOM_GOAL_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    goals = registry.get("kingdom_goal_registry", {}).get("goals", [])
    assert isinstance(goals, list)
