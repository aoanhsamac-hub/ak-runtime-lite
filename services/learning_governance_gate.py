from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class GateResult:
    gate: str
    passed: bool
    details: str = ""


@dataclass
class GovernanceReport:
    record_id: str
    record_type: str
    gates: list[GateResult] = field(default_factory=list)
    all_passed: bool = False

    @property
    def summary(self) -> str:
        passed = sum(1 for g in self.gates if g.passed)
        total = len(self.gates)
        return f"{passed}/{total} gates passed for {self.record_type}:{self.record_id}"


GOVERNANCE_GATES = [
    "traceability",
    "evidence_quality",
    "confidence_threshold",
    "ownership",
    "review_authority",
    "risk_appropriate",
    "no_auto_promotion",
    "duplication",
    "canonical_mapping",
    "graph_integrity",
    "independent_review",
    "promotion_eligibility",
    "no_activation",
    "evidence_gate",
    "validation_gate",
    "maturity_gate",
    "hermes_review_gate",
    "sage_review_gate",
    "no_agent_adoption_gate",
    "no_evolution_gate",
]


class LearningGovernanceGate:
    """Governance gates for learning intelligence.

    Validates that signals, insights, and candidate skills satisfy
    AK governance requirements before they are recorded.
    """

    def __init__(self):
        self._min_confidence = 0.3
        self._min_evidence_score = 1
        self._allowed_reviewers = {"Sage", "Hermes", "Hung Vuong", "Admin"}
        self._allowed_agents = {"Janus", "Sage", "Hermes", "Iris", "Helen", "LangLieu", "YetKieu"}

    def evaluate_signal(self, record: dict[str, Any]) -> GovernanceReport:
        gates = [
            self._check_traceability(record, "signal"),
            self._check_evidence_quality(record),
            self._check_confidence(record),
            self._check_ownership(record),
            self._check_review_authority(record),
            self._check_risk(record),
            self._check_no_auto_promotion(record),
            self._check_duplication(record),
        ]
        return GovernanceReport(
            record_id=record.get("signal_id", record.get("source_id", "unknown")),
            record_type="signal",
            gates=gates,
            all_passed=all(g.passed for g in gates),
        )

    def evaluate_insight(self, record: dict[str, Any]) -> GovernanceReport:
        gates = [
            self._check_traceability(record, "insight"),
            self._check_evidence_quality(record),
            self._check_confidence(record),
            self._check_ownership(record),
            self._check_review_authority(record),
            self._check_risk(record),
            self._check_no_auto_promotion(record),
            self._check_duplication(record),
        ]
        return GovernanceReport(
            record_id=record.get("insight_id", "unknown"),
            record_type="insight",
            gates=gates,
            all_passed=all(g.passed for g in gates),
        )

    def evaluate_candidate_skill(self, record: dict[str, Any]) -> GovernanceReport:
        gates = [
            self._check_traceability(record, "candidate_skill"),
            self._check_evidence_quality(record),
            self._check_confidence(record),
            self._check_ownership(record),
            self._check_review_authority(record),
            self._check_risk(record),
            self._check_status_locked(record),
            self._check_duplication(record),
        ]
        return GovernanceReport(
            record_id=record.get("candidate_skill_id", record.get("candidate_skill_id", "unknown")),
            record_type="candidate_skill",
            gates=gates,
            all_passed=all(g.passed for g in gates),
        )

    def evaluate_cluster(self, record: dict[str, Any]) -> GovernanceReport:
        gates = [
            self._check_traceability(record, "cluster"),
            self._check_evidence_quality(record),
            self._check_confidence(record),
            self._check_ownership(record),
            self._check_review_authority(record),
            self._check_risk(record),
            self._check_no_auto_promotion(record),
            self._check_duplication(record),
        ]
        return GovernanceReport(
            record_id=record.get("cluster_id", "unknown"),
            record_type="cluster",
            gates=gates,
            all_passed=all(g.passed for g in gates),
        )

    def evaluate_family(self, record: dict[str, Any]) -> GovernanceReport:
        gates = [
            self._check_traceability(record, "family"),
            self._check_evidence_quality(record),
            self._check_confidence(record),
            self._check_ownership(record),
            self._check_review_authority(record),
            self._check_risk(record),
            self._check_no_auto_promotion(record),
            self._check_canonical_mapping(record),
        ]
        return GovernanceReport(
            record_id=record.get("family_id", "unknown"),
            record_type="family",
            gates=gates,
            all_passed=all(g.passed for g in gates),
        )

    def evaluate_canonical(self, record: dict[str, Any]) -> GovernanceReport:
        gates = [
            self._check_traceability(record, "canonical"),
            self._check_evidence_quality(record),
            self._check_confidence(record),
            self._check_ownership(record),
            self._check_review_authority(record),
            self._check_risk(record),
            self._check_no_auto_promotion(record),
            self._check_canonical_mapping(record),
            self._check_graph_integrity(record),
        ]
        return GovernanceReport(
            record_id=record.get("canonical_id", "unknown"),
            record_type="canonical",
            gates=gates,
            all_passed=all(g.passed for g in gates),
        )

    def evaluate_capability(self, record: dict[str, Any]) -> GovernanceReport:
        gates = [
            self._check_traceability(record, "capability"),
            self._check_evidence_quality(record),
            self._check_confidence(record),
            self._check_ownership(record),
            self._check_review_authority(record),
            self._check_risk(record),
            self._check_canonical_mapping(record),
            self._check_graph_integrity(record),
            self._check_promotion_eligibility(record),
            self._check_no_activation(record),
        ]
        return GovernanceReport(
            record_id=record.get("canonical_id", record.get("capability_id", "unknown")),
            record_type="capability",
            gates=gates,
            all_passed=all(g.passed for g in gates),
        )

    def _check_traceability(self, record: dict[str, Any], kind: str) -> GateResult:
        trace_fields = {
            "signal": ["source_kind", "source_id", "source_hash"],
            "insight": ["source_signal_ids"],
            "candidate_skill": ["source_signal_ids"],
            "cluster": ["source_signal_ids"],
            "promotion": ["canonical_id", "decision_id", "skill_id"],
            "capability": ["canonical_id", "source_capability_ids", "domain"],
        }
        fields = trace_fields.get(kind, [])
        optional = [] if kind not in ("candidate_skill",) else ["source_insight_ids", "source_lesson_ids"]
        missing = [f for f in fields if not record.get(f)]
        result = len(missing) == 0
        details = "All trace fields present" if result else f"Missing trace fields: {missing}"
        if result and kind == "candidate_skill":
            has_some = any(record.get(f) for f in fields + optional)
            if not has_some:
                result = False
                details = "No traceability IDs found across all source fields"
            else:
                details += " (+source_insight_ids and source_lesson_ids optional)"
        return GateResult(gate="traceability", passed=result, details=details)

    def _check_evidence_quality(self, record: dict[str, Any]) -> GateResult:
        evidence = record.get("evidence", {}) or {}
        if isinstance(evidence, dict):
            has_content = len(evidence) > 0
        else:
            has_content = bool(evidence)
        return GateResult(
            gate="evidence_quality",
            passed=has_content,
            details="Evidence present" if has_content else "No evidence provided",
        )

    def _check_confidence(self, record: dict[str, Any]) -> GateResult:
        score = record.get("confidence_score", 0) or 0
        return GateResult(
            gate="confidence_threshold",
            passed=score >= self._min_confidence,
            details=f"Confidence {score} >= {self._min_confidence}" if score >= self._min_confidence
                    else f"Confidence {score} < {self._min_confidence}",
        )

    def _check_ownership(self, record: dict[str, Any]) -> GateResult:
        owner = record.get("owner_agent", "")
        return GateResult(
            gate="ownership",
            passed=owner in self._allowed_agents,
            details=f"Owner: {owner}" if owner in self._allowed_agents
                    else f"Unknown owner: {owner}",
        )

    def _check_review_authority(self, record: dict[str, Any]) -> GateResult:
        reviewer = record.get("reviewer_agent", "")
        return GateResult(
            gate="review_authority",
            passed=reviewer in self._allowed_reviewers,
            details=f"Reviewer: {reviewer}" if reviewer in self._allowed_reviewers
                    else f"Unauthorized reviewer: {reviewer}",
        )

    def _check_risk(self, record: dict[str, Any]) -> GateResult:
        risk = record.get("risk_level", "")
        valid_risks = {"LEVEL_0_SOVEREIGN", "LEVEL_1_MODERATE", "LEVEL_2_HIGH", "LEVEL_3_CRITICAL"}
        return GateResult(
            gate="risk_appropriate",
            passed=risk in valid_risks,
            details=f"Risk: {risk}" if risk in valid_risks else f"Invalid risk: {risk}",
        )

    def _check_no_auto_promotion(self, record: dict[str, Any]) -> GateResult:
        status = record.get("status", "")
        if status != "CANDIDATE":
            return GateResult(
                gate="no_auto_promotion",
                passed=False,
                details=f"status={status}, expected CANDIDATE",
            )
        approval = record.get("approval_status", "")
        activation = record.get("activation_status", "")
        if not approval and not activation:
            return GateResult(
                gate="no_auto_promotion",
                passed=True,
                details="status=CANDIDATE (signal/insight, no promotion fields)",
            )
        locked = approval == "PENDING_REVIEW" and activation == "DISABLED"
        return GateResult(
            gate="no_auto_promotion",
            passed=locked,
            details=f"status={status}, approval={approval}, activation={activation}"
                    if not locked else "All statuses locked to non-promoted values",
        )

    def _check_status_locked(self, record: dict[str, Any]) -> GateResult:
        status = record.get("status", "")
        approval = record.get("approval_status", "")
        activation = record.get("activation_status", "")
        locked = status == "CANDIDATE" and approval == "PENDING_REVIEW" and activation == "DISABLED"
        return GateResult(
            gate="status_locked",
            passed=locked,
            details="Statuses locked" if locked else
                    f"status={status}, approval={approval}, activation={activation}",
        )

    def _check_duplication(self, record: dict[str, Any]) -> GateResult:
        return GateResult(
            gate="duplication",
            passed=True,
            details="Duplication check deferred to SkillDeduplicationEngine",
        )

    def _check_canonical_mapping(self, record: dict[str, Any]) -> GateResult:
        classification = record.get("classification", "")
        mapped = record.get("supercedes_canonical_id", record.get("family_id", ""))
        if classification and classification not in ("CANONICAL", ""):
            if not mapped:
                return GateResult(
                    gate="canonical_mapping", passed=False,
                    details=f"Non-canonical classification '{classification}' without canonical mapping",
                )
            return GateResult(
                gate="canonical_mapping", passed=True,
                details=f"Non-canonical '{classification}' mapped to canonical reference",
            )
        return GateResult(
            gate="canonical_mapping", passed=True,
            details="Canonical or no classification set",
        )

    def evaluate_promotion(self, record: dict[str, Any]) -> GovernanceReport:
        gates = [
            self._check_traceability(record, "promotion"),
            self._check_evidence_quality(record),
            self._check_confidence(record),
            self._check_ownership(record),
            self._check_review_authority(record),
            self._check_risk(record),
            self._check_canonical_mapping(record),
            self._check_promotion_eligibility(record),
            self._check_independent_review(record),
        ]
        return GovernanceReport(
            record_id=record.get("decision_id", record.get("canonical_id", "unknown")),
            record_type="promotion",
            gates=gates,
            all_passed=all(g.passed for g in gates),
        )

    def _check_promotion_eligibility(self, record: dict[str, Any]) -> GateResult:
        classification = record.get("classification", "")
        status = record.get("status", "")
        if classification != "CANONICAL":
            return GateResult(
                gate="promotion_eligibility", passed=False,
                details=f"Classification '{classification}' not eligible for promotion",
            )
        if status != "CANDIDATE":
            return GateResult(
                gate="promotion_eligibility", passed=False,
                details=f"Status '{status}' not eligible for promotion",
            )
        return GateResult(
            gate="promotion_eligibility", passed=True,
            details="Classification=CANONICAL, status=CANDIDATE",
        )

    def _check_independent_review(self, record: dict[str, Any]) -> GateResult:
        recommender = record.get("recommender", "")
        reviewer = record.get("reviewer", "")
        if not recommender or not reviewer:
            return GateResult(
                gate="independent_review", passed=False,
                details=f"Missing recommender or reviewer: recommender={recommender}, reviewer={reviewer}",
            )
        if recommender == reviewer:
            return GateResult(
                gate="independent_review", passed=False,
                details=f"Recommender '{recommender}' equals reviewer — independence violated",
            )
        return GateResult(
            gate="independent_review", passed=True,
            details=f"Recommender={recommender}, Reviewer={reviewer} — independent",
        )

    def _check_graph_integrity(self, record: dict[str, Any]) -> GateResult:
        metadata = record.get("metadata", {}) or {}
        edges = metadata.get("graph_edges", [])
        if not edges:
            return GateResult(
                gate="graph_integrity", passed=True,
                details="No graph edges to validate",
            )
        invalid = [e for e in edges if not e.get("target_id")]
        return GateResult(
            gate="graph_integrity",
            passed=len(invalid) == 0,
            details=f"{len(edges)} edges, {len(invalid)} invalid" if invalid else f"{len(edges)} valid edges",
        )

    def _check_no_activation(self, record: dict[str, Any]) -> GateResult:
        status = record.get("status", "")
        activation = record.get("activation_status", "")
        if activation and activation != "DISABLED":
            return GateResult(
                gate="no_activation", passed=False,
                details=f"activation_status={activation}, expected DISABLED",
            )
        if status and status not in ("CANDIDATE", "PENDING_REVIEW"):
            return GateResult(
                gate="no_activation", passed=False,
                details=f"status={status}, expected CANDIDATE or PENDING_REVIEW",
            )
        return GateResult(
            gate="no_activation", passed=True,
            details="No activation — status locked",
        )

    def evaluate_validation(self, record: dict[str, Any]) -> GovernanceReport:
        gates = [
            self._check_traceability(record, "capability"),
            self._check_evidence_quality(record),
            self._check_confidence(record),
            self._check_ownership(record),
            self._check_review_authority(record),
            self._check_risk(record),
            self._check_no_auto_promotion(record),
            self._check_canonical_mapping(record),
            self._check_graph_integrity(record),
            self._check_evidence_gate(record),
            self._check_validation_gate(record),
            self._check_maturity_gate(record),
            self._check_promotion_eligibility(record),
            self._check_no_activation(record),
            self._check_no_agent_adoption(record),
            self._check_no_evolution(record),
        ]
        return GovernanceReport(
            record_id=record.get("canonical_id", record.get("capability_id", "unknown")),
            record_type="capability_validation",
            gates=gates,
            all_passed=all(g.passed for g in gates),
        )

    def _check_evidence_gate(self, record: dict[str, Any]) -> GateResult:
        evidence = record.get("evidence", {}) or {}
        if isinstance(evidence, dict):
            score = evidence.get("evidence_score", evidence.get("avg_confidence", 0.0))
        else:
            score = 0.0
        has_evidence = record.get("has_evidence", bool(evidence))
        if has_evidence and score >= 0.3:
            return GateResult(gate="evidence_gate", passed=True,
                              details=f"Evidence sufficient: score={score}")
        return GateResult(gate="evidence_gate", passed=False,
                          details=f"Evidence insufficient: has_evidence={has_evidence}, score={score}")

    def _check_validation_gate(self, record: dict[str, Any]) -> GateResult:
        val_score = record.get("validation_score", record.get("avg_metric", 0.0))
        if val_score >= 0.3:
            return GateResult(gate="validation_gate", passed=True,
                              details=f"Validation score={val_score}")
        return GateResult(gate="validation_gate", passed=False,
                          details=f"Validation insufficient: score={val_score}")

    def _check_maturity_gate(self, record: dict[str, Any]) -> GateResult:
        mat_level = record.get("maturity_level", "EMERGING")
        mat_score = record.get("maturity_score", 0.0)
        if mat_level in ("ESTABLISHED", "ADVANCED", "SOVEREIGN") or mat_score >= 0.5:
            return GateResult(gate="maturity_gate", passed=True,
                              details=f"Maturity {mat_level}, score={mat_score}")
        return GateResult(gate="maturity_gate", passed=False,
                          details=f"Maturity {mat_level}, score={mat_score} — needs ESTABLISHED+")

    def _check_no_agent_adoption(self, record: dict[str, Any]) -> GateResult:
        adoption = record.get("agent_adoption_status", "NOT_ASSIGNED")
        if adoption == "NOT_ASSIGNED":
            return GateResult(gate="no_agent_adoption_gate", passed=True,
                              details="Agent adoption status: NOT_ASSIGNED")
        return GateResult(gate="no_agent_adoption_gate", passed=False,
                          details=f"Agent adoption status: {adoption}")

    def _check_no_evolution(self, record: dict[str, Any]) -> GateResult:
        evolution = record.get("evolution_status", "LOCKED")
        if evolution == "LOCKED":
            return GateResult(gate="no_evolution_gate", passed=True,
                              details="Evolution status: LOCKED")
        return GateResult(gate="no_evolution_gate", passed=False,
                          details=f"Evolution status: {evolution}")
