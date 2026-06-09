# Tests for REH Directive Manager

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services import reh_directive_manager as dm

def setup_function():
    """Clear registry for each test."""
    pass

def test_create_directive():
    d = dm.create_directive("Test Directive", "Hung Vuong", "HIGH", "2026-07-01", "Test objective")
    assert d["directive_id"].startswith("DIR-")
    assert d["title"] == "Test Directive"
    assert d["status"] == "PROPOSED"

def test_update_directive_status():
    d = dm.create_directive("Update Test", "Hung Vuong", "MEDIUM", "2026-07-01", "Test")
    updated = dm.update_directive(d["directive_id"], status="APPROVED")
    assert updated["status"] == "APPROVED"

def test_close_directive():
    d = dm.create_directive("Close Test", "Hung Vuong", "LOW", "2026-07-01", "Test")
    closed = dm.close_directive(d["directive_id"])
    assert closed["status"] == "CLOSED"

def test_directive_audit_trail():
    d = dm.create_directive("Audit Test", "Hung Vuong", "MEDIUM", "2026-07-01", "Test")
    assert len(d["audit_trail"]) >= 1
    assert "DIRECTIVE_CREATED" in d["audit_trail"][0]