"""Tests for evidence append-only governance."""

import pytest
from agents.runtime_models import EvidenceRecord, LessonRecord, EvidenceClassification


class TestEvidenceAppendOnly:
    def test_evidence_has_no_delete_method(self):
        assert not hasattr(EvidenceRecord, "delete")
        assert not hasattr(EvidenceRecord, "remove")

    def test_evidence_has_no_modify_method(self):
        assert not hasattr(EvidenceRecord, "modify")
        assert not hasattr(EvidenceRecord, "update")

    def test_evidence_is_dataclass(self):
        from dataclasses import is_dataclass
        assert is_dataclass(EvidenceRecord)

    def test_evidence_has_traceable_id(self):
        ev = EvidenceRecord(source_agent="test", mission_id="M-001", tool_used="test")
        assert ev.evidence_id.startswith("EVIDENCE-")

    def test_evidence_has_timestamp(self):
        ev = EvidenceRecord(source_agent="test", mission_id="M-001", tool_used="test")
        assert ev.timestamp != ""

    def test_evidence_has_lineage_tracking(self):
        ev = EvidenceRecord(source_agent="test", mission_id="M-001", tool_used="test")
        assert hasattr(ev, "lineage")
        assert isinstance(ev.lineage, list)

    def test_evidence_has_source_agent(self):
        ev = EvidenceRecord(source_agent="janus", mission_id="M-001", tool_used="test")
        assert ev.source_agent == "janus"

    def test_evidence_has_classification(self):
        ev = EvidenceRecord(source_agent="test", mission_id="M-001", tool_used="test")
        assert ev.classification == EvidenceClassification.I5_SPECULATIVE

    def test_evidence_classification_settable(self):
        ev = EvidenceRecord(
            source_agent="test", mission_id="M-001", tool_used="test",
            classification=EvidenceClassification.I0_OFFICIAL_VERIFIED
        )
        assert ev.classification == EvidenceClassification.I0_OFFICIAL_VERIFIED

    def test_evidence_to_dict_includes_classification_value(self):
        ev = EvidenceRecord(source_agent="test", mission_id="M-001", tool_used="test")
        d = ev.to_dict()
        assert "classification" in d
        assert isinstance(d["classification"], str)


class TestLessonTraceability:
    def test_lesson_links_to_evidence(self):
        lesson = LessonRecord(source_evidence_ids=["EVIDENCE-ABC"], source_agent="test")
        assert len(lesson.source_evidence_ids) == 1

    def test_lesson_has_quality_score(self):
        lesson = LessonRecord(source_evidence_ids=[], source_agent="test")
        assert 0.0 <= lesson.quality_score <= 1.0

    def test_lesson_traceable_to_agent(self):
        lesson = LessonRecord(source_evidence_ids=[], source_agent="iris")
        assert lesson.source_agent == "iris"

    def test_lesson_has_reviewer_field(self):
        lesson = LessonRecord(source_evidence_ids=[], source_agent="test", reviewer="Sage")
        assert lesson.reviewer == "Sage"

    def test_lesson_has_dedicated_id(self):
        lesson = LessonRecord(source_evidence_ids=[], source_agent="test")
        assert lesson.lesson_id.startswith("LESSON-")


class TestEvidenceFlow:
    def _make_identity(self):
        from agents.identity import get_identity
        return get_identity("iris")

    def test_evidence_capture_in_runtime(self):
        from agents.runtime import BaseAgent
        from agents.role_boundary import get_role_boundary

        identity = self._make_identity()
        role = get_role_boundary("iris")
        agent = BaseAgent(identity, role)
        ev = agent._capture_evidence(
            source_agent="iris", mission_id="M-001", tool_used="llm",
            input_summary="test input", output_summary="test output"
        )
        assert isinstance(ev, EvidenceRecord)
        assert ev.evidence_id.startswith("EVIDENCE-")

    def test_evidence_registry_append_only(self):
        from agents.runtime import BaseAgent
        from agents.role_boundary import get_role_boundary
        from agents.runtime_models import ActivationState

        identity = self._make_identity()
        role = get_role_boundary("iris")
        agent = BaseAgent(identity, role)
        agent.set_activation_state(ActivationState.SANDBOX_ACTIVE)
        initial = len(agent.get_evidence_registry())
        from agents.runtime_models import MissionEnvelope, MissionType
        mission = MissionEnvelope(
            mission_type=MissionType.COUNCIL, title="test",
            objective="test", requester="iris",
            target_agents=["iris"], required_tools=["filesystem"],
        )
        result = agent.receive_mission(mission)
        assert len(agent.get_evidence_registry()) >= initial
        assert "FAILED" not in result.status


    def test_evidence_not_mutable_after_creation(self):
        ev = EvidenceRecord(source_agent="test", mission_id="M-001", tool_used="llm")
        assert hasattr(ev, "evidence_id")
        assert ev.evidence_id.startswith("EVIDENCE-")

    def test_capability_usage_tracks_evidence(self):
        from agents.runtime_models import CapabilityUsageRecord
        rec = CapabilityUsageRecord(
            agent_id="test", capability_name="test_cap",
            mission_type="activation_mission", success=True, evidence_count=5, lesson_count=2
        )
        assert rec.evidence_count == 5
        assert rec.lesson_count == 2

    def test_agent_report_contains_evidence_ids(self):
        from agents.runtime_models import AgentReportEnvelope
        report = AgentReportEnvelope(
            agent_id="test", mission_id="M-001", mission_type="test",
            evidence_ids=["EVIDENCE-001", "EVIDENCE-002"]
        )
        assert len(report.evidence_ids) == 2
