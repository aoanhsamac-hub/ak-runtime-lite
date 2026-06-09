from __future__ import annotations

from typing import Any, Sequence

from agents.audit_hook import append_agent_audit
from agents.identity import AgentIdentity
from agents.lifecycle import AgentLifecycleState, can_be_operational, can_receive_task
from agents.report_envelope import ReportEnvelope, ReportStatus
from agents.role_boundary import RoleBoundary
from agents.runtime_models import (
    ActivationState,
    AgentContext,
    AgentReportEnvelope,
    CapabilityUsageRecord,
    EvidenceClassification,
    EvidenceRecord,
    LessonRecord,
    MissionEnvelope,
    MissionStatus,
    MissionType,
    ToolRequest,
    ToolResult,
    ToolStatus,
    _utc_now,
)
from agents.task_envelope import TaskEnvelope, TaskStatus
from agents.router import TaskRouter
from governance.governance_gate import evaluate_proposal
from memory.agent_memory import AgentMemoryClient, agent_memory_client
from memory.memory_interface import MemoryInterface


class BaseAgent:
    def __init__(
        self,
        identity: AgentIdentity,
        role_boundary: RoleBoundary,
        memory_interface: MemoryInterface | None = None,
        memory_client: AgentMemoryClient | None = None,
    ):
        self.identity = identity
        self.role_boundary = role_boundary
        self.lifecycle_state = AgentLifecycleState.CREATED.value
        self.memory_client = memory_client or agent_memory_client(
            identity.agent_id, memory_interface or MemoryInterface()
        )
        self.activation_state = ActivationState.LOCKED
        self._evidence_registry: list[EvidenceRecord] = []
        self._lesson_registry: list[LessonRecord] = []
        self._usage_registry: list[CapabilityUsageRecord] = []
        self._tool_results: list[dict[str, Any]] = []

    def boot(self) -> dict:
        if not can_be_operational(self.identity, self.role_boundary) or self.memory_client is None:
            self.lifecycle_state = AgentLifecycleState.DEGRADED.value
        else:
            self.lifecycle_state = AgentLifecycleState.OPERATIONAL.value
        return {"agent_id": self.identity.agent_id, "status": self.status()}

    def status(self) -> str:
        return "operational" if self.lifecycle_state == AgentLifecycleState.OPERATIONAL.value else self.lifecycle_state.lower()

    def get_context(self) -> AgentContext:
        return AgentContext(
            agent_id=self.identity.agent_id,
            agent_name=self.identity.name,
            role=self.identity.constitutional_role,
            department=self.identity.department,
            authority_level=self.identity.authority_level,
            activation_state=self.activation_state,
        )

    def receive_task(self, task: TaskEnvelope | dict) -> ReportEnvelope:
        task = self._coerce_task(task)
        if not can_receive_task(self.lifecycle_state):
            return self.create_report(
                task,
                {
                    "status": ReportStatus.REJECTED.value,
                    "summary": "agent cannot receive task in current lifecycle state",
                },
            )
        validation = self.validate_task(task)
        if not validation["valid"]:
            task.status = TaskStatus.BLOCKED.value
            return self.create_report(
                task,
                {
                    "status": ReportStatus.REVIEW_REQUIRED.value,
                    "summary": "task validation failed",
                    "risks": validation["reasons"],
                },
            )
        authority = self.validate_authority(task)
        if not authority["valid"]:
            task.status = TaskStatus.REJECTED.value
            return self.create_report(
                task,
                {
                    "status": ReportStatus.REJECTED.value,
                    "summary": "authority invalid",
                    "risks": authority["reasons"],
                    "review_needed": authority.get("required_reviewers", []),
                },
            )
        return self.execute_task(task)

    def validate_task(self, task: TaskEnvelope) -> dict:
        base = task.validate()
        reasons = list(base.get("missing", []))
        if task.target_agent != self.identity.agent_id:
            reasons.append("target agent mismatch")
        if any(
            item.lower() in {".env", "secret", "credential", "credentials"}
            for item in task.input_refs + task.allowed_tools
        ):
            reasons.append("secret access blocked")
        return {"valid": not reasons, "reasons": reasons}

    def validate_authority(self, task: TaskEnvelope) -> dict:
        action = task.metadata.get("action", "")
        target_path = task.metadata.get("target_path", "")
        reasons = []
        if action and not self.role_boundary.allows(action):
            reasons.append(f"action not allowed: {action}")
        if action and self.role_boundary.forbids(action):
            reasons.append(f"action forbidden: {action}")
        gate = evaluate_proposal(
            {
                "title": task.title,
                "description": task.objective,
                "target_path": target_path,
                "approvers": task.required_approvals,
                "governance_valid": True,
            }
        )
        if gate["blocked"]:
            reasons.append(gate["reason"])
        return {
            "valid": not reasons,
            "reasons": reasons,
            "required_reviewers": gate.get("required_approvers", []),
        }

    def execute_task(self, task: TaskEnvelope) -> ReportEnvelope:
        task.status = TaskStatus.COMPLETED.value
        result = {
            "status": ReportStatus.FINAL.value,
            "summary": "dry-run task accepted and reported",
            "actions_taken": ["validated", "dry_run_reported"],
        }
        report = self.create_report(task, result)
        self.record_decision_trace(task, result)
        self.append_audit(
            {
                "task_id": task.task_id,
                "issue_id": task.issue_id,
                "action": "dry_run",
                "result": report.status,
            }
        )
        return report

    def create_report(
        self, task: TaskEnvelope, result: dict[str, Any]
    ) -> ReportEnvelope:
        return ReportEnvelope(
            task_id=task.task_id,
            issue_id=task.issue_id,
            agent=self.identity.agent_id,
            status=result.get("status", ReportStatus.FINAL.value),
            summary=result.get("summary", ""),
            actions_taken=result.get("actions_taken", []),
            risks=result.get("risks", []),
            review_needed=result.get("review_needed", []),
            recommendation=result.get("recommendation", "dry-run only"),
        )

    def record_decision_trace(
        self, task: TaskEnvelope, result: dict[str, Any]
    ) -> None:
        try:
            self.memory_client.record_decision(
                task.title,
                result.get("summary", ""),
                [task.task_id],
                result.get("status", "UNKNOWN"),
                issue_id=task.issue_id,
            )
        except Exception:
            pass

    def append_audit(self, event: dict[str, Any]) -> dict:
        return append_agent_audit(
            "agent_action",
            self.identity.agent_id,
            event.get("task_id", ""),
            event.get("issue_id", ""),
            event.get("action", ""),
            event.get("result", ""),
        )

    def shutdown(self) -> dict:
        self.lifecycle_state = AgentLifecycleState.SUSPENDED.value
        return {"agent_id": self.identity.agent_id, "status": self.status()}

    # --- Operational Layer ---

    def receive_mission(self, mission: MissionEnvelope) -> AgentReportEnvelope:
        steps: list[str] = []
        evidence_ids: list[str] = []

        if self.activation_state == ActivationState.LOCKED:
            return AgentReportEnvelope(
                agent_id=self.identity.agent_id,
                mission_id=mission.mission_id,
                mission_type=mission.mission_type.value,
                summary="Agent is LOCKED; cannot accept missions",
                status="LOCKED",
            )

        steps.append("mission_received")

        for tool_name in mission.required_tools:
            tool_result = self._call_tool(tool_name, mission.input_data)
            tr = tool_result.to_dict()
            tr["tool_name"] = tool_name
            self._tool_results.append(tr)
            evidence = self._capture_evidence(
                source_agent=self.identity.agent_id,
                mission_id=mission.mission_id,
                tool_used=tool_name,
                input_summary=mission.objective,
                output_summary=str(tool_result.output)[:200] if tool_result.success else tool_result.error,
            )
            self._evidence_registry.append(evidence)
            evidence_ids.append(evidence.evidence_id)
            steps.append(f"tool_called:{tool_name}" if tool_result.success else f"tool_failed:{tool_name}")

        lesson = self._distill_lesson(
            source_evidence_ids=evidence_ids,
            mission_id=mission.mission_id,
        )
        if lesson:
            self._lesson_registry.append(lesson)

        usage = self._record_usage(
            capability_name=mission.mission_type.value,
            success=all(r.get("success", False) for r in self._tool_results if r.get("tool_name") in mission.required_tools),
        )
        self._usage_registry.append(usage)
        steps.append("evidence_captured")
        steps.append("lesson_distilled")
        steps.append("usage_recorded")

        mission.status = MissionStatus.COMPLETED
        mission.completed_at = _utc_now()

        return AgentReportEnvelope(
            agent_id=self.identity.agent_id,
            mission_id=mission.mission_id,
            mission_type=mission.mission_type.value,
            summary=f"Mission completed. {len(evidence_ids)} evidence items, {1 if lesson else 0} lessons.",
            evidence_ids=evidence_ids,
            lesson_ids=[lesson.lesson_id] if lesson else [],
            tool_results=list(self._tool_results),
            status="COMPLETED",
        )

    def _call_tool(self, tool_name: str, params: dict[str, Any]) -> ToolResult:
        from connectors.llm_connector import LLMConnector
        from connectors.filesystem_connector import FilesystemConnector
        from connectors.git_connector import GitConnector
        from connectors.opencode_connector import OpenCodeConnector

        llm = getattr(self, "llm", None) or LLMConnector()
        tools = {
            "llm": llm,
            "filesystem": FilesystemConnector(),
            "git": GitConnector(),
            "opencode": OpenCodeConnector(),
        }
        handler = tools.get(tool_name)
        if handler is None:
            return ToolResult(success=False, error=f"unknown tool: {tool_name}")
        try:
            result = handler.execute(**params) if hasattr(handler, "execute") else handler.prepare_task(**params)
            return ToolResult(success=True, output=result)
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def _capture_evidence(
        self,
        source_agent: str,
        mission_id: str,
        tool_used: str,
        input_summary: str,
        output_summary: str,
    ) -> EvidenceRecord:
        return EvidenceRecord(
            source_agent=source_agent,
            mission_id=mission_id,
            tool_used=tool_used,
            input_summary=input_summary,
            output_summary=output_summary,
            classification=EvidenceClassification.I3_THEORY,
            owner=source_agent,
            reviewer="Sage",
        )

    def _distill_lesson(
        self,
        source_evidence_ids: list[str],
        mission_id: str,
    ) -> LessonRecord | None:
        if not source_evidence_ids:
            return None
        return LessonRecord(
            source_evidence_ids=source_evidence_ids,
            source_agent=self.identity.agent_id,
            mission_id=mission_id,
            title=f"Lesson from {mission_id}",
            description=f"Distilled from {len(source_evidence_ids)} evidence items",
            context=str(self.identity.constitutional_role),
            outcome="completed",
            quality_score=0.8,
            owner=self.identity.agent_id,
            reviewer="Sage",
        )

    def _record_usage(
        self, capability_name: str, success: bool
    ) -> CapabilityUsageRecord:
        return CapabilityUsageRecord(
            agent_id=self.identity.agent_id,
            capability_name=capability_name,
            mission_type=capability_name,
            success=success,
            evidence_count=len(self._evidence_registry),
            lesson_count=len(self._lesson_registry),
        )

    def get_evidence_registry(self) -> list[EvidenceRecord]:
        return list(self._evidence_registry)

    def get_lesson_registry(self) -> list[LessonRecord]:
        return list(self._lesson_registry)

    def get_usage_registry(self) -> list[CapabilityUsageRecord]:
        return list(self._usage_registry)

    def set_activation_state(self, state: ActivationState) -> dict:
        self.activation_state = state
        return {
            "agent_id": self.identity.agent_id,
            "activation_state": state.value,
        }

    def generate_report_envelope(
        self, mission_id: str = "", mission_type: str = ""
    ) -> AgentReportEnvelope:
        return AgentReportEnvelope(
            agent_id=self.identity.agent_id,
            mission_id=mission_id,
            mission_type=mission_type,
            summary=f"{self.identity.name} report for {mission_type or 'unknown'}",
            evidence_ids=[e.evidence_id for e in self._evidence_registry],
            lesson_ids=[l.lesson_id for l in self._lesson_registry],
            tool_results=list(self._tool_results),
            status="DRAFT",
        )

    def _coerce_task(self, task: TaskEnvelope | dict) -> TaskEnvelope:
        if isinstance(task, TaskEnvelope):
            return task
        return TaskEnvelope(**task)


class AgentRuntime:
    def __init__(self, router: TaskRouter | None = None, dry_run: bool = True):
        self.router = router or TaskRouter()
        self.dry_run = dry_run

    def run(self, task) -> dict:
        routed = self.router.route(task)
        return {
            "status": routed["status"],
            "dry_run": self.dry_run,
            "execution_enabled": False,
            "trading_enabled": False,
            "mt5_enabled": False,
            "route": routed,
        }
