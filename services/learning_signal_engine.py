from __future__ import annotations

from typing import Any

from memory.learning_registry.schemas import LearningSignalRecord, SIGNAL_TYPES, stable_hash, utc_now


class LearningSignalEngine:
    """Extracts learning signals from approved knowledge.

    No autonomous learning — signals are recorded as CANDIDATE only.
    """

    def __init__(self, signal_registry):
        self.signal_registry = signal_registry

    def extract_from_approved_lessons(self, lessons: list[dict[str, Any]], owner_agent: str = "Sage") -> list[LearningSignalRecord]:
        signals: list[LearningSignalRecord] = []
        for lesson in lessons:
            score = lesson.get("confidence_score", 0) or 0
            source_path = (lesson.get("source_path", "") or "").lower()
            domain = (lesson.get("domain", "") or "")
            evidence = lesson.get("evidence", {}) or {}

            if score >= 70:
                signals.append(self._make_signal(
                    signal_type="PATTERN", source_kind="lesson",
                    source_id=lesson.get("candidate_id", ""),
                    title=f"Pattern: {lesson.get('extracted_title', '')}",
                    description=f"High-confidence lesson pattern (score={score})",
                    content=lesson.get("extracted_summary", ""),
                    confidence_score=score / 100.0, evidence=evidence,
                    owner_agent=owner_agent, tags=["lesson", "pattern"],
                ))
            if evidence.get("source_quality", 0) >= 4 and evidence.get("validation_level", 0) >= 3:
                signals.append(self._make_signal(
                    signal_type="GOVERNANCE", source_kind="lesson",
                    source_id=lesson.get("candidate_id", ""),
                    title=f"Governance: {lesson.get('extracted_title', '')}",
                    description="High-quality validated lesson",
                    content=lesson.get("extracted_summary", ""),
                    confidence_score=score / 100.0, evidence=evidence,
                    owner_agent=owner_agent, tags=["lesson", "governance"],
                ))
            if domain:
                signals.append(self._make_signal(
                    signal_type="DATASET", source_kind="lesson",
                    source_id=lesson.get("candidate_id", ""),
                    title=f"Dataset: {domain} - {lesson.get('extracted_title', '')}",
                    description=f"Domain-specific knowledge: {domain}",
                    content=lesson.get("extracted_summary", ""),
                    confidence_score=score / 100.0, evidence=evidence,
                    owner_agent=owner_agent,
                    tags=["lesson", "dataset", domain.lower().replace(" ", "_")],
                ))
            if "trade" in source_path or "market" in source_path or "trading" in domain.lower():
                signals.append(self._make_signal(
                    signal_type="TRADING", source_kind="lesson",
                    source_id=lesson.get("candidate_id", ""),
                    title=f"Trading: {lesson.get('extracted_title', '')}",
                    description=f"Trading/market knowledge from {domain}",
                    content=lesson.get("extracted_summary", ""),
                    confidence_score=score / 100.0, evidence=evidence,
                    owner_agent=owner_agent, tags=["lesson", "trading"],
                ))
            if "risk" in source_path or "security" in source_path or "risk" in domain.lower():
                signals.append(self._make_signal(
                    signal_type="RISK", source_kind="lesson",
                    source_id=lesson.get("candidate_id", ""),
                    title=f"Risk: {lesson.get('extracted_title', '')}",
                    description=f"Risk/Security knowledge from {domain}",
                    content=lesson.get("extracted_summary", ""),
                    confidence_score=score / 100.0, evidence=evidence,
                    owner_agent=owner_agent, tags=["lesson", "risk"],
                ))
            if "exec" in source_path:
                signals.append(self._make_signal(
                    signal_type="EXECUTION", source_kind="lesson",
                    source_id=lesson.get("candidate_id", ""),
                    title=f"Execution: {lesson.get('extracted_title', '')}",
                    description=f"Execution knowledge from {domain}",
                    content=lesson.get("extracted_summary", ""),
                    confidence_score=score / 100.0, evidence=evidence,
                    owner_agent=owner_agent, tags=["lesson", "execution"],
                ))
            if evidence.get("outcome_evidence", 0) >= 3:
                signals.append(self._make_signal(
                    signal_type="DECISION", source_kind="lesson",
                    source_id=lesson.get("candidate_id", ""),
                    title=f"Decision: {lesson.get('extracted_title', '')}",
                    description=f"Decision evidence from {domain}",
                    content=lesson.get("extracted_summary", ""),
                    confidence_score=score / 100.0, evidence=evidence,
                    owner_agent=owner_agent, tags=["lesson", "decision"],
                ))
            if evidence.get("reuse_value", 0) >= 4:
                signals.append(self._make_signal(
                    signal_type="PERFORMANCE", source_kind="lesson",
                    source_id=lesson.get("candidate_id", ""),
                    title=f"Performance: {lesson.get('extracted_title', '')}",
                    description=f"High-reuse knowledge (reuse={evidence.get('reuse_value', 0)})",
                    content=lesson.get("extracted_summary", ""),
                    confidence_score=score / 100.0, evidence=evidence,
                    owner_agent=owner_agent, tags=["lesson", "performance"],
                ))
        return self._persist_signals(signals)

    def extract_from_approved_skills(self, skills: list[dict[str, Any]], owner_agent: str = "Sage") -> list[LearningSignalRecord]:
        signals: list[LearningSignalRecord] = []
        for skill in skills:
            score = skill.get("confidence_score", 0) or 0
            source_path = (skill.get("source_path", "") or "").lower()
            signals.append(self._make_signal(
                signal_type="PATTERN", source_kind="skill",
                source_id=skill.get("candidate_id", ""),
                title=f"Pattern: {skill.get('extracted_title', '')}",
                description=f"Approved skill pattern (score={score})",
                content=skill.get("extracted_summary", ""),
                confidence_score=score / 100.0,
                evidence=skill.get("evidence", {}),
                owner_agent=owner_agent, tags=["skill", "pattern"],
            ))
            signals.append(self._make_signal(
                signal_type="PERFORMANCE", source_kind="skill",
                source_id=skill.get("candidate_id", ""),
                title=f"Performance: {skill.get('extracted_title', '')}",
                description=f"Approved skill (score={score})",
                content=skill.get("extracted_summary", ""),
                confidence_score=score / 100.0,
                evidence=skill.get("evidence", {}),
                owner_agent=owner_agent, tags=["skill", "performance"],
            ))
            if "memory" in source_path:
                signals.append(self._make_signal(
                    signal_type="EXECUTION" if "exec" in source_path else "PATTERN",
                    source_kind="skill", source_id=skill.get("candidate_id", ""),
                    title=f"Execution: {skill.get('extracted_title', '')}",
                    description="Skill with execution relevance",
                    content=skill.get("extracted_summary", ""),
                    confidence_score=score / 100.0,
                    evidence=skill.get("evidence", {}),
                    owner_agent=owner_agent, tags=["skill", "execution"],
                ))
        return self._persist_signals(signals)

    def extract_from_approved_datasets(self, datasets: list[dict[str, Any]], owner_agent: str = "Sage") -> list[LearningSignalRecord]:
        signals: list[LearningSignalRecord] = []
        for ds in datasets:
            score = ds.get("confidence_score", 0) or 0
            signals.append(self._make_signal(
                signal_type="DATASET",
                source_kind="dataset",
                source_id=ds.get("candidate_id", ""),
                title=f"Dataset: {ds.get('extracted_title', '')}",
                description=f"Approved dataset (score={score})",
                content=ds.get("extracted_summary", ""),
                confidence_score=score / 100.0,
                evidence=ds.get("evidence", {}),
                owner_agent=owner_agent,
                tags=["dataset"],
            ))
        return self._persist_signals(signals)

    def extract_from_approved_traces(self, traces: list[dict[str, Any]], owner_agent: str = "Sage") -> list[LearningSignalRecord]:
        signals: list[LearningSignalRecord] = []
        for trace in traces:
            score = trace.get("confidence_score", 0) or 0
            outcome = trace.get("outcome", "")
            decision = trace.get("decision", "")
            reasoning = trace.get("reasoning", "")
            evidence = trace.get("evidence", {}) or {}
            source_id = trace.get("trace_id", trace.get("candidate_id", ""))
            if "fail" in outcome.lower() or "error" in outcome.lower():
                signals.append(self._make_signal(
                    signal_type="ANOMALY", source_kind="trace",
                    source_id=source_id,
                    title=f"Anomaly: {decision}",
                    description=f"Failed/error outcome: {outcome}",
                    content=reasoning, confidence_score=score / 100.0,
                    evidence=evidence, owner_agent=owner_agent,
                    tags=["trace", "anomaly"],
                ))
            else:
                signals.append(self._make_signal(
                    signal_type="REPEATABILITY", source_kind="trace",
                    source_id=source_id,
                    title=f"Repeatable: {decision}",
                    description=f"Successful outcome: {outcome}",
                    content=reasoning, confidence_score=score / 100.0,
                    evidence=evidence, owner_agent=owner_agent,
                    tags=["trace", "repeatable"],
                ))
            signals.append(self._make_signal(
                signal_type="DECISION", source_kind="trace",
                source_id=source_id,
                title=f"Decision: {decision}",
                description=f"Decision trace: {outcome}",
                content=reasoning, confidence_score=score / 100.0,
                evidence=evidence, owner_agent=owner_agent,
                tags=["trace", "decision"],
            ))
            if "exec" in (trace.get("source_path", "") or "").lower():
                signals.append(self._make_signal(
                    signal_type="EXECUTION", source_kind="trace",
                    source_id=source_id,
                    title=f"Execution: {decision}",
                    description="Execution-related decision trace",
                    content=reasoning, confidence_score=score / 100.0,
                    evidence=evidence, owner_agent=owner_agent,
                    tags=["trace", "execution"],
                ))
        return self._persist_signals(signals)

    def extract_all(self, lessons: list[dict] | None = None,
                    skills: list[dict] | None = None,
                    datasets: list[dict] | None = None,
                    traces: list[dict] | None = None,
                    owner_agent: str = "Sage") -> list[LearningSignalRecord]:
        all_signals: list[LearningSignalRecord] = []
        if lessons:
            all_signals.extend(self.extract_from_approved_lessons(lessons, owner_agent))
        if skills:
            all_signals.extend(self.extract_from_approved_skills(skills, owner_agent))
        if datasets:
            all_signals.extend(self.extract_from_approved_datasets(datasets, owner_agent))
        if traces:
            all_signals.extend(self.extract_from_approved_traces(traces, owner_agent))
        return all_signals

    def _make_signal(self, **kwargs) -> LearningSignalRecord:
        return LearningSignalRecord(**kwargs)

    def _persist_signals(self, signals: list[LearningSignalRecord]) -> list[LearningSignalRecord]:
        persisted = []
        for sig in signals:
            persisted.append(self.signal_registry.create_candidate(**sig.to_dict()))
        return persisted
