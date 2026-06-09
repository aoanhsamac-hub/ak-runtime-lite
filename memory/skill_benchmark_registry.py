"""Skill Benchmark System for AK-SANDBOX-01."""

from __future__ import annotations

from datetime import datetime, timezone


class SkillBenchmarkRegistry:
    def __init__(self):
        self._benchmarks = {}

    def record_benchmark(self, skill_id: str, test_name: str, score: float, owner_agent: str) -> dict:
        key = f"{skill_id}:{test_name}"
        self._benchmarks[key] = {"skill_id": skill_id, "test_name": test_name, "score": score, "owner_agent": owner_agent, "tested_at": datetime.now(timezone.utc).isoformat()}
        return self._benchmarks[key]

    def get_history(self, skill_id: str) -> list[dict]:
        return [b for b in self._benchmarks.values() if b["skill_id"] == skill_id]


class BenchmarkHistoryRegistry:
    def __init__(self):
        self._history = []

    def append(self, skill_id: str, benchmark_record: dict) -> None:
        self._history.append({"skill_id": skill_id, **benchmark_record})


SKILL_BENCHMARK = SkillBenchmarkRegistry()
BENCHMARK_HISTORY = BenchmarkHistoryRegistry()

__all__ = ["SkillBenchmarkRegistry", "BenchmarkHistoryRegistry", "SKILL_BENCHMARK", "BENCHMARK_HISTORY"]