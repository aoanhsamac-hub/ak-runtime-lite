from services.skill_family_engine import SkillFamilyEngine
from services.canonical_skill_engine import CanonicalSkillEngine
from services.skill_graph_engine import SkillGraphEngine


def test_build_graph_contains_nodes_and_edges(
    candidate_skill_registry, family_registry, canonical_registry,
):
    candidate_skill_registry.create_candidate(
        name="Trading Signal", description="A trading signal skill",
        owner_agent="Sage", confidence_score=0.85, tags=["trading"],
    )
    fam_engine = SkillFamilyEngine(candidate_skill_registry, family_registry)
    fam_engine.discover_families(owner_agent="Sage")
    can_engine = CanonicalSkillEngine(candidate_skill_registry, family_registry, canonical_registry)
    can_engine.classify_all(owner_agent="Sage")
    graph_engine = SkillGraphEngine(candidate_skill_registry, family_registry, canonical_registry)
    graph = graph_engine.build_graph()
    assert len(graph.nodes) >= 1


def test_graph_has_family_nodes(candidate_skill_registry, family_registry, canonical_registry):
    candidate_skill_registry.create_candidate(
        name="Trading Execution", description="A trading skill",
        owner_agent="Sage", confidence_score=0.80, tags=["trading"],
    )
    fam_engine = SkillFamilyEngine(candidate_skill_registry, family_registry)
    fam_engine.discover_families(owner_agent="Sage")
    graph_engine = SkillGraphEngine(candidate_skill_registry, family_registry, canonical_registry)
    graph = graph_engine.build_graph()
    family_nodes = [n for n in graph.nodes if n.node_type == "family"]
    assert len(family_nodes) >= 1


def test_graph_edges_are_typed(candidate_skill_registry, family_registry, canonical_registry):
    candidate_skill_registry.create_candidate(
        name="Risk Skill", description="A risk skill",
        owner_agent="Sage", confidence_score=0.85, tags=["risk"],
    )
    fam_engine = SkillFamilyEngine(candidate_skill_registry, family_registry)
    fam_engine.discover_families(owner_agent="Sage")
    can_engine = CanonicalSkillEngine(candidate_skill_registry, family_registry, canonical_registry)
    can_engine.classify_all(owner_agent="Sage")
    graph_engine = SkillGraphEngine(candidate_skill_registry, family_registry, canonical_registry)
    graph = graph_engine.build_graph()
    for e in graph.edges:
        assert e.relationship in (
            "PARENT_SKILL", "CHILD_SKILL", "RELATED_SKILL",
            "DEPENDENT_SKILL", "PREREQUISITE_SKILL",
        )


def test_graph_to_dict_serializable(candidate_skill_registry, family_registry, canonical_registry):
    candidate_skill_registry.create_candidate(
        name="Governance Skill", description="A governance skill",
        owner_agent="Sage", confidence_score=0.75, tags=["governance"],
    )
    fam_engine = SkillFamilyEngine(candidate_skill_registry, family_registry)
    fam_engine.discover_families(owner_agent="Sage")
    graph_engine = SkillGraphEngine(candidate_skill_registry, family_registry, canonical_registry)
    graph = graph_engine.build_graph()
    d = graph.to_dict()
    assert "nodes" in d
    assert "edges" in d


def test_empty_registry_returns_empty_graph(family_registry, canonical_registry):
    empty = type("EmptyRegistry", (), {"list_all": lambda *a, **kw: []})()
    graph_engine = SkillGraphEngine(empty, family_registry, canonical_registry)
    graph = graph_engine.build_graph()
    assert len(graph.nodes) == 0
    assert len(graph.edges) == 0
