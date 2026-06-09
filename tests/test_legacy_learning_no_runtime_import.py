"""Verify legacy audit script does not import code into active AK runtime."""

from pathlib import Path


LEGACY_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "audit_legacy_learning.py"
AK_FORBIDDEN_DIRS = ["agents", "execution", "connectors", "governance", "sovereign"]


def test_audit_script_does_not_write_to_forbidden_dirs():
    source = Path(LEGACY_SCRIPT).read_text(encoding="utf-8")
    for d in AK_FORBIDDEN_DIRS:
        for i, line in enumerate(source.splitlines(), 1):
            stripped = line.strip()
            if d in stripped.lower() and ("write_" in stripped.lower() or "copy" in stripped.lower() or "dst " in stripped.lower() or "target" in stripped.lower()):
                assert False, f"Script writes to forbidden dir '{d}' at line {i}: {stripped}"


def test_audit_script_default_is_dry_run():
    source = LEGACY_SCRIPT.read_text(encoding="utf-8")
    assert "DRY_RUN = True" in source


def test_audit_script_does_not_import_legacy_runtime():
    source = LEGACY_SCRIPT.read_text(encoding="utf-8")
    assert "import legacy" not in source.lower()
    assert "from legacy" not in source.lower()


def test_no_legacy_runtime_reference_in_agents():
    agents_dir = Path(__file__).resolve().parent.parent / "agents"
    for py_file in agents_dir.rglob("*.py"):
        content = py_file.read_text(encoding="utf-8", errors="ignore")
        if "legacy" in content.lower():
            for i, line in enumerate(content.splitlines(), 1):
                if "legacy" in line.lower():
                    assert False, f"{py_file.relative_to(agents_dir)}:{i} references 'legacy': {line.strip()}"
