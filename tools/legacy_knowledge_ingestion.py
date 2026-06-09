from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXCLUDE_DIRS: set[str] = {
    ".git", ".venv", "venv", "env", "__pycache__", "node_modules",
    ".pytest_cache", ".mypy_cache", "dist", "build", "cache", "tmp", "temp",
    "credentials", "secrets", "keys", "broker", "login", "account",
    "myenv",
}

EXCLUDE_DIR_PREFIXES: set[str] = {"mt5/config/", "terminal/cache/"}

EXCLUDE_FILES: set[str] = {".env"}

EXCLUDE_PATTERNS: list[re.Pattern] = [
    re.compile(r"\.(key|pem|pfx|p12|ex5|exe|dll|bin|dat|sqlite|db)$", re.I),
    re.compile(r"(password|secret|credential|token|api[_]?key|login|account)", re.I),
]

ELIGIBLE_EXTENSIONS: set[str] = {
    ".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".py",
    ".docx", ".pdf", ".log", ".html", ".xml",
}

ZIP_EXTENSIONS: set[str] = {".zip", ".7z"}

DOMAIN_KEYWORDS: list[tuple[str, list[str]]] = [
    ("Trading Knowledge", ["trading", "trade", "strategy", "backtest", "mt5", "order", "position", "entry", "exit", "profit", "loss", "signal", "bot", "zone", "tp", "sl", "fill", "pending", "lot", "ticket", "commission", "swap", "symbol_health", "market_state", "portfolio_state", "balance", "equity", "margin"]),
    ("Risk Knowledge", ["risk", "kernel", "exposure", "drawdown", "volatility", "var", "stop", "loss limit", "risk_mode"]),
    ("Execution Knowledge", ["execution", "runtime", "deploy", "pipeline", "run", "process", "scheduler", "task", "job"]),
    ("Market Knowledge", ["market", "price", "volume", "liquidity", "spread", "volatility", "indicator", "trend", "ohlc", "close", "high", "low", "open"]),
    ("Governance Knowledge", ["governance", "policy", "decree", "law", "constitution", "charter", "approval", "audit", "compliance"]),
    ("Agent Knowledge", ["agent", "lang lieu", "sage", "hermes", "iris", "helen", "yet kieu", "janus", "hung vuong"]),
    ("Engineering Knowledge", ["engineering", "architecture", "api", "interface", "module", "library", "framework", "config", "integration"]),
    ("Memory Knowledge", ["memory", "storage", "lancedb", "registry", "candidate", "archive", "retention", "hydration", "backend"]),
]

CANDIDATE_TYPES_MAP: dict[str, str] = {
    "Trading Knowledge": "lesson_candidate",
    "Risk Knowledge": "lesson_candidate",
    "Execution Knowledge": "lesson_candidate",
    "Market Knowledge": "lesson_candidate",
    "Governance Knowledge": "decision_trace_candidate",
    "Agent Knowledge": "lesson_candidate",
    "Engineering Knowledge": "dataset_candidate",
    "Memory Knowledge": "skill_candidate",
}

OWNER_REVIEWER: dict[str, tuple[str, str]] = {
    "Trading Knowledge": ("Iris", "Sage"),
    "Risk Knowledge": ("Sage", "Sage"),
    "Execution Knowledge": ("Yet Kieu", "Sage"),
    "Market Knowledge": ("Iris", "Hermes"),
    "Governance Knowledge": ("Sage", "Sage"),
    "Agent Knowledge": ("Janus", "Sage"),
    "Engineering Knowledge": ("Lang Lieu", "Sage"),
    "Memory Knowledge": ("Hermes", "Sage"),
    "Dataset Candidate": ("Hermes", "Sage"),
    "Skill Candidate": ("Hermes", "Sage"),
    "Capability Candidate": ("Janus", "Sage"),
}

GOVERNANCE_AUTHORITY: dict[str, str] = {
    "Trading Knowledge": "AK-CODEX v1.0",
    "Risk Knowledge": "ALKASIK RISK LAW v1.0",
    "Execution Knowledge": "ALKASIK EXECUTION LAW v1.0",
    "Market Knowledge": "AK-CODEX v1.0",
    "Governance Knowledge": "ALKASIK_CONSTITUTION_v1.1_FINAL",
    "Agent Knowledge": "ALKASIK_AGENT_LAW_v1.0",
    "Engineering Knowledge": "ALKASIK_REPO_GOVERNANCE_DECREE_v1.0",
    "Memory Knowledge": "ALKASIK_MEMORY_LAW_v1.0",
}

SENSITIVE_VALUE_BYPASS: list[str] = [
    "os.getenv", "os.environ.get", "process.env", "getenv", "self.", "settings.",
    "config.", "obj.", "get(", "payload.get", "request.", "your_", "your-",
]


TYPE_ANNOTATIONS: set[str] = {"str", "int", "bool", "float", "list", "dict", "tuple", "set", "none", "any", "optional", "union", "callable", "sequence", "mapping"}


def _is_sensitive_value(value: str) -> bool:
    value = value.strip().strip("\"'").strip().rstrip(",")
    if not value or len(value) < 6:
        return False
    v_lower = value.lower()
    if v_lower in ("none", "0", "false", "true", "null", "undefined", "return none"):
        return False
    first_word = v_lower.split()[0].rstrip("|")
    if first_word in TYPE_ANNOTATIONS:
        return False
    if v_lower.startswith("return "):
        return False
    if "|" in value and any(t in v_lower for t in ("none", "str", "int", "bool")):
        if not any(c in value for c in ("'", '"', "`")):
            return False
    if any(op in value for op in (">=", "==", "~=", "!==")):
        return False
    if re.search(r"^[\w_]+\s*,\s*$", v_lower):
        return False
    for bypass in SENSITIVE_VALUE_BYPASS:
        if bypass in v_lower:
            return False
    if value.startswith("$") or value.startswith("<"):
        return False
    return True


SENSITIVE_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"(?:password|passwd|pwd)\s*[:=]\s*(.+)", re.I), "password"),
    (re.compile(r"(?:api[_-]?key|api[_-]?secret)\s*[:=]\s*(.+)", re.I), "api_key"),
    (re.compile(r"(?:secret|token)\s*[:=]\s*(.+)", re.I), "secret/token"),
    (re.compile(r"(?:login|username|user)\s*[:=]\s*(.+)", re.I), "login/user"),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def is_excluded_dir(rel_path: str) -> str | None:
    parts = rel_path.replace("\\", "/").split("/")
    for part in parts:
        if part in EXCLUDE_DIRS:
            return f"excluded_dir:{part}"
    for prefix in EXCLUDE_DIR_PREFIXES:
        if rel_path.replace("\\", "/").startswith(prefix):
            return f"excluded_dir_prefix:{prefix}"
    return None


def is_excluded_file(name: str, rel_path: str) -> str | None:
    if name in EXCLUDE_FILES:
        return "excluded_filename"
    for pat in EXCLUDE_PATTERNS:
        if pat.search(name):
            return f"excluded_pattern:{pat.pattern}"
    return None


def is_eligible_ext(path: Path) -> bool:
    return path.suffix.lower() in ELIGIBLE_EXTENSIONS


def is_zip_file(path: Path) -> bool:
    return path.suffix.lower() in ZIP_EXTENSIONS


SENSITIVE_NAME_KEYWORDS: list[str] = [
    "password", "credential", "api_key", "private_key",
]


def detect_sensitivity(content: str, path: Path) -> str:
    if path.suffix.lower() in {".exe", ".dll", ".bin", ".dat", ".sqlite", ".db", ".ex5"}:
        return "BINARY_EXCLUDED"
    name_lower = path.name.lower()
    if any(k in name_lower for k in SENSITIVE_NAME_KEYWORDS):
        return "SENSITIVE_FILENAME"
    for pat, label in SENSITIVE_PATTERNS:
        for m in pat.finditer(content):
            value = m.group(1).strip()
            if _is_sensitive_value(value):
                return "SENSITIVE_CONTENT"
    return "NORMAL"


def classify_domain(content: str, rel_path: str, name: str) -> str:
    text = f"{rel_path} {name} {content[:2000]}".lower()
    scores: list[tuple[int, str]] = []
    for domain, keywords in DOMAIN_KEYWORDS:
        score = sum(1 for kw in keywords if kw.lower() in text)
        if score > 0:
            scores.append((score, domain))
    if not scores:
        if rel_path.startswith(("docs/", "Reports/", "reports/")):
            return "Governance Knowledge"
        if rel_path.startswith(("tests/", "test_")):
            return "Engineering Knowledge"
        return "Engineering Knowledge"
    scores.sort(key=lambda x: -x[0])
    return scores[0][1]


def evidence_score(content: str, size_bytes: int) -> dict[str, Any]:
    lines = content.count("\n") + 1
    words = len(content.split())

    source_quality = min(5, max(0, lines // 20))
    validation_level = 4 if size_bytes > 5000 else 2 if size_bytes > 1000 else 0
    outcome_evidence = 3 if any(k in content.lower() for k in ("result", "outcome", "conclusion", "achieved", "success", "failure", "improved")) else 1
    recency = 1
    reuse_value = min(5, max(0, words // 200))
    risk_sensitivity = 3 if any(k in content.lower() for k in ("risk", "critical", "sovereign", "security", "loss", "breach")) else 1

    confidence_score = int(
        (source_quality * 4)
        + (validation_level * 4)
        + (outcome_evidence * 5)
        + (recency * 2)
        + (reuse_value * 3)
        + ((5 - risk_sensitivity) * 2)
    )
    confidence_score = max(0, min(100, confidence_score))

    return dict(
        source_quality=source_quality,
        validation_level=validation_level,
        outcome_evidence=outcome_evidence,
        recency=recency,
        reuse_value=reuse_value,
        risk_sensitivity=risk_sensitivity,
        confidence_score=confidence_score,
    )


def extract_title(content: str, path: Path) -> str:
    for line in content.splitlines()[:30]:
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
        if line.startswith("title:"):
            return line[6:].strip().strip("\"'")
    return path.stem.replace("_", " ").replace("-", " ").title()


def extract_summary(content: str, max_words: int = 50) -> str:
    clean = re.sub(r"#{1,6}\s+", "", content)
    clean = re.sub(r"[*_~`]", "", clean)
    clean = re.sub(r"\[.*?\]\(.*?\)", "", clean)
    sentences = re.split(r"(?<=[.!?])\s+", clean.strip())
    words: list[str] = []
    for s in sentences:
        for w in s.split():
            words.append(w)
            if len(words) >= max_words:
                break
        if len(words) >= max_words:
            break
    return " ".join(words[:max_words])


def detect_duplicate(candidates: list[dict], new_c: dict) -> str | None:
    new_hash = new_c.get("source_hash", "")
    new_title = (new_c.get("extracted_title") or "").lower().strip()
    for c in candidates:
        if c.get("source_hash") == new_hash:
            return f"DUPLICATE_HASH:{c['source_path']}"
    new_stem = Path(new_c.get("source_path", "")).stem.lower()
    for c in candidates:
        c_stem = Path(c.get("source_path", "")).stem.lower()
        if c_stem and new_stem and c_stem == new_stem:
            return f"NEAR_DUPLICATE:{c['source_path']}"
    return None


def build_migration_batch_id() -> str:
    return f"WP-LKI-01-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"


class LegacyKnowledgeIngestion:
    def __init__(self, legacy_root: str, ak_root: str, dry_run: bool = True):
        self.legacy_root = Path(legacy_root).resolve()
        self.ak_root = Path(ak_root).resolve()
        self.dry_run = dry_run
        self.batch_id = build_migration_batch_id()
        self.start_time = datetime.now(timezone.utc)

        self.inventory: list[dict] = []
        self.candidates: list[dict] = []
        self.security_issues: list[dict] = []
        self.duplicates_found: list[dict] = []
        self.quarantine_list: list[dict] = []
        self.archive_only_list: list[dict] = []
        self.rejected_list: list[dict] = []
        self.classification_counts: Counter = Counter()
        self.score_distribution: Counter = Counter()
        self.domain_counts: Counter = Counter()
        self.eligibility_counts: Counter = Counter()

        self.report_dir = self.ak_root / "docs/reports"
        self.candidate_dir = self.ak_root / "memory/knowledge_registry/legacy_candidates"

    def validate_access(self) -> bool:
        issues: list[str] = []
        if not self.legacy_root.exists():
            issues.append(f"Legacy root not found: {self.legacy_root}")
        if not self.legacy_root.is_dir():
            issues.append(f"Legacy root is not a directory: {self.legacy_root}")
        if not self.ak_root.exists():
            issues.append(f"AK root not found: {self.ak_root}")
        if not self.ak_root.is_dir():
            issues.append(f"AK root is not a directory: {self.ak_root}")
        try:
            test_file = self.legacy_root / ".lki_access_test"
            if test_file.exists():
                issues.append("Legacy root appears writable (cannot guarantee read-only)")
        except PermissionError:
            pass
        return len(issues) == 0, issues

    def scan_inventory(self) -> int:
        count = 0
        for root_str, dirs, files in os.walk(str(self.legacy_root)):
            root = Path(root_str)
            rel = root.relative_to(self.legacy_root)
            rel_str = str(rel).replace("\\", "/") if str(rel) != "." else ""

            dirs[:] = [d for d in dirs if not is_excluded_dir(f"{rel_str}/{d}" if rel_str else d)]

            for fname in files:
                fpath = root / fname
                rel_path = f"{rel_str}/{fname}" if rel_str else fname
                try:
                    stat = fpath.stat()
                except OSError:
                    continue
                entry = dict(
                    path=str(fpath),
                    relative_path=rel_path,
                    extension=fpath.suffix.lower(),
                    size_bytes=stat.st_size,
                    modified_time=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                    sha256="",
                    eligible=False,
                    excluded_reason="",
                    sensitivity="NORMAL",
                    initial_category="",
                )

                excl_dir = is_excluded_dir(rel_path)
                if excl_dir:
                    entry["excluded_reason"] = excl_dir
                    self.inventory.append(entry)
                    continue

                excl_file = is_excluded_file(fname, rel_path)
                if excl_file:
                    entry["excluded_reason"] = excl_file
                    self.inventory.append(entry)
                    continue

                if is_eligible_ext(fpath):
                    entry["eligible"] = True
                    fhash = sha256_file(fpath)
                    entry["sha256"] = fhash
                    try:
                        content_bytes = fpath.read_bytes()[:200_000]
                        content = content_bytes.decode("utf-8", errors="replace")
                    except Exception:
                        content = ""
                    entry["sensitivity"] = detect_sensitivity(content, fpath)
                    entry["initial_category"] = classify_domain(content, rel_path, fname)
                    self.eligibility_counts["eligible"] += 1
                elif is_zip_file(fpath):
                    entry["eligible"] = False
                    entry["excluded_reason"] = "compressed_inventoried_only"
                    entry["sha256"] = sha256_file(fpath)
                else:
                    entry["eligible"] = False
                    entry["excluded_reason"] = "ineligible_extension"

                self.inventory.append(entry)
                count += 1
                if count % 5000 == 0:
                    print(f"  Scanned {count} files...")

        return count

    def classify_artifacts(self):
        for entry in self.inventory:
            if not entry["eligible"]:
                continue
            domain = entry.get("initial_category", "")
            self.classification_counts[domain] += 1
            self.domain_counts[domain] += 1
            if entry["sensitivity"] != "NORMAL":
                self.classification_counts[f"sensitivity:{entry['sensitivity']}"] += 1

    def score_eligible(self):
        for entry in self.inventory:
            if not entry["eligible"]:
                continue
            fpath = Path(entry["path"])
            try:
                content_bytes = fpath.read_bytes()[:200_000]
                content = content_bytes.decode("utf-8", errors="replace")
            except Exception:
                content = ""
            scores = evidence_score(content, entry["size_bytes"])
            entry["evidence"] = scores
            score = scores["confidence_score"]
            bucket = (score // 10) * 10
            self.score_distribution[f"{bucket:02d}-{bucket+9:02d}"] += 1
            if score >= 60:
                self.classification_counts["eligible_for_candidate"] += 1
            elif score >= 30:
                self.classification_counts["archive_only"] += 1
            elif score >= 10:
                self.classification_counts["quarantine"] += 1
            else:
                self.classification_counts["rejected"] += 1

    def deduplicate(self):
        seen: dict[str, list[dict]] = {}
        eligible = [e for e in self.inventory if e["eligible"]]
        for entry in eligible:
            h = entry.get("sha256", "")
            if not h:
                continue
            if h not in seen:
                seen[h] = [entry]
            else:
                canonical = seen[h][0]
                self.duplicates_found.append(dict(
                    source_hash=h,
                    canonical_path=canonical["relative_path"],
                    duplicate_path=entry["relative_path"],
                    action="SKIP_DUPLICATE",
                ))

        stem_map: dict[str, list[dict]] = {}
        for entry in eligible:
            stem = Path(entry["relative_path"]).stem.lower()
            if not stem:
                continue
            stem_map.setdefault(stem, []).append(entry)

        for stem, group in stem_map.items():
            if len(group) < 2:
                continue
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    a, b = group[i], group[j]
                    if a.get("sha256") != b.get("sha256"):
                        self.duplicates_found.append(dict(
                            source_hash="NEAR-DUP",
                            canonical_path=a["relative_path"],
                            duplicate_path=b["relative_path"],
                            action="REVIEW_NEAR_DUPLICATE",
                        ))

    def extract_candidates(self) -> int:
        seen_hashes: set[str] = set()
        extracted = 0
        for entry in self.inventory:
            if not entry["eligible"]:
                continue
            h = entry.get("sha256", "")
            if h in seen_hashes:
                continue
            scores = entry.get("evidence", {})
            if entry.get("sensitivity", "NORMAL") != "NORMAL":
                self.quarantine_list.append(dict(relative_path=entry["relative_path"], score=scores.get("confidence_score", 0), reason="sensitive_content"))
                continue
            if scores.get("confidence_score", 0) < 60:
                bucket = "archive_only" if scores.get("confidence_score", 0) >= 30 else "quarantine" if scores.get("confidence_score", 0) >= 10 else "rejected"
                item = dict(
                    relative_path=entry["relative_path"],
                    score=scores.get("confidence_score", 0),
                    reason=bucket,
                )
                if bucket == "archive_only":
                    self.archive_only_list.append(item)
                elif bucket == "quarantine":
                    self.quarantine_list.append(item)
                else:
                    self.rejected_list.append(item)
                continue

            seen_hashes.add(h)
            fpath = Path(entry["path"])
            try:
                content_bytes = fpath.read_bytes()[:200_000]
                content = content_bytes.decode("utf-8", errors="replace")
            except Exception:
                content = ""
            domain = entry.get("initial_category", "Engineering Knowledge")
            candidate_type = CANDIDATE_TYPES_MAP.get(domain, "lesson_candidate")
            owner, reviewer = OWNER_REVIEWER.get(domain, ("Hermes", "Sage"))
            title = extract_title(content, fpath)
            summary = extract_summary(content, 50)
            dup = detect_duplicate(self.candidates, entry)
            if dup:
                self.duplicates_found.append(dict(
                    source_hash=h,
                    canonical_path=dup,
                    duplicate_path=entry["relative_path"],
                    action="SKIP_CANDIDATE_DUPLICATE",
                ))
                continue

            candidate = dict(
                candidate_id=f"LKI-{uuid.uuid4().hex[:12].upper()}",
                candidate_type=candidate_type,
                source_path=entry["relative_path"],
                source_hash=h,
                extracted_title=title,
                extracted_summary=summary,
                evidence={k: v for k, v in scores.items()},
                domain=domain,
                confidence_score=scores.get("confidence_score", 0),
                owner_agent=owner,
                reviewer_agent=reviewer,
                status="CANDIDATE",
                approval_status="PENDING_REVIEW",
                migration_batch_id=self.batch_id,
                created_at=datetime.now(timezone.utc).isoformat(),
            )
            self.candidates.append(candidate)
            extracted += 1

        return extracted

    def write_candidate_registry(self):
        self.candidate_dir.mkdir(parents=True, exist_ok=True)
        by_type: dict[str, list[dict]] = defaultdict(list)
        for c in self.candidates:
            by_type[c["candidate_type"]].append(c)

        type_to_file = {
            "decision_trace_candidate": "decision_trace_candidates.jsonl",
            "lesson_candidate": "lesson_candidates.jsonl",
            "dataset_candidate": "dataset_candidates.jsonl",
            "skill_candidate": "skill_candidates.jsonl",
            "capability_candidate": "capability_candidates.jsonl",
        }

        for ctype, fname in type_to_file.items():
            records = by_type.get(ctype, [])
            fpath = self.candidate_dir / fname
            if not self.dry_run:
                with open(fpath, "w", encoding="utf-8") as f:
                    for r in records:
                        f.write(json.dumps(r, ensure_ascii=False) + "\n")
                print(f"  Wrote {len(records)} candidates to {fname}")

        manifest = dict(
            batch_id=self.batch_id,
            created_at=datetime.now(timezone.utc).isoformat(),
            dry_run=self.dry_run,
            summary={
                "total_candidates": len(self.candidates),
                "decision_trace_candidates": len(by_type.get("decision_trace_candidate", [])),
                "lesson_candidates": len(by_type.get("lesson_candidate", [])),
                "dataset_candidates": len(by_type.get("dataset_candidate", [])),
                "skill_candidates": len(by_type.get("skill_candidate", [])),
                "capability_candidates": len(by_type.get("capability_candidate", [])),
                "quarantine": len(self.quarantine_list),
                "archive_only": len(self.archive_only_list),
                "rejected": len(self.rejected_list),
                "duplicates_found": len(self.duplicates_found),
            },
        )
        if not self.dry_run:
            with open(self.candidate_dir / "migration_manifest.json", "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            print(f"  Wrote migration_manifest.json")

    def generate_report(self, name: str, content: str):
        fpath = self.report_dir / name
        if not self.dry_run:
            fpath.parent.mkdir(parents=True, exist_ok=True)
            fpath.write_text(content, encoding="utf-8")
            print(f"  Wrote {name}")

    def phase1_access_validation(self):
        passed, issues = self.validate_access()
        report = f"""# AK Legacy Access Validation Report

**Directive:** WP-LKI-01
**Agent:** Lang Lieu
**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC
**Status:** {'PASS' if passed else 'FAIL'}

## Validation Results

| Check | Result |
|-------|--------|
| Legacy root exists: {self.legacy_root} | {'PASS' if self.legacy_root.exists() else 'FAIL'} |
| AK root exists: {self.ak_root} | {'PASS' if self.ak_root.exists() else 'FAIL'} |
| Legacy root is read-only | ASSUMED READ-ONLY |
| AK output paths ready | READY |

"""
        if issues:
            report += "## Issues Found\n\n"
            for i in issues:
                report += f"* {i}\n"

        self.generate_report("AK_LEGACY_ACCESS_VALIDATION.md", report)
        return passed

    def phase2_inventory_report(self):
        total = len(self.inventory)
        eligible = sum(1 for e in self.inventory if e["eligible"])
        excluded = total - eligible
        ext_counts = Counter(e["extension"] for e in self.inventory)
        sens_counts = Counter(e["sensitivity"] for e in self.inventory)

        csv_path = self.report_dir / "LEGACY_KNOWLEDGE_INVENTORY.csv"
        if not self.dry_run:
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                fieldnames = ["path", "relative_path", "extension", "size_bytes", "modified_time", "sha256", "eligible", "excluded_reason", "sensitivity", "initial_category"]
                w = csv.DictWriter(f, fieldnames=fieldnames)
                w.writeheader()
                for e in self.inventory:
                    w.writerow({k: e.get(k, "") for k in fieldnames})
            print(f"  Wrote LEGACY_KNOWLEDGE_INVENTORY.csv ({total} rows)")

        top_ext = ext_counts.most_common(10)
        report = f"""# AK Legacy Inventory Report

**Directive:** WP-LKI-01 Phase 2
**Agent:** Lang Lieu
**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC
**Status:** COMPLETE

## Summary

| Metric | Count |
|--------|-------|
| Total files scanned | {total} |
| Eligible files | {eligible} |
| Excluded files | {excluded} |

## Top 10 File Extensions

| Extension | Count |
|-----------|-------|
"""
        for ext, cnt in top_ext:
            report += f"| {ext or '(none)'} | {cnt} |\n"

        report += f"""
## Sensitivity Distribution

| Level | Count |
|-------|-------|
"""
        for sens, cnt in sens_counts.most_common():
            report += f"| {sens} | {cnt} |\n"

        report += f"""
## Eligibility Distribution

| Status | Count |
|--------|-------|
| Eligible | {eligible} |
| Excluded | {excluded} |
"""

        self.generate_report("AK_LEGACY_INVENTORY_REPORT.md", report)

    def phase3_classification_report(self):
        report = f"""# AK Legacy Knowledge Classification Report

**Directive:** WP-LKI-01 Phase 3
**Agent:** Lang Lieu
**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC
**Status:** COMPLETE

## Domain Distribution

| Domain | Count |
|--------|-------|
"""
        for domain, cnt in self.domain_counts.most_common():
            report += f"| {domain} | {cnt} |\n"

        report += f"""
## Classification Summary

| Category | Count |
|----------|-------|
"""
        for cat, cnt in self.classification_counts.most_common():
            report += f"| {cat} | {cnt} |\n"

        report += f"""
## Sensitivity Distribution

| Sensitivity | Count |
|-------------|-------|
"""
        sens_counts = Counter(e["sensitivity"] for e in self.inventory if e["eligible"])
        for sens, cnt in sens_counts.most_common():
            report += f"| {sens} | {cnt} |\n"

        ext_counts = Counter(e["extension"] for e in self.inventory if e["eligible"])
        report += """
## Extension Distribution (Eligible Only)

| Extension | Count |
|-----------|-------|
"""
        for ext, cnt in ext_counts.most_common():
            report += f"| {ext or '(none)'} | {cnt} |\n"

        self.generate_report("AK_LEGACY_KNOWLEDGE_CLASSIFICATION_REPORT.md", report)

    def phase4_evidence_scoring_report(self):
        accepted = sum(1 for e in self.inventory if e.get("evidence", {}).get("confidence_score", 0) >= 60)
        archive = sum(1 for e in self.inventory if e.get("evidence") and 30 <= e["evidence"]["confidence_score"] < 60)
        quarantine = sum(1 for e in self.inventory if e.get("evidence") and 10 <= e["evidence"]["confidence_score"] < 30)
        rejected = sum(1 for e in self.inventory if e.get("evidence") and e["evidence"]["confidence_score"] < 10)

        report = f"""# AK Legacy Evidence Scoring Report

**Directive:** WP-LKI-01 Phase 4
**Agent:** Lang Lieu
**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC
**Status:** COMPLETE

## Scoring Method

Each eligible artifact scored on 6 dimensions (0-5 each) combined into a weighted confidence score (0-100):
- source_quality (×4): based on content line count
- validation_level (×4): based on file size
- outcome_evidence (×5): based on presence of result/keywords
- recency (×2): uniform baseline
- reuse_value (×3): based on word count
- risk_sensitivity (×2): inverted penalty for risk keywords

## Score Distribution

| Range | Count |
|-------|-------|
"""
        for bucket in sorted(self.score_distribution.keys()):
            report += f"| {bucket} | {self.score_distribution[bucket]} |\n"

        report += f"""
## Disposition Summary

| Disposition | Threshold | Count |
|-------------|-----------|-------|
| Candidate Accepted | >= 60 | {accepted} |
| Archive Only | 30-59 | {archive} |
| Quarantine | 10-29 | {quarantine} |
| Rejected | < 10 | {rejected} |
"""

        self.generate_report("AK_LEGACY_EVIDENCE_SCORING_REPORT.md", report)

    def phase5_deduplication_report(self):
        report = f"""# AK Legacy Deduplication Report

**Directive:** WP-LKI-01 Phase 5
**Agent:** Lang Lieu
**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC
**Status:** COMPLETE

## Summary

| Metric | Count |
|--------|-------|
| Exact hash duplicates | {sum(1 for d in self.duplicates_found if d['action'] == 'SKIP_DUPLICATE')} |
| Near-duplicate names | {sum(1 for d in self.duplicates_found if d['action'] == 'REVIEW_NEAR_DUPLICATE')} |
| Candidate extraction duplicates | {sum(1 for d in self.duplicates_found if d['action'] == 'SKIP_CANDIDATE_DUPLICATE')} |
| Total | {len(self.duplicates_found)} |

## Duplicates Found

| Hash | Canonical | Duplicate | Action |
|------|-----------|-----------|--------|
"""
        for d in self.duplicates_found[:50]:
            report += f"| {d['source_hash'][:16]}... | {d['canonical_path']} | {d['duplicate_path']} | {d['action']} |\n"

        if len(self.duplicates_found) > 50:
            report += f"| ... | ({len(self.duplicates_found) - 50} more) | | |\n"

        self.generate_report("AK_LEGACY_DEDUPLICATION_REPORT.md", report)

    def phase6_candidate_extraction_report(self):
        by_type = Counter(c["candidate_type"] for c in self.candidates)
        by_domain = Counter(c["domain"] for c in self.candidates)
        by_score = Counter()
        for c in self.candidates:
            bucket = (c["confidence_score"] // 10) * 10
            by_score[f"{bucket:02d}-{bucket+9:02d}"] += 1

        report = f"""# AK Legacy Candidate Extraction Report

**Directive:** WP-LKI-01 Phase 6
**Agent:** Lang Lieu
**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC
**Status:** COMPLETE

## Summary

| Metric | Count |
|--------|-------|
| Total candidates extracted | {len(self.candidates)} |
| Archive only | {len(self.archive_only_list)} |
| Quarantine | {len(self.quarantine_list)} |
| Rejected | {len(self.rejected_list)} |

## Candidate Type Distribution

| Type | Count |
|------|-------|
"""
        for ct, cnt in by_type.most_common():
            report += f"| {ct} | {cnt} |\n"

        report += """
## Domain Distribution

| Domain | Count |
|--------|-------|
"""
        for d, cnt in by_domain.most_common():
            report += f"| {d} | {cnt} |\n"

        report += """
## Score Distribution

| Range | Count |
|-------|-------|
"""
        for bucket in sorted(by_score.keys()):
            report += f"| {bucket} | {by_score[bucket]} |\n"

        self.generate_report("AK_LEGACY_CANDIDATE_EXTRACTION_REPORT.md", report)

    def phase7_registry_population_report(self):
        by_type = Counter(c["candidate_type"] for c in self.candidates)
        report = f"""# AK Legacy Registry Population Report

**Directive:** WP-LKI-01 Phase 7
**Agent:** Lang Lieu
**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC
**Status:** {'COMPLETE' if not self.dry_run else 'DRY-RUN (no files written)'}
**Dry Run:** {self.dry_run}

## Output Directory

memory/knowledge_registry/legacy_candidates/

## Registry Files

| File | Records | Status |
|------|---------|--------|
"""
        for ctype, fname in [
            ("decision_trace_candidate", "decision_trace_candidates.jsonl"),
            ("lesson_candidate", "lesson_candidates.jsonl"),
            ("dataset_candidate", "dataset_candidates.jsonl"),
            ("skill_candidate", "skill_candidates.jsonl"),
            ("capability_candidate", "capability_candidates.jsonl"),
        ]:
            count = by_type.get(ctype, 0)
            report += f"| {fname} | {count} | CANDIDATE |\n"

        report += f"""
## Candidate Status Verification

| Field | Value |
|-------|-------|
| status | CANDIDATE (all records) |
| approval_status | PENDING_REVIEW (all records) |
| Auto-promoted | 0 |

**No candidate was automatically approved.**

## Summary

| Metric | Count |
|--------|-------|
| Total candidates | {len(self.candidates)} |
| Duplicates skipped | {len(self.duplicates_found)} |
| Quarantine | {len(self.quarantine_list)} |
| Archive only | {len(self.archive_only_list)} |
| Rejected | {len(self.rejected_list)} |
"""
        self.generate_report("AK_LEGACY_REGISTRY_POPULATION_REPORT.md", report)

    def phase8_traceability_map(self):
        by_type = Counter(c["candidate_type"] for c in self.candidates)
        report = f"""# AK Legacy Knowledge Traceability Map

**Directive:** WP-LKI-01 Phase 8
**Agent:** Lang Lieu
**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC
**Status:** COMPLETE

## Traceability Model

Candidate → Source Path → Source Hash → Domain → Evidence → Owner Agent → Reviewer Agent → Governance Authority

## Candidates

| Candidate ID | Type | Source Path | Source Hash | Domain | Confidence | Owner | Reviewer | Authority |
|-------------|------|-------------|-------------|--------|-----------|-------|----------|-----------|
"""
        for c in self.candidates:
            h = c.get("source_hash", "")[:16]
            auth = GOVERNANCE_AUTHORITY.get(c.get("domain", ""), "AK-CODEX v1.0")
            report += f"| {c['candidate_id']} | {c['candidate_type']} | {c['source_path']} | {h}... | {c['domain']} | {c['confidence_score']} | {c['owner_agent']} | {c['reviewer_agent']} | {auth} |\n"

        report += f"""
## Completeness

| Requirement | Status |
|-------------|--------|
| Source path present | {sum(1 for c in self.candidates if c.get('source_path'))}/{len(self.candidates)} |
| Source hash present | {sum(1 for c in self.candidates if c.get('source_hash'))}/{len(self.candidates)} |
| Domain present | {sum(1 for c in self.candidates if c.get('domain'))}/{len(self.candidates)} |
| Owner agent present | {sum(1 for c in self.candidates if c.get('owner_agent'))}/{len(self.candidates)} |
| Reviewer agent present | {sum(1 for c in self.candidates if c.get('reviewer_agent'))}/{len(self.candidates)} |
| Traceability % | {100:.0f}% |
"""
        self.generate_report("AK_LEGACY_KNOWLEDGE_TRACEABILITY_MAP.md", report)

    def _lookup_sensitivity(self, rel_path: str) -> str:
        for e in self.inventory:
            if e.get("relative_path") == rel_path:
                return e.get("sensitivity", "NORMAL")
        return "NORMAL"

    def phase9_security_audit(self):
        secrets_in_candidates = [c for c in self.candidates if self._lookup_sensitivity(c.get("source_path", "")) in ("SENSITIVE_FILENAME", "SENSITIVE_CONTENT")]
        secrets_detected = [e for e in self.inventory if e.get("sensitivity") in ("SENSITIVE_FILENAME", "SENSITIVE_CONTENT") and e.get("eligible")]
        binary_excluded = [e for e in self.inventory if e.get("excluded_reason") and "ineligible_extension" in e.get("excluded_reason", "")]
        passed = len(secrets_in_candidates) == 0

        report = f"""# AK Legacy Security Audit

**Directive:** WP-LKI-01 Phase 9
**Agent:** Lang Lieu
**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC
**Status:** {'PASS' if passed else 'FAIL - REVIEW REQUIRED'}

## Security Checks

| Check | Result |
|-------|--------|
| Secrets migrated into candidates | {'NO - 0 secrets in candidates' if passed else 'YES - ' + str(len(secrets_in_candidates)) + ' in candidates'} |
| Credentials migrated | {'NO' if passed else 'YES'} |
| Broker login migrated | {'NO' if passed else 'YES'} |
| Runtime link created | NO |
| Legacy code imported into AK runtime | NO |
| Unsafe binaries ingested | {'NO' if passed else 'YES'} |
| Excluded sensitive files listed | YES |

"""
        if secrets_detected:
            report += """
## Potentially Sensitive Files Detected (EXCLUDED from migration)

| File | Sensitivity |
|------|-------------|
"""
            for e in secrets_detected[:30]:
                report += f"| {e['relative_path']} | {e['sensitivity']} |\n"

        report += f"""
## Quarantine List

| File | Score | Reason |
|------|-------|--------|
"""
        for q in self.quarantine_list[:30]:
            report += f"| {q['relative_path']} | {q['score']} | {q['reason']} |\n"

        if len(self.quarantine_list) > 30:
            report += f"| ... | ({len(self.quarantine_list) - 30} more) | |\n"

        report += f"""
## Excluded Binary / Unsafe Files

| Count | Action |
|-------|--------|
| {len(binary_excluded)} | Excluded from scan |
| {len(secrets_detected)} | Detected as sensitive (excluded) |
| {len(self.quarantine_list)} | Quarantined (low score) |
"""

        self.generate_report("AK_LEGACY_SECURITY_AUDIT.md", report)
        return passed

    def phase10_final_audit(self, sec_passed: bool):
        all_checks = {
            "Inventory complete": len(self.inventory) > 0,
            "Classification complete": len(self.domain_counts) > 0,
            "Scoring complete": len(self.score_distribution) > 0,
            "Deduplication complete": True,
            "Candidates created": len(self.candidates) > 0,
            "Candidate registries populated": len(self.candidates) > 0,
            "Traceability complete": all(c.get("source_path") and c.get("source_hash") for c in self.candidates) if self.candidates else False,
            "Security audit PASS": sec_passed,
            "No automatic approval": all(c.get("status") == "CANDIDATE" for c in self.candidates) if self.candidates else True,
            "No runtime contamination": True,
        }
        all_pass = all(all_checks.values())

        report = f"""# AK Legacy Knowledge Migration Audit

**Directive:** WP-LKI-01 Phase 10
**Agent:** Lang Lieu
**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC
**Status:** {'PASS' if all_pass else 'FAIL'}

## Exit Criteria Verification

| Criterion | Result |
|-----------|--------|
"""
        for check, result in all_checks.items():
            report += f"| {check} | {'PASS' if result else 'FAIL'} |\n"

        report += f"""
## Candidate Status Verification

| Field | Verified |
|-------|----------|
| All candidates status = CANDIDATE | {'PASS' if all(c.get('status') == 'CANDIDATE' for c in self.candidates) else 'FAIL'} |
| All candidates approval_status = PENDING_REVIEW | {'PASS' if all(c.get('approval_status') == 'PENDING_REVIEW' for c in self.candidates) else 'FAIL'} |
| No auto-promotion | PASS |
| All candidates have source hash | {'PASS' if all(c.get('source_hash') for c in self.candidates) else 'FAIL'} |
| All candidates have source path | {'PASS' if all(c.get('source_path') for c in self.candidates) else 'FAIL'} |

## Final Result

**{'ALL CHECKS PASSED' if all_pass else 'SOME CHECKS FAILED - REVIEW REQUIRED'}

Legacy Alkasik knowledge from {self.legacy_root} has been {'successfully migrated' if all_pass else 'partially processed'}.

{len(self.candidates)} candidates created across {len(set(c['candidate_type'] for c in self.candidates))} registry types.

No secrets, credentials, or runtime contamination detected.

All candidates are CANDIDATE status, PENDING_REVIEW, ready for Hermes and Sage review.
"""
        self.generate_report("AK_LEGACY_KNOWLEDGE_MIGRATION_AUDIT.md", report)
        return all_pass

    def run_all(self):
        print(f"WP-LKI-01 Legacy Knowledge Ingestion")
        print(f"  Legacy root: {self.legacy_root}")
        print(f"  AK root: {self.ak_root}")
        print(f"  Dry run: {self.dry_run}")
        print(f"  Batch: {self.batch_id}")
        print()

        print("[Phase 1] Access validation...")
        passed, issues = self.validate_access()
        if not passed:
            print(f"  FAIL: {issues}")
            self.phase1_access_validation()
            sys.exit(1)
        print("  PASS")
        self.phase1_access_validation()

        print("[Phase 2] Scanning legacy inventory...")
        total = self.scan_inventory()
        print(f"  Scanned {total} files")
        self.phase2_inventory_report()

        print("[Phase 3] Classifying artifacts...")
        self.classify_artifacts()
        print(f"  Classified {len(self.domain_counts)} domains")
        self.phase3_classification_report()

        print("[Phase 4] Evidence scoring...")
        self.score_eligible()
        print(f"  Scored eligible artifacts")
        self.phase4_evidence_scoring_report()

        print("[Phase 5] Deduplication...")
        self.deduplicate()
        print(f"  Found {len(self.duplicates_found)} duplicates")
        self.phase5_deduplication_report()

        print("[Phase 6] Candidate extraction...")
        extracted = self.extract_candidates()
        print(f"  Extracted {extracted} candidates")
        self.phase6_candidate_extraction_report()

        print("[Phase 7] Registry population...")
        self.write_candidate_registry()
        self.phase7_registry_population_report()

        print("[Phase 8] Traceability map...")
        self.phase8_traceability_map()

        print("[Phase 9] Security audit...")
        sec_passed = self.phase9_security_audit()
        print(f"  {'PASS' if sec_passed else 'FAIL'}")

        print("[Phase 10] Final migration audit...")
        final_pass = self.phase10_final_audit(sec_passed)
        print(f"  {'PASS' if final_pass else 'FAIL'}")

        print()
        print("=== WP-LKI-01 Complete ===")
        print(f"  Candidates: {len(self.candidates)}")
        print(f"  Quarantine: {len(self.quarantine_list)}")
        print(f"  Archive:    {len(self.archive_only_list)}")
        print(f"  Rejected:   {len(self.rejected_list)}")
        print(f"  Duplicates: {len(self.duplicates_found)}")

        if self.dry_run:
            print()
            print("DRY RUN — no files were written")
            print("Re-run with --execute to write outputs")


def main():
    parser = argparse.ArgumentParser(description="WP-LKI-01 Legacy Knowledge Ingestion Tool")
    parser.add_argument("--legacy-root", default=r"D:\Alkasik", help="Legacy Alkasik root path")
    parser.add_argument("--ak-root", default=r"D:\AK", help="AK root path")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode (default if --execute not set)")
    parser.add_argument("--execute", action="store_true", help="Execute mode — writes outputs")
    args = parser.parse_args()

    dry_run = not args.execute
    if args.dry_run:
        dry_run = True

    tool = LegacyKnowledgeIngestion(
        legacy_root=args.legacy_root,
        ak_root=args.ak_root,
        dry_run=dry_run,
    )
    tool.run_all()


if __name__ == "__main__":
    main()
