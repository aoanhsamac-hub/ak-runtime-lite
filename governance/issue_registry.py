import re
from datetime import datetime, timezone
from pathlib import Path

from governance.models.issue import ISSUE_STATUSES, Issue


DEFAULT_ISSUE_REGISTRY = Path(__file__).resolve().parent / "registries" / "issue_registry.yaml"
ISSUE_ID_PATTERN = re.compile(r"^ISSUE-\d{4}-\d{4}$")


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_text(path: Path) -> str:
    if not path.exists():
        return "issue_registry:\n  status: ACTIVE\n  issues: []\n"
    return path.read_text(encoding="utf-8")


def next_issue_id(path: str | Path | None = None) -> str:
    registry_path = Path(path) if path else DEFAULT_ISSUE_REGISTRY
    text = _read_text(registry_path)
    year = datetime.now(timezone.utc).year
    numbers = []
    for match in re.findall(rf"ISSUE-{year}-(\d{{4}})", text):
        numbers.append(int(match))
    return f"ISSUE-{year}-{(max(numbers) + 1 if numbers else 1):04d}"


def create_issue(title: str, description: str, risk_level: str, proposer: str, reviewers: list[str] | None = None, approvers: list[str] | None = None, path: str | Path | None = None) -> dict:
    registry_path = Path(path) if path else DEFAULT_ISSUE_REGISTRY
    issue = Issue(
        issue_id=next_issue_id(registry_path),
        title=title,
        description=description,
        status="Draft",
        risk_level=risk_level,
        proposer=proposer,
        reviewers=reviewers or [],
        approvers=approvers or [],
    )
    append_issue(issue.to_dict(), registry_path)
    return issue.to_dict()


def append_issue(issue: dict, path: str | Path | None = None) -> None:
    registry_path = Path(path) if path else DEFAULT_ISSUE_REGISTRY
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    if not registry_path.exists():
        registry_path.write_text("issue_registry:\n  status: ACTIVE\n  issues:\n", encoding="utf-8")
    with registry_path.open("a", encoding="utf-8") as handle:
        handle.write(f"  - issue_id: {issue['issue_id']}\n")
        handle.write(f"    title: {issue['title']}\n")
        handle.write(f"    description: {issue['description']}\n")
        handle.write(f"    status: {issue['status']}\n")
        handle.write(f"    risk_level: {issue['risk_level']}\n")
        handle.write(f"    proposer: {issue['proposer']}\n")
        handle.write("    reviewers:\n")
        for reviewer in issue.get("reviewers", []):
            handle.write(f"      - {reviewer}\n")
        handle.write("    approvers:\n")
        for approver in issue.get("approvers", []):
            handle.write(f"      - {approver}\n")
        handle.write(f"    created_at: {issue.get('created_at', _now())}\n")
        handle.write(f"    updated_at: {issue.get('updated_at', _now())}\n")


def validate_issue(issue: dict) -> dict:
    required = ("issue_id", "title", "description", "status", "risk_level", "proposer", "reviewers", "approvers", "created_at", "updated_at")
    missing = [field for field in required if field not in issue]
    valid_id = bool(ISSUE_ID_PATTERN.match(str(issue.get("issue_id", ""))))
    valid_status = issue.get("status") in ISSUE_STATUSES
    return {"valid": not missing and valid_id and valid_status, "missing": missing, "valid_id": valid_id, "valid_status": valid_status}
