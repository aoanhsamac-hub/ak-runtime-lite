from agents.runtime import AgentRuntime
from agents.task_envelope import TaskEnvelope


def test_agent_runtime_is_dry_run_only():
    runtime = AgentRuntime()
    task = TaskEnvelope("Code", "architecture", "Janus", "lang_lieu", metadata={"action": "architecture", "target_path": "docs/readme.md"}, required_approvals=["Janus"])
    result = runtime.run(task)
    assert result["dry_run"] is True
    assert result["execution_enabled"] is False
    assert result["trading_enabled"] is False
    assert result["mt5_enabled"] is False
