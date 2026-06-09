# Tests for Kingdom Progress Tracker

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services import kingdom_progress_tracker as pt
from services import kingdom_task_manager as tm

def test_get_directive_progress():
    t1 = tm.create_task("DIR-PROG-01", "Task 1", "hermes", "HIGH", "2026-07-01")
    t2 = tm.create_task("DIR-PROG-01", "Task 2", "iris", "MEDIUM", "2026-07-01")
    tm.update_task(t1["task_id"], progress=50.0)
    tm.update_task(t2["task_id"], progress=75.0)
    
    result = pt.get_directive_progress("DIR-PROG-01")
    assert "progress" in result
    assert "total_tasks" in result

def test_get_agent_progress():
    result = pt.get_agent_progress("hermes")
    assert "agent" in result
    assert "total_tasks" in result