from __future__ import annotations

from agents.registry import AgentRegistry
from agents.role_boundary import get_role_boundary
from agents.task_envelope import TaskEnvelope, TaskStatus
from governance.policy_engine import is_protected_module


ROUTING_RULES = (
    (("governance", "risk", "compliance"), "sage"),
    (("memory", "dataset", "lesson", "skill"), "hermes"),
    (("market", "economics", "portfolio", "budget"), "iris"),
    (("information", "macro", "external context"), "helen"),
    (("code", "architecture", "testing", "test", "refactor"), "lang_lieu"),
    (("security", "infrastructure", "runtime"), "yet_kieu"),
    (("multi-agent", "mission", "orchestration"), "janus"),
)


class TaskRouter:
    def __init__(self, registry: AgentRegistry | None = None):
        self.registry = registry or AgentRegistry()

    def choose_agent(self, task: TaskEnvelope | dict) -> str:
        text = " ".join(str(value).lower() for value in (task.to_dict() if isinstance(task, TaskEnvelope) else task).values())
        for keywords, agent_id in ROUTING_RULES:
            if any(keyword in text for keyword in keywords):
                return agent_id
        return "janus"

    def route(self, task: TaskEnvelope | dict, issue_id: str = "") -> dict:
        task = task if isinstance(task, TaskEnvelope) else TaskEnvelope(**task)
        target = task.target_agent or self.choose_agent(task)
        valid = self.registry.validate_agent(target)
        if issue_id:
            task.issue_id = issue_id
        if not valid["valid"]:
            task.status = TaskStatus.BLOCKED.value
            return {"status": "BLOCKED", "target_agent": target, "task": task.to_dict(), "reason": "invalid target agent"}
        boundary = get_role_boundary(target)
        action = task.metadata.get("action", "")
        target_path = task.metadata.get("target_path", "")
        if action and not boundary.allows(action):
            task.status = TaskStatus.REJECTED.value
            return {"status": "REJECTED", "target_agent": target, "task": task.to_dict(), "reason": "target agent lacks permission"}
        if is_protected_module(target_path) and "Sage" not in task.required_approvals:
            task.status = TaskStatus.BLOCKED.value
            return {"status": "BLOCKED", "target_agent": target, "task": task.to_dict(), "reason": "protected module requires Sage review"}
        task.target_agent = target
        task.status = TaskStatus.ROUTED.value
        return {"status": "ROUTED", "target_agent": target, "task": task.to_dict(), "reason": "routed only; not executed"}
