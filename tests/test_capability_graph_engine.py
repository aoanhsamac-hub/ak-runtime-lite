from services.capability_family_engine import CapabilityFamilyEngine
from services.canonical_capability_engine import CanonicalCapabilityEngine
from services.capability_graph_engine import CapabilityGraphEngine


def test_build_graph_has_nodes(cap_candidate_registry, cap_family_registry, cap_canonical_registry):
    cap_candidate_registry.create(
        name="Trading Capability", description="T",
        domain="Trading", owner_agent="Sage", confidence_score=0.85,
    )
    CapabilityFamilyEngine(cap_candidate_registry, cap_family_registry).discover_families()
    CanonicalCapabilityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry).classify_all()
    engine = CapabilityGraphEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry)
    graph = engine.build_graph()
    assert len(graph.nodes) >= 1


def test_graph_has_edges(cap_candidate_registry, cap_family_registry, cap_canonical_registry):
    for d in ["Trading", "Risk"]:
        cap_candidate_registry.create(
            name=f"{d} Capability", description=d,
            domain=d, owner_agent="Sage", confidence_score=0.80,
        )
    CapabilityFamilyEngine(cap_candidate_registry, cap_family_registry).discover_families()
    CanonicalCapabilityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry).classify_all()
    engine = CapabilityGraphEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry)
    graph = engine.build_graph()
    assert len(graph.edges) >= 1
    for e in graph.edges:
        assert e.relationship in (
            "PARENT_CAPABILITY", "CHILD_CAPABILITY", "RELATED_CAPABILITY",
            "DEPENDENT_CAPABILITY", "PREREQUISITE_CAPABILITY",
        )


def test_graph_to_dict(cap_candidate_registry, cap_family_registry, cap_canonical_registry):
    cap_candidate_registry.create(
        name="Test Capability", description="T",
        domain="Agent", owner_agent="Sage", confidence_score=0.75,
    )
    CapabilityFamilyEngine(cap_candidate_registry, cap_family_registry).discover_families()
    CanonicalCapabilityEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry).classify_all()
    engine = CapabilityGraphEngine(cap_candidate_registry, cap_family_registry, cap_canonical_registry)
    graph = engine.build_graph()
    d = graph.to_dict()
    assert "nodes" in d
    assert "edges" in d


def test_empty_registry(cap_family_registry, cap_canonical_registry):
    empty = type("Empty", (), {"list_all": lambda *a, **kw: []})()
    engine = CapabilityGraphEngine(empty, cap_family_registry, cap_canonical_registry)
    graph = engine.build_graph()
    assert len(graph.nodes) == 0
