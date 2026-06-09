from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from memory.decision_trace_registry import DecisionTraceRegistry
from memory.schemas import DecisionTraceRecord


@dataclass
class DecisionTraceResult:
    trace: DecisionTraceRecord | None
    status: str
    issues: list[str]


REQUIRED_EVIDENCE_FIELDS = {"decision", "reasoning", "evidence", "outcome"}


class DecisionTracePipeline:
    def __init__(self, registry: DecisionTraceRegistry):
        self.registry = registry

    def process(self, payload: dict[str, Any]) -> DecisionTraceResult:
        issues = self._validate(payload)
        if issues:
            return DecisionTraceResult(trace=None, status="BLOCKED", issues=issues)
        trace = self.registry.record(**payload)
        return DecisionTraceResult(trace=trace, status="CANDIDATE", issues=[])

    def _validate(self, payload: dict[str, Any]) -> list[str]:
        issues = []
        for field in REQUIRED_EVIDENCE_FIELDS:
            if not payload.get(field):
                issues.append(f"missing required field: {field}")
        agent = payload.get("agent")
        if not agent:
            issues.append("missing agent")
        evidence = payload.get("evidence", [])
        if not isinstance(evidence, list) or len(evidence) < 1:
            issues.append("evidence must be a non-empty list")
        return issues

    def submit_for_review(self, trace_id: str, reviewer: str) -> DecisionTraceResult:
        try:
            reviewed = self.registry.mark_reviewed(trace_id, reviewer)
            return DecisionTraceResult(trace=reviewed, status="REVIEWED", issues=[])
        except (KeyError, ValueError) as exc:
            return DecisionTraceResult(trace=None, status="ERROR", issues=[str(exc)])

    def approve(self, trace_id: str, reviewer: str) -> DecisionTraceResult:
        try:
            approved = self.registry.approve(trace_id, reviewer)
            return DecisionTraceResult(trace=approved, status="APPROVED", issues=[])
        except (KeyError, ValueError) as exc:
            return DecisionTraceResult(trace=None, status="ERROR", issues=[str(exc)])
