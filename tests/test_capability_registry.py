from memory.capability_registry import CapabilityRegistry
from memory.lancedb_adapter import LanceDBAdapter

from tests.test_lancedb_adapter import FakeBackend


def test_capability_requires_active_or_approved_skills(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    registry = CapabilityRegistry(adapter)

    capability = registry.create(
        name="Knowledge Capability",
        skills=[{"skill_id": "S-1", "status": "ACTIVE"}],
        owner_agent="Hermes",
        reviewer_agent="Sage",
        status="DRAFT",
        maturity_level="M1",
        metrics={"lessons": 20},
    )

    assert capability.capability_id.startswith("CAP-")
    assert capability.skills == ["S-1"]


def test_capability_rejects_draft_skills(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    registry = CapabilityRegistry(adapter)

    try:
        registry.create(
            name="Bad Capability",
            skills=[{"skill_id": "S-1", "status": "DRAFT"}],
            owner_agent="Hermes",
            reviewer_agent="Sage",
            status="DRAFT",
            maturity_level="M1",
            metrics={},
        )
    except ValueError as exc:
        assert "active or approved" in str(exc).lower()
    else:
        raise AssertionError("draft skills must be rejected")
