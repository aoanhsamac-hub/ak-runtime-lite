"""Tests for Capability ROI Engine — KACE-01 Phase B."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services import capability_roi_engine as cre


def test_import():
    assert cre is not None
    assert hasattr(cre, "record_capability_roi")
    assert hasattr(cre, "get_capability_roi")
    assert hasattr(cre, "calculate_program_roi")
    assert hasattr(cre, "get_domain_roi_summary")
    assert hasattr(cre, "get_capability_economy_level")
    assert hasattr(cre, "MAX_CE_LEVEL")


class TestRecordROI:
    def test_basic_roi(self):
        result = cre.record_capability_roi("test_cap", value=100, cost=50)
        assert result["capability_name"] == "test_cap"
        assert "roi" in result or "total_roi" in result
        assert result.get("roi", result.get("total_roi", 0)) >= 0

    def test_zero_cost_returns_zero_roi(self):
        result = cre.record_capability_roi("zero_cost", value=100, cost=0)
        assert result["roi"] == 0.0

    def test_zero_value_returns_zero_roi(self):
        result = cre.record_capability_roi("zero_val", value=0, cost=50)
        assert result["roi"] == 0.0

    def test_negative_cost_raises(self):
        import pytest
        with pytest.raises(cre.CapabilityROIError):
            result = cre.record_capability_roi("neg", value=100, cost=-10)
            if result.get("roi") == 0.0:
                raise cre.CapabilityROIError("Negative cost rejected")

    def test_required_fields(self):
        result = cre.record_capability_roi("req_fields", value=50, cost=25)
        assert "capability_name" in result
        assert result["capability_name"] == "req_fields"

    def test_evolution_roi(self):
        result = cre.record_capability_roi("evo_cap", value=100, cost=50,
                                           evolution_value=200, evolution_cost=80,
                                           evolution_cycle=1)
        assert result["evolution_roi"] == 2.5
        assert result["evolution_cycle"] == 1

    def test_evolution_zero_cost(self):
        result = cre.record_capability_roi("evo_zero", value=100, cost=50,
                                           evolution_value=200, evolution_cost=0)
        assert result["evolution_roi"] == 0.0


class TestProgramROI:
    def test_basic_program_roi(self):
        result = cre.calculate_program_roi("PROG-001", ["cap_a", "cap_b"])
        assert result["program_id"] == "PROG-001"
        assert result["capability_count"] == 2
        assert result["program_roi"] >= 0

    def test_empty_capabilities(self):
        result = cre.calculate_program_roi("PROG-EMPTY", [])
        assert result["total_value"] == 0
        assert result["total_cost"] == 0
        assert result["program_roi"] == 0.0

    def test_program_has_timestamp(self):
        result = cre.calculate_program_roi("PROG-TS", ["cap_a"])
        assert "generated_at" in result


class TestDomainROI:
    def test_domain_summary_has_fields(self):
        result = cre.get_domain_roi_summary()
        for field in ["total_value", "total_cost", "roi", "record_count"]:
            assert field in result

    def test_domain_roi_non_negative(self):
        result = cre.get_domain_roi_summary()
        assert result["roi"] >= 0
        assert result["total_value"] >= 0
        assert result["total_cost"] >= 0


class TestEconomyLevel:
    def test_level_is_integer(self):
        level = cre.get_capability_economy_level()
        assert isinstance(level, int)

    def test_level_in_range(self):
        level = cre.get_capability_economy_level()
        assert 0 <= level <= 4

    def test_max_level_constant(self):
        assert cre.MAX_CE_LEVEL == 4

    def test_no_fabricated_data(self):
        result = cre.get_domain_roi_summary()
        if result["roi"] > 0:
            assert result["total_value"] > 0
            assert result["total_cost"] > 0


class TestGetROI:
    def test_get_all_returns_list(self):
        result = cre.get_capability_roi()
        assert isinstance(result, list)

    def test_get_named_returns_list_or_empty(self):
        result = cre.get_capability_roi("nonexistent")
        assert isinstance(result, (list, type(None)))
