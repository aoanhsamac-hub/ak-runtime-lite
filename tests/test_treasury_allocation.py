"""Tests for PSOP-01A treasury allocation engine."""

from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "treasury"
SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "docs" / "schemas"

from services import treasury_allocation_engine as tae


def _reset_treasury_data():
    for fname in ["kingdom_treasury.json", "royal_treasury.json"]:
        path = DATA_DIR / fname
        data = json.loads(path.read_text(encoding="utf-8"))
        data["entries"] = []
        data["status"] = "INITIALIZED"
        data["updated_at"] = None
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def setup_function():
    _reset_treasury_data()


def test_allocate_valid_revenue():
    result = tae.allocate(10000.0, "REV-2026-0001", "Iris")
    assert result["allocation_breakdown"]["total_revenue"] == 10000.0
    assert result["allocation_breakdown"]["kingdom_treasury_92"] == 9200.0
    assert result["allocation_breakdown"]["royal_treasury_8"] == 800.0


def test_92_8_split_accuracy():
    result = tae.allocate(1000.0, "REV-2026-0002", "Iris")
    nt = result["allocation_breakdown"]["kingdom_treasury_92"]
    rt = result["allocation_breakdown"]["royal_treasury_8"]
    assert nt == 920.0
    assert rt == 80.0
    assert nt + rt == 1000.0


def test_rounding_remainder_goes_to_kingdom():
    result = tae.allocate(100.03, "REV-2026-0003", "Iris")
    nt = result["allocation_breakdown"]["kingdom_treasury_92"]
    rt = result["allocation_breakdown"]["royal_treasury_8"]
    assert abs(nt + rt - 100.03) < 0.01


def test_revenue_validated():
    try:
        tae.allocate(-100, "REV-2026-0004", "Iris")
        assert False, "Should have raised"
    except tae.AllocationError as e:
        assert "positive" in str(e).lower()


def test_zero_amount_raises():
    try:
        tae.allocate(0, "REV-2026-0005", "Iris")
        assert False, "Should have raised"
    except tae.AllocationError as e:
        assert "positive" in str(e).lower()


def test_kingdom_treasury_recorded():
    tae.allocate(5000.0, "REV-2026-0006", "Janus")
    nt_path = DATA_DIR / "kingdom_treasury.json"
    nt = json.loads(nt_path.read_text(encoding="utf-8"))
    entries = nt.get("entries", [])
    assert len(entries) >= 1
    assert entries[0]["to_account"] == "KingdomTreasury"
    assert entries[0]["transaction_type"] == "Allocation"
    assert entries[0]["reference"] == "REV-2026-0006"


def test_royal_treasury_recorded():
    tae.allocate(5000.0, "REV-2026-0007", "Janus")
    rt_path = DATA_DIR / "royal_treasury.json"
    rt = json.loads(rt_path.read_text(encoding="utf-8"))
    entries = rt.get("entries", [])
    assert len(entries) >= 1
    assert entries[0]["to_account"] == "RoyalTreasury"


def test_audit_trail_generated():
    result = tae.allocate(25000.0, "REV-2026-0008", "Sage")
    assert result["audit_id"].startswith("AUDIT-ALLOC-")
    assert result["kingdom_treasury"]["audit_id"] == result["audit_id"]
    assert result["royal_treasury"]["audit_id"] == result["audit_id"]


def test_get_allocation_count():
    _reset_treasury_data()
    assert tae.get_allocation_count() == 0
    tae.allocate(1000.0, "REV-2026-0009", "Iris")
    assert tae.get_allocation_count() >= 1


def test_get_allocation_history():
    _reset_treasury_data()
    tae.allocate(3000.0, "REV-2026-0010", "Iris")
    history = tae.get_allocation_history()
    assert "kingdom_treasury_entries" in history
    assert "royal_treasury_entries" in history


def test_large_allocation():
    result = tae.allocate(1000000.0, "REV-2026-0011", "Janus")
    assert result["allocation_breakdown"]["kingdom_treasury_92"] == 920000.0
    assert result["allocation_breakdown"]["royal_treasury_8"] == 80000.0
