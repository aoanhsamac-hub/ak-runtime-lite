from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
from services import treasury_evidence_collector as tec


def test_treasury_evidence_registry_exists():
    path = REGISTRIES_DIR / "TREASURY_EVIDENCE_REGISTRY.yaml"
    assert path.exists()


def test_treasury_evidence_registry_structure():
    path = REGISTRIES_DIR / "TREASURY_EVIDENCE_REGISTRY.yaml"
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    inner = registry.get("treasury_evidence_registry", {})
    assert "evidence_records" in inner
    assert "status" in inner
    assert "version" in inner


def test_import_treasury_collector():
    assert tec is not None
    assert hasattr(tec, "collect_treasury_evidence")
    assert hasattr(tec, "collect_revenue_event")
    assert hasattr(tec, "collect_expense_event")
    assert hasattr(tec, "collect_reserve_event")
    assert hasattr(tec, "collect_treasury_event")
    assert hasattr(tec, "get_all_evidence")
    assert hasattr(tec, "get_evidence_summary")


def test_collect_revenue_event():
    result = tec.collect_revenue_event({"source": "test"})
    assert result["evidence_id"].startswith("TREASURY-EVID-")
    assert result["event_type"] == "revenue"


def test_collect_expense_event():
    result = tec.collect_expense_event({"category": "test"})
    assert result["event_type"] == "expense"


def test_collect_reserve_event():
    result = tec.collect_reserve_event({"reserve_type": "strategic"})
    assert result["event_type"] == "reserve"


def test_collect_treasury_event():
    result = tec.collect_treasury_event({"action": "rebalance"})
    assert result["event_type"] == "treasury"


def test_invalid_event_type_raises():
    import pytest
    with pytest.raises(ValueError):
        tec.collect_treasury_evidence("invalid_type")


def test_get_treasury_evidence_summary():
    summary = tec.get_evidence_summary()
    assert "total_records" in summary
    assert "by_event_type" in summary


def test_no_synthetic_treasury_evidence():
    records = tec.get_all_evidence()
    for r in records:
        assert "evidence_id" in r
        assert r.get("event_type") in tec.EVIDENCE_TYPES
        assert r.get("event_data", {}) != {}


def test_treasury_evidence_no_fabricated_amounts():
    records = tec.get_all_evidence()
    for r in records:
        ed = r.get("event_data", {})
        assert "amount" not in ed or ed.get("amount", 0) >= 0
