from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from memory.dataset_registry import DatasetRegistry
from memory.schemas import DatasetRecord


@dataclass
class DatasetProductionResult:
    dataset: DatasetRecord | None
    status: str
    issues: list[str]


REQUIRED_DATASET_FIELDS = {"name", "source", "owner_agent", "reviewer_agent", "risk_level"}


class DatasetProductionPipeline:
    def __init__(self, registry: DatasetRegistry):
        self.registry = registry

    def process(self, payload: dict[str, Any]) -> DatasetProductionResult:
        issues = self._validate(payload)
        if issues:
            return DatasetProductionResult(dataset=None, status="BLOCKED", issues=issues)
        dataset = self.registry.create(**payload)
        return DatasetProductionResult(dataset=dataset, status="CANDIDATE", issues=[])

    def _validate(self, payload: dict[str, Any]) -> list[str]:
        issues = []
        for field in REQUIRED_DATASET_FIELDS:
            if not payload.get(field):
                issues.append(f"missing required field: {field}")
        source = payload.get("source", "")
        if source and not isinstance(source, str):
            issues.append("source must be a string")
        return issues
