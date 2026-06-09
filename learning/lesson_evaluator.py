from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Protocol, Sequence


class LessonStatus(Enum):
    DRAFT = "DRAFT"
    REVIEWED = "REVIEWED"
    APPROVED = "APPROVED"
    DEPRECATED = "DEPRECATED"
    QUARANTINE = "QUARANTINE"


class InformationClassification(Enum):
    I0_OFFICIAL_VERIFIED = "I0_OFFICIAL_VERIFIED"
    I1_PROBABLE = "I1_PROBABLE"
    I2_HYPOTHESIS = "I2_HYPOTHESIS"
    I3_THEORY = "I3_THEORY"
    I4_SCENARIO = "I4_SCENARIO"
    I5_SPECULATIVE = "I5_SPECULATIVE"
    I6_FICTION = "I6_FICTION"
    I7_LEGEND = "I7_LEGEND"
    I8_RUMOR = "I8_RUMOR"
    I9_REJECTED = "I9_REJECTED"


class LessonEvaluationError(ValueError):
    """Raised when lesson evaluation violates AK governance contracts."""


@dataclass(frozen=True)
class LessonEvaluation:
    lesson_id: str
    status: LessonStatus
    quality_score: float
    evidence_count: int
    blocked: bool = False
    reason: str = "evaluated"
    source: str | None = None
    author: str | None = None
    reviewer: str | None = None
    date: str | None = None
    validation_result: str | None = None
    version: str | None = None
    information_classification: InformationClassification | None = None
    metadata: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        d = {
            "lesson_id": self.lesson_id,
            "status": self.status.value,
            "quality_score": self.quality_score,
            "evidence_count": self.evidence_count,
            "blocked": self.blocked,
            "reason": self.reason,
            "source": self.source,
            "author": self.author,
            "reviewer": self.reviewer,
            "date": self.date,
            "validation_result": self.validation_result,
            "version": self.version,
            "information_classification": self.information_classification.value if self.information_classification else None,
            "metadata": dict(self.metadata),
        }
        return d


class LessonProvider(Protocol):
    def lesson_records(self) -> Sequence[Mapping[str, object]]:
        """Return already-governed lesson records without backend access."""


class LessonValidationLayer:
    REQUIRED_FIELDS = ("lesson_id", "context", "outcome", "status")

    def validate_governance(self, context: Mapping[str, object]) -> None:
        if not context:
            raise LessonEvaluationError("governance context is required")
        if context.get("governance_valid") is not True:
            raise LessonEvaluationError("governance context is invalid")
        if not str(context.get("issue_id", "")).strip():
            raise LessonEvaluationError("issue_id is required for WP3.5 lesson evaluation")
        if not str(context.get("reviewer", "")).strip():
            raise LessonEvaluationError("reviewer is required for WP3.5 lesson evaluation")

    def validate_lesson(self, lesson: Mapping[str, object]) -> None:
        missing = [f for f in self.REQUIRED_FIELDS if f not in lesson]
        if missing:
            raise LessonEvaluationError(f"lesson missing fields: {', '.join(missing)}")
        lesson_id = lesson.get("lesson_id", "")
        if not str(lesson_id).strip():
            raise LessonEvaluationError("lesson_id is required")

    def validate_status_transition(
        self, from_status: str, to_status: str
    ) -> None:
        allowed = {
            LessonStatus.DRAFT.value: [LessonStatus.DRAFT.value, LessonStatus.REVIEWED.value, LessonStatus.QUARANTINE.value],
            LessonStatus.REVIEWED.value: [LessonStatus.APPROVED.value, LessonStatus.DRAFT.value, LessonStatus.QUARANTINE.value],
            LessonStatus.APPROVED.value: [LessonStatus.DEPRECATED.value, LessonStatus.QUARANTINE.value],
            LessonStatus.DEPRECATED.value: [],
            LessonStatus.QUARANTINE.value: [LessonStatus.DRAFT.value, LessonStatus.REVIEWED.value],
        }
        if to_status not in allowed.get(from_status, []):
            raise LessonEvaluationError(f"invalid status transition: {from_status} -> {to_status}")


@dataclass(frozen=True)
class LessonEvaluatorConfig:
    precision: int = 4


class LessonEvaluator:
    def __init__(self, config: LessonEvaluatorConfig | None = None, validator: LessonValidationLayer | None = None):
        self.config = config or LessonEvaluatorConfig()
        self.validator = validator or LessonValidationLayer()

    def evaluate(
        self,
        lesson: Mapping[str, object],
        governance: Mapping[str, object],
    ) -> LessonEvaluation:
        self.validator.validate_governance(governance)
        self.validator.validate_lesson(lesson)

        status = self._parse_status(lesson.get("status", "DRAFT"))
        evidence = self._extract_evidence(lesson)
        quality_score = self._calculate_quality(evidence)

        return LessonEvaluation(
            lesson_id=str(lesson["lesson_id"]),
            status=status,
            quality_score=quality_score,
            evidence_count=len(evidence),
            reviewer=governance.get("reviewer"),
            date=governance.get("timestamp"),
            metadata={
                "issue_id": governance.get("issue_id"),
                "source": governance.get("source", "UNKNOWN"),
                "phase": "WP3.5 Phase 1B",
                "mode": "advisory_evaluation_only",
            },
        )

    def block_result(self, lesson_id: str, reason: str) -> LessonEvaluation:
        return LessonEvaluation(
            lesson_id=lesson_id,
            status=LessonStatus.QUARANTINE,
            quality_score=0.0,
            evidence_count=0,
            blocked=True,
            reason=reason,
            metadata={"blocked": True, "reason": reason},
        )

    def _parse_status(self, value: str | LessonStatus) -> LessonStatus:
        if isinstance(value, LessonStatus):
            return value
        try:
            return LessonStatus(value.upper())
        except ValueError:
            raise LessonEvaluationError(f"invalid lesson status: {value}")

    def _extract_evidence(self, lesson: Mapping[str, object]) -> Sequence[Mapping[str, object]]:
        evidence = lesson.get("evidence", ())
        if evidence is None:
            return ()
        return list(evidence) if isinstance(evidence, list) else []

    def _calculate_quality(self, evidence: Sequence[Mapping[str, object]]) -> float:
        if not evidence:
            return 0.0
        total = sum(float(record.get("confidence", 0.0)) for record in evidence if isinstance(record.get("confidence"), (int, float)))
        return round(total / len(evidence), self.config.precision)