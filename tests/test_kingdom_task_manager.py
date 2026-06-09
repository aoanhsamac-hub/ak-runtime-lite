# Tests for Kingdom Task Manager

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services import kingdom_task_manager as tm

def test_create_task():
    t = tm.create_task("DIR-0001", "Test Task", "hermes", "HIGH", "2026-07-01")
    assert t["task_id"].startswith("TASK-")
    assert t["directive_id"] == "DIR-0001"
    assert t["status"] == "NOT_STARTED"

def test_update_task_progress():
    t = tm.create_task("DIR-0001", "Progress Test", "iris", "MEDIUM", "2026-07-01")
    updated = tm.update_task(t["task_id"], progress=50.0)
    assert updated["progress"] == 50.0

def test_update_task_status():
    t = tm.create_task("DIR-0001", "Status Test", "helen", "LOW", "2026-07-01")
    updated = tm.update_task(t["task_id"], status="COMPLETE")
    assert updated["status"] == "COMPLETE"

def test_close_task():
    t = tm.create_task("DIR-0001", "Close Test", "yet_kieu", "CRITICAL", "2026-07-01")
    closed = tm.close_task(t["task_id"])
    assert closed["status"] == "COMPLETE"
    assert closed["progress"] == 100.0

def test_task_audit_trail():
    t = tm.create_task("DIR-0001", "Audit Test", "lang_lieu", "HIGH", "2026-07-01")
    assert "TASK_CREATED" in t["audit_trail"][0]