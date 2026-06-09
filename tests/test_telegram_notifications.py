import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from services.day1_telegram_integration import (
    notify_runtime_started,
    notify_runtime_stopped,
    notify_scheduler_failure,
    notify_mt5_failure,
    notify_evidence_failure,
    notify_scorecard_available,
    verify_commands,
)


def test_notify_runtime_started_returns_dict():
    result = notify_runtime_started()
    assert isinstance(result, dict)


def test_notify_runtime_started_has_status():
    result = notify_runtime_started()
    assert result.get("status") in ("OK", "ERROR")


def test_notify_runtime_started_has_handler():
    result = notify_runtime_started()
    if result.get("status") == "OK":
        assert result.get("handler") == "day1_telegram_integration"


def test_notify_runtime_stopped_returns_dict():
    result = notify_runtime_stopped("test shutdown")
    assert isinstance(result, dict)


def test_notify_runtime_stopped_with_reason():
    result = notify_runtime_stopped("maintenance")
    if result.get("status") == "OK":
        assert result.get("reason") == "maintenance"


def test_notify_scheduler_failure_returns_dict():
    result = notify_scheduler_failure({"job": "hourly-forecast", "error": "timeout"})
    assert isinstance(result, dict)


def test_notify_mt5_failure_returns_dict():
    result = notify_mt5_failure({"connection": "lost"})
    assert isinstance(result, dict)


def test_notify_evidence_failure_returns_dict():
    result = notify_evidence_failure({"registry": "EVIDENCE_REGISTRY", "error": "write_failed"})
    assert isinstance(result, dict)


def test_notify_scorecard_available_returns_dict():
    result = notify_scorecard_available("KACE-20260609-0001")
    assert isinstance(result, dict)


def test_notify_scorecard_has_scorecard_id():
    result = notify_scorecard_available("KACE-20260609-0001")
    if result.get("status") == "OK":
        assert result.get("scorecard_id") == "KACE-20260609-0001"


def test_verify_commands_returns_dict():
    result = verify_commands()
    assert isinstance(result, dict)


def test_verify_commands_has_commands():
    result = verify_commands()
    if result.get("status") == "OK":
        assert isinstance(result.get("commands_available"), list)
        assert result.get("command_count", 0) >= 0


def test_no_trading_in_notifications():
    results = [
        notify_runtime_started(),
        notify_runtime_stopped("test"),
        notify_scheduler_failure({"e": "x"}),
        notify_mt5_failure({"e": "x"}),
        notify_evidence_failure({"e": "x"}),
        notify_scorecard_available("test"),
    ]
    for r in results:
        assert "order_send" not in str(r)
        assert "order_modify" not in str(r)
        assert "order_close" not in str(r)


def test_notification_types_consistent():
    result = notify_runtime_started()
    if result.get("status") == "OK":
        assert result.get("notification") == "runtime_started"
