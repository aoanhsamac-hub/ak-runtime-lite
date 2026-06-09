from memory.lancedb_adapter import LanceDBAdapter
from memory.lesson_registry import LessonRegistry
from memory.skill_registry import SkillRegistry
from connectors.hermes_import_adapter import HermesSkillImporter, HermesSkillManifest
from connectors.opencode_import_adapter import OpenCodeSkillImporter, WorkflowSkillManifest
from tests.test_lancedb_adapter import FakeBackend


def _setup_registry(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    lessons = LessonRegistry(adapter)
    lesson = lessons.create_candidate(
        title="Import lesson", summary="Summary", content="Content",
        source="import", owner_agent="Hermes", reviewer_agent="Sage",
        risk_level="LEVEL_1_MODERATE", tags=[],
    )
    lessons.mark_reviewed(lesson.lesson_id, "Sage")
    lessons.approve(lesson.lesson_id, "Sage")
    skills = SkillRegistry(adapter, lessons)
    return skills, lesson


def test_hermes_import_parse_manifest():
    importer = HermesSkillImporter(None)
    data = {
        "skill_id": "H-SKILL-001",
        "name": "market-analyzer",
        "description": "Analyze market patterns",
        "version": "2.1",
        "owner": "Hermes",
        "status": "APPROVED",
        "category": "trading",
        "dependencies": ["H-SKILL-000"],
        "required_tools": ["python3"],
        "risk_level": "LEVEL_2_HIGH",
    }
    manifest = importer.parse_manifest(data)
    assert manifest.name == "market-analyzer"
    assert manifest.hermes_skill_id == "H-SKILL-001"
    assert manifest.version == "2.1"
    assert manifest.category == "trading"


def test_hermes_import_skill(tmp_path):
    skills, lesson = _setup_registry(tmp_path)
    importer = HermesSkillImporter(skills)
    manifest = HermesSkillManifest(
        hermes_skill_id="H-001",
        name="hermes-skill",
        description="From Hermes",
        owner="Hermes",
    )
    ak_id = importer.import_skill(manifest)
    record = skills.get(ak_id)
    assert record.name == "hermes-skill"
    assert record.category == "imported"
    assert record.source == "hermes"
    assert record.lifecycle_stage == "PROPOSED"


def test_hermes_import_log(tmp_path):
    skills, lesson = _setup_registry(tmp_path)
    importer = HermesSkillImporter(skills)
    manifest = HermesSkillManifest(hermes_skill_id="H-002", name="h-skill", description="H-skill desc", owner="Hermes")
    importer.import_skill(manifest)
    log = importer.get_import_log()
    assert len(log) == 1
    assert log[0]["hermes_skill_id"] == "H-002"
    assert log[0]["name"] == "h-skill"
    assert log[0]["status"] == "PROPOSED"


def test_hermes_dry_run():
    importer = HermesSkillImporter(None)
    result = importer.dry_run({"name": "dry-test", "skill_id": "H-003", "owner": "Hermes"})
    assert result["dry_run"] is True
    assert result["ak_lifecycle_stage"] == "PROPOSED"
    assert result["ak_category"] == "imported"


def test_hermes_manifest_invalid_status():
    try:
        HermesSkillManifest(
            hermes_skill_id="H-001", name="test", status="INVALID", owner="Hermes",
        )
    except ValueError as exc:
        assert "status" in str(exc).lower()
    else:
        raise AssertionError("invalid status should fail")


def test_hermes_manifest_invalid_category():
    try:
        HermesSkillManifest(
            hermes_skill_id="H-001", name="test", owner="Hermes", category="invalid",
        )
    except ValueError as exc:
        assert "category" in str(exc).lower()
    else:
        raise AssertionError("invalid category should fail")


def test_opencode_detect_source():
    importer = OpenCodeSkillImporter(None)
    assert importer.detect_source({"name": "test", "openhands_version": "1.0"}) == "openhands"
    assert importer.detect_source({"name": "test"}) == "opencode"


def test_opencode_import_skill(tmp_path):
    skills, lesson = _setup_registry(tmp_path)
    importer = OpenCodeSkillImporter(skills)
    manifest = WorkflowSkillManifest(
        name="oc-skill",
        description="From OpenCode",
        source="opencode",
        author="LangLieu",
    )
    ak_id = importer.import_skill(manifest)
    record = skills.get(ak_id)
    assert record.name == "oc-skill"
    assert record.category == "imported"
    assert record.source == "opencode"
    assert record.lifecycle_stage == "PROPOSED"


def test_opencode_import_log(tmp_path):
    skills, lesson = _setup_registry(tmp_path)
    importer = OpenCodeSkillImporter(skills)
    manifest = WorkflowSkillManifest(name="oc-2", description="OC-2", source="opencode")
    importer.import_skill(manifest)
    log = importer.get_import_log()
    assert len(log) == 1
    assert log[0]["name"] == "oc-2"


def test_opencode_dry_run():
    importer = OpenCodeSkillImporter(None)
    result = importer.dry_run({"name": "dry-oc", "description": "Dry run test", "skill_id": "OC-001", "tools": ["python3"]})
    assert result["dry_run"] is True
    assert result["detected_source"] == "opencode"
    assert result["max_lifecycle_stage"] == "READY_FOR_SANDBOX"


def test_opencode_openhands_import(tmp_path):
    skills, lesson = _setup_registry(tmp_path)
    importer = OpenCodeSkillImporter(skills)
    data = {
        "name": "oh-skill",
        "description": "From OpenHands",
        "openhands_version": "1.0",
        "oh_skill": True,
        "author": "Community",
    }
    manifest = importer.parse_manifest(data)
    assert manifest.source == "openhands"
    ak_id = importer.import_skill(manifest)
    record = skills.get(ak_id)
    assert record.source == "openhands"


def test_imported_skill_category_source(tmp_path):
    skills, lesson = _setup_registry(tmp_path)
    importer = HermesSkillImporter(skills)
    manifest = HermesSkillManifest(hermes_skill_id="H-004", name="cat-test", description="Cat test", owner="Hermes")
    ak_id = importer.import_skill(manifest)
    record = skills.get(ak_id)
    assert record.category == "imported"
    assert record.source == "hermes"
    assert record.lifecycle_stage == "PROPOSED"


def test_opencode_manifest_invalid_source():
    try:
        WorkflowSkillManifest(name="test", source="invalid_source")
    except ValueError as exc:
        assert "source" in str(exc).lower()
    else:
        raise AssertionError("invalid source should fail")