"""Verify legacy audit script detects secret patterns correctly."""

from pathlib import Path
from scripts.audit_legacy_learning import _contains_secret, SECRET_PATTERNS
import tempfile


def test_detects_openai_api_key():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("OPENAI_API_KEY=sk-proj-1234567890abcdef1234567890abcdef")
        p = Path(f.name)
    try:
        assert _contains_secret(p) is True
    finally:
        p.unlink()


def test_detects_generic_api_key():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("api_key = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6'")
        p = Path(f.name)
    try:
        assert _contains_secret(p) is True
    finally:
        p.unlink()


def test_detects_private_key_header():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("-----BEGIN RSA PRIVATE KEY-----\nABCDEF\n-----END RSA PRIVATE KEY-----")
        p = Path(f.name)
    try:
        assert _contains_secret(p) is True
    finally:
        p.unlink()


def test_clean_file_no_secret():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("# Weekly Report\n\nAll systems operational.")
        p = Path(f.name)
    try:
        assert _contains_secret(p) is False
    finally:
        p.unlink()


def test_audit_script_returns_no_secrets_on_legacy():
    from scripts.audit_legacy_learning import audit_legacy
    result = audit_legacy(dry_run=True)
    secrets = [i for i in result["inventory"] if i["contains_secret_pattern"]]
    assert len(secrets) == 0, f"Found {len(secrets)} secrets in legacy files"


def test_secret_patterns_compiled():
    for p in SECRET_PATTERNS:
        assert hasattr(p, "search")
