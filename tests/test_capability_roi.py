from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services import capability_roi_engine as cre
from services import capability_value_engine as cve


def test_import_roi_engine():
    assert cre is not None
    assert hasattr(cre, "record_capability_roi")
    assert hasattr(cre, "get_capability_roi")
    assert hasattr(cre, "calculate_program_roi")
    assert hasattr(cre, "get_domain_roi_summary")
    assert hasattr(cre, "get_capability_economy_level")


def test_record_capability_roi():
    result = cre.record_capability_roi("test_capability", value=100, cost=50)
    assert result["capability_name"] == "test_capability"
    assert "roi" in result


def test_roi_zero_cost_returns_zero():
    result = cre.record_capability_roi("zero_cost_cap", value=100, cost=0)
    assert result["roi"] == 0.0


def test_calculate_program_roi():
    result = cre.calculate_program_roi("PROG-TEST", ["cap_a", "cap_b"])
    assert result["program_id"] == "PROG-TEST"
    assert "program_roi" in result
    assert "capability_count" in result


def test_get_domain_roi_summary():
    result = cre.get_domain_roi_summary()
    assert "total_value" in result
    assert "total_cost" in result
    assert "roi" in result


def test_capability_economy_level_initial():
    level = cre.get_capability_economy_level()
    assert isinstance(level, int)
    assert 0 <= level <= cre.MAX_CE_LEVEL


def test_economy_level_not_exceed_max():
    assert cre.MAX_CE_LEVEL == 4


def test_import_value_engine():
    assert cve is not None
    assert hasattr(cve, "assess_capability_value")
    assert hasattr(cve, "get_domain_value_summary")


def test_assess_capability_value():
    result = cve.assess_capability_value("test", usage_count=5, task_completion_rate=0.8, outcome_quality=0.9)
    assert result["capability_name"] == "test"
    assert "total_value" in result
    assert result["cap_level"] <= cve.MAX_CE_LEVEL


def test_assess_value_no_name_raises():
    import pytest
    with pytest.raises(cve.CapabilityValueError):
        cve.assess_capability_value("")


def test_get_domain_value_summary():
    result = cve.get_domain_value_summary()
    assert "domains" in result
    assert "average_value_score" in result
    assert "domain_count" in result


def test_no_fabricated_roi():
    result = cre.get_domain_roi_summary()
    assert result.get("roi", 0) >= 0
    assert result.get("total_value", 0) >= 0
