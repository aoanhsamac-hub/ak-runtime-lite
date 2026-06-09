from memory.lancedb_adapter import LanceDBAdapter
from memory.kingdom_memory_platform import KingdomMemoryPlatform, RETENTION_CLASSES

from tests.test_lancedb_adapter import FakeBackend


def _mp():
    return KingdomMemoryPlatform(db_path=":memory:", adapter=LanceDBAdapter(":memory:", backend=FakeBackend()))


def test_retention_classes_defined():
    assert "TRANSIENT" in RETENTION_CLASSES
    assert "OPERATIONAL" in RETENTION_CLASSES
    assert "CANONICAL" in RETENTION_CLASSES
    assert "ARCHIVAL" in RETENTION_CLASSES


def test_transient_has_30_day_retention():
    info = RETENTION_CLASSES["TRANSIENT"]
    assert info["retention_days"] == 30
    assert info["archive_policy"] == "auto_delete"


def test_operational_has_365_day_retention():
    info = RETENTION_CLASSES["OPERATIONAL"]
    assert info["retention_days"] == 365
    assert info["archive_policy"] == "auto_archive"


def test_canonical_is_permanent():
    info = RETENTION_CLASSES["CANONICAL"]
    assert info["retention_days"] is None
    assert info["archive_policy"] == "permanent"


def test_archival_is_compressed():
    info = RETENTION_CLASSES["ARCHIVAL"]
    assert info["retention_days"] is None
    assert info["archive_policy"] == "compressed"


def test_evidence_has_retention_fields():
    mp = _mp()
    record = mp.record_evidence({"evidence_id": "ret-test-evidence"})
    assert "retention_class" in record
    assert "archive_policy" in record
    assert "compaction_policy" in record
    assert "retention_until" in record
    assert record["retention_class"] == "OPERATIONAL"


def test_lesson_candidate_has_retention_fields():
    mp = _mp()
    record = mp.record_lesson_candidate({"lesson_id": "ret-test-lesson"})
    assert record["retention_class"] == "OPERATIONAL"
    assert record["archive_policy"] == "auto_archive"


def test_knowledge_has_canonical_retention():
    mp = _mp()
    record = mp.promote_to_knowledge("ret-test-know", {"lesson_id": "ret-test-know"})
    assert record["retention_class"] == "CANONICAL"
    assert record["archive_policy"] == "permanent"


def test_capability_roi_has_canonical_retention():
    mp = _mp()
    record = mp.record_capability_roi({"roi_id": "ret-test-roi"})
    assert record["retention_class"] == "CANONICAL"
    assert record["archive_policy"] == "permanent"


def test_apply_retention_policy_dry_run():
    mp = _mp()
    result = mp.apply_retention_policy(dry_run=True)
    assert result["dry_run"] is True
    assert "actions" in result
    assert len(result["actions"]) == len(mp.MANDATORY_TABLES)
