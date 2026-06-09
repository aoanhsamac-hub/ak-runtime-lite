"""Governance health monitor for PSOP-02."""

from pathlib import Path


REGISTRIES_DIR = Path(__file__).resolve().parent.parent / "docs" / "registries"
CHARTERS_DIR = Path(__file__).resolve().parent.parent / "docs" / "charters"

REQUIRED_CHARTERS = [
    "AK_TREASURY_CHARTER_v1.0_FINAL.md",
    "AK_ROYAL_TREASURY_CHARTER_v1.0_FINAL.md",
    "JANUS_CHARTER_v1.0_FINAL.md",
    "HERMES_CHARTER_v1.0_FINAL.md",
]

REQUIRED_REGISTRIES = [
    "TREASURY_HEALTH_REGISTRY.yaml",
    "TREASURY_STATUS_REGISTRY.yaml",
    "TREASURY_ACCOUNT_REGISTRY.yaml",
    "TREASURY_TRANSACTION_REGISTRY.yaml",
    "TREASURY_REPORT_REGISTRY.yaml",
    "TREASURY_TRANSACTION_STATUS_REGISTRY.yaml",
    "KINGDOM_HEALTH_REGISTRY.yaml",
    "KINGDOM_STATUS_REGISTRY.yaml",
]


def check():
    findings = []
    score = 100

    for charter in REQUIRED_CHARTERS:
        path = CHARTERS_DIR / charter
        if not path.exists():
            findings.append(f"Missing charter: {charter}")
            score -= 20

    for reg in REQUIRED_REGISTRIES:
        path = REGISTRIES_DIR / reg
        if not path.exists():
            findings.append(f"Missing registry: {reg}")
            score -= 10

    if score < 0:
        score = 0

    if len(findings) == 0:
        status = "HEALTHY"
        detail = "All charters and registries present"
    elif score >= 70:
        status = "WATCH"
        detail = f"{len(findings)} compliance gaps: {'; '.join(findings[:3])}"
    elif score >= 40:
        status = "WARNING"
        detail = f"{len(findings)} compliance gaps: {'; '.join(findings[:3])}"
    else:
        status = "CRITICAL"
        detail = f"Severe compliance gaps: {'; '.join(findings[:3])}"

    return {"status": status, "score": score, "detail": detail, "findings": findings}
