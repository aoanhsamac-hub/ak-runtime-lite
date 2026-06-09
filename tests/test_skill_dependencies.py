from memory.lancedb_adapter import LanceDBAdapter
from memory.dependency_registry import SkillDependencyRegistry, SkillOwnershipRegistry
from memory.schemas.dependencies import SkillDependencyRecord, SkillOwnershipRecord
from memory.schemas.records import DEPENDENCY_RELATIONSHIP_TYPES
from tests.test_lancedb_adapter import FakeBackend


def test_dependency_create(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    reg = SkillDependencyRegistry(adapter)
    dep = reg.create(
        source_skill_id="SKILL-001",
        target_id="SKILL-002",
        target_type="skill",
        relationship_type="depends_on",
        created_by="Hermes",
    )
    assert dep.dependency_id.startswith("DEP-")
    assert dep.source_skill_id == "SKILL-001"
    assert dep.target_id == "SKILL-002"
    assert dep.relationship_type == "depends_on"


def test_dependency_invalid_relationship_type(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    reg = SkillDependencyRegistry(adapter)
    try:
        reg.create(
            source_skill_id="SKILL-001",
            target_id="SKILL-002",
            target_type="skill",
            relationship_type="invalid_rel",
        )
    except ValueError as exc:
        assert "relationship_type" in str(exc).lower()
    else:
        raise AssertionError("invalid relationship_type should fail")


def test_dependency_invalid_target_type(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    reg = SkillDependencyRegistry(adapter)
    try:
        reg.create(
            source_skill_id="SKILL-001",
            target_id="SYS-001",
            target_type="invalid_type",
            relationship_type="depends_on",
        )
    except ValueError as exc:
        assert "target_type" in str(exc).lower()
    else:
        raise AssertionError("invalid target_type should fail")


def test_dependency_get_by_source(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    reg = SkillDependencyRegistry(adapter)
    reg.create(source_skill_id="S1", target_id="T1", target_type="skill", relationship_type="depends_on")
    reg.create(source_skill_id="S1", target_id="T2", target_type="tool", relationship_type="requires_tool")
    reg.create(source_skill_id="S2", target_id="T3", target_type="skill", relationship_type="depends_on")
    deps = reg.get_by_source("S1")
    assert len(deps) == 2
    assert all(d.source_skill_id == "S1" for d in deps)


def test_dependency_get_by_target(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    reg = SkillDependencyRegistry(adapter)
    reg.create(source_skill_id="S1", target_id="T1", target_type="skill", relationship_type="depends_on")
    reg.create(source_skill_id="S2", target_id="T1", target_type="skill", relationship_type="supersedes")
    deps = reg.get_by_target("T1")
    assert len(deps) == 2
    deps_filtered = reg.get_by_target("T1", target_type="skill")
    assert len(deps_filtered) == 2


def test_dependency_all_relationship_types():
    expected = {
        "depends_on", "conflicts_with", "supersedes", "enhances",
        "requires_dataset", "produces_dataset",
        "requires_tool", "provides_tool",
        "assigned_to", "executable_by", "monitored_by",
        "part_of_capability", "enables_capability",
    }
    assert DEPENDENCY_RELATIONSHIP_TYPES == expected


def test_dependency_circular_detection(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    reg = SkillDependencyRegistry(adapter)
    reg.create(source_skill_id="A", target_id="B", target_type="skill", relationship_type="depends_on")
    reg.create(source_skill_id="B", target_id="C", target_type="skill", relationship_type="depends_on")
    reg.create(source_skill_id="C", target_id="D", target_type="skill", relationship_type="depends_on")
    assert reg.check_circular("A", "D", "skill") is False
    reg.create(source_skill_id="D", target_id="A", target_type="skill", relationship_type="depends_on")
    assert reg.check_circular("A", "D", "skill") is True


def test_dependency_delete(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    reg = SkillDependencyRegistry(adapter)
    dep = reg.create(source_skill_id="S1", target_id="T1", target_type="skill", relationship_type="depends_on")
    reg.delete(dep.dependency_id)
    try:
        reg.get(dep.dependency_id)
    except KeyError:
        pass
    else:
        raise AssertionError("deleted dependency should not be found")


def test_ownership_create(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    reg = SkillOwnershipRegistry(adapter)
    own = reg.create(
        skill_id="SKILL-001",
        owner_agent="Hermes",
        primary_users=["Sage"],
        secondary_users=["LangLieu"],
        assigned_by="Hung Vuong",
    )
    assert own.ownership_id.startswith("OWN-")
    assert own.owner_agent == "Hermes"
    assert own.access_level == "OWNER"


def test_ownership_get_by_skill(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    reg = SkillOwnershipRegistry(adapter)
    reg.create(skill_id="SKILL-001", owner_agent="Hermes", assigned_by="Sage")
    reg.create(skill_id="SKILL-002", owner_agent="Sage", assigned_by="Hung Vuong")
    own = reg.get_by_skill("SKILL-001")
    assert own is not None
    assert own.owner_agent == "Hermes"
    own2 = reg.get_by_skill("SKILL-003")
    assert own2 is None


def test_ownership_get_by_owner(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    reg = SkillOwnershipRegistry(adapter)
    reg.create(skill_id="S1", owner_agent="Hermes", assigned_by="Sage")
    reg.create(skill_id="S2", owner_agent="Hermes", assigned_by="Sage")
    reg.create(skill_id="S3", owner_agent="Sage", assigned_by="Hermes")
    owned = reg.get_by_owner("Hermes")
    assert len(owned) == 2


def test_ownership_get_by_user(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    reg = SkillOwnershipRegistry(adapter)
    reg.create(skill_id="S1", owner_agent="Hermes", primary_users=["Sage"],
               secondary_users=["LangLieu"], assigned_by="Hung Vuong")
    primary = reg.get_by_user("Sage", "PRIMARY_USER")
    assert len(primary) == 1
    secondary = reg.get_by_user("LangLieu", "SECONDARY_USER")
    assert len(secondary) == 1
    owner = reg.get_by_user("Hermes", "OWNER")
    assert len(owner) == 1


def test_ownership_update(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    reg = SkillOwnershipRegistry(adapter)
    reg.create(skill_id="S1", owner_agent="Hermes", assigned_by="Sage")
    updated = reg.update("S1", owner_agent="Sage", assigned_by="Hung Vuong")
    assert updated.owner_agent == "Sage"


def test_ownership_forbidden_users_validation():
    try:
        SkillOwnershipRecord(
            skill_id="S1", owner_agent="Hermes", primary_users=["Sage"],
            forbidden_users=["Sage"], assigned_by="Hung Vuong",
        )
    except ValueError as exc:
        assert "forbidden" in str(exc).lower()
    else:
        raise AssertionError("primary in forbidden_users should fail")