import os
import subprocess
from pathlib import Path

from agents.base import BaseAgent
from agents.identity import get_identity
from agents.role_boundary import get_role_boundary
from agents.runtime_models import AgentReportEnvelope
from connectors.llm_connector import LLMConnector


class YetKieuAgent(BaseAgent):
    def __init__(self, memory_interface=None, memory_client=None, llm_connector=None):
        super().__init__(get_identity("yet_kieu"), get_role_boundary("yet_kieu"), memory_interface, memory_client)
        self.llm = llm_connector or LLMConnector()

    def get_identity(self):
        return self.identity

    def get_role_boundary(self):
        return self.role_boundary

    def check_infrastructure(self) -> dict:
        checks = {}
        try:
            result = subprocess.run(
                ["python", "--version"],
                capture_output=True, text=True, timeout=10,
            )
            checks["python"] = {"available": result.returncode == 0, "version": result.stdout.strip()}
        except Exception as e:
            checks["python"] = {"available": False, "error": str(e)}

        checks["disk_space"] = self._check_disk_space()
        checks["repo_integrity"] = self._check_repo()
        return {
            "all_ok": all(c.get("available", True) if isinstance(c, dict) else True for c in checks.values()),
            "checks": checks,
        }

    def _check_disk_space(self) -> dict:
        try:
            stat = os.statvfs(Path.cwd().anchor if os.name == "posix" else Path.cwd().root)
            free_gb = stat.f_frsize * stat.f_bavail / (1024**3)
            return {"available": True, "free_gb": round(free_gb, 2), "healthy": free_gb > 1.0}
        except Exception:
            return {"available": True, "free_gb": 0.0, "healthy": True}

    def _check_repo(self) -> dict:
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                capture_output=True, text=True, cwd=Path.cwd(), timeout=10,
            )
            return {
                "available": result.returncode == 0,
                "dirty": bool(result.stdout.strip()),
                "output": result.stdout.strip()[:200] if result.stdout else "clean",
            }
        except Exception as e:
            return {"available": False, "error": str(e)}

    def security_review(self) -> dict:
        findings = []
        env_file = Path.cwd() / ".env"
        if env_file.exists():
            findings.append({"severity": "WARNING", "finding": ".env file exists - check for secrets"})

        pycache_dirs = list(Path.cwd().rglob("__pycache__"))
        if pycache_dirs:
            findings.append({"severity": "INFO", "finding": f"{len(pycache_dirs)} __pycache__ directories present"})

        return {
            "findings": findings,
            "risk_level": "LOW" if not any(f["severity"] == "WARNING" for f in findings) else "MEDIUM",
            "reviewed_by": self.identity.agent_id,
        }

    def backup_posture(self) -> dict:
        archive_dir = Path.cwd() / "archive"
        return {
            "archive_exists": archive_dir.exists(),
            "archive_entries": len(list(archive_dir.iterdir())) if archive_dir.exists() else 0,
            "backup_status": "present" if archive_dir.exists() else "no_archive_found",
        }

    def incident_report(self, incident: dict) -> dict:
        prompt = (
            f"Analyze infrastructure incident:\n"
            f"Type: {incident.get('type', 'unknown')}\n"
            f"Description: {incident.get('description', 'none')}\n"
            f"Severity: {incident.get('severity', 'LOW')}\n"
            f"Provide: incident assessment, root cause, recommended actions."
        )
        llm_result = self.llm.execute(prompt)
        return {
            "incident": incident,
            "analysis": llm_result.get("content", ""),
            "mode": llm_result.get("mode", "mock"),
            "requires_escalation": incident.get("severity", "LOW") in ("HIGH", "CRITICAL"),
        }

    def generate_infrastructure_report(self, mission_id: str) -> AgentReportEnvelope:
        infra = self.check_infrastructure()
        security = self.security_review()
        return AgentReportEnvelope(
            agent_id=self.identity.agent_id,
            mission_id=mission_id,
            mission_type="infrastructure_mission",
            summary=f"Infrastructure check: {infra.get('all_ok', False)}, Security: {len(security.get('findings', []))} findings",
            status="COMPLETED",
            metadata={"infrastructure": infra, "security": security},
        )


def create_agent(memory_interface=None, memory_client=None, llm_connector=None):
    return YetKieuAgent(memory_interface, memory_client, llm_connector)
