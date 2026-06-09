from services.learning_governance_gate import LearningGovernanceGate


def test_governance_gate_evaluates_signal_pass():
    gate = LearningGovernanceGate()
    record = {
        "signal_id": "LSIG-001",
        "signal_type": "PATTERN",
        "source_kind": "lesson",
        "source_id": "LKI-001",
        "source_hash": "abc123",
        "confidence_score": 0.85,
        "evidence": {"quality": 4},
        "owner_agent": "Sage",
        "reviewer_agent": "Sage",
        "risk_level": "LEVEL_1_MODERATE",
        "status": "CANDIDATE",
        "approval_status": "PENDING_REVIEW",
        "activation_status": "DISABLED",
    }
    report = gate.evaluate_signal(record)
    assert report.all_passed
    assert len(report.gates) == 8


def test_governance_gate_fails_missing_traceability():
    gate = LearningGovernanceGate()
    record = {
        "signal_id": "LSIG-002",
        "signal_type": "PATTERN",
        "source_kind": "",
        "source_id": "",
        "confidence_score": 0.85,
        "evidence": {"quality": 4},
        "owner_agent": "Sage",
        "reviewer_agent": "Sage",
        "risk_level": "LEVEL_1_MODERATE",
    }
    report = gate.evaluate_signal(record)
    assert not report.all_passed
    trace = [g for g in report.gates if g.gate == "traceability"]
    assert len(trace) == 1
    assert not trace[0].passed


def test_governance_gate_fails_low_confidence():
    gate = LearningGovernanceGate()
    record = {
        "signal_id": "LSIG-003",
        "signal_type": "PATTERN",
        "source_kind": "lesson",
        "source_id": "LKI-001",
        "source_hash": "abc",
        "confidence_score": 0.10,
        "evidence": {"quality": 4},
        "owner_agent": "Sage",
        "reviewer_agent": "Sage",
        "risk_level": "LEVEL_1_MODERATE",
    }
    report = gate.evaluate_signal(record)
    assert not report.all_passed
    conf = [g for g in report.gates if g.gate == "confidence_threshold"]
    assert not conf[0].passed


def test_governance_gate_fails_unknown_owner():
    gate = LearningGovernanceGate()
    record = {
        "signal_id": "LSIG-004",
        "signal_type": "PATTERN",
        "source_kind": "lesson",
        "source_id": "LKI-001",
        "source_hash": "abc",
        "confidence_score": 0.85,
        "evidence": {"quality": 4},
        "owner_agent": "UnknownAgent",
        "reviewer_agent": "Sage",
        "risk_level": "LEVEL_1_MODERATE",
    }
    report = gate.evaluate_signal(record)
    assert not report.all_passed
    owner = [g for g in report.gates if g.gate == "ownership"]
    assert not owner[0].passed


def test_governance_gate_fails_invalid_risk():
    gate = LearningGovernanceGate()
    record = {
        "signal_id": "LSIG-005",
        "signal_type": "PATTERN",
        "source_kind": "lesson",
        "source_id": "LKI-001",
        "source_hash": "abc",
        "confidence_score": 0.85,
        "evidence": {"quality": 4},
        "owner_agent": "Sage",
        "reviewer_agent": "Sage",
        "risk_level": "INVALID_RISK",
    }
    report = gate.evaluate_signal(record)
    assert not report.all_passed
    risk = [g for g in report.gates if g.gate == "risk_appropriate"]
    assert not risk[0].passed


def test_governance_gate_evaluates_insight():
    gate = LearningGovernanceGate()
    record = {
        "insight_id": "INS-001",
        "insight_type": "TREND",
        "source_signal_ids": ["LSIG-001"],
        "confidence_score": 0.75,
        "evidence": {"source_count": 1},
        "owner_agent": "Sage",
        "reviewer_agent": "Sage",
        "risk_level": "LEVEL_1_MODERATE",
        "status": "CANDIDATE",
        "approval_status": "PENDING_REVIEW",
        "activation_status": "DISABLED",
    }
    report = gate.evaluate_insight(record)
    assert report.all_passed


def test_governance_gate_evaluates_candidate_skill():
    gate = LearningGovernanceGate()
    record = {
        "candidate_skill_id": "CSK-001",
        "name": "Test Skill",
        "source_insight_ids": ["INS-001"],
        "source_signal_ids": ["LSIG-001"],
        "source_lesson_ids": ["LKI-001"],
        "confidence_score": 0.80,
        "evidence": {"quality": 4},
        "owner_agent": "Sage",
        "reviewer_agent": "Sage",
        "risk_level": "LEVEL_1_MODERATE",
        "status": "CANDIDATE",
        "approval_status": "PENDING_REVIEW",
        "activation_status": "DISABLED",
    }
    report = gate.evaluate_candidate_skill(record)
    assert report.all_passed


def test_governance_gate_detects_auto_promotion():
    gate = LearningGovernanceGate()
    record = {
        "signal_id": "LSIG-006",
        "signal_type": "PATTERN",
        "source_kind": "lesson",
        "source_id": "LKI-001",
        "source_hash": "abc",
        "confidence_score": 0.85,
        "evidence": {"quality": 4},
        "owner_agent": "Sage",
        "reviewer_agent": "Sage",
        "risk_level": "LEVEL_1_MODERATE",
        "status": "ACTIVE",
        "approval_status": "APPROVED",
        "activation_status": "ENABLED",
    }
    report = gate.evaluate_signal(record)
    promo = [g for g in report.gates if g.gate == "no_auto_promotion"]
    assert len(promo) == 1
    assert not promo[0].passed


def test_governance_report_summary():
    from services.learning_governance_gate import GovernanceReport, GateResult
    report = GovernanceReport(
        record_id="LSIG-001",
        record_type="signal",
        gates=[
            GateResult(gate="traceability", passed=True),
            GateResult(gate="confidence", passed=False),
        ],
        all_passed=False,
    )
    assert "1/2 gates passed" in report.summary


def test_audit_layer_records_event():
    from services.learning_audit_layer import LearningAuditLayer
    audit = LearningAuditLayer()
    event = audit.record(
        agent="Sage",
        action="SIGNAL_EXTRACTED",
        record_type="signal",
        record_id="LSIG-001",
        details={"count": 3},
    )
    assert event.event_id.startswith("AUDIT-")
    assert event.agent == "Sage"
    assert event.action == "SIGNAL_EXTRACTED"
    assert event.status == "recorded"


def test_audit_layer_rejects_unknown_action():
    from services.learning_audit_layer import LearningAuditLayer
    audit = LearningAuditLayer()
    try:
        audit.record(agent="Sage", action="UNKNOWN", record_type="signal")
    except ValueError as exc:
        assert "Unknown audit action" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_audit_layer_list_events():
    from services.learning_audit_layer import LearningAuditLayer
    audit = LearningAuditLayer()
    audit.record(agent="Sage", action="SIGNAL_EXTRACTED", record_type="signal")
    audit.record(agent="Janus", action="INSIGHT_CREATED", record_type="insight")
    audit.record(agent="Sage", action="SKILL_CANDIDATE_CREATED", record_type="candidate_skill")

    all_events = audit.list_events()
    assert len(all_events) == 3

    sage_events = audit.list_events(agent="Sage")
    assert len(sage_events) == 2

    signal_events = audit.list_events(record_type="signal")
    assert len(signal_events) == 1


def test_audit_layer_get_trail():
    from services.learning_audit_layer import LearningAuditLayer
    audit = LearningAuditLayer()
    audit.record(agent="Sage", action="GOVERNANCE_CHECK", record_type="signal", record_id="LSIG-001")
    audit.record(agent="Sage", action="GOVERNANCE_PASS", record_type="signal", record_id="LSIG-001")
    audit.record(agent="Janus", action="SIGNAL_EXTRACTED", record_type="signal", record_id="LSIG-002")

    trail = audit.get_trail("LSIG-001")
    assert len(trail) == 2


def test_audit_layer_export():
    from services.learning_audit_layer import LearningAuditLayer
    audit = LearningAuditLayer()
    audit.record(agent="Sage", action="DRY_RUN", record_type="integration", details={"status": "ok"})
    exported = audit.export()
    assert len(exported) == 1
    assert exported[0]["agent"] == "Sage"
    assert exported[0]["action"] == "DRY_RUN"


def test_audit_layer_clear():
    from services.learning_audit_layer import LearningAuditLayer
    audit = LearningAuditLayer()
    audit.record(agent="Sage", action="DRY_RUN", record_type="test")
    assert len(audit.list_events()) == 1
    audit.clear()
    assert len(audit.list_events()) == 0
