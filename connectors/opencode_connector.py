from __future__ import annotations

import shutil
from pathlib import Path

from governance.governance_gate import evaluate_proposal


PROTECTED_PATHS = (
    ".env",
    "credentials",
    "sovereign",
    "governance",
    "risk_kernel",
    "execution",
    "security",
)


class OpenCodeConnector:
    mode = "adapter_only"

    def __init__(self, executable: str = "opencode"):
        self.executable = executable

    def prepare_task(
        self,
        task: str,
        target_paths: list[str],
        sage_review: bool = False,
        approval_gate: bool = False,
    ) -> dict:
        protected = [path for path in target_paths if self._is_protected(path)]
        governance_gate = self._governance_gate(task, target_paths, protected, sage_review, approval_gate)
        if protected and not (sage_review and approval_gate):
            return {
                "status": "BLOCKED",
                "mode": self.mode,
                "task": task,
                "target_paths": target_paths,
                "protected_paths": protected,
                "governance_gate": governance_gate,
                "execution_enabled": False,
                "reason": "Sage Review + Approval Gate required for protected paths",
            }
        executable_path = shutil.which(self.executable)
        status = "READY" if executable_path else "UNAVAILABLE"
        return {
            "status": status,
            "mode": self.mode,
            "task": task,
            "target_paths": target_paths,
            "protected_paths": protected,
            "opencode_path": executable_path,
            "governance_gate": governance_gate,
            "execution_enabled": False,
            "reason": "adapter request prepared; direct execution disabled",
        }

    def _is_protected(self, path: str) -> bool:
        normalized = path.replace("\\", "/").strip("/").lower()
        if ":" in normalized:
            normalized = normalized.split(":", 1)[1].strip("/")
        parts = set(normalized.split("/"))
        return any(
            normalized == protected or normalized.startswith(protected + "/") or protected in parts
            for protected in PROTECTED_PATHS
        )

    def _governance_gate(
        self,
        task: str,
        target_paths: list[str],
        protected: list[str],
        sage_review: bool,
        approval_gate: bool,
    ) -> dict:
        if protected and not (sage_review and approval_gate):
            return {
                "decision": "BLOCK",
                "blocked": True,
                "reason": "protected OpenCode target requires Sage Review + Approval Gate",
            }
        if not target_paths:
            return {"decision": "BLOCK", "blocked": True, "reason": "target path is required"}
        proposal = {
            "title": "OpenCode adapter request",
            "description": task,
            "target_path": target_paths[0],
            "proposer": "LangLieu",
            "approvers": ["Janus"] if not protected else ["Sage", "HungVuong"],
        }
        gate = evaluate_proposal(proposal)
        if not protected and gate["risk_level"] == "LEVEL_0_LOW":
            gate = dict(gate)
            gate["decision"] = "ALLOW"
            gate["blocked"] = False
            gate["reason"] = "adapter-only unprotected request allowed after path validation"
        return gate
