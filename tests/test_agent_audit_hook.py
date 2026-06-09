from agents.audit_hook import append_agent_audit


def test_agent_audit_event_appended(tmp_path):
    log = tmp_path / "audit.jsonl"
    record = append_agent_audit("agent_action", "sage", "TASK-1", "ISSUE-2026-0001", "review", "OK", log)
    assert log.exists()
    assert record["actor"] == "sage"
    assert len(log.read_text(encoding="utf-8").splitlines()) == 1
