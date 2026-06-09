from __future__ import annotations

from typing import Any


class CapabilityEvidenceEngine:
    """Accumulates evidence from validation scenarios for capabilities."""

    def __init__(self, evidence_registry, audit_layer=None):
        self.evidence_registry = evidence_registry
        self.audit_layer = audit_layer

    def record_evidence(self, capability_id: str, scenario_id: str,
                        evidence_type: str, result: str, metric: float = 0.0,
                        source_artifacts: list[str] | None = None,
                        source_hashes: list[str] | None = None,
                        confidence: float = 0.0, risk_observation: str = "",
                        reviewer_agent: str = "Sage",
                        audit_trace_id: str = "") -> Any:
        record = self.evidence_registry.create(
            capability_id=capability_id,
            scenario_id=scenario_id,
            evidence_type=evidence_type,
            result=result,
            metric=metric,
            source_artifacts=source_artifacts or [],
            source_hashes=source_hashes or [],
            confidence=confidence,
            risk_observation=risk_observation,
            reviewer_agent=reviewer_agent,
            audit_trace_id=audit_trace_id,
        )
        if self.audit_layer:
            self.audit_layer.record(
                agent=reviewer_agent,
                action="EVIDENCE_RECORDED",
                record_type="evidence",
                record_id=record.evidence_id,
                details={
                    "capability_id": capability_id,
                    "scenario_id": scenario_id,
                    "evidence_type": evidence_type,
                    "result": result,
                    "metric": metric,
                },
            )
        return record

    def record_validation_evidence(self, capability_id: str, scenario_id: str,
                                    validation_result: dict[str, Any],
                                    reviewer_agent: str = "Sage") -> Any:
        return self.record_evidence(
            capability_id=capability_id,
            scenario_id=scenario_id,
            evidence_type="VALIDATION_RESULT",
            result=validation_result.get("status", "UNKNOWN"),
            metric=1.0 if validation_result.get("status") == "PASSED" else 0.0,
            source_artifacts=[validation_result.get("scenario_id", "")],
            confidence=1.0 if validation_result.get("status") == "PASSED" else 0.0,
            reviewer_agent=reviewer_agent,
        )

    def record_documentation_evidence(self, capability_id: str, scenario_id: str,
                                       documentation_found: bool,
                                       reviewer_agent: str = "Sage") -> Any:
        return self.record_evidence(
            capability_id=capability_id,
            scenario_id=scenario_id,
            evidence_type="DOCUMENTATION",
            result="FOUND" if documentation_found else "NOT_FOUND",
            metric=1.0 if documentation_found else 0.0,
            confidence=1.0 if documentation_found else 0.0,
            reviewer_agent=reviewer_agent,
        )

    def evaluate_evidence_sufficiency(self, capability_id: str) -> dict[str, Any]:
        records = self.evidence_registry.get_evidence_for_capability(capability_id)
        if not records:
            return {
                "capability_id": capability_id,
                "has_evidence": False,
                "evidence_count": 0,
                "avg_confidence": 0.0,
                "avg_metric": 0.0,
                "evidence_types": [],
                "sufficient": False,
                "gap": "No evidence recorded",
            }
        confidences = [r.confidence for r in records]
        metrics = [r.metric for r in records]
        types = list({r.evidence_type for r in records})
        avg_conf = sum(confidences) / len(confidences)
        avg_metric = sum(metrics) / len(metrics)
        sufficient = avg_conf >= 0.5 and avg_metric >= 0.5 and len(types) >= 2
        return {
            "capability_id": capability_id,
            "has_evidence": True,
            "evidence_count": len(records),
            "avg_confidence": round(avg_conf, 2),
            "avg_metric": round(avg_metric, 2),
            "evidence_types": types,
            "sufficient": sufficient,
            "gap": None if sufficient else "Need more evidence types or higher confidence",
        }
