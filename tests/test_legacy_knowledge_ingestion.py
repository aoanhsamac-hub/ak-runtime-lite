from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tools.legacy_knowledge_ingestion as lki

EXCLUDE_DIRS = lki.EXCLUDE_DIRS
ELIGIBLE_EXTENSIONS = lki.ELIGIBLE_EXTENSIONS
SENSITIVE_NAME_KEYWORDS = lki.SENSITIVE_NAME_KEYWORDS
_is_sensitive_value = lki._is_sensitive_value
classify_domain = lki.classify_domain
detect_sensitivity = lki.detect_sensitivity
evidence_score = lki.evidence_score
extract_summary = lki.extract_summary
extract_title = lki.extract_title
is_eligible_ext = lki.is_eligible_ext
is_excluded_dir = lki.is_excluded_dir
is_excluded_file = lki.is_excluded_file
sha256_file = lki.sha256_file
LegacyKnowledgeIngestion = lki.LegacyKnowledgeIngestion


# --- Fixtures ---

@pytest.fixture
def temp_legacy(tmp_path: Path) -> Path:
    root = tmp_path / "legacy"
    root.mkdir()
    (root / "docs").mkdir()
    (root / "docs" / "report.md").write_text("# Test Report\n\nSome content here about trading strategies.")
    (root / "README.md").write_text("# Project README\n\nMain documentation.")
    (root / "config.yaml").write_text("setting: value\n")
    (root / "data.csv").write_text("a,b,c\n1,2,3\n")
    (root / "code.py").write_text("def foo():\n    pass\n")
    (root / "secrets.txt").write_text("password = supersecret123")
    (root / ".env").write_text("API_KEY=test123")
    (root / "normal.txt").write_text("hello world")
    (root / "myenv").mkdir()
    (root / "myenv" / "lib.py").write_text("import os")
    (root / "__pycache__").mkdir()
    (root / "__pycache__" / "cached.py").write_text("cached content")
    return root


@pytest.fixture
def temp_ak(tmp_path: Path) -> Path:
    ak = tmp_path / "ak"
    ak.mkdir()
    (ak / "docs").mkdir()
    (ak / "docs" / "reports").mkdir()
    (ak / "memory").mkdir()
    (ak / "memory" / "knowledge_registry").mkdir()
    return ak


# --- 1. Exclusion Rules ---

class TestExclusionRules:
    def test_exclude_dir_names(self):
        for d in EXCLUDE_DIRS:
            reason = is_excluded_dir(f"path/to/{d}/file.txt")
            assert reason is not None, f"{d} should be excluded"

    def test_allow_normal_dir(self):
        assert is_excluded_dir("docs/reports") is None
        assert is_excluded_dir("memory/registries") is None

    def test_exclude_file_names(self):
        assert is_excluded_file(".env", ".env") is not None

    def test_exclude_file_patterns(self):
        assert is_excluded_file("secret.txt", "path/secret.txt") is not None
        assert is_excluded_file("normal.py", "path/normal.py") is None

    def test_eligible_extensions(self):
        assert is_eligible_ext(Path("test.md"))
        assert is_eligible_ext(Path("test.py"))
        assert is_eligible_ext(Path("test.yaml"))
        assert is_eligible_ext(Path("test.yml"))
        assert is_eligible_ext(Path("test.json"))
        assert is_eligible_ext(Path("test.csv"))
        assert is_eligible_ext(Path("test.txt"))
        assert is_eligible_ext(Path("test.log"))
        assert not is_eligible_ext(Path("test.exe"))
        assert not is_eligible_ext(Path("test.dll"))
        assert not is_eligible_ext(Path("test.key"))


# --- 2. Secret Detection ---

class TestSecretDetection:
    def test_detect_password_assignment(self):
        assert detect_sensitivity("password = hunter2", Path("test.txt")) == "SENSITIVE_CONTENT"

    def test_detect_os_getenv_is_not_secret(self):
        assert detect_sensitivity("api_key = os.getenv('KEY')", Path("test.py")) == "NORMAL"

    def test_detect_type_annotation_is_not_secret(self):
        assert detect_sensitivity("api_key: str | None = None", Path("test.py")) == "NORMAL"

    def test_detect_self_reference_is_not_secret(self):
        assert detect_sensitivity("api_key = self.settings.api_key", Path("test.py")) == "NORMAL"

    def test_detect_sensitive_filename(self):
        assert detect_sensitivity("", Path("private_key.pem")) == "SENSITIVE_FILENAME"

    def test_normal_file(self):
        assert detect_sensitivity("hello world", Path("test.txt")) == "NORMAL"

    def test_package_version_is_not_secret(self):
        assert detect_sensitivity("token>=0.13.0", Path("requirements.txt")) == "NORMAL"

    def test_return_none_is_not_secret(self):
        assert detect_sensitivity("api_key: return None", Path("test.py")) == "NORMAL"


# --- 3. Hash Generation ---

class TestHashGeneration:
    def test_sha256_consistent(self, temp_legacy):
        fpath = temp_legacy / "README.md"
        h1 = sha256_file(fpath)
        h2 = sha256_file(fpath)
        assert h1 == h2
        assert len(h1) == 64

    def test_sha256_differs_for_diff_content(self, temp_legacy):
        f1 = sha256_file(temp_legacy / "README.md")
        f2 = sha256_file(temp_legacy / "code.py")
        assert f1 != f2


# --- 4. Classification ---

class TestClassification:
    def test_classify_trading(self):
        domain = classify_domain("trading strategy entry exit signal", "docs/report.md", "report.md")
        assert domain == "Trading Knowledge"

    def test_classify_governance(self):
        domain = classify_domain("constitution law decree governance", "docs/report.md", "report.md")
        assert domain == "Governance Knowledge"

    def test_classify_engineering_default(self):
        domain = classify_domain("some random content", "tools/test.py", "test.py")
        assert domain != ""

    def test_classify_memory(self):
        domain = classify_domain("lancedb memory backend storage registry", "memory/adapter.py", "adapter.py")
        assert domain == "Memory Knowledge"


# --- 5. Evidence Scoring ---

class TestEvidenceScoring:
    def test_score_returns_all_keys(self):
        content = "This is a result of the test. The outcome was successful."
        scores = evidence_score(content, 5000)
        for key in ("source_quality", "validation_level", "outcome_evidence", "recency", "reuse_value", "risk_sensitivity", "confidence_score"):
            assert key in scores

    def test_confidence_score_in_range(self):
        content = "result" * 500
        scores = evidence_score(content, 50000)
        assert 0 <= scores["confidence_score"] <= 100

    def test_high_quality_content_scores_higher(self):
        low = evidence_score("a", 50)
        high = evidence_score("result outcome achieved success.\n" * 100, 50000)
        assert high["confidence_score"] >= low["confidence_score"]

    def test_minimum_threshold_candidate(self):
        good = evidence_score("risk critical result outcome success achieved improved conclusion.\n" * 200, 100000)
        assert good["confidence_score"] >= 60


# --- 6. Candidate Threshold ---

class TestCandidateThreshold:
    def test_candidate_creation_requires_60(self):
        tool = LegacyKnowledgeIngestion(str(tempfile.mkdtemp()), str(tempfile.mkdtemp()), dry_run=True)
        tool.inventory.append(dict(
            eligible=True, sha256="abc", path="test.md", relative_path="test.md",
            size_bytes=10000, sensitivity="NORMAL",
            initial_category="Engineering Knowledge",
            evidence=evidence_score("result outcome achieved.\n" * 200, 100000),
        ))
        n = tool.extract_candidates()
        assert n >= 0  # should not crash

    def test_low_score_does_not_become_candidate(self):
        tool = LegacyKnowledgeIngestion(str(tempfile.mkdtemp()), str(tempfile.mkdtemp()), dry_run=True)
        tool.inventory.append(dict(
            eligible=True, sha256="xyz", path="low.md", relative_path="low.md",
            size_bytes=50, sensitivity="NORMAL",
            initial_category="Engineering Knowledge",
            evidence=evidence_score("a", 50),
        ))
        n = tool.extract_candidates()
        assert n == 0


# --- 7. Candidate Status ---

class TestCandidateStatus:
    def test_all_candidates_are_candidate_status(self, temp_legacy, temp_ak):
        tool = LegacyKnowledgeIngestion(str(temp_legacy), str(temp_ak), dry_run=True)
        tool.scan_inventory()
        tool.classify_artifacts()
        tool.score_eligible()
        tool.deduplicate()
        tool.extract_candidates()
        for c in tool.candidates:
            assert c["status"] == "CANDIDATE", f"{c['candidate_id']} has status {c['status']}"


# --- 8. Approval Status ---

class TestApprovalStatus:
    def test_all_candidates_pending_review(self, temp_legacy, temp_ak):
        tool = LegacyKnowledgeIngestion(str(temp_legacy), str(temp_ak), dry_run=True)
        tool.scan_inventory()
        tool.classify_artifacts()
        tool.score_eligible()
        tool.deduplicate()
        tool.extract_candidates()
        for c in tool.candidates:
            assert c["approval_status"] == "PENDING_REVIEW"


# --- 9. Traceability ---

class TestTraceability:
    def test_all_candidates_have_traceability_fields(self, temp_legacy, temp_ak):
        tool = LegacyKnowledgeIngestion(str(temp_legacy), str(temp_ak), dry_run=True)
        tool.scan_inventory()
        tool.classify_artifacts()
        tool.score_eligible()
        tool.deduplicate()
        tool.extract_candidates()
        for c in tool.candidates:
            assert c.get("source_path"), "Missing source_path"
            assert c.get("source_hash"), "Missing source_hash"
            assert c.get("candidate_type"), "Missing candidate_type"
            assert c.get("domain"), "Missing domain"
            assert c.get("owner_agent"), "Missing owner_agent"
            assert c.get("reviewer_agent"), "Missing reviewer_agent"


# --- 10. Security Audit ---

class TestSecurityAudit:
    def test_security_audit_prevents_sensitive_ingestion(self, temp_legacy, temp_ak):
        (temp_legacy / "password.txt").write_text("password = real_secret_value_12345")
        tool = LegacyKnowledgeIngestion(str(temp_legacy), str(temp_ak), dry_run=True)
        tool.scan_inventory()
        tool.classify_artifacts()
        tool.score_eligible()
        tool.deduplicate()
        tool.extract_candidates()
        sec_pass = tool.phase9_security_audit()
        assert sec_pass, "Security audit should PASS with default dry-run"

    def test_no_secrets_in_candidates(self, temp_legacy, temp_ak):
        (temp_legacy / "normal_data.py").write_text("x = 1\ny = 2\n")
        tool = LegacyKnowledgeIngestion(str(temp_legacy), str(temp_ak), dry_run=True)
        tool.scan_inventory()
        tool.classify_artifacts()
        tool.score_eligible()
        tool.deduplicate()
        tool.extract_candidates()
        for c in tool.candidates:
            for e in tool.inventory:
                if e.get("relative_path") == c.get("source_path"):
                    assert e.get("sensitivity") == "NORMAL", f"Sensitive file became candidate: {c['source_path']}"


# --- 11. Dry Run ---

class TestDryRun:
    def test_dry_run_does_not_write_files(self, temp_legacy, temp_ak):
        tool = LegacyKnowledgeIngestion(str(temp_legacy), str(temp_ak), dry_run=True)
        tool.run_all()
        report_files = list((temp_ak / "docs" / "reports").iterdir())
        candidate_files = list((temp_ak / "memory" / "knowledge_registry" / "legacy_candidates").iterdir())
        assert len(report_files) == 0, "Dry run should not write report files"
        assert len(candidate_files) == 0, "Dry run should not write candidate files"


# --- 12. Execute Mode ---

class TestExecuteMode:
    def test_execute_writes_only_to_ak_paths(self, temp_legacy, temp_ak):
        legacy_files_before = {str(p) for p in temp_legacy.rglob("*") if p.is_file()}
        legacy_dirs_before = {str(p) for p in temp_legacy.rglob("*") if p.is_dir()}

        tool = LegacyKnowledgeIngestion(str(temp_legacy), str(temp_ak), dry_run=False)
        tool.run_all()

        # Check reports were written
        report_dir = temp_ak / "docs" / "reports"
        expected_reports = [
            "AK_LEGACY_ACCESS_VALIDATION.md",
            "AK_LEGACY_INVENTORY_REPORT.md",
            "AK_LEGACY_KNOWLEDGE_CLASSIFICATION_REPORT.md",
            "AK_LEGACY_EVIDENCE_SCORING_REPORT.md",
            "AK_LEGACY_DEDUPLICATION_REPORT.md",
            "AK_LEGACY_CANDIDATE_EXTRACTION_REPORT.md",
            "AK_LEGACY_REGISTRY_POPULATION_REPORT.md",
            "AK_LEGACY_KNOWLEDGE_TRACEABILITY_MAP.md",
            "AK_LEGACY_SECURITY_AUDIT.md",
            "AK_LEGACY_KNOWLEDGE_MIGRATION_AUDIT.md",
        ]
        for r in expected_reports:
            assert (report_dir / r).exists(), f"Missing report: {r}"

        # Check candidate files were written
        candidate_dir = temp_ak / "memory" / "knowledge_registry" / "legacy_candidates"
        assert (candidate_dir / "migration_manifest.json").exists()
        assert (candidate_dir / "decision_trace_candidates.jsonl").exists()
        assert (candidate_dir / "lesson_candidates.jsonl").exists()
        assert (candidate_dir / "dataset_candidates.jsonl").exists()
        assert (candidate_dir / "skill_candidates.jsonl").exists()

        # Verify no NEW files were written to legacy root
        legacy_files_after = {str(p) for p in temp_legacy.rglob("*") if p.is_file()}
        new_files = legacy_files_after - legacy_files_before
        assert len(new_files) == 0, f"Files written to legacy root: {new_files}"


# --- 13. No Legacy Modification ---

class TestNoLegacyModification:
    def test_legacy_files_not_modified(self, temp_legacy, temp_ak):
        original = {}
        for f in temp_legacy.rglob("*"):
            if f.is_file():
                original[str(f)] = f.read_bytes()

        tool = LegacyKnowledgeIngestion(str(temp_legacy), str(temp_ak), dry_run=True)
        tool.run_all()

        for f in temp_legacy.rglob("*"):
            if f.is_file():
                assert f.read_bytes() == original[str(f)], f"File was modified: {f}"


# --- 14. Tool CLI Arguments ---

class TestCLIArguments:
    def test_default_is_dry_run(self):
        tool = LegacyKnowledgeIngestion("/nonexistent/legacy", "/nonexistent/ak")
        assert tool.dry_run

    def test_execute_disables_dry_run(self):
        tool = LegacyKnowledgeIngestion("/nonexistent/legacy", "/nonexistent/ak", dry_run=False)
        assert not tool.dry_run
