from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
from services import treasury_impact_tracker as ti
from services import kingdom_performance_monitor as npm


def test_import_treasury_impact():
    assert ti is not None
    assert hasattr(ti, "record_program_impact")
    assert hasattr(ti, "record_capability_impact")
    assert hasattr(ti, "get_treasury_contribution_summary")


def test_treasury_impact_registry_exists():
    path = REGISTRIES_DIR / "TREASURY_IMPACT_REGISTRY.yaml"
    assert path.exists()


def test_treasury_impact_registry_structure():
    path = REGISTRIES_DIR / "TREASURY_IMPACT_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    inner = registry.get("treasury_impact_registry", {})
    assert "program_impacts" in inner
    assert "capability_impacts" in inner
    assert "treasury_contributions" in inner


def test_record_program_impact():
    result = ti.record_program_impact("PROG-0001", "Test Program", treasury_contribution=1000.0)
    assert result["impact_id"].startswith("PI-")
    assert result["program_id"] == "PROG-0001"
    assert result["treasury_contribution"] == 1000.0


def test_record_capability_impact():
    result = ti.record_capability_impact("test_capability", treasury_contribution=500.0)
    assert result["impact_id"].startswith("CI-")
    assert result["capability_name"] == "test_capability"


def test_get_treasury_contribution_summary():
    result = ti.get_treasury_contribution_summary()
    assert "program_impact_count" in result
    assert "capability_impact_count" in result
    assert "total_treasury_contribution" in result
    assert "net_treasury_impact" in result


def test_no_fabricated_treasury_data():
    result = ti.get_treasury_contribution_summary()
    assert result.get("total_treasury_contribution", 0) >= 0
    assert result.get("net_treasury_impact", 0) >= 0


def test_import_kingdom_performance():
    assert npm is not None
    assert hasattr(npm, "get_kingdom_performance")


def test_get_kingdom_performance():
    result = npm.get_kingdom_performance()
    assert "goal_completion_rate" in result
    assert "program_completion_rate" in result
    assert "planning_efficiency" in result
    assert "planning_level" in result
    assert "capability_economy_level" in result
    assert "capability_roi" in result
    assert "knowledge_roi" in result
    assert "treasury_impact" in result


def test_planning_level_capped_in_performance():
    result = npm.get_kingdom_performance()
    assert result["planning_level"] <= npm.MAX_PLANNING_LEVEL
    assert result["capability_economy_level"] <= npm.MAX_CE_LEVEL
