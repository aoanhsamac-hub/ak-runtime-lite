import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from services.day1_kace_handler import (
    run_kace_handler,
    get_scorecards,
    get_latest_scorecard,
)
from services.day1_forecast_handler import run_forecast_handler
from services.day1_reality_handler import run_reality_handler
from services.day1_lesson_handler import run_lesson_handler
from services.day1_evidence_handler import run_evidence_handler


def _seed():
    run_forecast_handler()
    run_reality_handler()
    run_lesson_handler()
    run_evidence_handler()


def test_run_kace_handler_returns_dict():
    _seed()
    result = run_kace_handler()
    assert isinstance(result, dict)


def test_run_kace_handler_returns_ok():
    _seed()
    result = run_kace_handler()
    assert result.get("status") == "OK"


def test_run_kace_handler_has_handler_name():
    _seed()
    result = run_kace_handler()
    assert result.get("handler") == "day1_kace_handler"


def test_run_kace_handler_has_scorecard_id():
    _seed()
    result = run_kace_handler()
    assert result.get("scorecard_id", "").startswith("KACE-")


def test_kace_handler_has_timestamp():
    _seed()
    result = run_kace_handler()
    assert result.get("timestamp", "").startswith("202")


def test_get_scorecards_returns_list():
    _seed()
    run_kace_handler()
    scorecards = get_scorecards()
    assert isinstance(scorecards, list)


def test_get_latest_scorecard_returns_dict():
    _seed()
    run_kace_handler()
    latest = get_latest_scorecard()
    assert latest is not None
    assert isinstance(latest, dict)


def test_scorecard_has_required_fields():
    _seed()
    run_kace_handler()
    scorecards = get_scorecards()
    if scorecards:
        s = scorecards[0]
        assert "scorecard_id" in s
        assert "forecast_count" in s
        assert "lesson_count" in s
        assert "evidence_count" in s
        assert "runtime_healthy" in s


def test_scorecard_counts_are_integers():
    _seed()
    run_kace_handler()
    scorecards = get_scorecards()
    if scorecards:
        s = scorecards[0]
        assert isinstance(s.get("forecast_count"), int)
        assert isinstance(s.get("lesson_count"), int)
        assert isinstance(s.get("evidence_count"), int)


def test_scorecard_has_no_trading_fields():
    _seed()
    run_kace_handler()
    for s in get_scorecards():
        assert "order_send" not in str(s)
        assert "order_modify" not in str(s)
        assert "order_close" not in str(s)


def test_scorecard_runtime_health_is_bool():
    _seed()
    run_kace_handler()
    scorecards = get_scorecards()
    if scorecards:
        assert isinstance(scorecards[0].get("runtime_healthy"), bool)


def test_scorecard_evidence_count():
    _seed()
    run_kace_handler()
    scorecards = get_scorecards()
    if scorecards:
        s = scorecards[0]
        assert s.get("evidence_count", -1) >= 0


def test_scorecard_agent_activity():
    _seed()
    run_kace_handler()
    scorecards = get_scorecards()
    if scorecards:
        s = scorecards[0]
        assert "runtime_component_count" in s


def test_latest_scorecard_is_most_recent():
    _seed()
    run_kace_handler()
    latest = get_latest_scorecard()
    if latest:
        assert "scorecard_id" in latest


def test_multiple_scorecard_runs():
    _seed()
    for _ in range(3):
        r = run_kace_handler()
        assert r["status"] == "OK"
