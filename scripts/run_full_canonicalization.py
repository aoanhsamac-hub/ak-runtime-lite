"""Seed 33 candidate skills + run full canonicalization pipeline + export data."""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from memory.learning_registry import (
    CandidateSkillRegistry, SkillFamilyRegistry, CanonicalSkillRegistry,
)
from services.skill_family_engine import SkillFamilyEngine
from services.canonical_skill_engine import CanonicalSkillEngine
from services.skill_graph_engine import SkillGraphEngine
from services.skill_maturity_engine import SkillMaturityEngine
from services.learning_governance_gate import LearningGovernanceGate

skill_reg = CandidateSkillRegistry()
family_reg = SkillFamilyRegistry()
canon_reg = CanonicalSkillRegistry()

# === SEED 33 candidate skills ===
skills_data = [
    ("Trading Skills Skill: Market Trend Analysis", "Trading market analysis skill derived from MARKET insights", 0.82,
     ["trading", "market", "discovered"], {"discovery_method": "insight", "insight_type": "MARKET", "category": "Trading Skills"}),
    ("Trading Skills Skill: Market Risk Assessment", "Trading risk assessment skill derived from MARKET insights", 0.78,
     ["trading", "risk", "discovered"], {"discovery_method": "insight", "insight_type": "MARKET", "category": "Trading Skills"}),
    ("Trading Skills Skill: Market Execution Pattern", "Trading execution pattern skill derived from MARKET insights", 0.75,
     ["trading", "execution", "discovered"], {"discovery_method": "insight", "insight_type": "MARKET", "category": "Trading Skills"}),
    ("Trading Skills Discovery: Trading Cluster (32 signals)", "Trading cluster-derived skill from 32 trading signals", 0.82,
     ["trading", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "TRADING", "category": "Trading Skills"}),
    ("Trading Skills Discovery: Domain Cluster: trading (18 signals)", "Trading domain cluster-derived skill", 0.79,
     ["trading", "domain", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "TRADING", "category": "Trading Skills"}),
    ("Risk Skills Skill: Risk Anomaly Detection", "Risk anomaly detection skill from RISK insights", 0.81,
     ["risk", "anomaly", "discovered"], {"discovery_method": "insight", "insight_type": "RISK", "category": "Risk Skills"}),
    ("Risk Skills Skill: Risk Assessment Protocol", "Risk assessment protocol skill from RISK insights", 0.77,
     ["risk", "assessment", "discovered"], {"discovery_method": "insight", "insight_type": "RISK", "category": "Risk Skills"}),
    ("Risk Skills Skill: Risk Mitigation Strategy", "Risk mitigation strategy skill from RISK insights", 0.74,
     ["risk", "mitigation", "discovered"], {"discovery_method": "insight", "insight_type": "RISK", "category": "Risk Skills"}),
    ("Risk Skills Discovery: Risk Cluster (4 signals)", "Risk cluster-derived skill from 4 risk signals", 0.80,
     ["risk", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "RISK", "category": "Risk Skills"}),
    ("Risk Skills Discovery: Domain Cluster: risk (6 signals)", "Risk domain cluster-derived skill", 0.76,
     ["risk", "domain", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "RISK", "category": "Risk Skills"}),
    ("Execution Skills Skill: Execution Workflow", "Execution workflow skill from EXECUTION insights", 0.83,
     ["execution", "workflow", "discovered"], {"discovery_method": "insight", "insight_type": "EXECUTION", "category": "Execution Skills"}),
    ("Execution Skills Skill: Execution Optimization", "Execution optimization skill from EXECUTION insights", 0.79,
     ["execution", "optimization", "discovered"], {"discovery_method": "insight", "insight_type": "EXECUTION", "category": "Execution Skills"}),
    ("Execution Skills Skill: Execution Monitoring", "Execution monitoring skill from EXECUTION insights", 0.76,
     ["execution", "monitoring", "discovered"], {"discovery_method": "insight", "insight_type": "EXECUTION", "category": "Execution Skills"}),
    ("Execution Skills Discovery: Execution Cluster (3 signals)", "Execution cluster-derived skill from 3 execution signals", 0.81,
     ["execution", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "EXECUTION", "category": "Execution Skills"}),
    ("Governance Skills Skill: Governance Compliance", "Governance compliance skill from GOVERNANCE insights", 0.85,
     ["governance", "compliance", "discovered"], {"discovery_method": "insight", "insight_type": "GOVERNANCE", "category": "Governance Skills"}),
    ("Governance Skills Skill: Governance Policy Review", "Governance policy skill from GOVERNANCE insights", 0.80,
     ["governance", "policy", "discovered"], {"discovery_method": "insight", "insight_type": "GOVERNANCE", "category": "Governance Skills"}),
    ("Governance Skills Skill: Governance Audit Protocol", "Governance audit skill from GOVERNANCE insights", 0.78,
     ["governance", "audit", "discovered"], {"discovery_method": "insight", "insight_type": "GOVERNANCE", "category": "Governance Skills"}),
    ("Governance Skills Discovery: Governance Cluster (101 signals)", "Governance cluster-derived skill from 101 governance signals", 0.84,
     ["governance", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "GOVERNANCE", "category": "Governance Skills"}),
    ("Memory Skills Skill: Performance Repeatability", "Performance repeatability skill from PERFORMANCE insights", 0.80,
     ["memory", "performance", "discovered"], {"discovery_method": "insight", "insight_type": "PERFORMANCE", "category": "Memory Skills"}),
    ("Memory Skills Skill: Memory Consolidation", "Memory consolidation skill from PERFORMANCE insights", 0.76,
     ["memory", "consolidation", "discovered"], {"discovery_method": "insight", "insight_type": "PERFORMANCE", "category": "Memory Skills"}),
    ("Memory Skills Skill: Pattern Retention", "Pattern retention skill from PERFORMANCE insights", 0.73,
     ["memory", "pattern", "discovered"], {"discovery_method": "insight", "insight_type": "PERFORMANCE", "category": "Memory Skills"}),
    ("Engineering Skills Skill: Pattern Recognition Engine", "Pattern recognition engineering skill from SKILL insights", 0.86,
     ["engineering", "pattern", "discovered"], {"discovery_method": "insight", "insight_type": "SKILL", "category": "Engineering Skills"}),
    ("Engineering Skills Skill: Dataset Processing Pipeline", "Dataset processing engineering skill from SKILL insights", 0.82,
     ["engineering", "dataset", "discovered"], {"discovery_method": "insight", "insight_type": "SKILL", "category": "Engineering Skills"}),
    ("Engineering Skills Discovery: Engineering Cluster (218 signals)", "Engineering cluster-derived skill from 218 signals", 0.85,
     ["engineering", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "ENGINEERING", "category": "Engineering Skills"}),
    ("Engineering Skills Discovery: Domain Cluster: engineering (45 signals)", "Engineering domain cluster-derived skill", 0.80,
     ["engineering", "domain", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "ENGINEERING", "category": "Engineering Skills"}),
    ("Engineering Skills Discovery: Domain Cluster: dataset (30 signals)", "Dataset domain cluster-derived skill", 0.77,
     ["engineering", "dataset", "domain", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "ENGINEERING", "category": "Engineering Skills"}),
    ("Engineering Skills Skill: Signal Processing Foundation", "Signal processing skill legacy version", 0.55,
     ["engineering", "signal", "discovered"], {"discovery_method": "insight", "insight_type": "SKILL", "category": "Engineering Skills"}),
    ("Engineering Skills Skill: Signal Processing v3", "Signal processing skill updated version", 0.91,
     ["engineering", "signal", "discovered"], {"discovery_method": "insight", "insight_type": "SKILL", "category": "Engineering Skills"}),
    ("Engineering Skills Skill: Data Pipeline Foundation", "Data pipeline foundation skill", 0.60,
     ["engineering", "data", "pipeline", "discovered"], {"discovery_method": "insight", "insight_type": "SKILL", "category": "Engineering Skills"}),
    ("Agent Skills Skill: Decision Process Workflow", "Decision workflow skill from PROCESS insights", 0.81,
     ["agent", "decision", "discovered"], {"discovery_method": "insight", "insight_type": "PROCESS", "category": "Agent Skills"}),
    ("Agent Skills Skill: Agent Coordination Protocol", "Agent coordination skill from PROCESS insights", 0.78,
     ["agent", "coordination", "discovered"], {"discovery_method": "insight", "insight_type": "PROCESS", "category": "Agent Skills"}),
    ("Agent Skills Skill: Task Delegation Strategy", "Task delegation skill from PROCESS insights", 0.75,
     ["agent", "delegation", "discovered"], {"discovery_method": "insight", "insight_type": "PROCESS", "category": "Agent Skills"}),
    ("Agent Skills Discovery: Decision Cluster (107 signals)", "Decision cluster-derived skill from 107 decision signals", 0.83,
     ["agent", "decision", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "DECISION", "category": "Agent Skills"}),
]

for i, (name, desc, conf, tags, evidence) in enumerate(skills_data, 1):
    skill_reg.create_candidate(
        name=name, description=desc,
        owner_agent="Sage", reviewer_agent="Sage",
        confidence_score=conf, risk_level="LEVEL_1_MODERATE",
        tags=tags, evidence=evidence,
        source_signal_ids=[f"LSIG-SEED-{i}"],
        source_insight_ids=[] if "Discovery:" in name else [f"INS-SEED-{i}"],
        metadata={"seed_id": i},
        test_cases=[], allowed_agents=["Sage"],
    )

skills = skill_reg.list_all()
print(f"Seeded {len(skills)} candidate skills")

# === RUN PIPELINE ===
families = SkillFamilyEngine(skill_reg, family_reg).discover_families(owner_agent="Sage")
print(f"Discovered {len(families)} families")

canonical = CanonicalSkillEngine(skill_reg, family_reg, canon_reg).classify_all(owner_agent="Sage")
print(f"Classified {len(canonical)} canonical records")

graph = SkillGraphEngine(skill_reg, family_reg, canon_reg).build_graph()
print(f"Built graph: {len(graph.nodes)} nodes, {len(graph.edges)} edges")

assessments = SkillMaturityEngine(skill_reg, family_reg, canon_reg).assess_all()
print(f"Assessed {len(assessments)} canonical skills")

governance = LearningGovernanceGate()

# Collect all data
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

# Classification breakdown
class_counts = {}
for c in all_canon:
    cls = c.classification
    class_counts[cls] = class_counts.get(cls, 0) + 1
data["classification_counts"] = class_counts

# Family breakdown
family_skills = {}
for f in all_families:
    family_skills[f.family_name] = {
        "count": len(f.member_skill_ids),
        "skill_ids": f.member_skill_ids,
        "skill_names": f.member_skill_names,
        "confidence": f.family_confidence,
    }
data["family_breakdown"] = family_skills

# Maturity distribution
maturity_dist = {}
readiness_dist = {}
domain_maturity = {}
for a in assessments:
    maturity_dist[a.maturity_level] = maturity_dist.get(a.maturity_level, 0) + 1
    readiness_dist[a.promotion_readiness] = readiness_dist.get(a.promotion_readiness, 0) + 1
data["maturity_distribution"] = maturity_dist
data["readiness_distribution"] = readiness_dist

# Graph metrics
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

# Governance audit
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
        "superseded_ids": c.superseded_ids,
        "overlapping_ids": c.overlapping_ids,
        "duplicate_ids": c.duplicate_ids,
        "family_id": c.family_id,
    }
    risk_analysis.append(entry)
data["risk_analysis"] = risk_analysis

# Additional: per-skill detail for reports
skill_detail = {}
for s in skills:
    fam_name = ""
    for f in all_families:
        if s.candidate_skill_id in f.member_skill_ids:
            fam_name = f.family_name
            break

    ass = None
    for a in assessments:
        matching_canon = [c for c in all_canon if a.skill_id == c.canonical_id and s.candidate_skill_id in c.source_skill_ids]
        if matching_canon:
            ass = a
            break

    canon_rec = None
    for c in all_canon:
        if s.candidate_skill_id in c.source_skill_ids:
            canon_rec = c
            break

    skill_detail[s.candidate_skill_id] = {
        "name": s.name,
        "family": fam_name,
        "confidence": s.confidence_score,
        "maturity_level": ass.maturity_level if ass else "N/A",
        "maturity_score": ass.maturity_score if ass else 0.0,
        "promotion_readiness": ass.promotion_readiness if ass else "N/A",
        "canonical_id": canon_rec.canonical_id if canon_rec else "N/A",
        "classification": canon_rec.classification if canon_rec else "N/A",
        "evidence": s.evidence,
        "tags": s.tags,
    }
data["skill_detail"] = skill_detail

os.makedirs("docs/reports", exist_ok=True)
with open("docs/reports/canonicalization_data.json", "w") as f:
    json.dump(data, f, indent=2, default=str)

print(f"\n=== DATA EXPORTED ===")
print(f"Classification counts: {class_counts}")
print(f"Maturity distribution: {maturity_dist}")
print(f"Readiness distribution: {readiness_dist}")
print(f"Graph: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
print(f"Governance PASS: {sum(1 for v in audit_results.values() if v['all_passed'])}/{len(audit_results)}")
