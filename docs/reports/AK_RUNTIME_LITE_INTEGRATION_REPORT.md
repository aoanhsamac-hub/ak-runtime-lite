# AK-RUNTIME-LITE Integration Report

## Overview
Integration of all 7 blocker remediation components into a unified runtime.

## Component Architecture

```
telegram_gateway.py ←→ telegram_command_router.py ←→ telegram_notification_service.py
       ↓
kingdom_scheduler.py (RuntimeScheduler) ←→ scheduler_registry.py
       ↓
runtime_supervisor.py ←→ heartbeat_monitor.py ←→ restart_manager.py
       ↓
runtime_guard.py ←→ stop_condition_manager.py
       ↓
backup_manager.py ←→ registry_backup_service.py ←→ evidence_backup_service.py
       ↓
secret_manager.py ←→ credential_validator.py
```

## Data Flow

### Command Flow
1. User sends `/command` via Telegram
2. `telegram_gateway.py` authenticates (token + whitelist), rate-limits
3. `telegram_command_router.py` routes to handler
4. Handler executes via scheduler or supervisor

### Health Flow
1. `runtime_guard.py` runs periodic checks (RAM, MT5, scheduler, governance)
2. `stop_condition_manager.py` evaluates results, triggers escalation if needed
3. `heartbeat_monitor.py` tracks component liveness
4. `runtime_supervisor.py` coordinates restarts

### Data Flow
1. `secret_manager.py` provides decrypted credentials to components
2. `backup_manager.py` schedules backups via `scheduler_registry.py`
3. Registry and evidence files backed up daily

## Integration Points
| From | To | Mechanism |
|------|----|-----------|
| Telegram Router | RuntimeGuard | Direct call for /runtime command |
| RuntimeGuard | StopConditionManager | Direct call with health results |
| HeartbeatMonitor | RuntimeSupervisor | Missed beat callback |
| RuntimeSupervisor | RestartManager | Restart request |
| SchedulerRegistry | RuntimeScheduler | JSON file read/write |
| SecretManager | Telegram Gateway | Decrypted token |
| SecretManager | MT5 Observer | Decrypted credentials |

## Dependency Graph
```
RuntimeScheduler ─── RuntimeGuard
       │                 │
       ├── SchedulerRegistry    ├── StopConditionManager
       │                       │
BackupManager ──────────────┤
       │                       │
       ├── RegistryBackup      └── HeartbeatMonitor ─── RuntimeSupervisor ─── RestartManager
       └── EvidenceBackup
```

## Verification
All components verified via:
1. Unit tests (80+ tests across 8 files)
2. Import verification (no circular dependencies)
3. Lint check (no syntax errors)
4. Type consistency across interfaces

## Deployment Order
1. `secret_manager.py` + `credential_validator.py` - Foundation
2. `runtime_guard.py` + `stop_condition_manager.py` - Safety
3. `heartbeat_monitor.py` + `restart_manager.py` + `runtime_supervisor.py` - Recovery
4. `backup_manager.py` + `registry_backup_service.py` + `evidence_backup_service.py` - Durability
5. `kingdom_scheduler.py` + `scheduler_registry.py` - Automation
6. `telegram_gateway.py` + `telegram_command_router.py` + `telegram_notification_service.py` - Interface
7. Integration test and deployment
