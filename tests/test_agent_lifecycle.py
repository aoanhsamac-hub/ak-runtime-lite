from agents.lifecycle import AgentLifecycleState, can_receive_task


def test_suspended_agent_cannot_receive_task():
    assert can_receive_task(AgentLifecycleState.SUSPENDED.value) is False
    assert can_receive_task(AgentLifecycleState.OPERATIONAL.value) is True
