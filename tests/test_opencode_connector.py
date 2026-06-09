from agents.lang_lieu.dev_orchestrator import LangLieuDevOrchestrator
from connectors.opencode_connector import OpenCodeConnector


def test_opencode_connector_blocks_protected_paths_without_approval():
    connector = OpenCodeConnector()

    result = connector.prepare_task("edit governance", ["governance/policy_engine.py"])

    assert result["status"] == "BLOCKED"
    assert result["execution_enabled"] is False
    assert "Sage Review" in result["reason"]
    assert result["governance_gate"]["decision"] == "BLOCK"


def test_opencode_connector_allows_unprotected_adapter_request():
    connector = OpenCodeConnector()

    result = connector.prepare_task("edit docs", ["docs/reports/example.md"])

    assert result["status"] in {"READY", "UNAVAILABLE"}
    assert result["execution_enabled"] is False
    assert result["mode"] == "adapter_only"
    assert result["governance_gate"]["decision"] == "ALLOW"


def test_opencode_connector_normalizes_windows_paths_for_protection():
    connector = OpenCodeConnector()

    result = connector.prepare_task("edit env", [r"D:\AK\.env"])

    assert result["status"] == "BLOCKED"
    assert result["protected_paths"] == [r"D:\AK\.env"]


def test_lang_lieu_orchestrator_returns_report_without_direct_execution():
    orchestrator = LangLieuDevOrchestrator(connector=OpenCodeConnector())

    report = orchestrator.run_task("prepare docs change", ["docs/reports/example.md"])

    assert report["agent"] == "lang_lieu"
    assert report["direct_execution"] is False
    assert "governance_review" in report
