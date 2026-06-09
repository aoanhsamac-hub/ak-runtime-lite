"""Seed 33 candidate skills based on WP35-1C-02 dry-run documented output."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from memory.learning_registry import CandidateSkillRegistry

reg = CandidateSkillRegistry()

skills_data = [
    # === 5 Trading Skills ===
    ("Trading Skills Skill: Market Trend Analysis (3 signals)", "Trading market analysis skill derived from MARKET insights", 0.82,
     ["trading", "market", "discovered"], {"discovery_method": "insight", "insight_type": "MARKET", "category": "Trading Skills"}),
    ("Trading Skills Skill: Market Risk Assessment (4 signals)", "Trading risk assessment skill derived from MARKET insights", 0.78,
     ["trading", "risk", "discovered"], {"discovery_method": "insight", "insight_type": "MARKET", "category": "Trading Skills"}),
    ("Trading Skills Skill: Market Execution Pattern (2 signals)", "Trading execution pattern skill derived from MARKET insights", 0.75,
     ["trading", "execution", "discovered"], {"discovery_method": "insight", "insight_type": "MARKET", "category": "Trading Skills"}),
    ("Trading Skills Discovery: Trading Cluster (32 signals)", "Trading cluster-derived skill from 32 trading signals", 0.82,
     ["trading", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "TRADING", "category": "Trading Skills"}),
    ("Trading Skills Discovery: Domain Cluster: trading (18 signals)", "Trading domain cluster-derived skill", 0.79,
     ["trading", "domain", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "TRADING", "category": "Trading Skills"}),
    # === 5 Risk Skills ===
    ("Risk Skills Skill: Risk Anomaly Detection (4 signals)", "Risk anomaly detection skill from RISK insights", 0.81,
     ["risk", "anomaly", "discovered"], {"discovery_method": "insight", "insight_type": "RISK", "category": "Risk Skills"}),
    ("Risk Skills Skill: Risk Assessment Protocol (3 signals)", "Risk assessment protocol skill from RISK insights", 0.77,
     ["risk", "assessment", "discovered"], {"discovery_method": "insight", "insight_type": "RISK", "category": "Risk Skills"}),
    ("Risk Skills Skill: Risk Mitigation Strategy (2 signals)", "Risk mitigation strategy skill from RISK insights", 0.74,
     ["risk", "mitigation", "discovered"], {"discovery_method": "insight", "insight_type": "RISK", "category": "Risk Skills"}),
    ("Risk Skills Discovery: Risk Cluster (4 signals)", "Risk cluster-derived skill from 4 risk signals", 0.80,
     ["risk", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "RISK", "category": "Risk Skills"}),
    ("Risk Skills Discovery: Domain Cluster: risk (6 signals)", "Risk domain cluster-derived skill", 0.76,
     ["risk", "domain", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "RISK", "category": "Risk Skills"}),
    # === 4 Execution Skills ===
    ("Execution Skills Skill: Execution Workflow (3 signals)", "Execution workflow skill from EXECUTION insights", 0.83,
     ["execution", "workflow", "discovered"], {"discovery_method": "insight", "insight_type": "EXECUTION", "category": "Execution Skills"}),
    ("Execution Skills Skill: Execution Optimization (2 signals)", "Execution optimization skill from EXECUTION insights", 0.79,
     ["execution", "optimization", "discovered"], {"discovery_method": "insight", "insight_type": "EXECUTION", "category": "Execution Skills"}),
    ("Execution Skills Skill: Execution Monitoring (2 signals)", "Execution monitoring skill from EXECUTION insights", 0.76,
     ["execution", "monitoring", "discovered"], {"discovery_method": "insight", "insight_type": "EXECUTION", "category": "Execution Skills"}),
    ("Execution Skills Discovery: Execution Cluster (3 signals)", "Execution cluster-derived skill from 3 execution signals", 0.81,
     ["execution", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "EXECUTION", "category": "Execution Skills"}),
    # === 4 Governance Skills ===
    ("Governance Skills Skill: Governance Compliance (3 signals)", "Governance compliance skill from GOVERNANCE insights", 0.85,
     ["governance", "compliance", "discovered"], {"discovery_method": "insight", "insight_type": "GOVERNANCE", "category": "Governance Skills"}),
    ("Governance Skills Skill: Governance Policy Review (2 signals)", "Governance policy skill from GOVERNANCE insights", 0.80,
     ["governance", "policy", "discovered"], {"discovery_method": "insight", "insight_type": "GOVERNANCE", "category": "Governance Skills"}),
    ("Governance Skills Skill: Governance Audit Protocol (2 signals)", "Governance audit skill from GOVERNANCE insights", 0.78,
     ["governance", "audit", "discovered"], {"discovery_method": "insight", "insight_type": "GOVERNANCE", "category": "Governance Skills"}),
    ("Governance Skills Discovery: Governance Cluster (101 signals)", "Governance cluster-derived skill from 101 governance signals", 0.84,
     ["governance", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "GOVERNANCE", "category": "Governance Skills"}),
    # === 3 Memory Skills ===
    ("Memory Skills Skill: Performance Repeatability (3 signals)", "Performance repeatability skill from PERFORMANCE insights", 0.80,
     ["memory", "performance", "discovered"], {"discovery_method": "insight", "insight_type": "PERFORMANCE", "category": "Memory Skills"}),
    ("Memory Skills Skill: Memory Consolidation (2 signals)", "Memory consolidation skill from PERFORMANCE insights", 0.76,
     ["memory", "consolidation", "discovered"], {"discovery_method": "insight", "insight_type": "PERFORMANCE", "category": "Memory Skills"}),
    ("Memory Skills Skill: Pattern Retention (2 signals)", "Pattern retention skill from PERFORMANCE insights", 0.73,
     ["memory", "pattern", "discovered"], {"discovery_method": "insight", "insight_type": "PERFORMANCE", "category": "Memory Skills"}),
    # === 8 Engineering Skills ===
    ("Engineering Skills Skill: Pattern Recognition Engine (3 signals)", "Pattern recognition engineering skill from SKILL insights", 0.86,
     ["engineering", "pattern", "discovered"], {"discovery_method": "insight", "insight_type": "SKILL", "category": "Engineering Skills"}),
    ("Engineering Skills Skill: Dataset Processing Pipeline (2 signals)", "Dataset processing engineering skill from SKILL insights", 0.82,
     ["engineering", "dataset", "discovered"], {"discovery_method": "insight", "insight_type": "SKILL", "category": "Engineering Skills"}),
    ("Engineering Skills Discovery: Engineering Cluster (218 signals)", "Engineering cluster-derived skill from 218 signals", 0.85,
     ["engineering", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "ENGINEERING", "category": "Engineering Skills"}),
    ("Engineering Skills Discovery: Domain Cluster: engineering (45 signals)", "Engineering domain cluster-derived skill", 0.80,
     ["engineering", "domain", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "ENGINEERING", "category": "Engineering Skills"}),
    ("Engineering Skills Discovery: Domain Cluster: dataset (30 signals)", "Dataset domain cluster-derived skill", 0.77,
     ["engineering", "dataset", "domain", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "ENGINEERING", "category": "Engineering Skills"}),
    ("Engineering Skills Skill: Signal Processing v1 (2 signals)", "Signal processing skill legacy version", 0.55,
     ["engineering", "signal", "discovered"], {"discovery_method": "insight", "insight_type": "SKILL", "category": "Engineering Skills"}),
    ("Engineering Skills Skill: Signal Processing v3 (2 signals)", "Signal processing skill updated version", 0.91,
     ["engineering", "signal", "discovered"], {"discovery_method": "insight", "insight_type": "SKILL", "category": "Engineering Skills"}),
    ("Engineering Skills Skill: Data Pipeline Foundation (2 signals)", "Data pipeline foundation skill", 0.60,
     ["engineering", "data", "pipeline", "discovered"], {"discovery_method": "insight", "insight_type": "SKILL", "category": "Engineering Skills"}),
    # === 4 Agent Skills ===
    ("Agent Skills Skill: Decision Process Workflow (3 signals)", "Decision workflow skill from PROCESS insights", 0.81,
     ["agent", "decision", "discovered"], {"discovery_method": "insight", "insight_type": "PROCESS", "category": "Agent Skills"}),
    ("Agent Skills Skill: Agent Coordination Protocol (2 signals)", "Agent coordination skill from PROCESS insights", 0.78,
     ["agent", "coordination", "discovered"], {"discovery_method": "insight", "insight_type": "PROCESS", "category": "Agent Skills"}),
    ("Agent Skills Skill: Task Delegation Strategy (2 signals)", "Task delegation skill from PROCESS insights", 0.75,
     ["agent", "delegation", "discovered"], {"discovery_method": "insight", "insight_type": "PROCESS", "category": "Agent Skills"}),
    ("Agent Skills Discovery: Decision Cluster (107 signals)", "Decision cluster-derived skill from 107 decision signals", 0.83,
     ["agent", "decision", "cluster", "discovered"], {"discovery_method": "cluster", "cluster_type": "DECISION", "category": "Agent Skills"}),
]

for i, (name, desc, conf, tags, evidence) in enumerate(skills_data, 1):
    reg.create_candidate(
        name=name,
        description=desc,
        owner_agent="Sage",
        reviewer_agent="Sage",
        confidence_score=conf,
        risk_level="LEVEL_1_MODERATE",
        tags=tags,
        evidence=evidence,
        source_signal_ids=[f"LSIG-SEED-{i}"],
        source_insight_ids=[] if "Discovery:" in name else [f"INS-SEED-{i}"],
        metadata={"seed_id": i},
        test_cases=[],
        allowed_agents=["Sage"],
    )

print(f"Seeded {len(skills_data)} candidate skills")
