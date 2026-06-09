from pathlib import Path


RISK_ORDER = {
    "LEVEL_0_LOW": 0,
    "LEVEL_1_MODERATE": 1,
    "LEVEL_2_HIGH": 2,
    "LEVEL_3_CRITICAL": 3,
    "LEVEL_4_CONSTITUTIONAL": 4,
}

DEFAULT_APPROVAL_MATRIX = Path(__file__).resolve().parent / "registries" / "approval_matrix.yaml"


def highest_risk(*levels: str) -> str:
    clean = [level for level in levels if level in RISK_ORDER]
    if not clean:
        return "LEVEL_0_LOW"
    return max(clean, key=lambda level: RISK_ORDER[level])


def parse_approval_matrix(path: str | Path | None = None) -> dict:
    matrix_path = Path(path) if path else DEFAULT_APPROVAL_MATRIX
    matrix: dict[str, dict[str, list[str]]] = {}
    current_level = None
    in_approvers = False
    for raw_line in matrix_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not raw_line.startswith(" ") and stripped.endswith(":"):
            current_level = stripped[:-1]
            matrix[current_level] = {"approvers": []}
            in_approvers = False
        elif current_level and stripped == "approvers:":
            in_approvers = True
        elif current_level and in_approvers and stripped.startswith("- "):
            matrix[current_level]["approvers"].append(stripped[2:].strip())
    return matrix


def validate_approvers(risk_level: str, approvers: list[str], matrix: dict | None = None) -> dict:
    matrix = matrix or parse_approval_matrix()
    required = matrix.get(risk_level, {}).get("approvers", [])
    missing = [approver for approver in required if approver not in approvers]
    return {"valid": not missing, "required": required, "provided": approvers, "missing": missing}


def approval_requirements(risk_level: str, extra_risk_level: str | None = None, matrix_path: str | Path | None = None) -> dict:
    matrix = parse_approval_matrix(matrix_path)
    final_level = highest_risk(risk_level, extra_risk_level or risk_level)
    approvers = matrix.get(final_level, {}).get("approvers", [])
    return {
        "risk_level": final_level,
        "approvers": approvers,
        "valid": bool(approvers),
        "reason": "approval requirements resolved" if approvers else "missing approval matrix entry",
    }
