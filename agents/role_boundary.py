from __future__ import annotations

from dataclasses import dataclass, field


TERMINAL_AUTONOMY_LEVELS = {
    "READ_ONLY": "READ_ONLY",
    "SANDBOX_WRITE": "SANDBOX_WRITE",
    "BRANCH_WRITE": "BRANCH_WRITE",
    "PROMOTION_CANDIDATE": "PROMOTION_CANDIDATE",
}

# Hierarchy: each level includes all lower levels
AUTONOMY_HIERARCHY: dict[str, int] = {
    "READ_ONLY": 0,
    "SANDBOX_WRITE": 1,
    "BRANCH_WRITE": 2,
    "PROMOTION_CANDIDATE": 3,
}


@dataclass(frozen=True)
class RoleBoundary:
    agent_id: str
    allowed_actions: tuple[str, ...]
    forbidden_actions: tuple[str, ...]
    protected_paths: tuple[str, ...] = ()
    required_reviewers: tuple[str, ...] = ("Sage",)
    can_execute: bool = False
    can_approve: bool = False
    can_veto: bool = False
    can_code: bool = False
    can_access_memory: bool = True
    can_use_opencode: bool = False
    autonomy_level: str = "READ_ONLY"

    def __post_init__(self):
        if self.autonomy_level not in TERMINAL_AUTONOMY_LEVELS:
            raise ValueError(f"invalid autonomy_level: {self.autonomy_level}")

    def allows_autonomy(self, required_level: str) -> bool:
        if required_level not in AUTONOMY_HIERARCHY:
            return False
        return AUTONOMY_HIERARCHY.get(self.autonomy_level, -1) >= AUTONOMY_HIERARCHY[required_level]

    def allows(self, action: str) -> bool:
        return action in self.allowed_actions and action not in self.forbidden_actions

    def forbids(self, action: str) -> bool:
        return action in self.forbidden_actions

    def touches_protected_path(self, path: str) -> bool:
        normalized = (path or "").replace("\\", "/").lstrip("./")
        return any(normalized == item or normalized.startswith(item.rstrip("/") + "/") for item in self.protected_paths)

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "allowed_actions": list(self.allowed_actions),
            "forbidden_actions": list(self.forbidden_actions),
            "protected_paths": list(self.protected_paths),
            "required_reviewers": list(self.required_reviewers),
            "can_execute": self.can_execute,
            "can_approve": self.can_approve,
            "can_veto": self.can_veto,
            "can_code": self.can_code,
            "can_access_memory": self.can_access_memory,
            "can_use_opencode": self.can_use_opencode,
            "autonomy_level": self.autonomy_level,
        }


COMMON_PROTECTED = ("sovereign/constitution", "sovereign/state_corpus", "sovereign/laws", "sovereign/registries", "governance", "execution", ".env")

ROLE_BOUNDARIES: dict[str, RoleBoundary] = {
    "janus": RoleBoundary("janus", ("orchestrate", "route_task", "coordinate", "aggregate_report", "request_review"), ("bypass_sage", "bypass_governance", "modify_law", "direct_execution", "self_approve_critical_change"), COMMON_PROTECTED, autonomy_level="SANDBOX_WRITE"),
    "sage": RoleBoundary("sage", ("review", "veto", "classify_risk", "require_rollback", "audit", "governance_gate_review"), ("direct_execution", "modify_law_without_process", "operate_trading", "self_deploy"), COMMON_PROTECTED, can_veto=True, autonomy_level="SANDBOX_WRITE"),
    "hermes": RoleBoundary("hermes", ("memory_review", "lesson_review", "dataset_review", "skill_review", "archive_review", "distillation"), ("trading_execution", "modify_risk_kernel", "modify_governance_without_review", "direct_lancedb_backend_access"), COMMON_PROTECTED, autonomy_level="SANDBOX_WRITE"),
    "iris": RoleBoundary("iris", ("market_analysis", "economic_analysis", "portfolio_analysis", "budget_proposal", "resource_allocation_proposal"), ("live_execution", "increase_risk_without_approval", "modify_risk_kernel", "direct_broker_call"), COMMON_PROTECTED, autonomy_level="READ_ONLY"),
    "helen": RoleBoundary("helen", ("information_validation", "macro_analysis", "civilization_analysis", "communication_draft", "external_context_review"), ("modify_governance", "modify_execution", "approve_risk", "direct_trading"), COMMON_PROTECTED, autonomy_level="READ_ONLY"),
    "lang_lieu": RoleBoundary("lang_lieu", ("code", "architecture", "refactor", "test", "review_code", "use_opencode_adapter", "create_technical_report"), ("self_approve_governance", "modify_protected_modules_without_sage_review", "read_env", "read_credentials", "deploy_live", "direct_execution"), COMMON_PROTECTED, can_code=True, can_use_opencode=True, autonomy_level="BRANCH_WRITE"),
    "yet_kieu": RoleBoundary("yet_kieu", ("monitor_infrastructure", "security_review", "incident_response", "runtime_observation", "approved_sop_execution"), ("modify_law", "modify_governance_without_review", "direct_trading", "read_unapproved_secret"), COMMON_PROTECTED, autonomy_level="SANDBOX_WRITE"),
}


def get_role_boundary(agent_id: str) -> RoleBoundary:
    return ROLE_BOUNDARIES[agent_id]
