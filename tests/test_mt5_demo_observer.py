"""Test MT5 Demo Observer - OBSERVE ONLY, NO EXECUTION."""

from connectors.mt5.mt5_demo_observer import MT5DemoObserver


def test_demo_observer_connects():
    obs = MT5DemoObserver()
    result = obs.connect()
    assert result["status"] == "connected"


def test_demo_observer_readonly_ohlcv():
    obs = MT5DemoObserver()
    obs.connect()
    ohlcv = obs.get_ohlcv("XAUUSDm", count=10)
    assert "symbol" in ohlcv
    assert ohlcv["symbol"] == "XAUUSDm"


def test_demo_observer_readonly_tick():
    obs = MT5DemoObserver()
    tick = obs.get_tick()
    assert "bid" in tick
    assert "ask" in tick


def test_demo_observer_health_check():
    obs = MT5DemoObserver()
    health = obs.health_check()
    assert health["status"] == "healthy"


def test_demo_observer_blocks_orders():
    obs = MT5DemoObserver()
    result = obs.place_order("BUY", "XAUUSDm")
    assert "error" in result
    assert "blocked" in result["error"].lower()


def test_demo_observer_blocks_closes():
    obs = MT5DemoObserver()
    result = obs.close_position("XAUUSDm")
    assert "error" in result
    assert "blocked" in result["error"].lower()