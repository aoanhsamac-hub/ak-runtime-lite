from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


RELATIONSHIP_TYPES = {"PARENT_CAPABILITY", "CHILD_CAPABILITY", "RELATED_CAPABILITY",
                       "DEPENDENT_CAPABILITY", "PREREQUISITE_CAPABILITY"}


@dataclass
class CapabilityGraphNode:
    node_id: str
    node_type: str
    label: str
    domain: str = ""
    classification: str = ""


@dataclass
class CapabilityGraphEdge:
    source_id: str
    target_id: str
    relationship: str
    weight: float = 1.0


@dataclass
class CapabilityGraph:
    nodes: list[CapabilityGraphNode] = field(default_factory=list)
    edges: list[CapabilityGraphEdge] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": [(n.node_id, n.node_type, n.label, n.domain, n.classification) for n in self.nodes],
            "edges": [(e.source_id, e.target_id, e.relationship, e.weight) for e in self.edges],
        }


class CapabilityGraphEngine:
    """Builds relationship graph from canonical capabilities and families."""

    def __init__(self, capability_registry, family_registry, canonical_registry):
        self.capability_registry = capability_registry
        self.family_registry = family_registry
        self.canonical_registry = canonical_registry

    def build_graph(self) -> CapabilityGraph:
        graph = CapabilityGraph()
        families = self.family_registry.list_all()
        canonicals = self.canonical_registry.list_all()
        family_map = {f.family_id: f for f in families}
        domain_families = {}
        for f in families:
            for key in ["Trading", "Risk", "Execution", "Governance", "Memory", "Engineering", "Agent"]:
                if key.lower() in f.family_name.lower():
                    domain_families[key] = f.family_id

        for f in families:
            graph.nodes.append(CapabilityGraphNode(
                node_id=f.family_id, node_type="family", label=f.family_name,
            ))
        for c in canonicals:
            graph.nodes.append(CapabilityGraphNode(
                node_id=c.canonical_id, node_type="canonical",
                label=c.name, domain=c.domain, classification=c.classification,
            ))

        for c in canonicals:
            if c.family_id in family_map:
                graph.edges.append(CapabilityGraphEdge(
                    source_id=c.canonical_id, target_id=c.family_id,
                    relationship="PARENT_CAPABILITY", weight=1.0,
                ))

        domain_groups = {}
        for c in canonicals:
            domain_groups.setdefault(c.domain, []).append(c)
        for domain, members in domain_groups.items():
            for i, a in enumerate(members):
                for b in members[i + 1:]:
                    graph.edges.append(CapabilityGraphEdge(
                        source_id=a.canonical_id, target_id=b.canonical_id,
                        relationship="RELATED_CAPABILITY",
                        weight=round((a.confidence_score + b.confidence_score) / 2, 2),
                    ))

        for c in canonicals:
            for sid in c.superseded_ids + c.overlapping_ids:
                graph.edges.append(CapabilityGraphEdge(
                    source_id=c.canonical_id, target_id=sid,
                    relationship="DEPENDENT_CAPABILITY", weight=0.5,
                ))
        return graph
