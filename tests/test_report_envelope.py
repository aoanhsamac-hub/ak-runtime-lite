from agents.report_envelope import ReportEnvelope


def test_report_envelope_generated():
    report = ReportEnvelope("TASK-1", "ISSUE-2026-0001", "sage", "FINAL", "done")
    assert report.report_id.startswith("REPORT-")
    assert report.to_dict()["agent"] == "sage"
