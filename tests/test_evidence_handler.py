import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from services.day1_evidence_handler import (
    run_evidence_handler,
    get_evidence,
    get_evidence_summary,
)
from services.day1_forecast_handler import run_forecast_handler
from services.day1_reality_handler import run_reality_handler
from services.day1_lesson_handler import run_lesson_handler


def _seed():
    run_forecast_handler()
    run_reality_handler()
    run_lesson_handler()


def test_run_evidence_handler_returns_dict():
    _seed()
    result = run_evidence_handler()
    assert isinstance(result, dict)


def test_run_evidence_handler_returns_ok():
    _seed()
    result = run_evidence_handler()
    assert result.get("status") == "OK"


def test_run_evidence_handler_has_handler_name():
    _seed()
    result = run_evidence_handler()
    assert result.get("handler") == "day1_evidence_handler"


def test_run_evidence_handler_has_evidence_id():
    _seed()
    result = run_evidence_handler()
    assert result.get("evidence_id", "").startswith("EVID-")


def test_evidence_handler_has_timestamp():
    _seed()
    result = run_evidence_handler()
    assert result.get("timestamp", "").startswith("202")


def test_get_evidence_returns_list():
    evidence = get_evidence()
    assert isinstance(evidence, list)


def test_get_evidence_summary_returns_dict():
    _seed()
    run_evidence_handler()
    summary = get_evidence_summary()
    assert isinstance(summary, dict)


def test_evidence_is_append_only():
    _seed()
    before = len(get_evidence())
    run_evidence_handler()
    after = len(get_evidence())
    assert after >= before


def test_evidence_has_required_fields():
    _seed()
    run_evidence_handler()
    records = get_evidence()
    if records:
        r = records[0]
        assert "evidence_id" in r
        assert "timestamp" in r
        assert "evidence_packages" in r


def test_evidence_packages_contains_sources():
    _seed()
    run_evidence_handler()
    records = get_evidence()
    if records:
        pkgs = records[0].get("evidence_packages", {})
        assert "forecast_evidence" in pkgs
        assert "reality_evidence" in pkgs
        assert "lesson_evidence" in pkgs
        assert "runtime_evidence" in pkgs


def test_evidence_is_immutable_marker():
    _seed()
    run_evidence_handler()
    records = get_evidence()
    if records:
        assert records[0].get("append_only") is True
        assert records[0].get("immutable") is True


def test_evidence_summary_has_status():
    _seed()
    run_evidence_handler()
    summary = get_evidence_summary()
    assert summary.get("status") == "APPEND_ONLY_IMMUTABLE_AUDITABLE"


def test_evidence_summary_has_total():
    _seed()
    run_evidence_handler()
    summary = get_evidence_summary()
    assert "total_evidence_records" in summary


def test_evidence_no_trading_fields():
    _seed()
    run_evidence_handler()
    for r in get_evidence():
        assert "order_send" not in str(r)
        assert "order_modify" not in str(r)
        assert "order_close" not in str(r)


def test_evidence_no_scheduler_duplication():
    _seed()
    run_evidence_handler()
    ids = [r.get("evidence_id") for r in get_evidence()]
    assert len(ids) == len(set(ids))


def test_evidence_no_governance_bypass():
    _seed()
    run_evidence_handler()
    for r in get_evidence():
        assert r.get("handler_type") == "day1_evidence_handler"
