import pytest
from services.capability_validation_engine import CapabilityValidationEngine, ValidationScenario


class TestCapabilityValidationEngine:
    def test_create_scenario(self):
        engine = CapabilityValidationEngine(None)
        s = engine.create_scenario(
            capability_id="CCAP-001", capability_name="Test Cap",
            objective="Test doc validation", scenario_type="DOCUMENTATION",
            mode="DOCUMENT_REVIEW", input="test input",
            expected_output="test output", validation_method="review",
            success_criteria="pass", failure_criteria="fail",
            owner_agent="Sage",
        )
        assert s.scenario_id.startswith("SCEN-")
        assert s.mode == "DOCUMENT_REVIEW"
        assert s.status == "PENDING"

    def test_forbidden_mode_raises(self):
        with pytest.raises(ValueError, match="invalid mode"):
            ValidationScenario(
                capability_id="CCAP-001", capability_name="T",
                objective="O", scenario_type="DOCUMENTATION",
                mode="LIVE", owner_agent="Sage",
            )

    def test_run_scenario_dry_run(self):
        engine = CapabilityValidationEngine(None)
        s = engine.create_scenario(
            capability_id="CCAP-001", capability_name="Test",
            objective="Test", scenario_type="DRY_RUN_WORKFLOW",
            mode="DRY_RUN", input="in", expected_output="out",
            validation_method="run", success_criteria="ok",
            failure_criteria="fail", owner_agent="Sage",
        )
        result = engine.run_scenario(s)
        assert result["status"] == "PASSED"
        assert result["mode"] == "DRY_RUN"

    def test_run_scenario_forbidden_mode_blocked(self):
        engine = CapabilityValidationEngine(None)
        s = engine.create_scenario(
            capability_id="CCAP-001", capability_name="Test",
            objective="Test", scenario_type="DRY_RUN_WORKFLOW",
            mode="DRY_RUN", input="in", expected_output="out",
            validation_method="run", success_criteria="ok",
            failure_criteria="fail", owner_agent="Sage",
        )
        result = engine.run_scenario(s, mode_override="LIVE")
        assert result["status"] == "BLOCKED"

    def test_create_scenarios_for_capability(self, cap_candidate_registry):
        from memory.capability_pipeline.schemas import CapabilityCandidateRecord
        cap = cap_candidate_registry.create(
            name="Trading Cap", description="Test",
            domain="Trading", owner_agent="Sage",
            confidence_score=0.8, evidence={},
        )
        engine = CapabilityValidationEngine(cap_candidate_registry)
        scenarios = engine.create_scenarios_for_capability(cap)
        assert len(scenarios) >= 2
        types = {s.scenario_type for s in scenarios}
        assert "DOCUMENTATION" in types
        assert "GOVERNANCE_SIMULATION" in types

    def test_list_scenarios(self):
        engine = CapabilityValidationEngine(None)
        engine.create_scenario(
            capability_id="CCAP-001", capability_name="A",
            objective="O", scenario_type="DOCUMENTATION",
            mode="DOCUMENT_REVIEW", owner_agent="Sage",
        )
        engine.create_scenario(
            capability_id="CCAP-002", capability_name="B",
            objective="O", scenario_type="REGISTRY",
            mode="REGISTRY_REVIEW", owner_agent="Sage",
        )
        assert len(engine.list_scenarios()) == 2
        assert len(engine.list_scenarios(capability_id="CCAP-001")) == 1
