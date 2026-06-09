from agents.runtime_models import (
    ActivationState,
    AgentReportEnvelope,
    CapabilityUsageRecord,
    EvidenceClassification,
    EvidenceRecord,
    LessonRecord,
    ToolResult,
)
from memory.learning_runtime import (
    AgentPerformanceRegistry,
    LearningRuntime,
    LessonCandidateRegistry,
)
from memory.evidence_registry import EvidenceRegistry
from memory.usage_registry import CapabilityUsageRegistry


def _to_dict(obj):
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if hasattr(obj, "__dict__"):
        return dict(obj.__dict__)
    return dict(obj)


class FakeEvidenceRegistry:
    def __init__(self):
        self._records = []

    def record_evidence(self, record):
        d = _to_dict(record)
        self._records.append(d)
        return d

    def get_all(self):
        return list(self._records)

    def get_by_agent(self, agent_id):
        return [r for r in self._records if r.get("source_agent") == agent_id]

    def get_by_mission(self, mission_id):
        return [r for r in self._records if r.get("mission_id") == mission_id]

    def summary(self):
        return {
            "total_evidence": len(self._records),
            "unique_agents": len(set(r.get("source_agent", "") for r in self._records)),
            "classifications": list(set(r.get("classification", "") for r in self._records)),
        }


class FakeLessonRegistry:
    def __init__(self):
        self._records = []

    def record_lesson(self, record):
        d = _to_dict(record)
        self._records.append(d)
        return d

    def get_all(self):
        return list(self._records)

    def get_by_agent(self, agent_id):
        return [r for r in self._records if r.get("source_agent") == agent_id]

    def summary(self):
        return {
            "total_lessons": len(self._records),
            "unique_agents": len(set(r.get("source_agent", "") for r in self._records)),
        }


class FakeUsageRegistry:
    def __init__(self):
        self._records = []

    def record_usage(self, record):
        d = _to_dict(record)
        self._records.append(d)
        return d

    def get_all(self):
        return list(self._records)

    def get_by_agent(self, agent_id):
        return [r for r in self._records if r.get("agent_id") == agent_id]

    def get_by_capability(self, capability_name):
        return [r for r in self._records if r.get("capability_name") == capability_name]

    def summary(self):
        total = len(self._records)
        successes = sum(1 for r in self._records if r.get("success"))
        agents = set(r.get("agent_id", "") for r in self._records)
        return {
            "total_usages": total,
            "success_count": successes,
            "success_rate": round(successes / total, 4) if total else 0.0,
            "unique_agents": len(agents),
            "agents": sorted(agents),
        }


class FakePerformanceRegistry:
    def __init__(self):
        self._records = []

    def record_performance(self, record):
        self._records.append(record)
        return record

    def get_all(self):
        return list(self._records)

    def get_by_agent(self, agent_id):
        return [r for r in self._records if r.get("agent_id") == agent_id]

    def summary(self):
        return {
            "total_records": len(self._records),
            "unique_agents": len(set(r.get("agent_id", "") for r in self._records)),
        }


def test_learning_runtime_processes_mission_output():
    runtime = LearningRuntime(
        evidence_registry=FakeEvidenceRegistry(),
        lesson_registry=FakeLessonRegistry(),
        usage_registry=FakeUsageRegistry(),
        performance_registry=FakePerformanceRegistry(),
    )
    report = AgentReportEnvelope(
        agent_id="hermes",
        mission_id="M-TEST-001",
        mission_type="memory_mission",
        summary="Test mission",
        evidence_ids=["EV-001", "EV-002"],
        lesson_ids=["LS-001"],
        status="COMPLETED",
    )
    result = runtime.process_mission_output(report)
    assert result["evidence_recorded"] == 2
    assert result["lessons_recorded"] == 1
    assert result["usage_recorded"] == 1
    assert result["performance_recorded"] == 1


def test_evidence_registry_records_and_retrieves():
    registry = FakeEvidenceRegistry()
    record = EvidenceRecord(
        source_agent="sage",
        mission_id="M-001",
        tool_used="llm",
        input_summary="test input",
        output_summary="test output",
    )
    registry.record_evidence(record)
    all_records = registry.get_all()
    assert len(all_records) == 1
    assert all_records[0].get("source_agent") == "sage"

    by_agent = registry.get_by_agent("sage")
    assert len(by_agent) == 1

    by_mission = registry.get_by_mission("M-001")
    assert len(by_mission) == 1


def test_lesson_registry_records_and_retrieves():
    registry = FakeLessonRegistry()
    lesson = LessonRecord(
        source_evidence_ids=["EV-001"],
        source_agent="hermes",
        mission_id="M-001",
        title="Test lesson",
        description="A test lesson",
    )
    registry.record_lesson(lesson)
    all_records = registry.get_all()
    assert len(all_records) == 1

    by_agent = registry.get_by_agent("hermes")
    assert len(by_agent) == 1


def test_usage_registry_records_and_retrieves():
    registry = FakeUsageRegistry()
    usage = CapabilityUsageRecord(
        agent_id="janus",
        capability_name="council_mission",
        success=True,
        evidence_count=3,
        lesson_count=1,
    )
    registry.record_usage(usage)
    all_records = registry.get_all()
    assert len(all_records) == 1

    by_agent = registry.get_by_agent("janus")
    assert len(by_agent) == 1

    by_cap = registry.get_by_capability("council_mission")
    assert len(by_cap) == 1


def test_usage_registry_summary():
    registry = FakeUsageRegistry()
    for i in range(5):
        registry.record_usage(CapabilityUsageRecord(
            agent_id=f"agent_{i}",
            capability_name="test",
            success=i % 2 == 0,
        ))
    summary = registry.summary()
    assert summary["total_usages"] == 5
    assert summary["unique_agents"] == 5
    assert summary["success_count"] == 3


def test_performance_registry():
    registry = FakePerformanceRegistry()
    registry.record_performance({"agent_id": "sage", "mission_id": "M-001", "status": "COMPLETED"})
    registry.record_performance({"agent_id": "hermes", "mission_id": "M-002", "status": "COMPLETED"})
    all_records = registry.get_all()
    assert len(all_records) == 2
    by_agent = registry.get_by_agent("sage")
    assert len(by_agent) == 1


def test_hermes_distill_lessons_from_draft():
    registry = FakeLessonRegistry()
    registry.record_lesson(LessonRecord(
        source_evidence_ids=["EV-001"],
        source_agent="hermes",
        mission_id="M-001",
        title="Draft lesson",
        status="DRAFT",
    ))
    runtime = LearningRuntime(
        evidence_registry=FakeEvidenceRegistry(),
        lesson_registry=registry,
        usage_registry=FakeUsageRegistry(),
        performance_registry=FakePerformanceRegistry(),
    )
    distilled = runtime.hermes_distill_lessons()
    assert len(distilled) >= 1


def test_sage_blocks_unsafe_activation_state():
    runtime = LearningRuntime(
        evidence_registry=FakeEvidenceRegistry(),
        lesson_registry=FakeLessonRegistry(),
        usage_registry=FakeUsageRegistry(),
        performance_registry=FakePerformanceRegistry(),
    )
    result = runtime.sage_block_unsafe(ActivationState.OPERATIONAL_APPROVED)
    assert result["blocked"] is True

    result = runtime.sage_block_unsafe(ActivationState.SANDBOX_ACTIVE)
    assert result["blocked"] is False


def test_janus_consolidates_council():
    runtime = LearningRuntime(
        evidence_registry=FakeEvidenceRegistry(),
        lesson_registry=FakeLessonRegistry(),
        usage_registry=FakeUsageRegistry(),
        performance_registry=FakePerformanceRegistry(),
    )
    reports = [
        AgentReportEnvelope(agent_id="sage", mission_id="M-1", mission_type="test", status="COMPLETED", evidence_ids=["EV-1"]),
        AgentReportEnvelope(agent_id="hermes", mission_id="M-1", mission_type="test", status="COMPLETED", evidence_ids=["EV-2"]),
        AgentReportEnvelope(agent_id="iris", mission_id="M-1", mission_type="test", status="COMPLETED", evidence_ids=["EV-3"]),
    ]
    consolidated = runtime.janus_consolidate_council(reports)
    assert consolidated["total_agents"] == 3
    assert consolidated["completed"] == 3
    assert consolidated["total_evidence"] == 3


def test_activation_readiness():
    runtime = LearningRuntime(
        evidence_registry=FakeEvidenceRegistry(),
        lesson_registry=FakeLessonRegistry(),
        usage_registry=FakeUsageRegistry(),
        performance_registry=FakePerformanceRegistry(),
    )
    readiness = runtime.check_activation_readiness()
    assert readiness["ready"] is False  # empty registries

    # Add enough data to pass readiness
    for i in range(7):
        runtime.evidence.record_evidence({"evidence_id": f"EV-{i:03d}", "source_agent": "test"})
    runtime.lessons.record_lesson({"lesson_id": "LS-001", "source_agent": "test"})
    for i in range(7):
        runtime.usage.record_usage({"agent_id": f"agent_{i}", "capability_name": "test", "success": True})

    readiness = runtime.check_activation_readiness()
    assert readiness["ready"] is True


def test_tool_result_dataclass():
    result = ToolResult(success=True, output="test output")
    assert result.success is True
    assert result.output == "test output"
    assert result.error == ""


def test_evidence_classification_enum():
    assert EvidenceClassification.I0_OFFICIAL_VERIFIED.value == "I0_OFFICIAL_VERIFIED"
    assert EvidenceClassification.I9_REJECTED.value == "I9_REJECTED"


def test_capability_usage_record_defaults():
    record = CapabilityUsageRecord(agent_id="test", capability_name="test_cap")
    assert record.success is False
    assert record.evidence_count == 0
    assert record.lesson_count == 0
    assert record.adoption_status == "not_tracked"
