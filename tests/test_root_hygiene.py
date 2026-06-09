"""Root Hygiene Gate — fail if unauthorized files/folders exist at repository root.

Approved root structure per WP-REPO-HYGIENE-01:
  Directories: agents/, archive/, connectors/, data/, docs/, execution/,
               governance/, learning/, memory/, pipelines/, scripts/,
               services/, sovereign/, tests/, tools/, workflows/
  Files: README.md, pyproject.toml, requirements.txt, pytest.ini, .gitignore,
         AK_PROJECT_CHARTER.md, AK_NO_LEGACY_RUNTIME_POLICY.md, .env.example,
         ak.bat, law.bat, AK_MEMORY.md
  Hidden: .venv/, .pytest_cache/, .git/, .gitignore
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

APPROVED_DIRECTORIES = {
    "agents", "archive", "connectors", "data", "docs", "execution",
    "governance", "learning", "memory", "pipelines", "scripts",
    "services", "sovereign", "tests", "tools", "workflows",
}

APPROVED_FILES = {
    "README.md", "pyproject.toml", "requirements.txt", ".gitignore",
    ".env.example", "ak.bat", "law.bat", "AK_MEMORY.md",
}

HIDDEN_ALLOWED = {
    ".venv", ".pytest_cache", ".git",
}


def _root_items():
    items = set()
    for p in ROOT.iterdir():
        items.add(p.name)
    return items


def test_no_unauthorized_root_directories():
    items = _root_items()
    for name in sorted(items):
        p = ROOT / name
        if p.is_dir() and not name.startswith("."):
            assert name in APPROVED_DIRECTORIES, (
                f"Unauthorized root directory: {name}/"
            )


def test_no_unauthorized_root_files():
    items = _root_items()
    for name in sorted(items):
        p = ROOT / name
        if p.is_file() and not name.startswith("."):
            assert name in APPROVED_FILES, (
                f"Unauthorized root file: {name}"
            )


def test_hidden_directories_are_allowed():
    items = _root_items()
    for name in sorted(items):
        p = ROOT / name
        if name.startswith(".") and p.is_dir():
            assert name in HIDDEN_ALLOWED, (
                f"Unauthorized hidden directory: {name}/"
            )
