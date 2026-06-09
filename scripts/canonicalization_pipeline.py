"""WP35-1C-02B-R Canonicalization Pipeline – run all engines, collect data."""
import sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from memory.learning_registry import (
    LearningSignalRegistry, InsightRegistry, CandidateSkillRegistry,
    SignalClusterRegistry, SkillFamilyRegistry, CanonicalSkillRegistry,
)
from services.skill_family_engine import SkillFamilyEngine
from services.canonical_skill_engine import CanonicalSkillEngine
from services.skill_graph_engine import SkillGraphEngine
from services.skill_maturity_engine import SkillMaturityEngine
from services.learning_governance_gate import LearningGovernanceGate

signal_reg = LearningSignalRegistry()
insight_reg = InsightRegistry()
skill_reg = CandidateSkillRegistry()
cluster_reg = SignalClusterRegistry()
family_reg = SkillFamilyRegistry()
canon_reg = CanonicalSkillRegistry()

governance = LearningGovernanceGate()

families = SkillFamilyEngine(skill_reg, family_reg).discover_families(owner_agent="Sage")
canonical = CanonicalSkillEngine(skill_reg, family_reg, canon_reg).classify_all(owner_agent="Sage")
graph = SkillGraphEngine(skill_reg, family_reg, canon_reg).build_graph()
assessments = SkillMaturityEngine(skill_reg, family_reg, canon_reg).assess_all()

skills = skill_reg.list_all()
all_families = family_reg.list_all()
all_canon = canon_reg.list_all()

data = {
    "skills": [s.to_dict() for s in skills],
    "families": [f.to_dict() for f in all_families],
    "canonical": [c.to_dict() for c in all_canon],
    "graph": graph.to_dict(),
    "assessments": [a.__dict__ for a in assessments],
    "counts": {
        "total_candidate_skills": len(skills),
        "total_families": len(all_families),
        "total_canonical": len(all_canon),
        "total_assessments": len(assessments),
        "graph_nodes": len(graph.nodes),
        "graph_edges": len(graph.edges),
    },
}

# classification breakdown
class_counts = {}
for c in all_canon:
    cls = c.classification
    class_counts[cls] = class_counts.get(cls, 0) + 1
data["classification_counts"] = class_counts

# family breakdown
family_skills = {}
for f in all_families:
    family_skills[f.family_name] = {
        "count": len(f.member_skill_ids),
        "skill_ids": f.member_skill_ids,
        "confidence": f.family_confidence,
    }
data["family_breakdown"] = family_skills

# maturity breakdown
maturity_dist = {}
readiness_dist = {}
domain_maturity = {}
for a in assessments:
    maturity_dist[a.maturity_level] = maturity_dist.get(a.maturity_level, 0) + 1
    readiness_dist[a.promotion_readiness] = readiness_dist.get(a.promotion_readiness, 0) + 1
data["maturity_distribution"] = maturity_dist
data["readiness_distribution"] = readiness_dist

# graph metrics
node_types = {}
for n in graph.nodes:
    node_types[n.node_type] = node_types.get(n.node_type, 0) + 1
rel_types = {}
for e in graph.edges:
    rel_types[e.relationship] = rel_types.get(e.relationship, 0) + 1

orphans = [n for n in graph.nodes if n.node_type == "canonical" and not any(e.source_id == n.node_id for e in graph.edges)]
critical = [n for n in graph.nodes if sum(1 for e in graph.edges if e.source_id == n.node_id) >= 3]

data["graph_metrics"] = {
    "node_types": node_types,
    "relationship_types": rel_types,
    "orphan_count": len(orphans),
    "critical_node_count": len(critical),
    "orphan_ids": [n.node_id for n in orphans],
    "critical_ids": [n.node_id for n in critical],
}

# governance audit
audit_results = {}
for c in all_canon:
    report = governance.evaluate_canonical(c.to_dict())
    audit_results[c.canonical_id] = {
        "all_passed": report.all_passed,
        "summary": report.summary,
        "gates": {g.gate: {"passed": g.passed, "details": g.details} for g in report.gates},
    }
data["governance_audit"] = audit_results

# Risk analysis
risk_analysis = []
for c in all_canon:
    entry = {
        "canonical_id": c.canonical_id,
        "name": c.name,
        "classification": c.classification,
        "confidence": c.confidence_score,
        "evidence": c.evidence,
        "tags": c.tags,
    }
    risk_analysis.append(entry)
data["risk_analysis"] = risk_analysis

os.makedirs("docs/reports", exist_ok=True)
with open("docs/reports/canonicalization_data.json", "w") as f:
    json.dump(data, f, indent=2, default=str)

print(f"Pipeline complete:")
print(f"  Candidate Skills: {len(skills)}")
print(f"  Families: {len(all_families)}")
print(f"  Canonical: {len(all_canon)}")
print(f"  Assessments: {len(assessments)}")
print(f"  Graph Nodes: {len(graph.nodes)}, Edges: {len(graph.edges)}")
print(f"  Classifications: {class_counts}")
print(f"  Maturity: {maturity_dist}")
print(f"  Readiness: {readiness_dist}")
print(f"  Governance PASS: {sum(1 for v in audit_results.values() if v['all_passed'])}/{len(audit_results)}")
