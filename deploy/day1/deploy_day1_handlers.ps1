param([string]$ReportPath = ".")

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== AK-Q1-DAY1-HANDLERS-DEPLOYMENT ===" -ForegroundColor Cyan
Write-Host "Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan

function Log { param([string]$msg) Write-Host "$(Get-Date -Format 'HH:mm:ss') $msg" }

Log "=== PHASE A: IRIS FORECAST HANDLER ==="
try { & "$scriptDir\phase_a_forecast_handler.ps1" -ReportPath "$ReportPath" } catch { Log "PHASE A FAILED: $_"; exit 1 }

Log "=== PHASE B: REALITY CHECK HANDLER ==="
try { & "$scriptDir\phase_b_reality_handler.ps1" -ReportPath "$ReportPath" } catch { Log "PHASE B FAILED: $_"; exit 1 }

Log "=== PHASE C: LESSON UPDATE HANDLER ==="
try { & "$scriptDir\phase_c_lesson_handler.ps1" -ReportPath "$ReportPath" } catch { Log "PHASE C FAILED: $_"; exit 1 }

Log "=== PHASE D: EVIDENCE COLLECTION HANDLER ==="
try { & "$scriptDir\phase_d_evidence_handler.ps1" -ReportPath "$ReportPath" } catch { Log "PHASE D FAILED: $_"; exit 1 }

Log "=== PHASE E: DAILY KACE SCORECARD HANDLER ==="
try { & "$scriptDir\phase_e_kace_handler.ps1" -ReportPath "$ReportPath" } catch { Log "PHASE E FAILED: $_"; exit 1 }

Log "=== PHASE F: DAILY EVIDENCE SUMMARY ==="
try { & "$scriptDir\phase_f_evidence_summary.ps1" -ReportPath "$ReportPath" } catch { Log "PHASE F FAILED: $_"; exit 1 }

Log "=== PHASE G: TELEGRAM INTEGRATION ==="
try { & "$scriptDir\phase_g_telegram_integration.ps1" -ReportPath "$ReportPath" } catch { Log "PHASE G FAILED: $_"; exit 1 }

Log "=== PHASE H: OPERATIONAL VALIDATION ==="
try { & "$scriptDir\phase_h_operational_validation.ps1" -ReportPath "$ReportPath" } catch { Log "PHASE H FAILED: $_"; exit 1 }

Log "=== PHASE I: DAY-1 BASELINE EVIDENCE ==="
try { & "$scriptDir\phase_i_day1_baseline.ps1" -ReportPath "$ReportPath" } catch { Log "PHASE I FAILED: $_"; exit 1 }

Log "=== PHASE J: REVIEWER LOOP ==="
try { & "$scriptDir\phase_j_reviewer_loop.ps1" -ReportPath "$ReportPath" } catch { Log "PHASE J FAILED: $_"; exit 1 }

Log "=== DAY-1 HANDLERS DEPLOYMENT COMPLETE ==="
Write-Host "All phases complete. Reports in: $ReportPath" -ForegroundColor Green
