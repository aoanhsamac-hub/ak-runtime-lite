"""MT5 Health Monitor - Verify demo connection quality."""

from datetime import datetime, timezone


class MT5HealthMonitor:
    def __init__(self, observer):
        self.observer = observer

    def check_connection(self) -> dict:
        return self.observer.health_check() if self.observer else {"status": "no_observer"}

    def check_symbol(self, symbol: str) -> dict:
        try:
            tick = self.observer.get_tick(symbol) if self.observer else {}
            return {"symbol": symbol, "connected": True, "bid": tick.get("bid", 0), "ask": tick.get("ask", 0)}
        except Exception as e:
            return {"symbol": symbol, "connected": False, "error": str(e)}

    def check_data_quality(self, symbol: str, count: int = 100) -> dict:
        try:
            ohlcv = self.observer.get_ohlcv(symbol, count) if self.observer else {"ohlcv": []}
            data = ohlcv.get("ohlcv", [])
            return {"symbol": symbol, "records": len(data), "quality": "good" if len(data) >= count * 0.8 else "degraded"}
        except Exception as e:
            return {"symbol": symbol, "records": 0, "quality": "error", "error": str(e)}