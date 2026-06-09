"""Minimal governance policy engine for AK.

This module is intentionally framework-free and fail-closed by default.
"""

LEVEL_0_LOW = 0
LEVEL_1_MODERATE = 1
LEVEL_2_HIGH = 2
LEVEL_3_CRITICAL = 3
LEVEL_4_CONSTITUTIONAL = 4

RISK_LABELS = {
    LEVEL_0_LOW: "LEVEL_0_LOW",
    LEVEL_1_MODERATE: "LEVEL_1_MODERATE",
    LEVEL_2_HIGH: "LEVEL_2_HIGH",
    LEVEL_3_CRITICAL: "LEVEL_3_CRITICAL",
    LEVEL_4_CONSTITUTIONAL: "LEVEL_4_CONSTITUTIONAL",
}

PROTECTED_MODULES = (
    ("sovereign/constitution", LEVEL_4_CONSTITUTIONAL, ["Sage"], "Hung Vuong"),
    ("sovereign/state_corpus", LEVEL_4_CONSTITUTIONAL, ["Sage"], "Hung Vuong"),
    ("governance/risk_kernel", LEVEL_4_CONSTITUTIONAL, ["Sage"], "Hung Vuong"),
    (".env", LEVEL_4_CONSTITUTIONAL, ["Yet Kieu"], "Hung Vuong"),
    ("sovereign/registries", LEVEL_3_CRITICAL, ["Sage"], "Janus"),
    ("governance", LEVEL_3_CRITICAL, ["Sage"], "Janus"),
    ("execution", LEVEL_3_CRITICAL, ["Sage"], "Janus"),
    ("infrastructure/security", LEVEL_3_CRITICAL, ["Yet Kieu"], "Sage"),
)

CRITICAL_KEYWORDS = (
    "governance",
    "risk",
    "execution",
    "security",
    "credential",
    "credentials",
    "secret",
    "password",
    "api_key",
    "live_mode",
)


def _normalize_path(path: str) -> str:
    return (path or "").replace("\\", "/").strip().lstrip("./")


def _risk_label(level: int) -> str:
    return RISK_LABELS.get(level, "LEVEL_0_LOW")


def is_protected_module(path: str) -> bool:
    normalized = _normalize_path(path)
    return any(
        normalized == prefix or normalized.startswith(prefix + "/")
        for prefix, _level, _reviewers, _approver in PROTECTED_MODULES
    )


def classify_change(change: dict) -> dict:
    path = _normalize_path(str(change.get("path", "")))
    text = " ".join(str(value).lower() for value in change.values())
    governance_valid = bool(change.get("governance_valid", True))

    risk_level = LEVEL_0_LOW
    required_reviewers = []
    required_approver = None
    reasons = []

    for prefix, level, reviewers, approver in PROTECTED_MODULES:
        if path == prefix or path.startswith(prefix + "/"):
            risk_level = max(risk_level, level)
            required_reviewers.extend(reviewers)
            required_approver = approver if level >= risk_level else required_approver
            reasons.append(f"protected module: {prefix}")

    if "sovereign/constitution" in path or "constitution" in text:
        risk_level = max(risk_level, LEVEL_4_CONSTITUTIONAL)
        required_reviewers.append("Sage")
        required_approver = "Hung Vuong"
        reasons.append("constitutional scope")

    if "sovereign/state_corpus" in path or "state_corpus" in text or "state corpus" in text:
        risk_level = max(risk_level, LEVEL_4_CONSTITUTIONAL)
        required_reviewers.append("Sage")
        required_approver = "Hung Vuong"
        reasons.append("state corpus scope")

    if any(keyword in path.lower() or keyword in text for keyword in CRITICAL_KEYWORDS):
        risk_level = max(risk_level, LEVEL_3_CRITICAL)
        if "Sage" not in required_reviewers:
            required_reviewers.append("Sage")
        required_approver = required_approver or "Janus"
        reasons.append("critical governance/security/execution keyword")

    if not governance_valid:
        risk_level = max(risk_level, LEVEL_3_CRITICAL)
        reasons.append("governance invalid")

    if not required_reviewers and risk_level > LEVEL_0_LOW:
        required_reviewers.append("Sage")

    return {
        "risk_level": _risk_label(risk_level),
        "required_reviewers": sorted(set(required_reviewers)),
        "required_approver": required_approver,
        "blocked": not governance_valid,
        "reason": "; ".join(reasons) if reasons else "standard low-risk change",
    }


def requires_approval(change: dict) -> dict:
    result = classify_change(change)
    result["blocked"] = bool(result["blocked"] or change.get("execution_requested") and not change.get("governance_valid", True))
    if result["blocked"] and "fail-closed" not in result["reason"]:
        result["reason"] = f"{result['reason']}; fail-closed"
    return result
