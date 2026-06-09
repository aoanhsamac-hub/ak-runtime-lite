from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Mapping, Protocol, Sequence, TypedDict


class LearningMetricsValidationError(ValueError):
    """Raised when learning metrics input violates AK governance contracts."""


class EvidenceRecord(TypedDict, total=False):
    evidence_id: str
    context: str
    outcome: str
    success: bool
    confidence: float
    dataset_refs: Sequence[str]


class GovernanceContext(TypedDict, total=False):
    issue_id: str
    actor: str
    reviewer: str
    risk_level: str
    governance_valid: bool
    source: str


class EvidenceProvider(Protocol):
    def evidence_records(self) -> Sequence[EvidenceRecord]:
        """Return already-governed evidence records without backend access."""


@dataclass(frozen=True)
class LearningMetrics:
    confidence_score: float
    success_rate: float
    recurrence_count: int
    evidence_count: int
    context_diversity: float
    outcome_stability: float
    dataset_support: float
    blocked: bool = False
    reason: str = "metrics calculated"
    metadata: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "confidence_score": self.confidence_score,
            "success_rate": self.success_rate,
            "recurrence_count": self.recurrence_count,
            "evidence_count": self.evidence_count,
            "context_diversity": self.context_diversity,
            "outcome_stability": self.outcome_stability,
            "dataset_support": self.dataset_support,
            "blocked": self.blocked,
            "reason": self.reason,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class MetricsCalculatorConfig:
    minimum_evidence: int = 3
    precision: int = 4


class MetricsValidationLayer:
    REQUIRED_FIELDS = ("evidence_id", "context", "outcome", "success", "confidence")

    def validate_governance(self, context: GovernanceContext) -> None:
        if not context:
            raise LearningMetricsValidationError("governance context is required")
        if context.get("governance_valid") is not True:
            raise LearningMetricsValidationError("governance context is invalid")
        if not str(context.get("issue_id", "")).strip():
            raise LearningMetricsValidationError("issue_id is required for WP3.5 metrics calculation")
        if not str(context.get("reviewer", "")).strip():
            raise LearningMetricsValidationError("reviewer is required for WP3.5 metrics calculation")

    def validate_records(self, records: Sequence[Mapping[str, object]]) -> None:
        if not records:
            raise LearningMetricsValidationError("at least one evidence record is required")
        for index, record in enumerate(records):
            missing = [field for field in self.REQUIRED_FIELDS if field not in record]
            if missing:
                raise LearningMetricsValidationError(f"evidence record {index} missing fields: {', '.join(missing)}")
            confidence = record["confidence"]
            if not isinstance(confidence, (int, float)):
                raise LearningMetricsValidationError(f"evidence record {index} confidence must be numeric")
            if confidence < 0 or confidence > 1:
                raise LearningMetricsValidationError(f"evidence record {index} confidence must be between 0 and 1")
            if not isinstance(record["success"], bool):
                raise LearningMetricsValidationError(f"evidence record {index} success must be boolean")
            for text_field in ("evidence_id", "context", "outcome"):
                if not str(record[text_field]).strip():
                    raise LearningMetricsValidationError(f"evidence record {index} {text_field} is required")


class MetricsCalculator:
    def __init__(self, config: MetricsCalculatorConfig | None = None, validator: MetricsValidationLayer | None = None):
        self.config = config or MetricsCalculatorConfig()
        self.validator = validator or MetricsValidationLayer()

    def calculate(self, evidence: Sequence[EvidenceRecord] | EvidenceProvider, governance: GovernanceContext) -> LearningMetrics:
        records = self._records_from(evidence)
        self.validator.validate_governance(governance)
        self.validator.validate_records(records)

        recurrence_count = len(records)
        evidence_count = len({str(record["evidence_id"]) for record in records})
        success_rate = self._ratio(sum(1 for record in records if bool(record["success"])), recurrence_count)
        context_diversity = self._ratio(len({str(record["context"]).strip().lower() for record in records}), recurrence_count)
        outcome_stability = self._outcome_stability(records)
        dataset_support = self._ratio(sum(1 for record in records if self._dataset_refs(record)), recurrence_count)
        average_record_confidence = sum(float(record["confidence"]) for record in records) / recurrence_count
        evidence_strength = min(1.0, evidence_count / max(1, self.config.minimum_evidence))

        confidence_score = self._round(
            success_rate * 0.25
            + evidence_strength * 0.20
            + context_diversity * 0.15
            + outcome_stability * 0.15
            + dataset_support * 0.15
            + average_record_confidence * 0.10
        )

        return LearningMetrics(
            confidence_score=confidence_score,
            success_rate=self._round(success_rate),
            recurrence_count=recurrence_count,
            evidence_count=evidence_count,
            context_diversity=self._round(context_diversity),
            outcome_stability=self._round(outcome_stability),
            dataset_support=self._round(dataset_support),
            metadata={
                "issue_id": governance["issue_id"],
                "reviewer": governance["reviewer"],
                "risk_level": governance.get("risk_level", "UNKNOWN"),
                "source": governance.get("source", "UNKNOWN"),
                "minimum_evidence": self.config.minimum_evidence,
                "phase": "WP3.5 Phase 1A",
                "mode": "advisory_metrics_only",
            },
        )

    def blocked_result(self, reason: str) -> LearningMetrics:
        return LearningMetrics(
            confidence_score=0.0,
            success_rate=0.0,
            recurrence_count=0,
            evidence_count=0,
            context_diversity=0.0,
            outcome_stability=0.0,
            dataset_support=0.0,
            blocked=True,
            reason=reason,
        )

    def _records_from(self, evidence: Sequence[EvidenceRecord] | EvidenceProvider) -> list[EvidenceRecord]:
        if hasattr(evidence, "evidence_records"):
            return list(evidence.evidence_records())
        return list(evidence)

    def _dataset_refs(self, record: Mapping[str, object]) -> Sequence[str]:
        refs = record.get("dataset_refs", ())
        if refs is None:
            return ()
        if isinstance(refs, str):
            return (refs,) if refs.strip() else ()
        return tuple(str(item) for item in refs if str(item).strip())

    def _outcome_stability(self, records: Sequence[Mapping[str, object]]) -> float:
        outcomes = [str(record["outcome"]).strip().lower() for record in records]
        most_common = Counter(outcomes).most_common(1)[0][1]
        return most_common / len(records)

    def _ratio(self, numerator: int, denominator: int) -> float:
        if denominator <= 0:
            return 0.0
        return numerator / denominator

    def _round(self, value: float) -> float:
        return round(value, self.config.precision)
