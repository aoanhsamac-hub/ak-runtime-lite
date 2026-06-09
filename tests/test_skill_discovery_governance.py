from services.learning_governance_gate import LearningGovernanceGate
from services.learning_audit_layer import LearningAuditLayer


def test_governance_gate_has_duplication_check():
    gate = LearningGovernanceGate()
    record = {
        "signal_id": "LSIG-001", "signal_type": "PATTERN",
        "source_kind": "lesson", "source_id": "L-1", "source_hash": "abc",
        "confidence_score": 0.85, "evidence": {"q": 1},
        "owner_agent": "Sage", "reviewer_agent": "Sage",
        "risk_level": "LEVEL_1_MODERATE", "status": "CANDIDATE",
    }
    report = gate.evaluate_signal(record)
    gates_by_name = {g.gate: g for g in report.gates}
    assert "duplication" in gates_by_name
    assert gates_by_name["duplication"].passed


def test_governance_gate_evaluates_cluster():
    gate = LearningGovernanceGate()
    record = {
        "cluster_id": "CLS-001", "cluster_type": "TRADING",
        "title": "Test Cluster", "description": "Test",
        "source_signal_ids": ["LSIG-1"],
        "confidence_score": 0.80, "evidence": {"count": 3},
        "owner_agent": "Sage", "reviewer_agent": "Sage",
        "risk_level": "LEVEL_1_MODERATE", "status": "CANDIDATE",
    }
    report = gate.evaluate_cluster(record)
    assert report.all_passed
    assert report.record_type == "cluster"


def test_cluster_gate_requires_traceability():
    gate = LearningGovernanceGate()
    record = {
        "cluster_id": "CLS-002", "cluster_type": "RISK",
        "title": "Bad Cluster", "description": "No traceability",
        "source_signal_ids": [],
        "confidence_score": 0.80, "evidence": {"count": 1},
        "owner_agent": "Sage", "reviewer_agent": "Sage",
        "risk_level": "LEVEL_1_MODERATE", "status": "CANDIDATE",
    }
    report = gate.evaluate_cluster(record)
    trace = [g for g in report.gates if g.gate == "traceability"]
    assert len(trace) == 1
    assert not trace[0].passed


def test_audit_layer_has_discovery_actions():
    audit = LearningAuditLayer()
    event = audit.record(
        agent="Sage",
        action="DISCOVERY_PIPELINE_RUN",
        record_type="pipeline",
        details={"status": "complete"},
    )
    assert event.action == "DISCOVERY_PIPELINE_RUN"
    assert event.status == "recorded"


def test_audit_layer_cluster_created():
    audit = LearningAuditLayer()
    event = audit.record(
        agent="Sage",
        action="CLUSTER_CREATED",
        record_type="cluster",
        record_id="CLS-001",
        details={"signal_count": 10},
    )
    assert event.action == "CLUSTER_CREATED"


def test_audit_layer_duplicate_detected():
    audit = LearningAuditLayer()
    event = audit.record(
        agent="Sage",
        action="DUPLICATE_DETECTED",
        record_type="candidate_skill",
        record_id="CSK-001",
        details={"match_id": "CSK-002"},
    )
    assert event.action == "DUPLICATE_DETECTED"


def test_governance_8_gates_for_skills():
    gate = LearningGovernanceGate()
    record = {
        "candidate_skill_id": "CSK-001", "name": "Test Skill",
        "description": "Test", "source_insight_ids": ["INS-1"],
        "source_signal_ids": ["LSIG-1"],
        "confidence_score": 0.80, "evidence": {"q": 1},
        "owner_agent": "Sage", "reviewer_agent": "Sage",
        "risk_level": "LEVEL_1_MODERATE",
        "status": "CANDIDATE", "approval_status": "PENDING_REVIEW",
        "activation_status": "DISABLED",
    }
    report = gate.evaluate_candidate_skill(record)
    assert len(report.gates) == 8
    gate_names = {g.gate for g in report.gates}
    assert "traceability" in gate_names
    assert "evidence_quality" in gate_names
    assert "confidence_threshold" in gate_names
    assert "ownership" in gate_names
    assert "review_authority" in gate_names
    assert "risk_appropriate" in gate_names
    assert "status_locked" in gate_names
    assert "duplication" in gate_names


def test_governance_8_gates_for_clusters():
    gate = LearningGovernanceGate()
    record = {
        "cluster_id": "CLS-001", "cluster_type": "ENGINEERING",
        "title": "Test", "description": "Test",
        "source_signal_ids": ["LSIG-1"],
        "confidence_score": 0.80, "evidence": {"q": 1},
        "owner_agent": "Sage", "reviewer_agent": "Sage",
        "risk_level": "LEVEL_1_MODERATE", "status": "CANDIDATE",
    }
    report = gate.evaluate_cluster(record)
    assert len(report.gates) == 8


def test_no_skill_promotion_governance():
    gate = LearningGovernanceGate()
    record = {
        "candidate_skill_id": "CSK-001", "name": "Promoted",
        "description": "Test", "source_insight_ids": ["INS-1"],
        "source_signal_ids": ["LSIG-1"],
        "confidence_score": 0.80, "evidence": {"q": 1},
        "owner_agent": "Sage", "reviewer_agent": "Sage",
        "risk_level": "LEVEL_1_MODERATE",
        "status": "ACTIVE", "approval_status": "APPROVED",
        "activation_status": "ENABLED",
    }
    report = gate.evaluate_candidate_skill(record)
    locked = [g for g in report.gates if g.gate == "status_locked"]
    assert len(locked) == 1
    assert not locked[0].passed


def test_audit_layer_merge_suggested():
    audit = LearningAuditLayer()
    event = audit.record(
        agent="Sage",
        action="MERGE_SUGGESTED",
        record_type="candidate_skill",
        record_id="CSK-001",
        details={"merge_with": "CSK-002", "reason": "duplicate"},
    )
    assert event.action == "MERGE_SUGGESTED"
