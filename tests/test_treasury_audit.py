"""Tests for PSOP-01A treasury audit service."""

from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "treasury"
REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"

from services import treasury_audit_service as tas
from services import treasury_revenue_ingestion as tri
from services import treasury_allocation_engine as tae


def _reset_all_data():
    for fname in ["kingdom_revenue.json", "kingdom_treasury.json", "royal_treasury.json"]:
        path = DATA_DIR / fname
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            data["entries"] = []
            data["status"] = "INITIALIZED"
            data["updated_at"] = None
            path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def setup_function():
    _reset_all_data()


def test_validate_revenue_empty():
    findings = tas.validate_revenue_records()
    assert len(findings) == 0


def test_validate_treasury_empty():
    findings = tas.validate_treasury_records()
    assert len(findings) == 0


def test_validate_allocation_empty():
    findings = tas.validate_allocation_records()
    assert len(findings) == 0


def test_validate_reporting_empty():
    findings = tas.validate_reporting_records()
    assert len(findings) == 0


def test_validate_audit_records_empty():
    findings = tas.validate_audit_records()
    assert len(findings) == 0


def test_full_audit_empty():
    result = tas.run_full_audit()
    assert result["status"] == "PASS"
    assert result["total_findings"] == 0


def test_full_audit_with_valid_data():
    tri.ingest_revenue(source="Trading", category="Operating", amount=10000, authority="Iris")
    result = tas.run_full_audit()
    assert result["status"] == "PASS"


def test_audit_detects_missing_audit_id():
    revenue_path = DATA_DIR / "kingdom_revenue.json"
    revenue = json.loads(revenue_path.read_text(encoding="utf-8"))
    bad_record = {
        "revenue_id": "REV-2026-9999",
        "timestamp": "2026-06-08T00:00:00",
        "source": "Trading",
        "amount": 1000,
        "authority": "Iris",
        "status": "RECORDED",
        "audit_id": None,
    }
    entries = revenue.get("entries", [])
    entries.append(bad_record)
    revenue["entries"] = entries
    revenue_path.write_text(json.dumps(revenue, indent=2), encoding="utf-8")

    findings = tas.validate_revenue_records()
    audit_findings = [f for f in findings if "audit_id" in str(f.get("issue", ""))]
    assert len(audit_findings) >= 1


def test_all_validation_types_return_list():
    for validator in [tas.validate_revenue_records, tas.validate_treasury_records,
                      tas.validate_allocation_records, tas.validate_reporting_records,
                      tas.validate_audit_records]:
        result = validator()
        assert isinstance(result, list)


def test_audit_has_severity_classification():
    result = tas.run_full_audit()
    assert "critical_count" in result
    assert "high_count" in result
    assert "medium_count" in result
    assert "low_count" in result


def test_audit_generates_audit_id():
    result = tas.run_full_audit()
    assert result["audit_id"].startswith("AUDIT-SVC-")


def test_single_finding_has_required_fields():
    tri.ingest_revenue(source="Trading", category="Operating", amount=10000, authority="Iris")
    result = tas.run_full_audit()
    for finding in result["findings"]:
        assert "record_id" in finding
        assert "type" in finding
        assert "severity" in finding
        assert "issue" in finding
