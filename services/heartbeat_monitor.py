"""Heartbeat Monitor - Tracks component health via periodic heartbeats."""

from datetime import datetime, timezone
from typing import Any


MISSED_BEAT_THRESHOLD = 3


class HeartbeatMonitor:
    def __init__(self, supervisor=None):
        self._supervisor = supervisor
        self._beats: dict[str, list[str]] = {}
        self._threshold = MISSED_BEAT_THRESHOLD

    def register(self, component: str) -> None:
        self._beats[component] = []

    def beat(self, component: str) -> dict:
        ts = datetime.now(timezone.utc).isoformat()
        if component not in self._beats:
            self._beats[component] = []
        self._beats[component].append(ts)
        if len(self._beats[component]) > 100:
            self._beats[component] = self._beats[component][-50:]
        if self._supervisor:
            self._supervisor.record_heartbeat(component)
        return {"component": component, "timestamp": ts, "total_beats": len(self._beats[component])}

    def last_beat(self, component: str) -> str | None:
        beats = self._beats.get(component, [])
        return beats[-1] if beats else None

    def beat_count(self, component: str) -> int:
        return len(self._beats.get(component, []))

    def missed_beats(self, component: str) -> int:
        last = self.last_beat(component)
        if last is None:
            return self._threshold + 1
        try:
            last_dt = datetime.fromisoformat(last)
            elapsed_minutes = (datetime.now(timezone.utc) - last_dt).total_seconds() / 60
            return int(elapsed_minutes // 1)
        except Exception:
            return 0

    def is_healthy(self, component: str) -> bool:
        return self.missed_beats(component) < self._threshold

    def all_healthy(self) -> dict[str, bool]:
        return {c: self.is_healthy(c) for c in self._beats}

    def summary(self) -> dict[str, Any]:
        return {
            "components": list(self._beats.keys()),
            "health": self.all_healthy(),
            "threshold": self._threshold,
        }
