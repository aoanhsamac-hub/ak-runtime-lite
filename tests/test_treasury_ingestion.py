"""Tests for PSOP-01A treasury revenue ingestion."""

from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "treasury"
SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "docs" / "schemas"

from services import treasury_revenue_ingestion as tri


def setup_function():
    path = DATA_DIR / "kingdom_revenue.json"
    template = {
        "registry": "kingdom_revenue",
        "status": "INITIALIZED",
        "version": "1.0",
        "created_at": "2026-06-08",
        "updated_at": None,
        "schema": "kingdom_revenue_schema",
        "entries": [],
    }
    path.write_text(json.dumps(template, indent=2), encoding="utf-8")


def test_ingest_valid_revenue():
    record = tri.ingest_revenue(
        source="Trading",
        category="Operating",
        amount=10000.0,
        authority="Iris",
        reference="REF-001",
        description="Test revenue",
    )
    assert record["source"] == "Trading"
    assert record["category"] == "Operating"
    assert record["amount"] == 10000.0
    assert record["authority"] == "Iris"
    assert record["status"] == "RECORDED"
    assert record["revenue_id"].startswith("REV-")
    assert record["audit_id"].startswith("AUDIT-REV-")


def test_invalid_source_raises():
    try:
        tri.ingest_revenue(source="InvalidSource", category="Operating", amount=100, authority="Iris")
        assert False, "Should have raised"
    except tri.RevenueIngestionError as e:
        assert "Invalid revenue source" in str(e)


def test_invalid_category_raises():
    try:
        tri.ingest_revenue(source="Trading", category="InvalidCategory", amount=100, authority="Iris")
        assert False, "Should have raised"
    except tri.RevenueIngestionError as e:
        assert "Invalid category" in str(e)


def test_negative_amount_raises():
    try:
        tri.ingest_revenue(source="Trading", category="Operating", amount=-100, authority="Iris")
        assert False, "Should have raised"
    except tri.RevenueIngestionError as e:
        assert "Amount must be positive" in str(e)


def test_empty_authority_raises():
    try:
        tri.ingest_revenue(source="Trading", category="Operating", amount=100, authority="")
        assert False, "Should have raised"
    except tri.RevenueIngestionError as e:
        assert "Authority must be" in str(e)


def test_get_revenue_count():
    assert tri.get_revenue_count() == 0
    tri.ingest_revenue(source="Investment", category="Capital", amount=5000, authority="Janus")
    assert tri.get_revenue_count() == 1


def test_update_revenue_status():
    record = tri.ingest_revenue(source="Service", category="Operating", amount=2500, authority="Iris")
    updated = tri.update_revenue_status(record["revenue_id"], "VERIFIED", "Janus")
    assert updated["status"] == "VERIFIED"


def test_get_revenue_by_status():
    tri.ingest_revenue(source="Technology", category="Operating", amount=3000, authority="Iris")
    records = tri.get_revenue_by_status("RECORDED")
    assert len(records) >= 1


def test_all_valid_sources():
    for source in tri.VALID_SOURCES:
        record = tri.ingest_revenue(source=source, category="Operating", amount=100, authority="Iris")
        assert record["source"] == source


def test_all_valid_categories():
    for cat in tri.VALID_CATEGORIES:
        record = tri.ingest_revenue(source="Trading", category=cat, amount=100, authority="Iris")
        assert record["category"] == cat


def test_revenue_has_audit_trail():
    record = tri.ingest_revenue(source="Consulting", category="Operating", amount=7500, authority="Sage")
    assert record["audit_id"] is not None
    assert record["created_at"] is not None
    assert record["timestamp"] is not None
