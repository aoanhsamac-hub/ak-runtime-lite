from agents.router import TaskRouter
from agents.task_envelope import TaskEnvelope


def test_router_sends_tasks_to_correct_agent():
    router = TaskRouter()
    task = TaskEnvelope("Budget", "budget proposal", "Janus", "")
    assert router.choose_agent(task) == "iris"
    task = TaskEnvelope("Code", "architecture refactor", "Janus", "")
    assert router.choose_agent(task) == "lang_lieu"


def test_protected_task_requires_sage_review():
    router = TaskRouter()
    task = TaskEnvelope("Protected", "code", "Janus", "lang_lieu", metadata={"action": "code", "target_path": "governance/policy_engine.py"})
    result = router.route(task)
    assert result["status"] == "BLOCKED"
    assert "Sage" in result["reason"]
