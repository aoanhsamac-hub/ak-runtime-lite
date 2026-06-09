from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
from services import capability_usage_collector as cuc
from services import capability_value_collector as cvc
from services import capability_roi_collector as crc


def test_usage_registry_exists():
    path = REGISTRIES_DIR / "CAPABILITY_USAGE_REGISTRY.yaml"
    assert path.exists()


def test_value_registry_exists():
    path = REGISTRIES_DIR / "CAPABILITY_VALUE_REGISTRY.yaml"
    assert path.exists()


def test_roi_registry_exists():
    path = REGISTRIES_DIR / "CAPABILITY_ROI_REGISTRY.yaml"
    assert path.exists()


def test_usage_registry_structure():
    path = REGISTRIES_DIR / "CAPABILITY_USAGE_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    inner = registry.get("capability_usage_registry", {})
    assert "evidence_records" in inner
    assert "status" in inner
    assert "version" in inner


def test_value_registry_structure():
    path = REGISTRIES_DIR / "CAPABILITY_VALUE_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    inner = registry.get("capability_value_registry", {})
    assert "evidence_records" in inner
    assert "status" in inner


def test_roi_registry_structure():
    path = REGISTRIES_DIR / "CAPABILITY_ROI_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    inner = registry.get("capability_roi_registry", {})
    assert "evidence_records" in inner
    assert "status" in inner


def test_usage_collector_imports():
    assert cuc is not None
    assert hasattr(cuc, "collect_usage")
    assert hasattr(cuc, "get_all_evidence")
    assert hasattr(cuc, "get_evidence_summary")


def test_value_collector_imports():
    assert cvc is not None
    assert hasattr(cvc, "collect_value")
    assert hasattr(cvc, "get_all_evidence")
    assert hasattr(cvc, "get_value_summary")


def test_roi_collector_imports():
    assert crc is not None
    assert hasattr(crc, "collect_roi")
    assert hasattr(crc, "get_all_evidence")
    assert hasattr(crc, "get_roi_summary")


def test_collect_usage():
    result = cuc.collect_usage("test_cap", "test_agent", "execute", "success")
    assert result["evidence_id"].startswith("USAGE-EVID-")
    assert result["capability_name"] == "test_cap"
    assert result["agent_id"] == "test_agent"
    assert result["operation_type"] == "execute"


def test_collect_usage_no_name_raises():
    import pytest
    with pytest.raises(ValueError):
        cuc.collect_usage("", "agent", "op", "ok")


def test_collect_usage_no_agent_raises():
    import pytest
    with pytest.raises(ValueError):
        cuc.collect_usage("cap", "", "op", "ok")


def test_collect_value():
    result = cvc.collect_value("test_cap", "outcome_achieved", ["ref1"])
    assert result["evidence_id"].startswith("VALUE-EVID-")
    assert result["capability_name"] == "test_cap"
    assert result["measurable_outcome"] == "outcome_achieved"


def test_collect_value_no_name_raises():
    import pytest
    with pytest.raises(ValueError):
        cvc.collect_value("", "outcome")


def test_collect_value_no_outcome_raises():
    import pytest
    with pytest.raises(ValueError):
        cvc.collect_value("cap", "")


def test_collect_roi():
    result = crc.collect_roi("test_cap", value=100, cost=50)
    assert result["evidence_id"].startswith("ROI-EVID-")
    assert result["capability_name"] == "test_cap"
    assert result["roi"] == 2.0


def test_collect_roi_zero_cost():
    result = crc.collect_roi("zero_cost", value=100, cost=0)
    assert result["roi"] == 0.0


def test_collect_roi_negative_raises():
    import pytest
    with pytest.raises(ValueError):
        crc.collect_roi("neg", value=-1, cost=50)


def test_collect_roi_no_name_raises():
    import pytest
    with pytest.raises(ValueError):
        crc.collect_roi("", value=100, cost=50)


def test_usage_summary():
    summary = cuc.get_evidence_summary()
    assert "total_records" in summary
    assert "unique_capabilities" in summary


def test_value_summary():
    summary = cvc.get_value_summary()
    assert "total_records" in summary
    assert "total_value_created" in summary


def test_roi_summary():
    summary = crc.get_roi_summary()
    assert "total_records" in summary
    assert "overall_roi" in summary


def test_no_synthetic_usage():
    records = cuc.get_all_evidence()
    for r in records:
        assert "evidence_id" in r
        assert r.get("outcome") != "simulated"
        assert r.get("outcome") != "synthetic"


def test_no_synthetic_value():
    records = cvc.get_all_evidence()
    for r in records:
        assert "evidence_id" in r
        assert r.get("value_created", 0) >= 0


def test_no_synthetic_roi():
    records = crc.get_all_evidence()
    for r in records:
        assert "evidence_id" in r
        assert r.get("value", 0) >= 0
        assert r.get("cost", 0) >= 0
