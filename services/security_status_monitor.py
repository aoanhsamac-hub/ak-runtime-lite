"""Security status monitor for PSOP-02."""

from pathlib import Path


INFRASTRUCTURE_DIR = Path(__file__).resolve().parent.parent / "infrastructure"
SERVICES_IRIS_DIR = Path(__file__).resolve().parent.parent / "services" / "iris"
AGENTS_DIR = Path(__file__).resolve().parent.parent / "agents"


def check():
    findings = []
    checks_passed = 0
    checks_total = 5

    yet_kieu_agent = AGENTS_DIR / "yet_kieu" / "agent.py"
    if yet_kieu_agent.exists():
        checks_passed += 1
    else:
        findings.append("Yet Kieu security agent not found")

    mt5_observer = INFRASTRUCTURE_DIR / "yet_kieu" / "mt5_health_monitor.py"
    alt_mt5 = Path(__file__).resolve().parent.parent / "connectors" / "mt5" / "mt5_demo_observer.py"
    if mt5_observer.exists() or alt_mt5.exists():
        checks_passed += 1
    else:
        findings.append("MT5 health monitor not found")

    zone_detector = SERVICES_IRIS_DIR / "zone_detector.py"
    if zone_detector.exists():
        checks_passed += 1
    else:
        findings.append("Zone detector not found")

    so_ps_dir = Path(__file__).resolve().parent.parent / "docs" / "sops"
    if so_ps_dir.exists():
        sop_count = len(list(so_ps_dir.glob("*.md")))
        if sop_count >= 8:
            checks_passed += 1
        else:
            findings.append(f"Only {sop_count} SOPs found, expected 8+")
    else:
        findings.append("SOPs directory not found")

    audit_service = Path(__file__).resolve().parent.parent / "services" / "treasury_audit_service.py"
    if audit_service.exists():
        checks_passed += 1
    else:
        findings.append("Treasury audit service not found")

    score = round(checks_passed / checks_total * 100)

    if checks_passed == checks_total:
        status = "HEALTHY"
        detail = f"All {checks_total} security checks passed"
    elif checks_passed >= checks_total - 1:
        status = "WATCH"
        detail = f"{checks_passed}/{checks_total} security checks passed"
    elif checks_passed >= checks_total - 2:
        status = "WARNING"
        detail = f"{checks_passed}/{checks_total} security checks passed: {'; '.join(findings)}"
    else:
        status = "CRITICAL"
        detail = f"Only {checks_passed}/{checks_total} security checks passed: {'; '.join(findings)}"

    return {
        "status": status,
        "score": score,
        "detail": detail,
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "findings": findings,
    }
