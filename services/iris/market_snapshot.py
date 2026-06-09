"""Market Snapshot Collector - Read OHLCV and market state."""

from datetime import datetime, timezone
from typing import Any


class MarketSnapshot:
    def __init__(self, symbol: str, timeframe: str):
        self.symbol = symbol
        self.timeframe = timeframe
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.ohlcv: list[dict[str, Any]] = []
        self.tick: dict[str, Any] = {}
        self.spread = 0.0
        self.session = "unknown"


class MarketSnapshotCollector:
    def __init__(self, observer=None):
        self.observer = observer

    def collect(self, symbol: str, timeframe: str, count: int = 100) -> MarketSnapshot:
        snap = MarketSnapshot(symbol, timeframe)
        ohlcv = self.observer.get_ohlcv(symbol, count) if self.observer else {"ohlcv": []}
        snap.ohlcv = ohlcv.get("ohlcv", [])
        tick = self.observer.get_tick(symbol) if self.observer else {}
        snap.tick = tick
        snap.spread = self.observer.get_spread(symbol) if self.observer else 0.0
        snap.session = self._detect_session()
        return snap

    def _detect_session(self) -> str:
        hour = datetime.now(timezone.utc).hour
        if 0 <= hour < 8:
            return "asia"
        if 8 <= hour < 16:
            return "europe"
        return "america"


__all__ = ["MarketSnapshot", "MarketSnapshotCollector"]