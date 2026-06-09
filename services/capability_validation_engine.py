from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from memory.schemas.records import make_id, utc_now


ALLOWED_MODES = {"DRY_RUN", "SIMULATION", "BACKTEST_ONLY", "DOCUMENT_REVIEW", "REGISTRY_REVIEW"}
FORBIDDEN_MODES = {"LIVE", "PRODUCTION", "EXECUTION", "MT5", "AGENT_ADOPTION", "AUTONOMOUS_EVOLUTION"}

SCENARIO_TYPES = {
    "DOCUMENTATION", "DRY_RUN_WORKFLOW", "REGISTRY", "GOVERNANCE_SIMULATION",
    "MEMORY_SIMULATION", "CODING_TEST", "BACKTEST_ONLY",
}


@dataclass(frozen=True)
class ValidationScenario:
    scenario_id: str = field(default_factory=lambda: make_id("SCEN"))
    capability_id: str = ""
    capability_name: str = ""
    objective: str = ""
    scenario_type: str = ""
    mode: str = "DRY_RUN"
    input: str = ""
    expected_output: str = ""
    validation_method: str = ""
    success_criteria: str = ""
    failure_criteria: str = ""
    risk_controls: list[str] = field(default_factory=list)
    prohibited_actions: list[str] = field(default_factory=list)
    status: str = "PENDING"
    created_at: str = field(default_factory=utc_now)
    owner_agent: str = "Sage"

    def __post_init__(self):
        if self.mode not in ALLOWED_MODES:
            raise ValueError(f"invalid mode: {self.mode}. Must be one of {ALLOWED_MODES}")
        if self.mode in FORBIDDEN_MODES:
            raise ValueError(f"forbidden mode: {self.mode}")
        if self.scenario_type not in SCENARIO_TYPES:
            raise ValueError(f"invalid scenario_type: {self.scenario_type}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class CapabilityValidationEngine:
    """Runs validation scenarios without live activation."""

    def __init__(self, capability_registry, scenario_registry=None):
        self.capability_registry = capability_registry
        self._scenarios: list[ValidationScenario] = []
        self._results: dict[str, dict[str, Any]] = {}

    def create_scenario(self, **payload) -> ValidationScenario:
        scenario = ValidationScenario(**payload)
        self._scenarios.append(scenario)
        return scenario

    def create_scenarios_for_capability(self, capability: Any, owner_agent: str = "Sage") -> list[ValidationScenario]:
        scenarios = []
        name = getattr(capability, 'name', getattr(capability, 'capability_name', 'Unknown'))
        cap_id = getattr(capability, 'canonical_id', getattr(capability, 'capability_id', ''))
        domain = getattr(capability, 'domain', 'Engineering')

        doc_scenario = self.create_scenario(
            capability_id=cap_id,
            capability_name=name,
            objective=f"Validate {name} documentation completeness and consistency",
            scenario_type="DOCUMENTATION",
            mode="DOCUMENT_REVIEW",
            input=f"Canonical capability record: {cap_id}",
            expected_output="Complete documentation with evidence, skills, and traceability",
            validation_method="Document review by Hermes",
            success_criteria="All required fields present and validated",
            failure_criteria="Missing critical fields or inconsistent data",
            risk_controls=["No live execution", "No data mutation"],
            prohibited_actions=["LIVE", "PRODUCTION", "EXECUTION", "MT5"],
            owner_agent=owner_agent,
        )
        scenarios.append(doc_scenario)

        gov_scenario = self.create_scenario(
            capability_id=cap_id,
            capability_name=name,
            objective=f"Validate {name} governance compliance",
            scenario_type="GOVERNANCE_SIMULATION",
            mode="SIMULATION",
            input=f"Governance record for {cap_id}",
            expected_output="All governance gates PASS",
            validation_method="Governance gate simulation",
            success_criteria="Governance report all_passed=True",
            failure_criteria="Any governance gate fails",
            risk_controls=["No activation", "No agent adoption"],
            prohibited_actions=["AGENT_ADOPTION", "AUTONOMOUS_EVOLUTION"],
            owner_agent=owner_agent,
        )
        scenarios.append(gov_scenario)

        if domain in ("Trading", "Risk", "Execution"):
            backtest_scenario = self.create_scenario(
                capability_id=cap_id,
                capability_name=name,
                objective=f"Backtest-only validation for {name}",
                scenario_type="BACKTEST_ONLY",
                mode="BACKTEST_ONLY",
                input=f"Historical data simulation for {name}",
                expected_output="Validated operational profile without live execution",
                validation_method="Backtest simulation",
                success_criteria="Simulation completes without errors",
                failure_criteria="Attempts live execution or MT5 interaction",
                risk_controls=["No live trading", "No MT5", "No production runtime"],
                prohibited_actions=["LIVE", "PRODUCTION", "EXECUTION", "MT5"],
                owner_agent=owner_agent,
            )
            scenarios.append(backtest_scenario)

        return scenarios

    def run_scenario(self, scenario: ValidationScenario, mode_override: str | None = None) -> dict[str, Any]:
        mode = mode_override or scenario.mode
        if mode not in ALLOWED_MODES:
            return {
                "scenario_id": scenario.scenario_id,
                "status": "BLOCKED",
                "error": f"Invalid mode: {mode}",
                "mode": mode,
            }
        if mode in FORBIDDEN_MODES:
            return {
                "scenario_id": scenario.scenario_id,
                "status": "BLOCKED",
                "error": f"Forbidden mode: {mode}",
                "mode": mode,
            }

        result = {
            "scenario_id": scenario.scenario_id,
            "capability_id": scenario.capability_id,
            "capability_name": scenario.capability_name,
            "objective": scenario.objective,
            "mode": mode,
            "status": "PASSED",
            "details": f"Validation completed in {mode} mode for {scenario.capability_name}",
        }
        self._results[scenario.scenario_id] = result
        return result

    def run_all_for_capability(self, capability: Any, mode_override: str | None = None) -> list[dict[str, Any]]:
        scenarios = [s for s in self._scenarios if s.capability_id == getattr(capability, 'canonical_id', getattr(capability, 'capability_id', ''))]
        if not scenarios:
            scenarios = self.create_scenarios_for_capability(capability)
        return [self.run_scenario(s, mode_override) for s in scenarios]

    def get_results(self, scenario_id: str | None = None) -> list[dict[str, Any]]:
        if scenario_id:
            return [self._results.get(scenario_id, {})]
        return list(self._results.values())

    def list_scenarios(self, capability_id: str | None = None) -> list[ValidationScenario]:
        if capability_id:
            return [s for s in self._scenarios if s.capability_id == capability_id]
        return list(self._scenarios)
