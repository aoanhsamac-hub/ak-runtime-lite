from agents.task_envelope import TaskEnvelope


def test_task_envelope_requires_task_id():
    task = TaskEnvelope("Title", "Objective", "Janus", "sage")
    assert task.task_id.startswith("TASK-")
    assert task.validate()["valid"] is True


def test_non_trivial_task_requires_issue_id():
    task = TaskEnvelope("Critical", "Objective", "Janus", "sage", risk_level="LEVEL_3_CRITICAL")
    result = task.validate()
    assert result["valid"] is False
    assert "issue_id" in result["missing"]
