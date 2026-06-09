from agents.base import BaseAgent
from agents.identity import get_identity
from agents.role_boundary import get_role_boundary
from agents.runtime_models import AgentReportEnvelope
from connectors.llm_connector import LLMConnector
from connectors.opencode_connector import OpenCodeConnector


class LangLieuAgent(BaseAgent):
    def __init__(self, memory_interface=None, memory_client=None, llm_connector=None):
        super().__init__(get_identity("lang_lieu"), get_role_boundary("lang_lieu"), memory_interface, memory_client)
        self.llm = llm_connector or LLMConnector()
        self.opencode = OpenCodeConnector()

    def get_identity(self):
        return self.identity

    def get_role_boundary(self):
        return self.role_boundary

    def opencode_status(self) -> dict:
        try:
            from agents.lang_lieu.dev_orchestrator import LangLieuDevOrchestrator
            return LangLieuDevOrchestrator().check_opencode()
        except Exception:
            return {"status": "UNAVAILABLE", "reason": "opencode adapter unavailable"}

    def plan_implementation(self, objective: str) -> dict:
        prompt = (
            f"Plan implementation for: {objective}\n"
            f"Provide: implementation steps, files to modify, test requirements, risk assessment."
        )
        llm_result = self.llm.execute(prompt)
        return {
            "objective": objective,
            "plan": llm_result.get("content", ""),
            "mode": llm_result.get("mode", "mock"),
            "status": "planned",
        }

    def review_code_quality(self, file_path: str, code_content: str) -> dict:
        prompt = (
            f"Review this code for quality and governance compliance:\n"
            f"File: {file_path}\n"
            f"```\n{code_content[:1000]}\n```\n"
            f"Provide: issues found, recommendations, governance concerns."
        )
        llm_result = self.llm.execute(prompt)
        return {
            "file": file_path,
            "review": llm_result.get("content", ""),
            "mode": llm_result.get("mode", "mock"),
        }

    def coordinate_code_generation(self, task: str, target_paths: list[str]) -> dict:
        return {
            "task": task,
            "target_paths": target_paths,
            "adapter_request": self.opencode.prepare_task(task, target_paths, sage_review=True, approval_gate=True),
            "status": "coordinated",
        }

    def run_tests(self, test_paths: list[str]) -> dict:
        import subprocess
        results = {}
        for path in test_paths:
            try:
                r = subprocess.run(
                    ["python", "-m", "pytest", path, "-q", "--tb=short"],
                    capture_output=True, text=True, timeout=60,
                )
                results[path] = {
                    "passed": r.returncode == 0,
                    "output": r.stdout.strip()[-200:] if r.stdout else r.stderr.strip()[-200:],
                }
            except Exception as e:
                results[path] = {"passed": False, "error": str(e)}
        return {
            "test_results": results,
            "all_passed": all(r.get("passed", False) for r in results.values()),
        }

    def generate_engineering_report(self, mission_id: str) -> AgentReportEnvelope:
        return AgentReportEnvelope(
            agent_id=self.identity.agent_id,
            mission_id=mission_id,
            mission_type="engineering_mission",
            summary="Engineering implementation completed",
            status="COMPLETED",
        )


def create_agent(memory_interface=None, memory_client=None, llm_connector=None):
    return LangLieuAgent(memory_interface, memory_client, llm_connector)
