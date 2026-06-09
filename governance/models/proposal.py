from dataclasses import dataclass


@dataclass
class Proposal:
    title: str
    description: str
    proposer: str
    target_path: str
    governance_valid: bool = True

    def to_change(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "proposer": self.proposer,
            "path": self.target_path,
            "governance_valid": self.governance_valid,
        }
