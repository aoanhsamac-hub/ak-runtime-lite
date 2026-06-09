from __future__ import annotations

from connectors.opencode_connector import OpenCodeConnector


class LangLieuDevOrchestrator:
    def __init__(self, connector: OpenCodeConnector | None = None):
        self.connector = connector or OpenCodeConnector()

    def run_task(
        self,
        task: str,
        target_paths: list[str],
        sage_review: bool = False,
        approval_gate: bool = False,
    ) -> dict:
        request = self.connector.prepare_task(
            task,
            target_paths,
            sage_review=sage_review,
            approval_gate=approval_gate,
        )
        return {
            "agent": "lang_lieu",
            "task": task,
            "adapter_request": request,
            "diff": None,
            "tests": [],
            "implementation_report": "OpenCode adapter-only request prepared; no direct execution performed.",
            "governance_review": {
                "required": request["status"] == "BLOCKED" or bool(request["protected_paths"]),
                "status": request["status"],
                "reason": request["reason"],
            },
            "direct_execution": False,
        }

