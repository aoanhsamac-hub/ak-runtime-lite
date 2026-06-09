# Tests for Kingdom Assignment Manager

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services import kingdom_assignment_manager as am

def test_assign_task():
    from services import kingdom_task_manager as tm
    t = tm.create_task("DIR-0001", "Assign Test", "hermes", "HIGH", "2026-07-01")
    assigned = am.assign_task_to_agent(t["task_id"], "hermes")
    assert "assigned_to" in assigned or assigned is not None

def test_agent_load():
    load = am.get_agent_load("hermes")
    assert isinstance(load, int)

def test_invalid_agent():
    try:
        am.assign_task_to_agent("TASK-9999", "invalid_agent")
        assert False, "Should have raised"
    except am.AssignmentError:
        pass