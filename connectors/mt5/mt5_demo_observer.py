"""MT5 Demo Observer - READ-ONLY adapter only. NO EXECUTION."""

import os
from pathlib import Path
import MetaTrader5 as mt5  # type: ignore


TIMEFRAME_MAP = {"M1": mt5.TIMEFRAME_M1, "M5": mt5.TIMEFRAME_M5, "M15": mt5.TIMEFRAME_M15, "H1": mt5.TIMEFRAME_H1, "H4": mt5.TIMEFRAME_H4, "D1": mt5.TIMEFRAME_D1}


class MT5DemoObserver:
    def __init__(self, symbol: str | None = None, timeframe: str | None = None):
        self.symbol = symbol or "XAUUSDm"
        self.timeframe = timeframe or "M5"
        self._connected = False
        self._mt5_available = self._check_mt5()

    def _check_mt5(self) -> bool:
        try:
            return mt5.initialize()
        except Exception:
            return False

    def connect(self) -> dict:
        if self._mt5_available:
            self._connected = True
            return {"status": "connected", "mode": "demo_readonly", "symbol": self.symbol, "mt5_real": True}
        self._connected = True
        return {"status": "connected", "mode": "mock_readonly", "symbol": self.symbol, "mt5_real": False}

    def disconnect(self) -> dict:
        if self._mt5_available:
            mt5.shutdown()
        self._connected = False
        return {"status": "disconnected"}

    def _get_real_ohlcv(self, symbol: str, count: int) -> dict:
        tf = TIMEFRAME_MAP.get(self.timeframe, mt5.TIMEFRAME_M5)
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, count)
        if rates is None:
            return {"symbol": symbol, "timeframe": self.timeframe, "ohlcv": [], "mode": "mt5_no_data"}
        ohlcv = []
        for r in rates:
            ohlcv.append({"time": int(r["time"]), "open": float(r["open"]), "high": float(r["high"]), "low": float(r["low"]), "close": float(r["close"]), "volume": float(r["tick_volume"])})
        return {"symbol": symbol, "timeframe": self.timeframe, "ohlcv": ohlcv, "mode": "real_mt5_data", "count": len(ohlcv)}

    def _get_real_tick(self, symbol: str) -> dict:
        tick = mt5.symbol_info_tick(symbol)
        if tick:
            return {"symbol": symbol, "bid": tick.bid, "ask": tick.ask, "spread": tick.ask - tick.bid, "mode": "real_mt5_data"}
        return {"symbol": symbol, "bid": 0, "ask": 0, "spread": 0, "mode": "mt5_no_data"}

    def get_ohlcv(self, symbol: str | None = None, count: int = 100) -> dict:
        sym = symbol or self.symbol
        if self._mt5_available and self._connected:
            return self._get_real_ohlcv(sym, count)
        return {"symbol": sym, "timeframe": self.timeframe, "ohlcv": [], "mode": "mock_demo_data"}

    def get_tick(self, symbol: str | None = None) -> dict:
        sym = symbol or self.symbol
        if self._mt5_available and self._connected:
            return self._get_real_tick(sym)
        return {"symbol": sym, "bid": 0, "ask": 0, "spread": 0, "mode": "mock_demo_tick"}

    def get_spread(self, symbol: str | None = None) -> float:
        result = self.get_tick(symbol)
        return float(result.get("spread", 0))

    def place_order(self, *args, **kwargs) -> dict:
        return {"error": "execution_blocked", "reason": "MT5 demo observer is read-only - NO EXECUTION ALLOWED"}

    def close_position(self, *args, **kwargs) -> dict:
        return {"error": "execution_blocked", "reason": "MT5 demo observer is read-only - NO EXECUTION ALLOWED"}

    def health_check(self) -> dict:
        term = mt5.terminal_info() if self._mt5_available else None
        return {"status": "healthy", "mode": "demo_readonly", "connected": self._connected, "mt5_real": bool(self._mt5_available), "terminal": term._asdict() if term else None}


__all__ = ["MT5DemoObserver"]