from services.learning_signal_engine import LearningSignalEngine
from memory.learning_registry import LearningSignalRegistry


def test_signal_engine_extracts_pattern_from_approved_lesson(signal_registry):
    engine = LearningSignalEngine(signal_registry)
    lessons = [
        {
            "candidate_id": "LKI-001",
            "extracted_title": "Memory Engine",
            "extracted_summary": "Memory management patterns",
            "confidence_score": 85,
            "evidence": {"source_quality": 5, "validation_level": 4},
            "domain": "Memory Knowledge",
            "owner_agent": "Sage",
        }
    ]
    signals = engine.extract_from_approved_lessons(lessons, owner_agent="Sage")
    assert len(signals) >= 1
    types = {s.signal_type for s in signals}
    assert "PATTERN" in types
    for sig in signals:
        assert sig.status == "CANDIDATE"
        assert sig.signal_id.startswith("LSIG-")


def test_signal_engine_extracts_governance_from_high_quality_lesson(signal_registry):
    engine = LearningSignalEngine(signal_registry)
    lessons = [
        {
            "candidate_id": "LKI-002",
            "extracted_title": "Audit Trail Pattern",
            "extracted_summary": "Governance audit procedures",
            "confidence_score": 90,
            "evidence": {"source_quality": 5, "validation_level": 4, "outcome_evidence": 5},
            "domain": "Governance Knowledge",
        }
    ]
    signals = engine.extract_from_approved_lessons(lessons, owner_agent="Sage")
    types = {s.signal_type for s in signals}
    assert "PATTERN" in types
    assert "GOVERNANCE" in types


def test_signal_engine_extracts_dataset_signal(signal_registry):
    engine = LearningSignalEngine(signal_registry)
    datasets = [
        {
            "candidate_id": "DS-001",
            "extracted_title": "Market Data 2024",
            "extracted_summary": "OHLCV dataset",
            "confidence_score": 78,
        }
    ]
    signals = engine.extract_from_approved_datasets(datasets, owner_agent="Sage")
    assert len(signals) == 1
    assert signals[0].signal_type == "DATASET"


def test_signal_engine_extracts_anomaly_from_failed_trace(signal_registry):
    engine = LearningSignalEngine(signal_registry)
    traces = [
        {
            "candidate_id": "TR-001",
            "trace_id": "TRACE-001",
            "decision": "Execute trade",
            "reasoning": "Market conditions met",
            "outcome": "Failed - insufficient margin",
            "evidence": {"error_code": "E1001"},
            "confidence_score": 50,
        }
    ]
    signals = engine.extract_from_approved_traces(traces, owner_agent="Sage")
    assert len(signals) == 2
    types = {s.signal_type for s in signals}
    assert "ANOMALY" in types
    assert "DECISION" in types


def test_signal_engine_extracts_repeatability_from_successful_trace(signal_registry):
    engine = LearningSignalEngine(signal_registry)
    traces = [
        {
            "candidate_id": "TR-002",
            "trace_id": "TRACE-002",
            "decision": "Analyze trend",
            "reasoning": "Trend detection successful",
            "outcome": "Success - trend identified",
            "evidence": {"accuracy": 0.92},
            "confidence_score": 88,
        }
    ]
    signals = engine.extract_from_approved_traces(traces, owner_agent="Sage")
    assert len(signals) == 2
    types = {s.signal_type for s in signals}
    assert "REPEATABILITY" in types
    assert "DECISION" in types


def test_signal_engine_extract_all_combines_sources(signal_registry):
    engine = LearningSignalEngine(signal_registry)
    lessons = [{"candidate_id": "L-1", "extracted_title": "L1", "extracted_summary": "C1",
                 "confidence_score": 80, "evidence": {}, "domain": "Test"}]
    skills = [{"candidate_id": "S-1", "extracted_title": "S1", "extracted_summary": "C2",
                "confidence_score": 75, "evidence": {}}]
    signals = engine.extract_all(lessons=lessons, skills=skills, owner_agent="Sage")
    assert len(signals) >= 2


def test_signal_engine_persists_to_registry(signal_registry):
    assert len(signal_registry.list_all()) == 0
    engine = LearningSignalEngine(signal_registry)
    engine.extract_from_approved_lessons(
        [{"candidate_id": "L-1", "extracted_title": "T1", "extracted_summary": "C1",
          "confidence_score": 80, "evidence": {}, "domain": "Test"}],
        owner_agent="Sage",
    )
    assert len(signal_registry.list_all()) > 0


def test_signal_engine_no_auto_promotion(signal_registry):
    engine = LearningSignalEngine(signal_registry)
    signals = engine.extract_from_approved_lessons(
        [{"candidate_id": "L-1", "extracted_title": "T1", "extracted_summary": "C1",
          "confidence_score": 80, "evidence": {}, "domain": "Test"}],
        owner_agent="Sage",
    )
    for sig in signals:
        assert sig.status == "CANDIDATE"
