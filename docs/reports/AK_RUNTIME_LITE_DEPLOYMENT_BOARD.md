# AK-RUNTIME-LITE DEPLOYMENT READINESS BOARD

## Authority
Janus

## Board Members
- Yết Kiêu (Infrastructure, Security, Capacity)
- Hermes (Evidence, Backup)
- Iris (MT5 Safety)
- Sage (Stop Conditions, Governance)

## Phase Summary

| Phase | Report | Result |
|-------|--------|--------|
| A - Infrastructure | RUNTIME_PREFLIGHT_INFRASTRUCTURE_REPORT.md | PASS (1 Warning) |
| B - Capacity | RUNTIME_PREFLIGHT_CAPACITY_REPORT.md | APPROVED (PC) / NOT_APPROVED (VPS) |
| C - Telegram | RUNTIME_PREFLIGHT_TELEGRAM_REPORT.md | FAIL |
| D - MT5 Safety | RUNTIME_PREFLIGHT_MT5_SAFETY_REPORT.md | PASS |
| E - Scheduler | RUNTIME_PREFLIGHT_SCHEDULER_REPORT.md | FAIL |
| F - Evidence | RUNTIME_PREFLIGHT_EVIDENCE_REPORT.md | PASS |
| G - Security | RUNTIME_PREFLIGHT_SECURITY_REPORT.md | FAIL |
| H - Recovery | RUNTIME_PREFLIGHT_RECOVERY_REPORT.md | FAIL |
| I - Backup | RUNTIME_PREFLIGHT_BACKUP_REPORT.md | FAIL |
| J - Stop Conditions | RUNTIME_PREFLIGHT_STOP_CONDITIONS_REPORT.md | FAIL |

## Overall Result: NOT_APPROVED

## Blocker Summary

| ID | Blocker | Phase | Severity |
|----|---------|-------|----------|
| B-1 | Telegram gateway completely unimplemented | C | CRITICAL |
| B-2 | Required scheduler tasks not registered | E | CRITICAL |
| B-3 | No credential/secrets storage | G | CRITICAL |
| B-4 | No crash recovery/supervisor | H | CRITICAL |
| B-5 | No backup strategy | I | CRITICAL |
| B-6 | Stop conditions not implemented | J | CRITICAL |
| B-7 | VPS capacity insufficient (333 MB available, ~530 MB required) | B | CRITICAL |

## Warnings

| ID | Warning | Phase |
|----|---------|-------|
| W-1 | ZeroClaw not installed on dev environment | A |
| W-2 | Windows Firewall DefaultInboundAction not configured to Block | G |
| W-3 | SMB ports exposed on LAN | G |
| W-4 | Evidence is in-memory only (lost on restart) | I |
| W-5 | No emergency stop procedure documented | J |

## Required Fixes Before Deployment

1. **Implement Telegram Bot** - Token storage, whitelist, command routing (6 commands), auth, alerts.
2. **Implement Scheduler Tasks** - Hourly (Iris Forecast, Reality Check, Lesson Update), Daily (KACE Review, Evidence Summary, Health Check), Weekly (Kingdom Review). Add hourly cadence support.
3. **Implement Credential Storage** - .env with icacls permissions, credential rotation policy.
4. **Implement Supervisor** - Watchdog process with auto-restart (max 3 retries), heartbeat, health check, failure escalation.
5. **Implement Backups** - Automated schedule, evidence persistence (LanceDB), rotational backup, disaster recovery plan.
6. **Implement Stop Conditions** - RAM monitor, MT5 disconnect handler, scheduler failure detector, evidence integrity checker, duplicate scheduler detection, governance violation enforcement.
7. **VPS Resource Upgrade or Runtime Optimization** - Reduce runtime memory footprint or upgrade VPS.

## Optional Improvements

1. Configure Windows Firewall DefaultInboundAction to Block.
2. Block SMB ports 139/445 on external interfaces.
3. Add backup verification (checksum validation).
4. Document emergency stop procedure.
5. Add Rate Limiting to Telegram commands.
