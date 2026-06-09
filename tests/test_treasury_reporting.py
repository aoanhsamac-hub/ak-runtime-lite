"""Tests for PSOP-01A treasury reporting service."""

from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "treasury"

from services import treasury_reporting_service as trs


def setup_function():
    for fname in ["kingdom_revenue.json", "kingdom_treasury.json", "royal_treasury.json",
                   "kingdom_fund.json", "strategic_reserve.json", "emergency_reserve.json"]:
        path = DATA_DIR / fname
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            data["entries"] = []
            data["status"] = "INITIALIZED"
            data["updated_at"] = None
            path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def test_get_revenue_summary_empty():
    summary = trs.get_revenue_summary()
    assert summary["total_revenue"] == 0
    assert summary["entry_count"] == 0
    assert summary["by_source"] == {}


def test_get_treasury_summary_empty():
    summary = trs.get_treasury_summary()
    assert summary["kingdom_treasury_entries"] == 0
    assert summary["royal_treasury_entries"] == 0
    assert summary["kingdom_fund_entries"] == 0


def test_get_reserve_summary_empty():
    summary = trs.get_reserve_summary()
    assert summary["strategic_reserve_entries"] == 0
    assert summary["emergency_reserve_entries"] == 0


def test_generate_monthly_report():
    report = trs.generate_monthly_report(6, 2026)
    assert report["report_type"] == "Monthly Treasury Report"
    assert report["period"] == "2026-06"
    assert report["status"] == "GENERATED"
    assert report["report_id"].startswith("RPT-")


def test_generate_quarterly_report():
    report = trs.generate_quarterly_report(2, 2026)
    assert report["report_type"] == "Quarterly Treasury Report"
    assert report["period"] == "2026-Q2"
    assert report["status"] == "GENERATED"


def test_generate_health_report():
    report = trs.generate_health_report()
    assert report["report_type"] == "Treasury Health Report"
    assert "health_data" in report
    assert "overall_status" in report


def test_monthly_report_has_revenue_summary():
    report = trs.generate_monthly_report(1, 2026)
    assert "revenue_summary" in report
    assert "total_revenue" in report["revenue_summary"]


def test_quarterly_report_has_treasury_summary():
    report = trs.generate_quarterly_report(1, 2026)
    assert "treasury_summary" in report


def test_health_report_has_health_data():
    report = trs.generate_health_report()
    assert len(report["health_data"]) >= 5
    for cat in ["revenue_health", "treasury_health", "budget_health", "reserve_health", "audit_health"]:
        assert cat in report["health_data"]
