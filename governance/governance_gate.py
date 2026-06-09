from governance.approval_engine import approval_requirements, validate_approvers
from governance.audit_engine import append_audit_record
from governance.issue_registry import create_issue
from governance.policy_engine import classify_change, is_protected_module


def evaluate_proposal(proposal: dict) -> dict:
    change = {
        "path": proposal.get("target_path") or proposal.get("path", ""),
        "description": proposal.get("description", ""),
        "governance_valid": proposal.get("governance_valid", True),
    }
    classification = classify_change(change)
    requirements = approval_requirements(classification["risk_level"])
    provided_approvers = proposal.get("approvers", [])
    approval_check = validate_approvers(requirements["risk_level"], provided_approvers)
    protected = is_protected_module(change["path"])

    blocked = bool(
        classification["blocked"]
        or not approval_check["valid"]
        or (protected and not provided_approvers)
    )
    reasons = [classification["reason"]]
    if approval_check["missing"]:
        reasons.append("missing approver: " + ", ".join(approval_check["missing"]))
    if protected and not provided_approvers:
        reasons.append("protected module requires approval")

    return {
        "decision": "BLOCK" if blocked else "ALLOW",
        "blocked": blocked,
        "risk_level": requirements["risk_level"],
        "required_approvers": requirements["approvers"],
        "provided_approvers": provided_approvers,
        "protected_module": protected,
        "reason": "; ".join(reasons),
    }


def run_governance_workflow(proposal: dict, audit: bool = True) -> dict:
    gate = evaluate_proposal(proposal)
    issue = create_issue(
        title=proposal.get("title", "Untitled Proposal"),
        description=proposal.get("description", ""),
        risk_level=gate["risk_level"],
        proposer=proposal.get("proposer", "UNKNOWN"),
        reviewers=proposal.get("reviewers", []),
        approvers=proposal.get("approvers", []),
    )
    audit_record = None
    if audit:
        audit_record = append_audit_record(
            actor=proposal.get("proposer", "UNKNOWN"),
            action="governance_gate_evaluate",
            target=proposal.get("target_path") or proposal.get("path", ""),
            result=gate["decision"],
            issue_id=issue["issue_id"],
        )
    return {"proposal": proposal, "issue": issue, "gate": gate, "audit_record": audit_record}
