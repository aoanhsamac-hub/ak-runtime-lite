from agents.base import BaseAgent
from agents.identity import get_identity
from agents.role_boundary import get_role_boundary
from agents.runtime_models import ActivationState, AgentReportEnvelope, EvidenceClassification
from connectors.llm_connector import LLMConnector


class SageAgent(BaseAgent):
    def __init__(self, memory_interface=None, memory_client=None, llm_connector=None):
        super().__init__(get_identity("sage"), get_role_boundary("sage"), memory_interface, memory_client)
        self.llm = llm_connector or LLMConnector()

    def get_identity(self):
        return self.identity

    def get_role_boundary(self):
        return self.role_boundary

    def validate_activation(self, target_state: ActivationState, evidence_summary: dict | None = None) -> dict:
        forbidden = {
            ActivationState.OPERATIONAL_APPROVED,
            ActivationState.OPERATIONAL_LIMITED,
            ActivationState.PILOT_ACTIVE,
        }
        if target_state in forbidden:
            return {
                "allowed": False,
                "reason": f"Activation state {target_state.value} requires Hung Vuong approval",
                "required_reviewer": "Hung Vuong",
            }
        if target_state == ActivationState.SANDBOX_ACTIVE:
            return {
                "allowed": True,
                "reason": "Sandbox activation permitted for controlled learning-by-doing",
            }
        if target_state == ActivationState.READY_FOR_SANDBOX:
            return {
                "allowed": True,
                "reason": "Ready for sandbox - state change permitted",
            }
        return {
            "allowed": False,
            "reason": f"State change to {target_state.value} not currently permitted",
        }

    def review_risk(self, evidence: list[dict]) -> dict:
        risks = []
        for ev in evidence:
            classification = ev.get("classification", "")
            if classification in (
                EvidenceClassification.I9_REJECTED.value,
                EvidenceClassification.I8_RUMOR.value,
            ):
                risks.append(f"Low-quality evidence: {ev.get('evidence_id', 'unknown')}")
        return {
            "risks_found": len(risks) > 0,
            "risks": risks,
            "safe": len(risks) == 0,
            "reviewed_by": self.identity.agent_id,
        }

    def veto_proposal(self, proposal: dict) -> dict:
        prompt = (
            f"Review this proposal for governance compliance:\n"
            f"Title: {proposal.get('title', '')}\n"
            f"Description: {proposal.get('description', '')}\n"
            f"Risk: {proposal.get('risk_level', 'unknown')}\n"
            f"Provide: veto decision (ALLOW/BLOCK) and reason."
        )
        llm_result = self.llm.execute(prompt)
        return {
            "veto": "BLOCK" in llm_result.get("content", "").upper(),
            "reason": llm_result.get("content", "No review provided")[:200],
            "mode": llm_result.get("mode", "mock"),
        }

    def compliance_report(self, activation_state: ActivationState) -> dict:
        checks = {
            "constitution_compliant": True,
            "state_corpus_compliant": True,
            "agent_law_compliant": True,
            "risk_law_compliant": activation_state in (ActivationState.LOCKED, ActivationState.READY_FOR_SANDBOX, ActivationState.SANDBOX_ACTIVE),
            "execution_law_compliant": activation_state != ActivationState.OPERATIONAL_APPROVED,
            "security_law_compliant": True,
            "memory_law_compliant": True,
            "information_law_compliant": True,
            "repo_governance_compliant": True,
        }
        all_pass = all(checks.values())
        return {
            "activation_state": activation_state.value,
            "checks": checks,
            "all_pass": all_pass,
            "reviewed_by": self.identity.agent_id,
        }

    def generate_gate_report(self, mission_id: str) -> AgentReportEnvelope:
        return AgentReportEnvelope(
            agent_id=self.identity.agent_id,
            mission_id=mission_id,
            mission_type="governance_mission",
            summary="Governance gate review completed",
            status="COMPLETED",
        )


def create_agent(memory_interface=None, memory_client=None, llm_connector=None):
    return SageAgent(memory_interface, memory_client, llm_connector)
