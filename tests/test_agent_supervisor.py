from agents.supervisor import AgentSupervisor


def test_agent_supervisor_boots_all_agents():
    report = AgentSupervisor().produce_agent_status_report()
    assert len(report["agents"]) == 7
    assert all(status == "operational" for status in report["agents"].values())
    assert report["autonomous_execution"] is False
