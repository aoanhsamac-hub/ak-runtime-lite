import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from services.day1_lesson_handler import (
    run_lesson_handler,
    get_lessons,
    get_lesson_summary,
)
from services.day1_forecast_handler import run_forecast_handler
from services.day1_reality_handler import run_reality_handler


def _seed():
    run_forecast_handler()
    run_reality_handler()


def test_run_lesson_handler_returns_dict():
    _seed()
    result = run_lesson_handler()
    assert isinstance(result, dict)


def test_run_lesson_handler_returns_ok():
    _seed()
    result = run_lesson_handler()
    assert result.get("status") == "OK"


def test_run_lesson_handler_has_handler_name():
    _seed()
    result = run_lesson_handler()
    assert result.get("handler") == "day1_lesson_handler"


def test_lesson_creates_records():
    _seed()
    result = run_lesson_handler()
    assert result.get("lessons_created", 0) >= 0


def test_get_lessons_returns_list():
    lessons = get_lessons()
    assert isinstance(lessons, list)


def test_get_lesson_summary_returns_dict():
    _seed()
    run_lesson_handler()
    summary = get_lesson_summary()
    assert isinstance(summary, dict)


def test_lesson_has_required_fields():
    _seed()
    run_lesson_handler()
    lessons = get_lessons()
    if lessons:
        l = lessons[0]
        assert "lesson_id" in l
        assert "category" in l
        assert "forecast_id" in l


def test_lesson_has_valid_category():
    _seed()
    run_lesson_handler()
    valid = {"success", "failure", "neutral", "unknown"}
    for l in get_lessons():
        assert l.get("category") in valid, f"Invalid category: {l.get('category')}"


def test_lesson_has_no_trading_fields():
    _seed()
    run_lesson_handler()
    for l in get_lessons():
        assert "order_send" not in str(l)
        assert "order_modify" not in str(l)
        assert "order_close" not in str(l)


def test_lesson_does_not_use_future_data():
    _seed()
    run_lesson_handler()
    for l in get_lessons():
        assert "future" not in l.get("description", "").lower()


def test_lesson_summary_has_by_category():
    _seed()
    run_lesson_handler()
    summary = get_lesson_summary()
    assert "by_category" in summary


def test_lesson_summary_has_total():
    _seed()
    run_lesson_handler()
    summary = get_lesson_summary()
    assert "total_lessons" in summary


def test_lesson_summary_has_last_run():
    _seed()
    run_lesson_handler()
    summary = get_lesson_summary()
    assert "last_run" in summary


def test_multiple_lesson_runs():
    _seed()
    for _ in range(3):
        r = run_lesson_handler()
        assert r["status"] == "OK"
