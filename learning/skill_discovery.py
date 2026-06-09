from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from typing import Mapping, Sequence
from uuid import uuid4

from learning.skill_evidence_policy import RiskClassification


class SkillDiscoveryError(ValueError):
    """Raised when skill discovery violates AK governance contracts."""


class CandidateStatus(Enum):
    DISCOVERED = "DISCOVERED"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"
    MERGED = "MERGED"


@dataclass(frozen=True)
class EvidencePattern:
    trigger_conditions: Sequence[str]
    reasoning_path: Sequence[str]
    outcome_pattern: str
    scope_boundaries: Mapping[str, object]
    method_summary: str
    limitations: Sequence[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "trigger_conditions": list(self.trigger_conditions),
            "reasoning_path": list(self.reasoning_path),
            "outcome_pattern": self.outcome_pattern,
            "scope_boundaries": dict(self.scope_boundaries),
            "method_summary": self.method_summary,
            "limitations": list(self.limitations),
        }


@dataclass
class EvidenceRequirements:
    minimum_lessons: int = 3
    minimum_distinct_tasks: int = 2
    minimum_evidence_weight: float = 2.5
    require_sage_review: bool = False
    require_janus_coordination: bool = False


_RISK_SEVERITY: dict[RiskClassification, int] = {
    RiskClassification.LOW: 0,
    RiskClassification.MEDIUM: 1,
    RiskClassification.HIGH: 2,
    RiskClassification.SOVEREIGN: 3,
}


def _max_risk(a: RiskClassification, b: RiskClassification) -> RiskClassification:
    return a if _RISK_SEVERITY.get(a, 0) >= _RISK_SEVERITY.get(b, 0) else b


@dataclass(frozen=True)
class SkillCandidate:
    candidate_id: str
    name: str
    description: str
    source_lesson_ids: Sequence[str]
    evidence_pattern: EvidencePattern
    confidence_score: float
    risk_classification: RiskClassification
    deduplication_key: str
    discovery_trace_id: str
    discovered_by: str
    discovered_at: str
    evidence_summary: Mapping[str, object]
    status: CandidateStatus
    governance_issue_id: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "candidate_id": self.candidate_id,
            "name": self.name,
            "description": self.description,
            "source_lesson_ids": list(self.source_lesson_ids),
            "evidence_pattern": self.evidence_pattern.to_dict(),
            "confidence_score": self.confidence_score,
            "risk_classification": self.risk_classification.value,
            "deduplication_key": self.deduplication_key,
            "discovery_trace_id": self.discovery_trace_id,
            "discovered_by": self.discovered_by,
            "discovered_at": self.discovered_at,
            "evidence_summary": dict(self.evidence_summary),
            "status": self.status.value,
            "governance_issue_id": self.governance_issue_id,
        }


class SkillDiscoveryValidationLayer:
    REQUIRED_LESSON_FIELDS = (
        "lesson_id", "source", "author", "reviewer",
        "status", "evidence", "context", "outcome",
    )

    def validate_governance(self, context: Mapping[str, object]) -> None:
        if not context:
            raise SkillDiscoveryError("governance context is required")
        if context.get("governance_valid") is not True:
            raise SkillDiscoveryError("governance context is invalid")
        if not str(context.get("issue_id", "")).strip():
            raise SkillDiscoveryError("issue_id is required for WP3.5 skill discovery")
        if not str(context.get("reviewer", "")).strip():
            raise SkillDiscoveryError("reviewer is required for WP3.5 skill discovery")

    def validate_approved_lessons(self, lessons: Sequence[Mapping[str, object]]) -> None:
        if not lessons:
            raise SkillDiscoveryError("at least one approved lesson is required")
        for index, lesson in enumerate(lessons):
            missing = [f for f in self.REQUIRED_LESSON_FIELDS if f not in lesson]
            if missing:
                raise SkillDiscoveryError(
                    f"lesson {index} missing fields: {', '.join(missing)}"
                )
            status = str(lesson.get("status", "")).upper()
            if status != "APPROVED":
                raise SkillDiscoveryError(
                    f"lesson {index} status must be APPROVED, got {status}"
                )


class SkillDiscovery:
    def __init__(
        self,
        requirements: EvidenceRequirements | None = None,
        validator: SkillDiscoveryValidationLayer | None = None,
    ):
        self._requirements = requirements or EvidenceRequirements()
        self._validator = validator or SkillDiscoveryValidationLayer()
        self._discovered_by: str = ""

    def discover(
        self,
        approved_lessons: Sequence[Mapping[str, object]],
        governance: Mapping[str, object],
    ) -> Sequence[SkillCandidate]:
        self._validator.validate_governance(governance)
        self._validator.validate_approved_lessons(approved_lessons)
        self._discovered_by = str(governance.get("actor", "Hermes"))
        discovered_at = str(
            governance.get("timestamp", datetime.now(timezone.utc).isoformat())
        )
        governance_issue_id = str(governance.get("issue_id", ""))

        groups = self._group_by_trigger(approved_lessons)
        candidates: list[SkillCandidate] = []

        for group in groups:
            if len(group) < self._requirements.minimum_lessons:
                continue

            distinct_tasks = len(
                {
                    str(l.get("context", "")).strip().lower()
                    for l in group
                    if str(l.get("context", "")).strip()
                }
            )
            if distinct_tasks < self._requirements.minimum_distinct_tasks:
                continue

            source_lesson_ids = [str(l.get("lesson_id", "")) for l in group]
            trigger_conditions = self._extract_triggers(group)
            reasoning_path = self._extract_reasoning(group)
            outcome_pattern = self._derive_outcome_pattern(group)
            scope_boundaries = self._infer_scope(group)
            method_summary = self._summarize_method(group)
            limitations = self._find_limitations(group)

            trigger_similarity = self._compute_trigger_similarity(group)
            outcome_consistency = self._compute_outcome_consistency(group)
            evidence_weight = self._compute_evidence_weight(group, outcome_consistency)
            if evidence_weight < self._requirements.minimum_evidence_weight:
                continue

            scope_clarity = self._compute_scope_clarity(scope_boundaries)
            confidence_score = self._round(
                evidence_weight * 0.40
                + trigger_similarity * 0.25
                + outcome_consistency * 0.20
                + scope_clarity * 0.15
            )

            sovereign_asset_impact = self._check_sovereign_assets(group)
            risk_classification = self._classify_risk(
                sovereign_asset_impact, evidence_weight, len(group)
            )

            canonical_name = self._generate_canonical_name(group)
            description = (
                f"Skill candidate discovered from {len(group)} approved lessons "
                f"in {scope_boundaries.get('domain', 'unknown')} domain"
            )
            trace_id = str(uuid4())
            dedup_key = self._build_deduplication_key(
                canonical_name, trigger_conditions
            )
            candidate_id = f"CANDIDATE-{trace_id[:8].upper()}"

            evidence_summary: dict[str, object] = {
                "lesson_count": len(group),
                "distinct_tasks": distinct_tasks,
                "evidence_weight": evidence_weight,
                "trigger_similarity": trigger_similarity,
                "outcome_consistency": outcome_consistency,
                "scope_clarity": scope_clarity,
                "sovereign_asset_impact": sovereign_asset_impact,
                "risk_classification": risk_classification.value,
            }

            pattern = EvidencePattern(
                trigger_conditions=trigger_conditions,
                reasoning_path=reasoning_path,
                outcome_pattern=outcome_pattern,
                scope_boundaries=scope_boundaries,
                method_summary=method_summary,
                limitations=limitations,
            )

            candidate = SkillCandidate(
                candidate_id=candidate_id,
                name=canonical_name,
                description=description,
                source_lesson_ids=source_lesson_ids,
                evidence_pattern=pattern,
                confidence_score=self._round(confidence_score),
                risk_classification=risk_classification,
                deduplication_key=dedup_key,
                discovery_trace_id=trace_id,
                discovered_by=self._discovered_by,
                discovered_at=discovered_at,
                evidence_summary=evidence_summary,
                status=CandidateStatus.DISCOVERED,
                governance_issue_id=governance_issue_id,
            )

            candidates.append(candidate)

        return self._deduplicate(candidates)

    def get_deduplication_threshold(self) -> float:
        return 0.8

    def get_candidate_evidence_requirements(self) -> EvidenceRequirements:
        return self._requirements

    def blocked_result(self, reason: str) -> Sequence[SkillCandidate]:
        return []

    def _group_by_trigger(
        self, lessons: Sequence[Mapping[str, object]]
    ) -> list[list[Mapping[str, object]]]:
        groups: dict[str, list[Mapping[str, object]]] = {}
        for lesson in lessons:
            ctx = str(lesson.get("context", "")).strip().lower()
            domain = ctx.split()[0] if ctx.split() else "unknown"
            groups.setdefault(domain, []).append(lesson)
        return list(groups.values())

    def _extract_triggers(
        self, lessons: Sequence[Mapping[str, object]]
    ) -> list[str]:
        triggers: set[str] = set()
        for lesson in lessons:
            ctx = str(lesson.get("context", "")).strip().lower()
            if ctx:
                triggers.add(ctx)
            outcome = str(lesson.get("outcome", "")).strip().lower()
            if outcome:
                triggers.add(outcome)
            evidence_list = lesson.get("evidence", [])
            if isinstance(evidence_list, list):
                for ev in evidence_list:
                    if isinstance(ev, dict):
                        ectx = str(ev.get("context", "")).strip().lower()
                        if ectx:
                            triggers.add(ectx)
        return sorted(triggers)

    def _extract_reasoning(
        self, lessons: Sequence[Mapping[str, object]]
    ) -> list[str]:
        steps: list[str] = []
        for lesson in lessons:
            outcome = str(lesson.get("outcome", "")).strip()
            if outcome and outcome not in steps:
                steps.append(outcome)
        return steps

    def _derive_outcome_pattern(
        self, lessons: Sequence[Mapping[str, object]]
    ) -> str:
        outcomes = [
            str(l.get("outcome", "")).strip().lower()
            for l in lessons
            if str(l.get("outcome", "")).strip()
        ]
        if not outcomes:
            return "unknown"
        return Counter(outcomes).most_common(1)[0][0]

    def _infer_scope(
        self, lessons: Sequence[Mapping[str, object]]
    ) -> dict[str, object]:
        agents: set[str] = set()
        contexts: set[str] = set()
        sources: set[str] = set()
        for lesson in lessons:
            if str(lesson.get("author", "")).strip():
                agents.add(str(lesson["author"]).strip())
            if str(lesson.get("context", "")).strip():
                contexts.add(str(lesson["context"]).strip())
            if str(lesson.get("source", "")).strip():
                sources.add(str(lesson["source"]).strip())

        domain = "unknown"
        if contexts:
            first_ctx = next(iter(contexts))
            domain = first_ctx.split()[0] if first_ctx.split() else "unknown"

        return {
            "domain": domain,
            "applicable_agents": sorted(agents),
            "applicable_contexts": sorted(contexts),
            "sources": sorted(sources),
        }

    def _summarize_method(
        self, lessons: Sequence[Mapping[str, object]]
    ) -> str:
        contexts = [
            str(l.get("context", "")).strip()
            for l in lessons
            if str(l.get("context", "")).strip()
        ]
        outcomes = [
            str(l.get("outcome", "")).strip()
            for l in lessons
            if str(l.get("outcome", "")).strip()
        ]
        if not contexts or not outcomes:
            return "No clear method extracted"
        return (
            f"Based on {len(lessons)} lessons across {len(set(contexts))} contexts, "
            f"produce {Counter(outcomes).most_common(1)[0][0]}"
        )

    def _find_limitations(
        self, lessons: Sequence[Mapping[str, object]]
    ) -> list[str]:
        limitations: list[str] = []
        if len(lessons) < 5:
            limitations.append(f"Limited lesson count ({len(lessons)})")
        contexts = {
            str(l.get("context", "")).strip().lower()
            for l in lessons
            if str(l.get("context", "")).strip()
        }
        if len(contexts) < 2:
            limitations.append("Limited context diversity")
        return limitations

    def _compute_evidence_weight(
        self, lessons: Sequence[Mapping[str, object]], outcome_consistency: float | None = None
    ) -> float:
        source_d = self._compute_source_diversity(lessons)
        dataset_d = self._compute_dataset_diversity(lessons)
        context_d = self._compute_context_diversity(lessons)
        reviewer_d = self._compute_reviewer_diversity(lessons)
        outcome_c = outcome_consistency if outcome_consistency is not None else self._compute_outcome_consistency(lessons)
        source_score = min(5.0, source_d * 5)
        dataset_score = min(5.0, dataset_d * 5)
        context_score = min(5.0, context_d * 5)
        reviewer_score = min(5.0, reviewer_d * 5)
        outcome_score = min(5.0, outcome_c * 5)
        return self._round(
            source_score * 0.20
            + dataset_score * 0.20
            + context_score * 0.20
            + reviewer_score * 0.20
            + outcome_score * 0.20
        )

    def _compute_source_diversity(
        self, lessons: Sequence[Mapping[str, object]]
    ) -> float:
        sources = {
            str(l.get("source", "")).strip().lower()
            for l in lessons
            if str(l.get("source", "")).strip()
        }
        if not sources or not lessons:
            return 0.0
        return len(sources) / len(lessons)

    def _compute_dataset_diversity(
        self, lessons: Sequence[Mapping[str, object]]
    ) -> float:
        all_refs: set[str] = set()
        for lesson in lessons:
            evidence_list = lesson.get("evidence", [])
            if isinstance(evidence_list, list):
                for ev in evidence_list:
                    refs = (
                        ev.get("dataset_refs", []) if isinstance(ev, dict) else []
                    )
                    if isinstance(refs, list):
                        all_refs.update(str(r) for r in refs if str(r).strip())
        if not all_refs or not lessons:
            return 0.0
        return min(1.0, len(all_refs) / max(1, len(lessons)))

    def _compute_context_diversity(
        self, lessons: Sequence[Mapping[str, object]]
    ) -> float:
        contexts = {
            str(l.get("context", "")).strip().lower()
            for l in lessons
            if str(l.get("context", "")).strip()
        }
        if not contexts or not lessons:
            return 0.0
        return len(contexts) / len(lessons)

    def _compute_reviewer_diversity(
        self, lessons: Sequence[Mapping[str, object]]
    ) -> float:
        reviewers = {
            str(l.get("reviewer", "")).strip().lower()
            for l in lessons
            if str(l.get("reviewer", "")).strip()
        }
        if not reviewers or not lessons:
            return 0.0
        return len(reviewers) / len(lessons)

    def _compute_outcome_consistency(
        self, lessons: Sequence[Mapping[str, object]]
    ) -> float:
        outcomes: list[bool] = []
        for lesson in lessons:
            evidence_list = lesson.get("evidence", [])
            if isinstance(evidence_list, list):
                for ev in evidence_list:
                    if isinstance(ev, dict) and isinstance(
                        ev.get("success"), bool
                    ):
                        outcomes.append(ev["success"])
        if not outcomes:
            return 0.0
        positive = sum(1 for o in outcomes if o)
        return positive / len(outcomes)

    def _compute_trigger_similarity(
        self, lessons: Sequence[Mapping[str, object]]
    ) -> float:
        triggers_list: list[set[str]] = []
        for lesson in lessons:
            ctx = str(lesson.get("context", "")).strip().lower()
            outcome = str(lesson.get("outcome", "")).strip().lower()
            t_set: set[str] = set()
            if ctx:
                t_set.update(ctx.split())
            if outcome:
                t_set.update(outcome.split())
            triggers_list.append(t_set)

        if len(triggers_list) < 2:
            return 1.0

        total_jaccard = 0.0
        pairs = 0
        for i in range(len(triggers_list)):
            for j in range(i + 1, len(triggers_list)):
                a, b = triggers_list[i], triggers_list[j]
                if not a and not b:
                    similarity = 1.0
                elif not a or not b:
                    similarity = 0.0
                else:
                    intersection = len(a & b)
                    union = len(a | b)
                    similarity = intersection / union if union > 0 else 1.0
                total_jaccard += similarity
                pairs += 1

        return total_jaccard / pairs if pairs > 0 else 1.0

    def _compute_scope_clarity(
        self, scope: Mapping[str, object]
    ) -> float:
        agents = scope.get("applicable_agents", [])
        contexts = scope.get("applicable_contexts", [])
        sources = scope.get("sources", [])
        clarity = 0.0
        if isinstance(agents, list) and len(agents) >= 2:
            clarity += 0.4
        if isinstance(contexts, list) and len(contexts) >= 2:
            clarity += 0.3
        if isinstance(sources, list) and len(sources) >= 2:
            clarity += 0.3
        return min(1.0, clarity)

    def _check_sovereign_assets(
        self, lessons: Sequence[Mapping[str, object]]
    ) -> bool:
        sovereign_domains = (
            "constitution",
            "risk_kernel",
            "security_law",
            "execution_law",
            "state_corpus",
            "governance",
        )
        for lesson in lessons:
            context = str(lesson.get("context", "")).strip().lower()
            for domain in sovereign_domains:
                if domain in context:
                    return True
            outcome = str(lesson.get("outcome", "")).strip().lower()
            for domain in sovereign_domains:
                if domain in outcome:
                    return True
        return False

    def _classify_risk(
        self,
        sovereign: bool,
        evidence_weight: float,
        lesson_count: int,
    ) -> RiskClassification:
        if sovereign:
            return RiskClassification.SOVEREIGN
        if evidence_weight >= 4.0 and lesson_count >= 5:
            return RiskClassification.HIGH
        if evidence_weight >= 3.0:
            return RiskClassification.MEDIUM
        return RiskClassification.LOW

    def _generate_canonical_name(
        self, lessons: Sequence[Mapping[str, object]]
    ) -> str:
        first_ctx = (
            str(lessons[0].get("context", "")).strip().lower()
            if lessons
            else "unknown"
        )
        domain = first_ctx.split()[0] if first_ctx.split() else "unknown"
        first_outcome = (
            str(lessons[0].get("outcome", "")).strip().lower()
            if lessons
            else "unknown"
        )
        words = first_outcome.split()[:2] if first_outcome.split() else ["unknown"]
        task = "_".join(words)
        return f"{domain}.{task}"

    def _build_deduplication_key(
        self, name: str, triggers: Sequence[str]
    ) -> str:
        raw = name + "|" + "|".join(sorted(triggers))
        return sha256(raw.encode("utf-8")).hexdigest()[:16]

    def _deduplicate(
        self, candidates: Sequence[SkillCandidate]
    ) -> Sequence[SkillCandidate]:
        if len(candidates) <= 1:
            return candidates

        seen: dict[str, SkillCandidate] = {}
        result: list[SkillCandidate] = []
        threshold = self.get_deduplication_threshold()

        for candidate in candidates:
            merged = False

            if candidate.deduplication_key in seen:
                merged_candidate = self._merge_candidates(
                    seen[candidate.deduplication_key], candidate
                )
                seen[candidate.deduplication_key] = merged_candidate
                result = [
                    c
                    for c in result
                    if c.candidate_id != seen[candidate.deduplication_key].candidate_id
                ]
                result.append(merged_candidate)
                merged = True
            else:
                for existing_key, existing in list(seen.items()):
                    jaccard = self._jaccard_similarity(
                        set(candidate.evidence_pattern.trigger_conditions),
                        set(existing.evidence_pattern.trigger_conditions),
                    )
                    if jaccard >= threshold:
                        merged_candidate = self._merge_candidates(
                            existing, candidate
                        )
                        seen[existing_key] = merged_candidate
                        result = [
                            c
                            for c in result
                            if c.candidate_id != existing.candidate_id
                        ]
                        result.append(merged_candidate)
                        merged = True
                        break

            if not merged:
                seen[candidate.deduplication_key] = candidate
                result.append(candidate)

        return result

    def _jaccard_similarity(self, a: set[str], b: set[str]) -> float:
        if not a and not b:
            return 1.0
        if not a or not b:
            return 0.0
        return len(a & b) / len(a | b)

    def _merge_candidates(
        self, a: SkillCandidate, b: SkillCandidate
    ) -> SkillCandidate:
        merged_ids = list(set(a.source_lesson_ids) | set(b.source_lesson_ids))
        merged_triggers = sorted(
            set(a.evidence_pattern.trigger_conditions)
            | set(b.evidence_pattern.trigger_conditions)
        )
        merged_reasoning = list(
            dict.fromkeys(
                a.evidence_pattern.reasoning_path
                + b.evidence_pattern.reasoning_path
            )
        )
        merged_method = (
            a.evidence_pattern.method_summary
            if len(a.source_lesson_ids) >= len(b.source_lesson_ids)
            else b.evidence_pattern.method_summary
        )
        merged_limitations = list(
            set(a.evidence_pattern.limitations + b.evidence_pattern.limitations)
        )
        merged_outcome = (
            a.evidence_pattern.outcome_pattern
            if a.evidence_pattern.outcome_pattern != "unknown"
            else b.evidence_pattern.outcome_pattern
        )
        merged_scope = dict(a.evidence_pattern.scope_boundaries)
        for k, v in b.evidence_pattern.scope_boundaries.items():
            if k in merged_scope:
                if isinstance(merged_scope[k], list) and isinstance(v, list):
                    merged_scope[k] = list(
                        set(merged_scope[k] + v)
                    )
            else:
                merged_scope[k] = v

        combined_confidence = self._round(
            (a.confidence_score + b.confidence_score) / 2
        )
        combined_risk = _max_risk(
            a.risk_classification, b.risk_classification
        )
        trace_id = str(uuid4())
        dedup_key = a.deduplication_key

        evidence_summary = dict(a.evidence_summary)
        evidence_summary["lesson_count"] = len(merged_ids)
        evidence_summary["merged_from"] = [a.candidate_id, b.candidate_id]

        pattern = EvidencePattern(
            trigger_conditions=merged_triggers,
            reasoning_path=merged_reasoning,
            outcome_pattern=merged_outcome,
            scope_boundaries=merged_scope,
            method_summary=merged_method,
            limitations=merged_limitations,
        )

        return SkillCandidate(
            candidate_id=f"CANDIDATE-{trace_id[:8].upper()}",
            name=a.name,
            description=a.description,
            source_lesson_ids=merged_ids,
            evidence_pattern=pattern,
            confidence_score=combined_confidence,
            risk_classification=combined_risk,
            deduplication_key=dedup_key,
            discovery_trace_id=trace_id,
            discovered_by=a.discovered_by,
            discovered_at=a.discovered_at,
            evidence_summary=evidence_summary,
            status=CandidateStatus.MERGED,
            governance_issue_id=a.governance_issue_id or b.governance_issue_id,
        )

    def _round(self, value: float) -> float:
        return round(float(value), 4)
