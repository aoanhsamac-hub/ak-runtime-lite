from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from memory.lancedb_adapter import LanceDBAdapter
from memory.schemas.records import make_id, utc_now


VALIDATION_TYPES = {
    "unit", "integration", "governance", "risk", "performance", "audit"
}


@dataclass
class ValidationResult:
    passed: bool
    validation_type: str
    score: float = 0.0
    details: str = ""
    blocking_issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)


class SkillValidationEngine:
    def __init__(self, adapter: LanceDBAdapter, skill_registry: Any, governance_gate: Any = None):
        self.adapter = adapter
        self.skill_registry = skill_registry
        self.governance_gate = governance_gate
        self._results: list[dict] = []

    def validate_skill(self, skill_id: str, validation_types: set[str] | None = None) -> ValidationResult:
        skill = self.skill_registry.get(skill_id)
        types_to_run = validation_types or VALIDATION_TYPES
        all_passed = True
        combined_issues = []
        combined_warnings = []

        if "unit" in types_to_run:
            result = self._unit_validation(skill)
            all_passed = all_passed and result.passed
            combined_issues.extend(result.blocking_issues)
            combined_warnings.extend(result.warnings)

        if "integration" in types_to_run:
            result = self._integration_validation(skill)
            all_passed = all_passed and result.passed
            combined_issues.extend(result.blocking_issues)
            combined_warnings.extend(result.warnings)

        if "governance" in types_to_run:
            result = self._governance_validation(skill)
            all_passed = all_passed and result.passed
            combined_issues.extend(result.blocking_issues)
            combined_warnings.extend(result.warnings)

        if "risk" in types_to_run:
            result = self._risk_validation(skill)
            all_passed = all_passed and result.passed
            combined_issues.extend(result.blocking_issues)
            combined_warnings.extend(result.warnings)

        if "performance" in types_to_run:
            result = self._performance_validation(skill)
            all_passed = all_passed and result.passed
            combined_issues.extend(result.blocking_issues)
            combined_warnings.extend(result.warnings)

        if "audit" in types_to_run:
            result = self._audit_validation(skill)
            all_passed = all_passed and result.passed
            combined_issues.extend(result.blocking_issues)
            combined_warnings.extend(result.warnings)

        score = sum(1 for t in types_to_run) / len(VALIDATION_TYPES)

        return ValidationResult(
            passed=all_passed,
            validation_type="full",
            score=score,
            details=f"Validated {len(types_to_run)} types: {', '.join(sorted(types_to_run))}",
            blocking_issues=combined_issues,
            warnings=combined_warnings,
            evidence_refs=[skill.skill_id],
        )

    def _unit_validation(self, skill) -> ValidationResult:
        issues = []
        from memory.schemas.records import SKILL_LIFECYCLE_STAGES
        if skill.lifecycle_stage not in SKILL_LIFECYCLE_STAGES:
            issues.append(f"Invalid lifecycle_stage: {skill.lifecycle_stage}")
        if not skill.name:
            issues.append("Missing name")
        if not skill.description:
            issues.append("Missing description")
        if not skill.owner_agent:
            issues.append("Missing owner_agent")
        return ValidationResult(
            passed=len(issues) == 0,
            validation_type="unit",
            blocking_issues=issues,
        )

    def _integration_validation(self, skill) -> ValidationResult:
        issues = []
        warnings = []
        if skill.dependencies:
            for dep_id in skill.dependencies:
                try:
                    self.skill_registry.get(dep_id)
                except KeyError:
                    issues.append(f"Dependency skill not found: {dep_id}")
        primary_ok = all(u in skill.allowed_agents for u in skill.primary_users if u)
        secondary_ok = all(u in skill.allowed_agents for u in skill.secondary_users if u)
        if not primary_ok:
            issues.append("Some primary users not in allowed_agents")
        if not secondary_ok:
            warnings.append("Some secondary users not in allowed_agents")
        return ValidationResult(
            passed=len(issues) == 0,
            validation_type="integration",
            blocking_issues=issues,
            warnings=warnings,
        )

    def _governance_validation(self, skill) -> ValidationResult:
        issues = []
        if self.governance_gate:
            try:
                report = self.governance_gate.evaluate_skill(skill.to_dict())
                if not report.all_passed:
                    issues.append("Governance gates failed")
            except Exception:
                pass
        if not skill.governance_requirements:
            issues.append("Missing governance_requirements")
        if skill.forbidden_users and skill.owner_agent in skill.forbidden_users:
            issues.append("Owner cannot be in forbidden_users")
        return ValidationResult(
            passed=len(issues) == 0,
            validation_type="governance",
            blocking_issues=issues,
        )

    def _risk_validation(self, skill) -> ValidationResult:
        issues = []
        valid_risk_levels = {"LEVEL_0_SOVEREIGN", "LEVEL_1_MODERATE", "LEVEL_2_HIGH", "LEVEL_3_CRITICAL", "LOW", "MEDIUM", "HIGH"}
        if skill.risk_level not in valid_risk_levels:
            issues.append(f"Invalid risk_level: {skill.risk_level}")
        if skill.risk_level in ("LEVEL_3_CRITICAL", "CRITICAL") and not skill.stop_conditions:
            issues.append("CRITICAL risk requires stop_conditions")
        if skill.risk_level in ("LEVEL_2_HIGH", "HIGH") and not skill.retirement_conditions:
            issues.append("HIGH risk requires retirement_conditions")
        if not skill.stop_conditions:
            issues.append("stop_conditions is required")
        return ValidationResult(
            passed=len(issues) == 0,
            validation_type="risk",
            blocking_issues=issues,
        )

    def _performance_validation(self, skill) -> ValidationResult:
        issues = []
        warnings = []
        if not skill.performance_metrics:
            warnings.append("No performance_metrics defined")
        if skill.test_cases:
            if len(skill.test_cases) < 1:
                issues.append("At least 1 test case required")
        else:
            warnings.append("No test_cases defined")
        return ValidationResult(
            passed=len(issues) == 0,
            validation_type="performance",
            blocking_issues=issues,
            warnings=warnings,
        )

    def _audit_validation(self, skill) -> ValidationResult:
        issues = []
        if not skill.audit_requirements:
            issues.append("Missing audit_requirements")
        if not skill.source_hash:
            issues.append("Missing source_hash")
        if not skill.created_at:
            issues.append("Missing created_at")
        return ValidationResult(
            passed=len(issues) == 0,
            validation_type="audit",
            blocking_issues=issues,
        )

    def validate_batch(self, skill_ids: list[str]) -> list[ValidationResult]:
        return [self.validate_skill(sid) for sid in skill_ids]

    def report(self, skill_id: str) -> dict:
        result = self.validate_skill(skill_id)
        record = {
            "skill_id": skill_id,
            "passed": result.passed,
            "score": result.score,
            "blocking_issues": result.blocking_issues,
            "warnings": result.warnings,
            "validated_at": utc_now(),
        }
        self._results.append(record)
        self.adapter.insert("ak_skill_validations", [record])
        return record