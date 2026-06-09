<#
.SYNOPSIS
AK-RUNTIME-LITE Production VPS Deployment — Master Script
Runs all phases A-H + Reviewer Loop sequentially.
Execute this on the target VPS.
#>

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$logFile = "$scriptDir\deploy_log.txt"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host "=== AK-RUNTIME-LITE PRODUCTION DEPLOYMENT ===" -ForegroundColor Cyan
Write-Host "Started: $timestamp" -ForegroundColor Cyan
Write-Host ""

function Log { param([string]$msg) "$(Get-Date -Format 'HH:mm:ss') $msg" | Out-File -Append $logFile; Write-Host $msg }

Log "=== PHASE A: VPS PRECHECK ==="
try { & "$scriptDir\phase_a_precheck.ps1" -ReportPath "$scriptDir" } catch { Log "PHASE A FAILED: $_"; exit 1 }

Log "=== PHASE B: SERVICE DEPLOYMENT ==="
try { & "$scriptDir\phase_b_deploy_services.ps1" -ReportPath "$scriptDir" } catch { Log "PHASE B FAILED: $_"; exit 1 }

Log "=== PHASE C: MT5 INTEGRATION ==="
try { & "$scriptDir\phase_c_mt5_validation.ps1" -ReportPath "$scriptDir" } catch { Log "PHASE C FAILED: $_"; exit 1 }

Log "=== PHASE D: TELEGRAM VALIDATION ==="
try { & "$scriptDir\phase_d_telegram_validation.ps1" -ReportPath "$scriptDir" } catch { Log "PHASE D FAILED: $_"; exit 1 }

Log "=== PHASE E: SCHEDULER ACTIVATION ==="
try { & "$scriptDir\phase_e_scheduler_activation.ps1" -ReportPath "$scriptDir" } catch { Log "PHASE E FAILED: $_"; exit 1 }

Log "=== PHASE F: SUPERVISOR VALIDATION ==="
try { & "$scriptDir\phase_f_supervisor_validation.ps1" -ReportPath "$scriptDir" } catch { Log "PHASE F FAILED: $_"; exit 1 }

Log "=== PHASE G: BASELINE CAPTURE ==="
try { & "$scriptDir\phase_g_baseline.ps1" -ReportPath "$scriptDir" } catch { Log "PHASE G FAILED: $_"; exit 1 }

Log "=== PHASE H: Q1-AUDIT-30D ACTIVATION ==="
try { & "$scriptDir\phase_h_q1_activation.ps1" -ReportPath "$scriptDir" } catch { Log "PHASE H FAILED: $_"; exit 1 }

Log "=== REVIEWER LOOP ==="
try { & "$scriptDir\reviewer_loop.ps1" -ReportPath "$scriptDir" } catch { Log "REVIEWER LOOP FAILED: $_"; exit 1 }

Log "=== DEPLOYMENT COMPLETE ==="
Write-Host "All phases complete. See reports in: $scriptDir" -ForegroundColor Green
Write-Host "Decision report: $scriptDir\PRODUCTION_DEPLOYMENT_REVIEWER_LOOP_REPORT.md" -ForegroundColor Yellow
