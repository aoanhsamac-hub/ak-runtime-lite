# Deployment Recommendation

## Recommendation: APPROVED WITH LIMITATIONS

## Deployment Steps

### Phase 1: Foundation (Day 0)
1. Copy all 15 service files to `D:\AK\services\` on target VPS
2. Copy 8 test files to `D:\AK\tests\`
3. Copy reports to `D:\AK\docs\reports\`
4. Install Python dependencies:
   ```powershell
   pip install cryptography psutil python-telegram-bot requests
   ```
5. Create secrets vault:
   ```powershell
   $env:SECRET_MASTER_PASSWORD = "your-master-password"
   python services/secret_manager.py  (CLI initialization)
   ```
6. Set env vars: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_WHITELIST`, `SECRET_MASTER_PASSWORD`
7. Run credential validation:
   ```python
   from services.credential_validator import CredentialValidator
   CredentialValidator().validate_all()
   ```

### Phase 2: VPS Optimization (Day 0)
1. Disable Search Indexing
2. Disable SysMain
3. Disable Diagnostic Services
4. Configure Defender exclusions
5. Set power plan to High Performance
6. Verify RAM > 500 MB available

### Phase 3: Startup (Day 1)
1. Start scheduler:
   ```python
   from services.kingdom_scheduler import RuntimeScheduler
   scheduler = RuntimeScheduler()
   scheduler.start()
   ```
2. Start supervisor:
   ```python
   from services.runtime_supervisor import RuntimeSupervisor
   supervisor = RuntimeSupervisor()
   supervisor.start()
   ```
3. Start Telegram gateway:
   ```python
   from services.telegram_gateway import start_gateway
   start_gateway()
   ```
4. Verify all components healthy via `/runtime` command or health API
5. Run test suite to verify

### Phase 4: Verification (Day 1-7)
1. Monitor RAM hourly (should stay above 200 MB)
2. Verify backup creation (daily)
3. Verify Telegram commands work
4. Test stop conditions by simulating failures
5. Generate and review first week's runtime report

## Rollback Plan
1. Stop all services (supervisor, scheduler, gateway)
2. Restore any corrupted files from backup
3. Revert VPS optimizations if needed:
   ```powershell
   Set-Service -Name WSearch -StartupType Automatic
   Set-Service -Name SysMain -StartupType Automatic
   ```
4. Verify system returns to baseline

## Monitoring
- **RAM**: RuntimeGuard hourly check (threshold: 200 MB)
- **Heartbeat**: 30s interval, 3-beat timeout (90s)
- **Backups**: Daily, with 14-day retention
- **Telegram**: Manual health check via /runtime command

## Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| RAM exhaustion | Medium | High | Stop condition at 200 MB |
| MT5 disconnect | Low | Medium | Alert + restart |
| Telegram token expiry | Low | Medium | Env var rotation |
| Vault password lost | Low | High | Regular vault backups |
