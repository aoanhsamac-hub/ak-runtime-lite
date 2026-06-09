from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_FILES = [
    "memory/lancedb_adapter.py",
    "memory/lesson_registry.py",
    "memory/skill_registry.py",
    "memory/capability_registry.py",
    "memory/dataset_registry.py",
    "memory/decision_trace_registry.py",
    "memory/learning_loop.py",
    "memory/knowledge_compression.py",
    "memory/distillation_pipeline.py",
    "memory/quarantine_policy.py",
    "memory/memory_interface.py",
    "memory/agent_memory.py",
    "memory/schemas/records.py",
    "connectors/opencode_connector.py",
    "agents/lang_lieu/dev_orchestrator.py",
    "tests/test_lancedb_adapter.py",
    "tests/test_learning_loop.py",
    "tests/test_skill_registry.py",
    "tests/test_capability_registry.py",
    "tests/test_decision_trace.py",
    "tests/test_memory_interface.py",
    "tests/test_agent_memory_interface.py",
    "tests/test_opencode_connector.py",
    "tests/test_wp3_acceptance.py",
    "docs/reports/AK_WP3_HERMES_NATIVE_MEMORY_PLATFORM_REPORT.md",
]

BANNED_BACKENDS = ["sqlite", "chroma", "faiss"]


def run_acceptance(root: Path, run_lancedb_smoke: bool = True) -> dict[str, Any]:
    root = root.resolve()
    checks = {
        "required_files": _check_required_files(root),
        "banned_memory_backends": _check_banned_memory_backends(root),
        "runtime_dependencies": _check_runtime_dependencies(root),
        "runtime_boundaries": _check_runtime_boundaries(root),
        "opencode_safety": _check_opencode_safety(root),
        "report_readiness": _check_report_readiness(root),
        "runtime_smoke": _check_runtime_smoke(root, run_lancedb_smoke),
    }
    weights = {
        "required_files": 0.22,
        "banned_memory_backends": 0.14,
        "runtime_dependencies": 0.12,
        "runtime_boundaries": 0.14,
        "opencode_safety": 0.14,
        "report_readiness": 0.10,
        "runtime_smoke": 0.14,
    }
    score = sum(weights[name] for name, check in checks.items() if check["passed"])
    return {
        "work_package": "WP3",
        "status": "PASS" if score >= 0.95 else "FAIL",
        "score": round(score, 4),
        "checks": checks,
        "review_items": [
            "Formal Sage review is still required before protected workflow integration.",
            "AK agents remain bootstrap-level and must not be represented as full autonomous reviewers.",
            "OpenCode remains adapter-only until executable and governance approval are present.",
        ],
    }


def _check_required_files(root: Path) -> dict[str, Any]:
    missing = [path for path in REQUIRED_FILES if not (root / path).exists()]
    return {"passed": not missing, "missing": missing, "count": len(REQUIRED_FILES)}


def _check_banned_memory_backends(root: Path) -> dict[str, Any]:
    hits: list[dict[str, str]] = []
    memory_root = root / "memory"
    if memory_root.exists():
        for path in memory_root.rglob("*.py"):
            text = path.read_text(encoding="utf-8").lower()
            for token in BANNED_BACKENDS:
                if token in text:
                    hits.append({"path": str(path.relative_to(root)), "token": token})
    return {"passed": not hits, "hits": hits}


def _check_runtime_dependencies(root: Path) -> dict[str, Any]:
    req = root / "requirements.txt"
    lines = set(req.read_text(encoding="utf-8").splitlines()) if req.exists() else set()
    missing = [dep for dep in ["lancedb", "pylance", "pytest"] if dep not in lines]
    return {"passed": not missing, "missing": missing}


def _check_runtime_boundaries(root: Path) -> dict[str, Any]:
    scanned = []
    hits = []
    for rel in ["memory", "connectors", "agents/lang_lieu"]:
        base = root / rel
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            scanned.append(str(path.relative_to(root)))
            text = path.read_text(encoding="utf-8").lower()
            for token in ["from hermes", "import hermes", "from openhands", "import openhands", "from lightagent", "import lightagent"]:
                if token in text:
                    hits.append({"path": str(path.relative_to(root)), "token": token})
    return {"passed": not hits, "scanned": scanned, "hits": hits}


def _check_opencode_safety(root: Path) -> dict[str, Any]:
    import sys

    sys.path.insert(0, str(root))
    try:
        from connectors.opencode_connector import OpenCodeConnector
    finally:
        try:
            sys.path.remove(str(root))
        except ValueError:
            pass
    connector = OpenCodeConnector()
    protected = connector.prepare_task("protect env", [r"D:\AK\.env"])
    unprotected = connector.prepare_task("docs", ["docs/reports/example.md"])
    passed = (
        protected["status"] == "BLOCKED"
        and protected["execution_enabled"] is False
        and protected["governance_gate"]["decision"] == "BLOCK"
        and unprotected["execution_enabled"] is False
        and unprotected["governance_gate"]["decision"] == "ALLOW"
    )
    return {"passed": passed, "protected": protected, "unprotected": unprotected}


def _check_report_readiness(root: Path) -> dict[str, Any]:
    report = root / "docs/reports/AK_WP3_HERMES_NATIVE_MEMORY_PLATFORM_REPORT.md"
    if not report.exists():
        return {"passed": False, "readiness": 0.0}
    readiness = 0.0
    for line in report.read_text(encoding="utf-8").splitlines():
        if line.startswith("Readiness:"):
            readiness = float(line.split(":", 1)[1].strip())
            break
    return {"passed": readiness >= 0.95, "readiness": readiness}


def _check_runtime_smoke(root: Path, run_lancedb_smoke: bool) -> dict[str, Any]:
    if not run_lancedb_smoke:
        return {"passed": True, "mode": "skipped_by_test"}
    import sys

    sys.path.insert(0, str(root))
    try:
        from memory.lancedb_adapter import LanceDBAdapter
    finally:
        try:
            sys.path.remove(str(root))
        except ValueError:
            pass
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    smoke_root = (
        Path(r"C:\Users\GiangKhoi\Documents\Alkasik Kingdom (AK)")
        / "_lancedb_runtime_smoke"
        / f"wp3_acceptance_{stamp}"
    )
    smoke_root.mkdir(parents=True, exist_ok=True)
    adapter = LanceDBAdapter(smoke_root)
    table_name = "wp3_acceptance_runtime"
    adapter.insert(table_name, [{"lesson_id": "WP3-ACCEPTANCE", "content": "wp3 acceptance runtime smoke"}])
    results = adapter.search(table_name, "wp3 acceptance runtime smoke", limit=1)
    return {"passed": len(results) == 1, "result_count": len(results)}


def main() -> None:
    result = run_acceptance(Path.cwd())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
