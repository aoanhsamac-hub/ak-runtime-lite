# Lang Lieu Autonomy Assessment

**Date:** 2026-06-08
**Phase:** C - Lang Lieu Reality Audit
**Status:** COMPLETE
**Classification:** EVIDENCE ONLY

---

## Constitutional Requirement (Article 8)

The constitution mandates:
```
Issue → Plan → Code Draft → Review → Test → Sage Review → Janus Approval → Deploy
```

This is an 8-step governed pipeline.

---

## Current State Assessment

### Infrastructure Evidence

| Component | Location | Status | Function |
|-----------|----------|--------|----------|
| `LangLieuDevOrchestrator` | `agents/lang_lieu/dev_orchestrator.py` | EXISTS | Wraps OpenCode connector |
| `OpenCodeConnector` | `connectors/opencode_connector.py` | EXISTS | Adapter-only mode |
| `boundaries.md` | `agents/lang_lieu/boundaries.md` | EXISTS | Governs allowed actions |

### Mode Analysis

From `opencode_connector.py` line 21:
```python
mode = "adapter_only"
```

This is a **critical constraint**: all operations are adapter-only, never direct execution.

### Execution Evidence

From `opencode_connector.py`:

1. **Line 35-45**: Protected paths always BLOCK unless Sage + Approval
2. **Line 56**: `"execution_enabled": False` - ALWAYS FALSE
3. **Line 47**: Returns `UNAVAILABLE` if executable not found (safe fail-closed)
4. **Line 57**: Reason text confirms "direct execution disabled"

### Protected Paths

From `opencode_connector.py` lines 9-17:
- `.env`
- `credentials`
- `sovereign`
- `governance`
- `risk_kernel`
- `execution`
- `security`

ANY of these in target paths = BLOCKED.

---

## What Lang Lieu CAN Do Today

1. **Prepare Task Requests**: Use `LangLieuDevOrchestrator.run_task()` to prepare requests
2. **Get Path Validation**: Connector validates protected paths
3. **Receive Governance Decision**: Get risk level and approval requirements
4. **Report Prepared Requests**: Return structure includes `implementation_report`
5. **NO DIRECT EXECUTION**: All paths lead to adapter requests only

## What Lang Lieu CANNOT Do Today

1. **Cannot execute code directly**
2. **Cannot modify files without OpenCode executable**
3. **Cannot bypass protected paths**
4. **Cannot skip Sage review/approval for protected areas**
5. **Cannot deploy without explicit governance gate**

---

## Dependency Analysis

### Current Dependencies

| Dependency | Required | Evidence |
|------------|----------|----------|
| OpenCode Executable | NO | Returns UNAVAILABLE if missing (line 47) |
| Sage Review | CONDITIONAL | Required for protected paths only |
| Approval Gate | CONDITIONAL | Required for protected paths only |
| Human Operator | NO | Fully automated adapter flow |
| Git | NO | Connector uses shutil which is stdlib |
| Reviewers | NO | Governs itself via connector |

---

## Autonomous Coding Maturity

### Scoring (0-5)

| Level | Description | Evidence | Score |
|-------|-------------|----------|-------|
| 0 | Documentation Only | ❌ Code exists | ❌ |
| 1 | Manual Assisted | ❌ No human-in-loop | ❌ |
| 2 | Tool Assisted | ✅ OpenCode adapter exists | ✅ |
| 3 | Sandbox Autonomous | ❌ No sandbox execution | ❌ |
| 4 | Governed Autonomous | ✅ Governance gates exist | ✅ |
| 5 | Production Autonomous | ❌ No production deployment | ❌ |

**Score: 2/5** (Tool Assisted)

### Gate Evidence

From `opencode_connector.py`:

1. **Risk Classification**: `evaluate_proposal()` provides risk level
2. **Protected Path Detection**: Automatic blocking for sensitive paths
3. **Approval Requirements**: Derived from target paths + risk level
4. **FAIL-CLOSED Design**: Missing executable = UNAVAILABLE (not error)

---

## Reality Decision

**Status: PARTIAL**

### Evidence-Based Assessment

- ✅ Code infrastructure exists (dev_orchestrator.py, opencode_connector.py)
- ✅ Governance gates are operational (evaluate_proposal integration)
- ✅ Safe-fail design (adapter_only, protected paths, execution_enabled=False)
- ✅ No constitutional violations (respects Article 8 mandatory review)
- ❌ Full pipeline automation (Issue→Plan→Deploy) not implemented
- ❌ No sandbox execution capability

### Autonomous Coding Governance

The current implementation:
- Follows Article 8 requirements (no direct execution)
- Implements Governance Gate correctly
- Blocks protected paths without approval
- Cannot fabricate or modify without governance

This is **compliant but incomplete** - the pipeline exists as adapter requests but not as full workflow automation.

---

## Conclusion

**Lang Lieu Maturity: PARTIAL (Level 2/5)**

Current implementation satisfies constitutional requirements (cannot self-deploy, must use governance) but does not provide the full 8-step automated pipeline. This is evidence-based reality, not marketing.

The system is **NOT_READY** for autonomous production deployment but is **READY** for governed tool-assisted operations.