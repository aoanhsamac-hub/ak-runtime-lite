from pathlib import Path

from workflows.wp3_acceptance import run_acceptance


def test_wp3_acceptance_scores_above_95_and_keeps_review_items_visible():
    result = run_acceptance(Path(__file__).resolve().parents[1], run_lancedb_smoke=False)

    assert result["score"] >= 0.95
    assert result["status"] == "PASS"
    assert result["checks"]["required_files"]["passed"] is True
    assert result["checks"]["banned_memory_backends"]["passed"] is True
    assert result["checks"]["runtime_dependencies"]["passed"] is True
    assert result["checks"]["opencode_safety"]["passed"] is True
    assert result["checks"]["runtime_smoke"]["passed"] is True
    assert result["review_items"]


def test_wp3_acceptance_detects_missing_required_file(tmp_path):
    root = tmp_path
    (root / "memory").mkdir()
    result = run_acceptance(root, run_lancedb_smoke=False)

    assert result["status"] == "FAIL"
    assert result["checks"]["required_files"]["passed"] is False
    assert result["score"] < 0.95
