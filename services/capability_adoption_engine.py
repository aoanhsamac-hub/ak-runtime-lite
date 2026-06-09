from __future__ import annotations

from typing import Any

from agents.identity import AGENT_IDENTITIES
from agents.runtime_models import CapabilityUsageRecord
from governance.governance_gate import evaluate_proposal
from memory.adoption_registry import (
    ADOPTION_TRANSITIONS,
    RISK_LEVELS,
    CapabilityAdoptionRegistry,
    AdoptionRecord,
)
from memory.capability_registry.official_capability_registry import (
    OfficialCapabilityRegistry,
)
from memory.capability_roi_registry import CapabilityROIRegistry
from memory.evidence_registry import EvidenceRegistry
from memory.usage_registry import CapabilityUsageRegistry


class CapabilityAssignmentPolicy:
    def __init__(self, official_registry: OfficialCapabilityRegistry):
        self._official = official_registry

    def can_assign(self, agent_id: str, official_capability_id: str) -> dict:
        if agent_id not in AGENT_IDENTITIES:
            return {"allowed": False, "reason": f"unknown agent: {agent_id}"}
        try:
            cap = self._official.get(official_capability_id)
        except KeyError as e:
            return {"allowed": False, "reason": str(e)}
        if cap.status != "APPROVED_AS_OFFICIAL":
            return {"allowed": False, "reason": f"capability not approved: {cap.status}"}
        return {"allowed": True, "reason": "assignment allowed"}

    def allowed_agents_for_risk(self, risk_level: str) -> list[str]:
        if risk_level in ("LEVEL_2_HIGH", "LEVEL_3_CRITICAL", "LEVEL_4_CONSTITUTIONAL"):
            return []
        return list(AGENT_IDENTITIES.keys())


class CapabilityAdoptionEngine:
    def __init__(
        self,
        official_registry: OfficialCapabilityRegistry,
        adoption_registry: CapabilityAdoptionRegistry,
        usage_registry: CapabilityUsageRegistry | None = None,
        roi_registry: CapabilityROIRegistry | None = None,
        evidence_registry: EvidenceRegistry | None = None,
    ):
        self._official = official_registry
        self._adoptions = adoption_registry
        self._usage = usage_registry
        self._roi = roi_registry
        self._evidence = evidence_registry
        self._policy = CapabilityAssignmentPolicy(official_registry)

    def propose_adoption(
        self,
        official_capability_id: str,
        assigned_agent: str,
        owner: str = "",
        risk_level: str = "LEVEL_1_MODERATE",
        validation_refs: list[str] | None = None,
        rollback_condition: str = "",
        roi_metric: str = "",
    ) -> dict:
        policy = self._policy.can_assign(assigned_agent, official_capability_id)
        if not policy["allowed"]:
            return {"success": False, "error": policy["reason"]}

        cap = self._official.get(official_capability_id)

        proposer = owner or "Janus"
        if risk_level in ("LEVEL_2_HIGH", "LEVEL_3_CRITICAL", "LEVEL_4_CONSTITUTIONAL"):
            approvers = ["Sage"]
        else:
            approvers = [proposer]

        gate = evaluate_proposal({
            "target_path": f"capability_adoption/{official_capability_id}/{assigned_agent}",
            "description": f"Adopt {cap.name} for {assigned_agent}",
            "risk_level": risk_level,
            "proposer": proposer,
            "approvers": approvers,
        })

        if gate["decision"] == "BLOCK":
            return {
                "success": False,
                "error": f"governance gate blocked: {gate['reason']}",
                "gate": gate,
                "risk_level": risk_level,
            }

        adoption = self._adoptions.create(
            official_capability_id=official_capability_id,
            owner=owner or "Janus",
            assigned_agent=assigned_agent,
            allowed_scope="sandbox",
            risk_level=risk_level,
            lifecycle_stage="PROPOSED",
            validation_refs=validation_refs or [],
            rollback_condition=rollback_condition,
            roi_metric=roi_metric,
        )

        self._official.update_adoption_stage(official_capability_id, "PROPOSED")

        return {
            "success": True,
            "adoption": adoption.to_dict(),
            "gate": gate,
        }

    def transition(self, adoption_id: str, target_stage: str, reason: str = "") -> dict:
        adoption = self._adoptions.get(adoption_id)
        allowed = ADOPTION_TRANSITIONS.get(adoption.lifecycle_stage, set())
        if target_stage not in allowed:
            return {
                "success": False,
                "error": f"cannot transition from {adoption.lifecycle_stage} to {target_stage}",
                "allowed_transitions": sorted(allowed),
            }

        cap = self._official.get(adoption.official_capability_id)

        if target_stage == "ASSIGNED_SANDBOX":
            if adoption.risk_level in ("LEVEL_2_HIGH", "LEVEL_3_CRITICAL", "LEVEL_4_CONSTITUTIONAL"):
                approvers = ["Sage"]
            else:
                approvers = [adoption.owner]
            gate = evaluate_proposal({
                "target_path": f"capability_adoption/assign/{adoption.official_capability_id}/{adoption.assigned_agent}",
                "description": f"Assign sandbox for {cap.name} to {adoption.assigned_agent}",
                "risk_level": adoption.risk_level,
                "proposer": adoption.owner,
                "approvers": approvers,
            })
            if gate["decision"] == "BLOCK":
                return {"success": False, "error": f"governance gate blocked: {gate['reason']}", "gate": gate}
            extra = {"assigned_at": utc_now()}
        elif target_stage == "SUSPENDED":
            sage_gate = evaluate_proposal({
                "target_path": f"capability_adoption/suspend/{adoption_id}",
                "description": f"Suspend adoption of {cap.name} for {adoption.assigned_agent}",
                "risk_level": adoption.risk_level,
                "proposer": adoption.owner,
                "approvers": [adoption.owner],
            })
            if sage_gate["decision"] == "BLOCK":
                return {"success": False, "error": f"suspend blocked: {sage_gate['reason']}", "gate": sage_gate}
            extra = {}
        elif target_stage == "RETIRED":
            extra = {}
        else:
            extra = {}

        updated = self._adoptions.update_stage(adoption_id, target_stage, **extra)
        self._official.update_adoption_stage(adoption.official_capability_id, target_stage)

        if self._evidence and reason:
            from agents.runtime_models import EvidenceRecord, EvidenceClassification
            ev = EvidenceRecord(
                source_agent="CapabilityAdoptionEngine",
                mission_id=f"adoption/{adoption_id}",
                tool_used="transition",
                input_summary=f"Transition {adoption.lifecycle_stage} -> {target_stage}",
                output_summary=reason,
                classification=EvidenceClassification.I1_PROBABLE,
                owner=adoption.owner,
                reviewer="Sage",
            )
            self._evidence.record_evidence(ev)

        return {
            "success": True,
            "adoption": updated.to_dict(),
            "transition": f"{adoption.lifecycle_stage} -> {target_stage}",
        }

    def record_usage(self, adoption_id: str, success: bool = True, **extra: Any) -> dict:
        adoption = self._adoptions.get(adoption_id)
        cap = self._official.get(adoption.official_capability_id)

        record = CapabilityUsageRecord(
            agent_id=adoption.assigned_agent,
            capability_name=cap.name,
            mission_type="sandbox_adoption",
            success=success,
            adoption_status=adoption.lifecycle_stage,
            **{k: v for k, v in extra.items() if k in ("duration_ms", "error", "evidence_count", "lesson_count", "roi_estimate")},
        )

        if self._usage:
            self._usage.record_usage(record)

        if self._roi:
            value = extra.get("value", 1.0 if success else 0.0)
            cost = extra.get("cost", 0.1)
            self._roi.record_roi(
                capability_name=cap.name,
                value=value,
                cost=cost,
                agent_id=adoption.assigned_agent,
                adoption_id=adoption_id,
            )

        if not success:
            new_failures = adoption.failure_count + 1
            updated = self._adoptions.update_stage(
                adoption_id, adoption.lifecycle_stage,
                failure_count=new_failures,
            )
            if new_failures >= 3:
                suspended = self._adoptions.update_stage(adoption_id, "SUSPENDED")
                self._official.update_adoption_stage(adoption.official_capability_id, "SUSPENDED")
                if self._evidence:
                    from agents.runtime_models import EvidenceRecord, EvidenceClassification
                    ev = EvidenceRecord(
                        source_agent="CapabilityAdoptionEngine",
                        mission_id=f"adoption/{adoption_id}",
                        tool_used="auto_suspend",
                        input_summary=f"Auto-suspend after {new_failures} failures",
                        output_summary="auto-suspended after 3 failures",
                        classification=EvidenceClassification.I1_PROBABLE,
                        owner=adoption.owner,
                        reviewer="Sage",
                    )
                    self._evidence.record_evidence(ev)

        return {"success": True, "usage": record.to_dict()}

    def get_agent_adoptions(self, agent_id: str) -> list[dict]:
        records = self._adoptions.list_by_agent(agent_id)
        result = []
        for r in records:
            try:
                cap = self._official.get(r.official_capability_id)
                result.append({**r.to_dict(), "capability_name": cap.name, "capability_domain": cap.domain})
            except KeyError:
                result.append(r.to_dict())
        return result

    def get_capability_adoptions(self, official_capability_id: str) -> list[dict]:
        return [r.to_dict() for r in self._adoptions.list_by_capability(official_capability_id)]

    def summary(self) -> dict:
        all_records = self._adoptions.list_all()
        stages: dict[str, int] = {}
        for r in all_records:
            stages[r.lifecycle_stage] = stages.get(r.lifecycle_stage, 0) + 1
        return {
            "total_adoptions": len(all_records),
            "by_stage": stages,
            "unique_agents": len({r.assigned_agent for r in all_records}),
            "unique_capabilities": len({r.official_capability_id for r in all_records}),
        }


def utc_now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
