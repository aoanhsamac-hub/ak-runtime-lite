# AK-RUNTIME-LITE Production Deployment Instructions

## Prerequisites
- VPS with Windows, MT5 Terminal, Tailscale
- All service files from `D:\AK\services\` copied to VPS
- Python 3.12+ with `cryptography`, `psutil`, `python-telegram-bot`, `requests`, `MetaTrader5`

## Step 1: Copy Deploy Package to VPS
Using Tailscale or any file transfer, copy the `D:\AK\deploy\` folder to the VPS.

## Step 2: Run VPS Optimization (Optional but Recommended)
```powershell
# Run as Administrator on VPS
.\deploy\vps_optimize.ps1
```

## Step 3: Set Environment Variables on VPS
```powershell
[Environment]::SetEnvironmentVariable("TELEGRAM_BOT_TOKEN", "your_token_here", "User")
[Environment]::SetEnvironmentVariable("TELEGRAM_WHITELIST", "user_id_1,user_id_2", "User")
[Environment]::SetEnvironmentVariable("AK_MASTER_SECRET", "your_master_password", "User")
```

## Step 4: Run Full Deployment
```powershell
.\deploy\deploy_all.ps1
```

This executes all 8 phases + reviewer loop sequentially.

## Step 5: Review Output
All reports are written to `.\deploy\`:
- PRODUCTION_DEPLOYMENT_PRECHECK_REPORT.md
- PRODUCTION_SERVICE_DEPLOYMENT_REPORT.md
- PRODUCTION_MT5_VALIDATION_REPORT.md
- PRODUCTION_TELEGRAM_VALIDATION_REPORT.md
- PRODUCTION_SCHEDULER_ACTIVATION_REPORT.md
- PRODUCTION_SUPERVISOR_REPORT.md
- DAY1_RUNTIME_BASELINE_REPORT.md
- Q1_AUDIT_DAY1_ACTIVATION_REPORT.md
- PRODUCTION_DEPLOYMENT_REVIEWER_LOOP_REPORT.md

## Step 6: Read Final Decision
Open `PRODUCTION_DEPLOYMENT_REVIEWER_LOOP_REPORT.md`
- **GO** → Q1-AUDIT-30D DAY-1 officially begins
- **NO-GO** → Fix issues and re-run

## Individual Phase Scripts
You can also run phases individually:
```powershell
.\deploy\phase_a_precheck.ps1
.\deploy\phase_b_deploy_services.ps1
.\deploy\phase_c_mt5_validation.ps1
.\deploy\phase_d_telegram_validation.ps1
.\deploy\phase_e_scheduler_activation.ps1
.\deploy\phase_f_supervisor_validation.ps1
.\deploy\phase_g_baseline.ps1
.\deploy\phase_h_q1_activation.ps1
.\deploy\reviewer_loop.ps1
```
