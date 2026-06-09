# Q1 Audit Evidence Index

**Prepared:** 2026-06-08
**Status:** INDEX — References all PSOP-04 evidence registries.

---

## Evidence Registry Index

| Registry | Location | Evidence Type | Collector Service |
|----------|----------|---------------|-------------------|
| CAPABILITY_USAGE_REGISTRY.yaml | docs/registries/ | Capability usage events | capability_usage_collector.py |
| CAPABILITY_VALUE_REGISTRY.yaml | docs/registries/ | Capability value evidence | capability_value_collector.py |
| CAPABILITY_ROI_REGISTRY.yaml | docs/registries/ | Capability ROI evidence | capability_roi_collector.py |
| TREASURY_EVIDENCE_REGISTRY.yaml | docs/registries/ | Treasury event evidence | treasury_evidence_collector.py |
| TRADING_EVIDENCE_REGISTRY.yaml | docs/registries/ | Trading observation evidence | forecast_evidence_collector.py, signal_evidence_collector.py, zone_evidence_collector.py |
| PROGRAM_EVIDENCE_REGISTRY.yaml | docs/registries/ | Program progress evidence | program_evidence_collector.py |

---

## Evidence Source Map

### Capability Evidence Chain

```
Usage Evidence (CAPABILITY_USAGE_REGISTRY.yaml)
    ↓ references usage_record_id → memory/usage_registry.py (JSONL) → ak_capability_usage (LanceDB)
Value Evidence (CAPABILITY_VALUE_REGISTRY.yaml)
    ↓ wraps capability_value_engine.py
ROI Evidence (CAPABILITY_ROI_REGISTRY.yaml)
    ↓ references roi_record_id → memory/capability_roi_registry.py (LanceDB)
```

### Treasury Evidence Chain

```
Treasury Events (TREASURY_EVIDENCE_REGISTRY.yaml)
    ↓ treasury_impact_id → treasury_impact_tracker.py → TREASURY_IMPACT_REGISTRY.yaml
```

### Trading Evidence Chain

```
Trading Observations (TRADING_EVIDENCE_REGISTRY.yaml)
    ↓ wraps PSOP-03 trading monitors → all INITIALIZED (no real trading)
```

### Program Evidence Chain

```
Program Evidence (PROGRAM_EVIDENCE_REGISTRY.yaml)
    ↓ reads goal_manager.get_goal_summary() + program_manager.get_program_summary()
```

---

## Audit Evidence Sources

| Audit Type | Evidence Source | Compiler Method |
|------------|----------------|-----------------|
| Treasury Audit | TREASURY_EVIDENCE_REGISTRY.yaml | audit_evidence_compiler.compile_treasury_audit() |
| Capability Audit | CAPABILITY_USAGE_REGISTRY.yaml, CAPABILITY_VALUE_REGISTRY.yaml, CAPABILITY_ROI_REGISTRY.yaml | audit_evidence_compiler.compile_capability_audit() |
| Program Audit | PROGRAM_EVIDENCE_REGISTRY.yaml | audit_evidence_compiler.compile_program_audit() |
| Governance Audit | All 6 evidence registries | audit_evidence_compiler.compile_governance_audit() |

---

## Compilation

`services/audit_evidence_compiler.py` provides:

- `compile_treasury_audit()` → Treasury evidence summary
- `compile_capability_audit()` → Capability evidence summary
- `compile_program_audit()` → Program evidence summary
- `compile_governance_audit()` → Registry completeness check
- `compile_all()` → Complete audit compilation

---

*Index prepared by PSOP-04 Audit Evidence Preparation. Actual audit execution requires Q1 data accumulation.*
