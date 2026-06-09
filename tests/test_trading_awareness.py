from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services import trading_health_monitor as thm
from services import forecast_accuracy_monitor as fam
from services import zone_quality_monitor as zqm
from services import signal_quality_monitor as sqm


def test_import_trading_health():
    assert thm is not None
    assert hasattr(thm, "check")


def test_import_forecast_accuracy():
    assert fam is not None
    assert hasattr(fam, "check")


def test_import_zone_quality():
    assert zqm is not None
    assert hasattr(zqm, "check")


def test_import_signal_quality():
    assert sqm is not None
    assert hasattr(sqm, "check")


def test_trading_health_returns_initialized():
    result = thm.check()
    assert result["status"] == "INITIALIZED"
    assert result["score"] == 0
    assert "checks" in result


def test_trading_health_has_no_execution_guard():
    result = thm.check()
    checks = result.get("checks", {})
    guard = checks.get("no_execution_guard", {})
    assert guard.get("status") == "PASS"


def test_trading_no_forbidden_modes():
    for monitor in [thm, fam, zqm, sqm]:
        assert hasattr(monitor, "FORBIDDEN_MODES")
        for mode in ["LIVE", "PRODUCTION", "EXECUTION", "ORDER_PLACEMENT", "STRATEGY_MODIFICATION"]:
            assert mode in monitor.FORBIDDEN_MODES, f"{monitor.__name__} missing FORBIDDEN_MODE: {mode}"


def test_forecast_accuracy_returns_initialized():
    result = fam.check()
    assert result["status"] == "INITIALIZED"
    assert result["score"] == 0
    assert result["accuracy"] is None


def test_zone_quality_returns_initialized():
    result = zqm.check()
    assert result["status"] == "INITIALIZED"
    assert result["score"] == 0
    assert result["zone_count"] == 0


def test_signal_quality_returns_initialized():
    result = sqm.check()
    assert result["status"] == "INITIALIZED"
    assert result["score"] == 0
    assert result["signal_count"] == 0


def test_all_trading_return_dict():
    for monitor in [thm, fam, zqm, sqm]:
        result = monitor.check()
        assert isinstance(result, dict), f"{monitor.__name__}.check() did not return dict"
        assert "status" in result
        assert "score" in result
        assert "generated_at" in result
