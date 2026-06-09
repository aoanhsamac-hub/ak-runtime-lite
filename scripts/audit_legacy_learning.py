#!/usr/bin/env python3
"""Audit legacy learning directory — dry-run only by default."""

import csv
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

DRY_RUN = True
LEGACY_ROOT = Path("D:/Alkasik/learning")
AK_QUARANTINE = Path(__file__).resolve().parent.parent / "memory" / "legacy_corpus" / "quarantine"
AK_INDEX_PATH = Path(__file__).resolve().parent.parent / "memory" / "legacy_corpus" / "legacy_learning_index.yaml"

SECRET_PATTERNS = [
    re.compile(r"(?i)(?:api[_-]?key|apikey|secret|token|password|credential)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-\.]{16,}"),
    re.compile(r"(?i)sk-[a-zA-Z0-9]{20,}"),
    re.compile(r"(?i)private\s*key"),
    re.compile(r"(?i)-----BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY"),
]

BLOCKED_EXTENSIONS = {".pyc", ".exe", ".dll", ".so", ".dylib", ".bin"}
BLOCKED_DIRECTORIES = {"__pycache__", "node_modules", ".venv", ".git", ".env"}
CODE_EXTENSIONS = {".py", ".ps1", ".sh", ".bat", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".go", ".rs"}


def _file_hash(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()[:65536]).hexdigest()[:16]
    except Exception:
        return "ERROR"


def _classify_path(path: Path) -> str:
    name = path.stem.lower()
    parent = path.parent.name.lower()
    full = str(path).lower()

    if "secret" in full or "credential" in full or "password" in full:
        return "REJECTED"
    if "trading" in full or "execution" in full or "mt5" in full or "broker" in full:
        return "TRADING_STRATEGY_KNOWLEDGE"
    if "market" in full or "intelligence" in full:
        return "MARKET_INTELLIGENCE"
    if "security" in full or "safety" in full:
        return "SECURITY_KNOWLEDGE"
    if "governance" in full or "rule" in full or "policy" in full:
        return "GOVERNANCE"
    if "skill" in full or "template" in full:
        return "SKILL"
    if "capability" in full or "evolution" in full:
        return "CAPABILITY"
    if "dataset" in full or "data" in parent:
        return "DATASET"
    if "lesson" in full or "memory" in full:
        return "MEMORY"
    if "behavior" in full or "pattern" in full:
        return "DECISION_TRACE"
    if "report" in full or "status" in full or "completion" in full or "progress" in full:
        return "LESSON"
    if "engineer" in full or "code" in parent or "implementation" in full:
        return "ENGINEERING_KNOWLEDGE"
    if "infrastructure" in full or "adaptive" in full or "scheduler" in full:
        return "INFRASTRUCTURE_KNOWLEDGE"
    if path.suffix in CODE_EXTENSIONS:
        return "ENGINEERING_KNOWLEDGE"

    return "UNKNOWN"


def _risk_level(path: Path, category: str) -> str:
    if category == "REJECTED":
        return "REJECTED"
    if path.suffix in CODE_EXTENSIONS:
        return "MEDIUM"
    if "secret" in str(path).lower():
        return "HIGH"
    if any(p in str(path).lower() for p in ("password", "credential", "token")):
        return "HIGH"
    return "LOW"


def _contains_code(path: Path) -> bool:
    return path.suffix in CODE_EXTENSIONS


def _contains_secret(path: Path) -> bool:
    try:
        content = path.read_text(errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                return True
    except Exception:
        pass
    return False


def _migration_status(category: str, risk: str, has_code: bool, has_secret: bool) -> str:
    if has_secret or category == "REJECTED":
        return "DO_NOT_IMPORT"
    if risk == "HIGH":
        return "REQUIRES_HUNG_VUONG_APPROVAL"
    if has_code:
        return "QUARANTINE_IMPORT"
    if category in ("GOVERNANCE", "LESSON", "SKILL", "CAPABILITY"):
        return "APPROVED_FOR_REVIEW"
    return "REQUIRES_SAGE_REVIEW"


def _target_registry(category: str) -> str:
    mapping = {
        "GOVERNANCE": "governance/registries",
        "MEMORY": "memory/legacy_corpus/quarantine",
        "LESSON": "memory/lesson_registry",
        "SKILL": "memory/skill_registry",
        "CAPABILITY": "memory/capability_registry",
        "DATASET": "memory/dataset_registry",
        "DECISION_TRACE": "memory/decision_trace_registry",
        "MARKET_INTELLIGENCE": "memory/legacy_corpus/quarantine",
        "ENGINEERING_KNOWLEDGE": "memory/legacy_corpus/quarantine",
        "INFRASTRUCTURE_KNOWLEDGE": "memory/legacy_corpus/quarantine",
        "SECURITY_KNOWLEDGE": "memory/legacy_corpus/quarantine",
        "TRADING_STRATEGY_KNOWLEDGE": "memory/legacy_corpus/quarantine",
    }
    return mapping.get(category, "memory/legacy_corpus/quarantine")


def _detected_type(path: Path) -> str:
    suffix_map = {
        ".md": "markdown_document",
        ".py": "python_source",
        ".json": "json_data",
        ".yaml": "yaml_config",
        ".yml": "yaml_config",
        ".txt": "text_file",
        ".csv": "csv_data",
        ".ps1": "powershell_script",
        ".bat": "batch_script",
        ".sh": "shell_script",
    }
    return suffix_map.get(path.suffix, f"unknown_{path.suffix}")


def audit_legacy(dry_run: bool = True) -> dict:
    if not LEGACY_ROOT.is_dir():
        return {"error": f"Legacy root not found: {LEGACY_ROOT}", "inventory": []}

    inventory = []
    secrets_found = 0
    code_files = 0
    blocked_dirs = 0

    for path in sorted(LEGACY_ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(LEGACY_ROOT)
        parts = path.relative_to(LEGACY_ROOT).parts
        if any(p in BLOCKED_DIRECTORIES for p in parts):
            blocked_dirs += 1
            continue
        if path.suffix in BLOCKED_EXTENSIONS:
            continue

        category = _classify_path(path)
        risk = _risk_level(path, category)
        has_code = _contains_code(path)
        has_secret = _contains_secret(path)
        if has_code:
            code_files += 1
        if has_secret:
            secrets_found += 1

        stat = path.stat()
        item = {
            "source_path": str(path),
            "relative_path": str(rel),
            "file_name": path.name,
            "file_type": _detected_type(path),
            "size": stat.st_size,
            "last_modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
            "hash": _file_hash(path),
            "detected_category": category,
            "risk_classification": risk,
            "contains_code": has_code,
            "contains_secret_pattern": has_secret,
            "migration_recommendation": _migration_status(category, risk, has_code, has_secret),
            "target_ak_registry": _target_registry(category),
            "quarantine_required": risk in ("MEDIUM", "HIGH") or has_code,
            "notes": "",
        }
        inventory.append(item)

    summary = {
        "dry_run": dry_run,
        "legacy_root": str(LEGACY_ROOT),
        "total_files": len(inventory),
        "code_files": code_files,
        "secrets_found": secrets_found,
        "blocked_directories_skipped": blocked_dirs,
        "categories": {},
        "risk_levels": {},
        "migration_statuses": {},
    }

    for item in inventory:
        cat = item["detected_category"]
        summary["categories"][cat] = summary["categories"].get(cat, 0) + 1
        rl = item["risk_classification"]
        summary["risk_levels"][rl] = summary["risk_levels"].get(rl, 0) + 1
        ms = item["migration_recommendation"]
        summary["migration_statuses"][ms] = summary["migration_statuses"].get(ms, 0) + 1

    return {"inventory": inventory, "summary": summary, "dry_run": dry_run}


def write_inventory_csv(inventory: list[dict], path: Path):
    if not inventory:
        return
    fields = list(inventory[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(inventory)


def write_index_yaml(inventory: list[dict], path: Path):
    lines = ["# Legacy Learning Index", f"# Generated: {datetime.now(timezone.utc).isoformat()}", f"# Source: {LEGACY_ROOT}", f"# Total: {len(inventory)} files", "", "files:"]
    for item in inventory:
        mig = item["migration_recommendation"]
        if mig == "DO_NOT_IMPORT":
            continue
        lines.append(f'  - path: "{item["relative_path"]}"')
        lines.append(f'    category: {item["detected_category"]}')
        lines.append(f'    risk: {item["risk_classification"]}')
        lines.append(f'    hash: {item["hash"]}')
        lines.append(f'    target: {item["target_ak_registry"]}')
        lines.append(f'    quarantine: {"true" if item["quarantine_required"] else "false"}')
        lines.append(f'    recommendation: {mig}')
    path.write_text("\n".join(lines) + "\n")


def main():
    import sys

    import_flag = "--import-quarantine" in sys.argv
    dry_run = not import_flag

    print("=" * 60)
    print("AK Legacy Learning Audit")
    print(f"Mode: {'DRY-RUN' if dry_run else 'QUARANTINE IMPORT'}")
    print("=" * 60)

    result = audit_legacy(dry_run=dry_run)
    inv = result["inventory"]
    summary = result["summary"]

    print(f"\nLegacy root: {summary['legacy_root']}")
    print(f"Total files: {summary['total_files']}")
    print(f"Code files: {summary['code_files']}")
    print(f"Secrets found: {summary['secrets_found']}")
    print(f"Blocked dirs skipped: {summary['blocked_directories_skipped']}")

    print("\n--- Categories ---")
    for cat, count in sorted(summary["categories"].items()):
        print(f"  {cat}: {count}")

    print("\n--- Risk Levels ---")
    for rl, count in sorted(summary["risk_levels"].items()):
        print(f"  {rl}: {count}")

    print("\n--- Migration Status ---")
    for ms, count in sorted(summary["migration_statuses"].items()):
        print(f"  {ms}: {count}")

    do_not_import = [i for i in inv if i["migration_recommendation"] == "DO_NOT_IMPORT"]
    if do_not_import:
        print(f"\n--- DO_NOT_IMPORT ({len(do_not_import)} files) ---")
        for item in do_not_import:
            print(f"  {item['relative_path']} [{item['risk_classification']}]")

    if secrets := [i for i in inv if i["contains_secret_pattern"]]:
        print(f"\n*** SECURITY ALERT: {len(secrets)} files contain secret patterns ***")
        for item in secrets:
            print(f"  {item['relative_path']}")

    reports_dir = Path(__file__).resolve().parent.parent / "docs" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    csv_path = reports_dir / "AK_LEGACY_LEARNING_INVENTORY.csv"
    write_inventory_csv(inv, csv_path)
    print(f"\nInventory CSV: {csv_path}")

    # Write index skeleton (always safe as it's just metadata)
    AK_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_index_yaml(inv, AK_INDEX_PATH)
    print(f"Index YAML: {AK_INDEX_PATH}")

    if dry_run:
        print("\nDRY-RUN COMPLETE — no files modified.")
        print("Use --import-quarantine to copy approved files to quarantine.")
        return 0

    # Import mode
    approved = [i for i in inv if i["migration_recommendation"] not in ("DO_NOT_IMPORT", "REQUIRES_HUNG_VUONG_APPROVAL")]
    AK_QUARANTINE.mkdir(parents=True, exist_ok=True)
    imported = 0
    for item in approved:
        src = Path(item["source_path"])
        dst = AK_QUARANTINE / item["relative_path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            dst.write_bytes(src.read_bytes())
            imported += 1
        except Exception as e:
            print(f"  ERROR importing {item['relative_path']}: {e}")

    print(f"\nImported {imported}/{len(approved)} files to quarantine.")
    return 0


if __name__ == "__main__":
    main()
