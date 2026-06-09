from __future__ import annotations

from enum import Enum


class AgentLifecycleState(str, Enum):
    CREATED = "CREATED"
    BOOTSTRAPPED = "BOOTSTRAPPED"
    OPERATIONAL = "OPERATIONAL"
    DEGRADED = "DEGRADED"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"
    DISSOLVED = "DISSOLVED"


def can_be_operational(identity, boundary) -> bool:
    return bool(identity and boundary)


def can_receive_task(state: str) -> bool:
    return state not in {AgentLifecycleState.SUSPENDED.value, AgentLifecycleState.ARCHIVED.value, AgentLifecycleState.DISSOLVED.value}


def can_execute_task(state: str) -> bool:
    return state == AgentLifecycleState.OPERATIONAL.value


def allowed_actions_for_state(state: str) -> tuple[str, ...]:
    if state == AgentLifecycleState.DEGRADED.value:
        return ("report", "observe")
    if state == AgentLifecycleState.OPERATIONAL.value:
        return ("receive", "report", "observe")
    return ()
