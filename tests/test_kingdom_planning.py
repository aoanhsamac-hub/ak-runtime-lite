from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services import kingdom_goal_manager as gm
from services import kingdom_program_manager as pm
from services import kingdom_planning_engine as pe


def test_import_goal_manager():
    assert gm is not None
    assert hasattr(gm, "create_goal")
    assert hasattr(gm, "get_goal")
    assert hasattr(gm, "list_goals")
    assert hasattr(gm, "transition_goal")
    assert hasattr(gm, "get_goal_summary")


def test_import_program_manager():
    assert pm is not None
    assert hasattr(pm, "create_program")
    assert hasattr(pm, "get_program")
    assert hasattr(pm, "list_programs")
    assert hasattr(pm, "transition_program")
    assert hasattr(pm, "get_program_summary")


def test_import_planning_engine():
    assert pe is not None
    assert hasattr(pe, "create_kingdom_plan")
    assert hasattr(pe, "get_planning_summary")
    assert hasattr(pe, "check_planning_compliance")


def test_create_goal():
    goal = gm.create_goal("Test Goal", "A test goal", "Kingdom Vision")
    assert goal["goal_id"].startswith("GOAL-")
    assert goal["status"] == "PROPOSED"
    assert goal["name"] == "Test Goal"


def test_get_goal():
    goal = gm.create_goal("Get Test", "Test retrieval", "Vision")
    retrieved = gm.get_goal(goal["goal_id"])
    assert retrieved is not None
    assert retrieved["goal_id"] == goal["goal_id"]


def test_list_goals_empty_status():
    goals = gm.list_goals("COMPLETED")
    assert isinstance(goals, list)


def test_transition_goal_forward():
    goal = gm.create_goal("Transition Test", "Test transition", "Vision")
    assert goal["status"] == "PROPOSED"
    updated = gm.transition_goal(goal["goal_id"], "APPROVED")
    assert updated["status"] == "APPROVED"


def test_transition_goal_backwards_raises():
    import pytest
    goal = gm.create_goal("Backwards Test", "Test backward", "Vision")
    gm.transition_goal(goal["goal_id"], "APPROVED")
    with pytest.raises(gm.GoalError):
        gm.transition_goal(goal["goal_id"], "PROPOSED")


def test_update_goal_progress():
    goal = gm.create_goal("Progress Test", "Test progress", "Vision")
    updated = gm.update_progress(goal["goal_id"], 50.0)
    assert updated["progress"] == 50.0


def test_invalid_progress_raises():
    import pytest
    goal = gm.create_goal("Invalid Progress", "Test invalid", "Vision")
    with pytest.raises(gm.GoalError):
        gm.update_progress(goal["goal_id"], 150.0)


def test_get_goal_summary():
    summary = gm.get_goal_summary()
    assert "total" in summary
    assert "by_status" in summary
    assert "average_progress" in summary


def test_get_goal_not_found():
    assert gm.get_goal("NONEXISTENT") is None


def test_create_program():
    program = pm.create_program("Test Program", "A test program", "Test objective")
    assert program["program_id"].startswith("PROG-")
    assert program["status"] == "PROPOSED"


def test_transition_program():
    program = pm.create_program("Transition Prog", "Test transition", "Objective")
    updated = pm.transition_program(program["program_id"], "APPROVED")
    assert updated["status"] == "APPROVED"


def test_program_backwards_raises():
    import pytest
    program = pm.create_program("Back Prog", "Test backward", "Objective")
    pm.transition_program(program["program_id"], "APPROVED")
    with pytest.raises(pm.ProgramError):
        pm.transition_program(program["program_id"], "PROPOSED")


def test_update_program_progress():
    program = pm.create_program("Prog Progress", "Test progress", "Objective")
    updated = pm.update_progress(program["program_id"], 75.0)
    assert updated["progress"] == 75.0


def test_get_program_summary():
    summary = pm.get_program_summary()
    assert "total" in summary
    assert "by_status" in summary
    assert "average_progress" in summary


def test_create_kingdom_plan():
    goal = gm.create_goal("Plan Goal", "For planning test", "Vision")
    plan = pe.create_kingdom_plan("Test Plan", "Test planning", [goal["goal_id"]])
    assert plan["plan_id"] is not None
    assert plan["status"] == "PROPOSED"


def test_get_planning_summary():
    summary = pe.get_planning_summary()
    assert "goal_summary" in summary
    assert "program_summary" in summary
    assert "planning_efficiency" in summary
    assert "planning_level" in summary


def test_planning_level_capped():
    summary = pe.get_planning_summary()
    assert summary["planning_level"] <= pe.MAX_PLANNING_LEVEL


def test_planning_compliance_check():
    result = pe.check_planning_compliance()
    assert "findings" in result
    assert "total_findings" in result


def test_no_budget_allocation_automation():
    import inspect
    source = inspect.getsource(pe)
    assert "budget" not in source.lower() or "allocation" not in source.lower() or "automation" not in source.lower()


def test_no_autonomous_planning():
    source = open(Path(__file__).resolve().parent.parent / "services" / "kingdom_planning_engine.py").read()
    assert "autonomous" not in source.lower()
    assert "auto_execute" not in source.lower()
    assert "schedule" not in source.lower()
