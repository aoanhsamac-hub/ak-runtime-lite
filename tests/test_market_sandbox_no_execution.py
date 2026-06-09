"""Verify no execution in market sandbox - NO LIVE TRADING."""

from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
FORBIDDEN_FUNCTIONS = ["order_send", "trade_execute", "buy", "sell", "place_order"]


def test_no_live_trading_in_scripts():
    for script in SCRIPT_DIR.glob("*.py"):
        content = script.read_text(encoding="utf-8")
        for func in FORBIDDEN_FUNCTIONS:
            if f"def {func}" in content or f".{func}" in content:
                if "blocked" not in content.lower() and "error" not in content.lower():
                    assert False, f"{script.name} contains {func}"


def test_mt5_observer_is_readonly():
    from connectors.mt5.mt5_demo_observer import MT5DemoObserver
    obs = MT5DemoObserver()
    order_result = obs.place_order("BUY")
    assert "error" in order_result
    close_result = obs.close_position()
    assert "error" in close_result