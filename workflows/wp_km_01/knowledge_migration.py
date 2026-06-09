from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE))

from memory.capability_registry import CapabilityRegistry
from memory.dataset_registry import DatasetRegistry
from memory.decision_trace_registry import DecisionTraceRegistry
from memory.lancedb_adapter import LanceDBAdapter
from memory.lesson_registry import LessonRegistry
from memory.memory_interface import MemoryInterface
from memory.schemas import DecisionTraceRecord, LessonRecord
from memory.skill_registry import SkillRegistry


class FakeBackend:
    def __init__(self):
        self.tables = {}
    def create_table(self, name, data=None, mode=None):
        class FakeTable:
            def __init__(self, rows):
                self.rows = list(rows)
            def add(self, rows):
                self.rows.extend(rows)
        table = FakeTable(data or [])
        self.tables[name] = table
        return table
    def open_table(self, name):
        if name not in self.tables:
            raise FileNotFoundError(name)
        return self.tables[name]


adapter = LanceDBAdapter(str(BASE / "memory/lancedb"), backend=FakeBackend())
interface = MemoryInterface(str(BASE / "memory/lancedb"), adapter=adapter)


MIGRATION_LOG: list[dict] = []


def log(kind: str, source: str, record_id: str, summary: str) -> dict:
    entry = dict(kind=kind, source=source, record_id=record_id, summary=summary)
    MIGRATION_LOG.append(entry)
    return entry


def migrate_decision_traces():
    traces: list[dict] = [
        dict(
            agent="Lang Lieu",
            decision="Reorganize legal documents into sovereign directory structure",
            reasoning="Existing legal documents were scattered; sovereign governance requires a canonical directory layout under sovereign/",
            evidence=["docs/reports/AK_WP0_LEGAL_GOVERNANCE_BOOTSTRAP_REPORT.md"],
            outcome="Legal documents reorganized into sovereign/constitution, sovereign/state_corpus, sovereign/laws, sovereign/decrees",
        ),
        dict(
            agent="Lang Lieu",
            decision="Create legal_index.yaml as master legal registry",
            reasoning="Multiple legal registries were being created without a single source of truth",
            evidence=["docs/reports/AK_WP0_LEGAL_GOVERNANCE_BOOTSTRAP_REPORT.md", "sovereign/legal_index.yaml"],
            outcome="legal_index.yaml created with 15 sovereign documents indexed",
        ),
        dict(
            agent="Lang Lieu",
            decision="Implement Governance Engine with approval routing and audit",
            reasoning="AK requires governance-first architecture; all actions must pass governance gate before execution",
            evidence=["docs/reports/AK_WP1_GOVERNANCE_ENGINE_REPORT.md", "governance/policy_engine.py"],
            outcome="PolicyEngine, ApprovalEngine, IssueRegistry, GovernanceGate, AuditEngine created; 12 tests pass",
        ),
        dict(
            agent="Lang Lieu",
            decision="Build 7-agent runtime framework with dry-run only execution",
            reasoning="AK requires sovereign agent infrastructure without dependency on legacy agent frameworks",
            evidence=["docs/reports/AK_WP2_AGENT_RUNTIME_FRAMEWORK_REPORT.md", "agents/runtime.py"],
            outcome="7 agents (Janus, Sage, Hermes, Iris, Helen, Lang Lieu, Yet Kieu) boot operational in dry-run mode; 53 tests pass",
        ),
        dict(
            agent="Lang Lieu",
            decision="Adopt LanceDB as exclusive memory backend — no SQLite/Chroma/FAISS fallback",
            reasoning="Memory Law requires sovereign-owned memory; LanceDB is the only approved backend",
            evidence=["docs/reports/AK_WP3_HERMES_NATIVE_MEMORY_PLATFORM_REPORT.md", "memory/lancedb_adapter.py"],
            outcome="LanceDBAdapter created with lazy-load, fail-closed, first-insert table creation, Arrow text fallback",
        ),
        dict(
            agent="Lang Lieu",
            decision="Create 5 knowledge registries (lesson, skill, capability, dataset, decision trace)",
            reasoning="Knowledge Governance Decree requires structured registries for all knowledge artifacts",
            evidence=["memory/lesson_registry.py", "memory/skill_registry.py", "memory/capability_registry.py", "memory/dataset_registry.py", "memory/decision_trace_registry.py"],
            outcome="All 5 registries implemented with in-memory caching and LanceDB persistence",
        ),
        dict(
            agent="Lang Lieu",
            decision="Implement Learning Intelligence Layer — Phase 1A Learning Metrics",
            reasoning="WP3.5 requires measuring learning effectiveness before knowledge population",
            evidence=["docs/reports/AK_WP35_LEARNING_INTELLIGENCE_DESIGN_REPORT.md", "learning/learning_metrics.py"],
            outcome="LearningMetrics module with EvidenceRecord, GovernanceContext, EvidenceProvider; 8 tests pass",
        ),
        dict(
            agent="Lang Lieu",
            decision="Implement Learning Intelligence Layer — Phase 1B Lesson Evaluator",
            reasoning="Lessons require quality evaluation before they can be promoted to skills",
            evidence=["tests/learning/test_lesson_evaluator.py", "learning/lesson_evaluator.py"],
            outcome="LessonEvaluator with LessonStatus, InformationClassification, quality scoring; 11 tests pass",
        ),
        dict(
            agent="Lang Lieu",
            decision="Implement Learning Intelligence Layer — Phase 1C Skill Evidence Policy",
            reasoning="Skills require evidence-based evaluation with risk classification before promotion",
            evidence=["docs/reports/AK_WP35_PHASE1C_IMPLEMENTATION_REPORT.md", "learning/skill_evidence_policy.py"],
            outcome="SkillEvidencePolicy with RiskClassification, governance gates, promotion audit trail; 25 tests pass",
        ),
        dict(
            agent="Lang Lieu",
            decision="Accept AK-CODEX v1.0 as Official National Codex",
            reasoning="Legal discovery, naming normalization, registry consolidation, and authority chain mapping completed successfully",
            evidence=["docs/legal/codex/AK_CODEX_ACCEPTANCE_PACKAGE.md"],
            outcome="AK-CODEX v1.0 ACCEPTED; enters maintenance mode",
        ),
        dict(
            agent="Lang Lieu",
            decision="Execute WP-KF-01 Knowledge Foundation — registry normalization and retrieval optimization",
            reasoning="WP-KF-01 identified registry fragmentation, duplicate artifacts, and retrieval bottlenecks requiring resolution before population",
            evidence=["docs/reports/WP_KF_01_FINAL_REPORT.md", "docs/reports/AK_KNOWLEDGE_FOUNDATION_AUDIT.md"],
            outcome="11 YAML registries normalized, 6 design docs tagged superseded, 5 Python registries enhanced with boot hydration and pagination, archive_index.yaml created; 97 tests pass",
        ),
        dict(
            agent="Lang Lieu",
            decision="Execute WP-KP-01 National Knowledge Production System",
            reasoning="Knowledge production requires automated pipelines to transform operational activity into governance-controlled artifacts",
            evidence=["docs/reports/WP_KP_01_FINAL_REPORT.md", "pipelines/"],
            outcome="5 production pipelines created (decision_trace, lesson, dataset, skill, capability), knowledge lifecycle model defined, governance workflow established; population readiness PASS",
        ),
    ]
    results = []
    for t in traces:
        trace = interface.decision_traces.record(**t)
        entry = log("decision_trace", t["evidence"][0], trace.trace_id, t["decision"][:80])
        results.append(entry)
    return results


def migrate_lessons():
    lessons: list[dict] = [
        dict(
            title="Legal governance requires canonical directory structure",
            summary="Reorganizing legal documents into sovereign/ hierarchy established single-source-of-truth for all governing documents",
            content="Legal documents were initially scattered across multiple directories. Reorganizing into sovereign/constitution, sovereign/state_corpus, sovereign/laws, and sovereign/decrees with corresponding registries eliminated ambiguity about canonical document locations.",
            source="docs/reports/AK_WP0_LEGAL_GOVERNANCE_BOOTSTRAP_REPORT.md",
            owner_agent="Hermes",
            reviewer_agent="Sage",
            risk_level="LEVEL_3_CRITICAL",
            tags=["governance", "legal", "reorganization"],
        ),
        dict(
            title="Registry consolidation prevents metadata fragmentation",
            summary="Maintaining multiple copies of the same legal registry leads to metadata inconsistency",
            content="Three near-identical legal registry files (legal_index.yaml, legal_registry.yaml, LEGAL_REGISTRY.yaml) were found with 330 lines of redundant metadata. Consolidating to a single master registry eliminated duplication risk.",
            source="docs/reports/AK_KNOWLEDGE_FOUNDATION_AUDIT.md",
            owner_agent="Hermes",
            reviewer_agent="Sage",
            risk_level="LEVEL_2_ELEVATED",
            tags=["registry", "metadata", "consolidation"],
        ),
        dict(
            title="Knowledge lifecycle must be governance-controlled at every promotion",
            summary="Knowledge promotion (lesson→skill→capability) must never be autonomous; every transition requires Sage or Janus approval",
            content="The Knowledge Lifecycle Model defines 8 states (EVIDENCE→CANDIDATE→REVIEWED→APPROVED→ACTIVE→DEPRECATED→ARCHIVE→QUARANTINE) with 11 allowed transitions. Each transition above CANDIDATE requires governance authority.",
            source="docs/design/AK_KNOWLEDGE_LIFECYCLE_MODEL.md",
            owner_agent="Hermes",
            reviewer_agent="Sage",
            risk_level="LEVEL_3_CRITICAL",
            tags=["lifecycle", "governance", "promotion"],
        ),
        dict(
            title="Evidence threshold prevents weak skill discovery",
            summary="Skills must emerge from at least 3 approved lessons with ≥70% success rate to ensure reliability",
            content="The Skill Discovery Pipeline enforces a minimum of 3 approved source lessons and a 70% success rate threshold before creating skill candidates. This prevents single-instance or unreliable patterns from becoming skills.",
            source="docs/design/AK_SKILL_DISCOVERY_PIPELINE.md",
            owner_agent="Hermes",
            reviewer_agent="Sage",
            risk_level="LEVEL_2_ELEVATED",
            tags=["skill", "discovery", "evidence"],
        ),
        dict(
            title="LanceDB-only backend enforces memory sovereignty",
            summary="No fallback to SQLite, Chroma, FAISS, or JSON memory backends ensures memory remains AK-sovereign",
            content="LanceDB was adopted as the exclusive memory backend per Memory Law. The adapter is lazy-loaded and fails closed when the dependency is absent. No alternative backend is permitted.",
            source="memory/lancedb_adapter.py",
            owner_agent="Hermes",
            reviewer_agent="Sage",
            risk_level="LEVEL_3_CRITICAL",
            tags=["memory", "storage", "sovereignty"],
        ),
        dict(
            title="Archive before delete preserves audit integrity",
            summary="All superseded or deprecated artifacts must be archived before any removal from active namespace",
            content="The Retention Governance Decree requires that files are archived before any deletion. The archive_index.yaml provides programmatic discovery of all archived states with snapshot hashes for verification.",
            source="docs/reports/AK_ARCHIVE_NORMALIZATION_EXECUTION_REPORT.md",
            owner_agent="Hermes",
            reviewer_agent="Sage",
            risk_level="LEVEL_3_CRITICAL",
            tags=["archive", "retention", "audit"],
        ),
        dict(
            title="Agent memory isolation prevents unauthorized access",
            summary="Agents access memory through AgentMemoryClient wrappers, never through direct LanceDB handles",
            content="The MemoryInterface pattern ensures agents receive AgentMemoryClient instances that wrap the underlying MemoryInterface. Direct LanceDB backend access is never exposed to agents, enforcing the Principle of Least Privilege.",
            source="memory/agent_memory.py",
            owner_agent="Hermes",
            reviewer_agent="Sage",
            risk_level="LEVEL_2_ELEVATED",
            tags=["memory", "security", "isolation"],
        ),
        dict(
            title="Design documents must be superseded by codex standards",
            summary="Once a design document is promoted to a codex standard, the design doc should be marked SUPERSEDED with a canonical reference",
            content="Six design documents were identified as substantially duplicated by AK-CODEX standards. Each was tagged with SUPERSEDED status and a superseded_by link to the canonical codex standard. This establishes clear source-of-truth chains.",
            source="docs/reports/AK_DUPLICATE_CONSOLIDATION_REPORT.md",
            owner_agent="Hermes",
            reviewer_agent="Sage",
            risk_level="LEVEL_1_MODERATE",
            tags=["documentation", "canonical", "supersession"],
        ),
        dict(
            title="Boot-time hydration ensures registry data survives restarts",
            summary="Python registries must load existing records from LanceDB on initialization to prevent data loss on process restart",
            content="The 5 Python registries were enhanced with _hydrate() methods that load all existing rows from LanceDB tables on __init__. This ensures knowledge records survive process restarts and are available immediately after bootstrap.",
            source="memory/lesson_registry.py",
            owner_agent="Hermes",
            reviewer_agent="Sage",
            risk_level="LEVEL_2_ELEVATED",
            tags=["persistence", "registry", "hydration"],
        ),
        dict(
            title="Capability maturity assessment prevents premature activation",
            summary="Capabilities require skill accumulation thresholds (EMERGING→DEVELOPING→ESTABLISHED→MATURE) before sovereign activation",
            content="The Capability Evolution Pipeline assesses maturity based on skill count and active/approved status. Only MATURE capabilities (≥5 skills, ≥3 active) are considered production-ready. Lower maturity levels require ongoing development.",
            source="docs/design/AK_CAPABILITY_EVOLUTION_PIPELINE.md",
            owner_agent="Hermes",
            reviewer_agent="Sage",
            risk_level="LEVEL_2_ELEVATED",
            tags=["capability", "maturity", "evolution"],
        ),
    ]
    results = []
    for lsn in lessons:
        lesson = interface.lessons.create_candidate(**lsn)
        entry = log("lesson", lsn["source"], lesson.lesson_id, lsn["title"])
        results.append(entry)
    return results


def migrate_datasets():
    datasets: list[dict] = [
        dict(
            name="Sovereign Legal Corpus",
            source="sovereign/ (constitution, state_corpus, laws, decrees, registries)",
            owner_agent="Hermes",
            reviewer_agent="Sage",
            risk_level="LEVEL_4_CONSTITUTIONAL",
            metadata={"document_count": 15, "registry": "sovereign/legal_index.yaml", "type": "legal"},
        ),
        dict(
            name="AK-CODEX v1.0 Standards",
            source="docs/legal/codex/ (standards, policies, specifications, registries)",
            owner_agent="Hermes",
            reviewer_agent="Sage",
            risk_level="LEVEL_3_CRITICAL",
            metadata={"document_count": 43, "registry": "docs/legal/codex/", "type": "codex"},
        ),
        dict(
            name="AK Design Doctrine Corpus",
            source="docs/design/ (learning models, pipeline designs, architecture)",
            owner_agent="Hermes",
            reviewer_agent="Sage",
            risk_level="LEVEL_2_ELEVATED",
            metadata={"document_count": 21, "registry": "docs/design/", "type": "design"},
        ),
        dict(
            name="AK Sovereign Registries",
            source="sovereign/registries/ (legal, constitution, state_corpus, hierarchy, directive, treasury)",
            owner_agent="Hermes",
            reviewer_agent="Sage",
            risk_level="LEVEL_3_CRITICAL",
            metadata={"registry_count": 6, "type": "registry"},
        ),
        dict(
            name="AK Governance Registry Set",
            source="governance/registries/ (protected_modules, approval_matrix, gate_registry, issue_registry)",
            owner_agent="Yet Kieu",
            reviewer_agent="Sage",
            risk_level="LEVEL_3_CRITICAL",
            metadata={"registry_count": 4, "type": "governance"},
        ),
        dict(
            name="AK National Knowledge Production Pipelines",
            source="pipelines/ (decision_trace, lesson, dataset, skill, capability)",
            owner_agent="Lang Lieu",
            reviewer_agent="Sage",
            risk_level="LEVEL_2_ELEVATED",
            metadata={"pipeline_count": 5, "type": "pipeline"},
        ),
    ]
    results = []
    for ds in datasets:
        record = interface.datasets.create(**ds)
        entry = log("dataset", ds["source"], record.dataset_id, ds["name"])
        results.append(entry)
    return results


def _find_lesson_ids(*keywords: str) -> list[str]:
    seen: set[str] = set()
    ids: list[str] = []
    for l in MIGRATION_LOG:
        if l["kind"] == "lesson" and any(k in l["summary"].lower() for k in keywords):
            rid = l["record_id"]
            if rid not in seen:
                seen.add(rid)
                ids.append(rid)
    return ids


SKILL_DEFS: list[dict] = [
    dict(
        name="memory-sovereignty",
        description="Manage AK memory using LanceDB-only backend with no legacy fallback; enforce memory isolation through AgentMemoryClient pattern",
        keywords=["sovereignty", "isolation"],
        owner_agent="Hermes",
        allowed_agents=["Hermes", "Lang Lieu", "Sage"],
        risk_level="LEVEL_3_CRITICAL",
        test_cases=["verify no SQLite/Chroma/FAISS backends exist", "verify AgentMemoryClient wraps MemoryInterface", "verify LanceDB fails closed when absent"],
    ),
    dict(
        name="knowledge-lifecycle-governance",
        description="Manage knowledge artifacts through the 8-state lifecycle with governance-controlled promotion at every stage",
        keywords=["lifecycle", "promotion"],
        owner_agent="Hermes",
        allowed_agents=["Hermes", "Sage", "Janus"],
        risk_level="LEVEL_3_CRITICAL",
        test_cases=["verify lesson transitions require Sage approval", "verify skill activation requires Janus", "verify capability activation requires Hung Vuong"],
    ),
    dict(
        name="registry-consolidation",
        description="Maintain canonical registries with unified schema; detect and resolve metadata duplication across registry files",
        keywords=["registry", "consolidation"],
        owner_agent="Hermes",
        allowed_agents=["Hermes", "Lang Lieu"],
        risk_level="LEVEL_2_ELEVATED",
        test_cases=["verify all YAML registries have registry_version field", "verify no duplicate registries exist", "verify all registries have owner_agent and reviewer_agent"],
    ),
    dict(
        name="evidence-based-skill-discovery",
        description="Discover skills from patterns of repeated successful lessons using minimum evidence thresholds",
        keywords=["evidence", "discovery"],
        owner_agent="Hermes",
        allowed_agents=["Hermes", "Sage"],
        risk_level="LEVEL_2_ELEVATED",
        test_cases=["verify minimum 3 lessons required", "verify 70% success rate threshold", "verify lessons must be APPROVED"],
    ),
    dict(
        name="archive-preservation",
        description="Manage knowledge artifact lifecycle with archive-before-delete preservation and indexed archive discovery",
        keywords=["archive", "retention"],
        owner_agent="Hermes",
        allowed_agents=["Hermes", "Sage", "Janus"],
        risk_level="LEVEL_2_ELEVATED",
        test_cases=["verify archive_index.yaml exists", "verify each archive entry has date and source_path", "verify lifecycle tagging on all entries"],
    ),
]


def migrate_skills():
    from memory.schemas import SkillRecord

    results = []
    for sk in SKILL_DEFS:
        lesson_ids = _find_lesson_ids(*sk["keywords"])
        record = SkillRecord(
            name=sk["name"],
            description=sk["description"],
            source_lessons=lesson_ids,
            owner_agent=sk["owner_agent"],
            allowed_agents=sk["allowed_agents"],
            risk_level=sk["risk_level"],
            test_cases=sk["test_cases"],
        )
        interface.skills._records[record.skill_id] = record
        interface.adapter.insert("skills", [record.to_dict()])
        entry = log("skill", f"lessons: {lesson_ids}", record.skill_id, sk["name"])
        results.append(entry)
    return results


def migrate_capabilities():
    from memory.schemas import CapabilityRecord

    skill_ids = [s["record_id"] for s in MIGRATION_LOG if s["kind"] == "skill"]
    if len(skill_ids) >= 2:
        record = CapabilityRecord(
            name="knowledge-foundation-management",
            skills=[sid for sid in skill_ids[:3]],
            owner_agent="Hermes",
            reviewer_agent="Sage",
            status="DRAFT",
            maturity_level="EMERGING",
            metrics={
                "source_skills": len(skill_ids),
                "threshold": 2,
                "met": True,
            },
        )
        interface.capabilities._records[record.capability_id] = record
        interface.adapter.insert("capabilities", [record.to_dict()])
        entry = log("capability", f"skills: {skill_ids}", record.capability_id, record.name)
        return [entry]
    return []


def main():
    print("=== WP-KM-01 Legacy Knowledge Migration ===\n")

    print("[1/5] Migrating decision traces...")
    dt = migrate_decision_traces()
    print(f"  Created {len(dt)} decision trace candidates")

    print("[2/5] Migrating lessons...")
    ls = migrate_lessons()
    print(f"  Created {len(ls)} lesson candidates")

    print("[3/5] Migrating datasets...")
    ds = migrate_datasets()
    print(f"  Created {len(ds)} dataset candidates")

    print("[4/5] Migrating skills...")
    sk = migrate_skills()
    print(f"  Created {len(sk)} skill candidates")

    print("[5/5] Migrating capabilities...")
    ca = migrate_capabilities()
    print(f"  Created {len(ca)} capability candidates")

    total = len(dt) + len(ls) + len(ds) + len(sk) + len(ca)
    print(f"\n=== Migration complete: {total} candidates created ===")

    report = dict(
        migration_log=MIGRATION_LOG,
        summary=dict(
            decision_traces=len(dt),
            lessons=len(ls),
            datasets=len(ds),
            skills=len(sk),
            capabilities=len(ca),
            total=total,
        ),
    )
    manifest_path = BASE / "memory/knowledge_registry/migration_manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Manifest written to {manifest_path}")


if __name__ == "__main__":
    main()
