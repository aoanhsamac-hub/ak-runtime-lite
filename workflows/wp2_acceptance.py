from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "agents/base.py",
    "agents/identity.py",
    "agents/role_boundary.py",
    "agents/task_envelope.py",
    "agents/report_envelope.py",
    "agents/registry.py",
    "agents/router.py",
    "agents/lifecycle.py",
    "agents/supervisor.py",
    "agents/runtime.py",
    "agents/audit_hook.py",
    "agents/registry.yaml",
    "docs/reports/AK_WP2_AGENT_RUNTIME_FRAMEWORK_REPORT.md",
]


def check_required_files():
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    return not missing, missing


def check_all_agents_boot():
    from agents.supervisor import AgentSupervisor

    report = AgentSupervisor().produce_agent_status_report()
    return len(report["agents"]) == 7 and all(status == "operational" for status in report["agents"].values()), report["agents"]


def check_role_boundaries_present():
    from agents.role_boundary import ROLE_BOUNDARIES

    return len(ROLE_BOUNDARIES) == 7, list(ROLE_BOUNDARIES)


def check_memory_interface_only():
    agent_files = list((ROOT / "agents").glob("**/*.py"))
    offenders = []
    for path in agent_files:
        text = path.read_text(encoding="utf-8")
        if "lancedb_adapter" in text or "LanceDBAdapter" in text:
            offenders.append(str(path.relative_to(ROOT)))
    return not offenders, offenders


def check_opencode_lang_lieu_only():
    from agents.role_boundary import ROLE_BOUNDARIES

    enabled = [agent_id for agent_id, boundary in ROLE_BOUNDARIES.items() if boundary.can_use_opencode]
    return enabled == ["lang_lieu"], enabled


def check_no_direct_execution():
    from agents.runtime import AgentRuntime

    runtime = AgentRuntime()
    return runtime.dry_run is True, {"dry_run": runtime.dry_run}


def check_no_secret_access():
    from agents.role_boundary import ROLE_BOUNDARIES

    return ROLE_BOUNDARIES["lang_lieu"].forbids("read_env") and ROLE_BOUNDARIES["yet_kieu"].forbids("read_unapproved_secret"), "secret access forbidden"


def check_tests_pass():
    cmd = [sys.executable, "-m", "pytest", str(ROOT / "tests"), "--basetemp", str(ROOT / "_pytest_tmp_wp2"), "-p", "no:cacheprovider"]
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return result.returncode == 0, result.stdout.splitlines()[-5:]


def main():
    checks = {
        "required_files": check_required_files(),
        "all_agents_boot": check_all_agents_boot(),
        "role_boundaries_present": check_role_boundaries_present(),
        "memory_interface_only": check_memory_interface_only(),
        "opencode_lang_lieu_only": check_opencode_lang_lieu_only(),
        "no_direct_execution": check_no_direct_execution(),
        "no_secret_access": check_no_secret_access(),
        "tests_pass": check_tests_pass(),
        "report_exists": ((ROOT / "docs/reports/AK_WP2_AGENT_RUNTIME_FRAMEWORK_REPORT.md").exists(), "report"),
    }
    passed = sum(1 for ok, _detail in checks.values() if ok)
    score = passed / len(checks)
    print("wp2_status:", "PASS" if score >= 1.0 else "FAIL")
    print("score:", round(score, 3))
    print("checks:")
    for name, (ok, detail) in checks.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
        print(f"    detail: {detail}")
    print("recommendation:", "G3 Agent Gate PASS" if score >= 1.0 else "review required")
    return 0 if score >= 1.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
