from dataclasses import dataclass, field


@dataclass
class ApprovalRequirement:
    risk_level: str
    approvers: list[str] = field(default_factory=list)
    valid: bool = True
    reason: str = ""

    def to_dict(self) -> dict:
        return {
            "risk_level": self.risk_level,
            "approvers": list(self.approvers),
            "valid": self.valid,
            "reason": self.reason,
        }
