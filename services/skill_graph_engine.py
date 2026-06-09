from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


RELATIONSHIP_TYPES = {"PARENT_SKILL", "CHILD_SKILL", "RELATED_SKILL", "DEPENDENT_SKILL", "PREREQUISITE_SKILL"}


@dataclass
class GraphNode:
    node_id: str
    node_type: str
    label: str
    family: str = ""
    classification: str = ""


@dataclass
class GraphEdge:
    source_id: str
    target_id: str
    relationship: str
    weight: float = 1.0


@dataclass
class SkillGraph:
    nodes: list[GraphNode] = field(default_factory=list)
    edges: list[GraphEdge] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": [(n.node_id, n.node_type, n.label, n.family, n.classification) for n in self.nodes],
            "edges": [(e.source_id, e.target_id, e.relationship, e.weight) for e in self.edges],
        }


class SkillGraphEngine:
    """Builds relationship graph from canonical skills and families."""

    def __init__(self, candidate_skill_registry, family_registry, canonical_registry):
        self.candidate_skill_registry = candidate_skill_registry
        self.family_registry = family_registry
        self.canonical_registry = canonical_registry

    def build_graph(self) -> SkillGraph:
        graph = SkillGraph()

        families = self.family_registry.list_all()
        canonical = self.canonical_registry.list_all()
        skills = self.candidate_skill_registry.list_all()
        skill_map = {s.candidate_skill_id: s for s in skills}
        family_map = {f.family_id: f for f in families}
        canonical_map = {c.canonical_id: c for c in canonical}

        for f in families:
            graph.nodes.append(GraphNode(
                node_id=f.family_id, node_type="family",
                label=f.family_name, family=f.family_name,
            ))

        for c in canonical:
            graph.nodes.append(GraphNode(
                node_id=c.canonical_id, node_type="canonical",
                label=c.name, family=c.family_id,
                classification=c.classification,
            ))

        for c in canonical:
            if c.family_id in family_map:
                graph.edges.append(GraphEdge(
                    source_id=c.canonical_id, target_id=c.family_id,
                    relationship="PARENT_SKILL", weight=1.0,
                ))
            family_map_inv = {f.family_id: f for f in families}
            for f_id, f_rec in family_map_inv.items():
                for mid in f_rec.member_skill_ids:
                    if mid in c.source_skill_ids:
                        graph.edges.append(GraphEdge(
                            source_id=c.canonical_id, target_id=f_id,
                            relationship="CHILD_SKILL", weight=0.8,
                        ))

        canonical_by_family: dict[str, list] = {}
        for c in canonical:
            canonical_by_family.setdefault(c.family_id, []).append(c)

        for fid, members in canonical_by_family.items():
            for i, a in enumerate(members):
                for b in members[i + 1:]:
                    graph.edges.append(GraphEdge(
                        source_id=a.canonical_id, target_id=b.canonical_id,
                        relationship="RELATED_SKILL",
                        weight=round((a.confidence_score + b.confidence_score) / 2, 2),
                    ))

        for c in canonical:
            for sid in c.superseded_ids + c.overlapping_ids + c.duplicate_ids:
                graph.edges.append(GraphEdge(
                    source_id=c.canonical_id, target_id=sid,
                    relationship="DEPENDENT_SKILL", weight=0.5,
                ))

        return graph
