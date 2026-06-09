"""NEURON T2 Prompt Evolution System Registries - SANDBOX ONLY."""

from __future__ import annotations

from datetime import datetime, timezone


class PromptRegistry:
    def __init__(self):
        self._prompts = {}

    def register(self, prompt_id: str, content: str, purpose: str, owner_agent: str, risk_level: str = "LEVEL_2_HIGH") -> dict:
        record = {
            "prompt_id": prompt_id,
            "content": content,
            "purpose": purpose,
            "owner_agent": owner_agent,
            "risk_level": risk_level,
            "version": 1,
            "review_status": "PENDING",
            "activation_state": "SANDBOX_ONLY",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._prompts[prompt_id] = record
        return record

    def get(self, prompt_id: str) -> dict | None:
        return self._prompts.get(prompt_id)

    def list_by_owner(self, owner: str) -> list[dict]:
        return [r for r in self._prompts.values() if r.get("owner_agent") == owner]

    def summary(self) -> dict:
        return {"total": len(self._prompts), "by_owner": {}}


class PromptVersionRegistry:
    def __init__(self):
        self._versions = {}

    def add_version(self, prompt_id: str, version: int, content: str, benchmark_score: float = 0.0) -> dict:
        key = f"{prompt_id}:v{version}"
        self._versions[key] = {"prompt_id": prompt_id, "version": version, "content": content, "benchmark_score": benchmark_score}
        return self._versions[key]

    def get_history(self, prompt_id: str) -> list[dict]:
        return [v for k, v in self._versions.items() if k.startswith(f"{prompt_id}:")]


class PromptBenchmarkRegistry:
    def __init__(self):
        self._benchmarks = []

    def record(self, prompt_id: str, version: int, score: float, test_input: str, test_output: str) -> dict:
        record = {
            "prompt_id": prompt_id,
            "version": version,
            "score": score,
            "test_input": test_input,
            "test_output": test_output,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._benchmarks.append(record)
        return record


PROMPTS = PromptRegistry()
PROMPT_VERSIONS = PromptVersionRegistry()
PROMPT_BENCHMARKS = PromptBenchmarkRegistry()

__all__ = ["PromptRegistry", "PromptVersionRegistry", "PromptBenchmarkRegistry", "PROMPTS", "PROMPT_VERSIONS", "PROMPT_BENCHMARKS"]