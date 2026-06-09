# register_runtime_tasks_vps.ps1 — Tao scheduled tasks cho runtime tren VPS (FIXED v2)
$ErrorActionPreference = "Continue"
$akPath = "C:\AK"
$fixPath = "$akPath\deploy\fix"
$syncPath = "$akPath\deploy\sync"

Write-Host "=== AK-RUNTIME :: REGISTER TASKS v2 ===" -ForegroundColor Cyan

New-Item -ItemType Directory -Path $fixPath -Force | Out-Null

# Xoa task cu neu co
Write-Host "[1/5] Xoa task cu..." -ForegroundColor Yellow
$oldTasks = @("AK_Runtime_Start_At_Boot", "AK_Runtime_Health_Check_Every_5min", "AK_Run_Handlers_Every_1h")
foreach ($t in $oldTasks) {
    schtasks /delete /tn $t /f 2>$null | Out-Null
}
Write-Host "  -> OK" -ForegroundColor Green

# Copy scripts
Write-Host "[2/5] Copy scripts..." -ForegroundColor Yellow
Copy-Item "$fixPath\vps_start_runtime.ps1" "$syncPath\start_runtime.ps1" -Force
Copy-Item "$fixPath\vps_health_check.ps1" "$syncPath\health_check.ps1" -Force
Write-Host "  -> OK" -ForegroundColor Green

# AK_Runtime_Start_At_Boot
Write-Host "[3/5] Tao task AK_Runtime_Start_At_Boot..." -ForegroundColor Yellow
$cmd = "cmd /c cd /d $akPath && powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$syncPath\start_runtime.ps1`""
schtasks /create /tn "AK_Runtime_Start_At_Boot" /tr "$cmd" /sc onstart /ru SYSTEM /rl HIGHEST /f 2>&1 | Out-Null
Write-Host "  -> OK" -ForegroundColor Green

# AK_Runtime_Health_Check_Every_5min
Write-Host "[4/5] Tao task AK_Runtime_Health_Check_Every_5min..." -ForegroundColor Yellow
$cmd = "cmd /c cd /d $akPath && powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$syncPath\health_check.ps1`""
schtasks /create /tn "AK_Runtime_Health_Check_Every_5min" /tr "$cmd" /sc minute /mo 5 /ru SYSTEM /rl HIGHEST /f 2>&1 | Out-Null
Write-Host "  -> OK" -ForegroundColor Green

# AK_Run_Handlers_Every_1h
Write-Host "[5/5] Tao task AK_Run_Handlers_Every_1h..." -ForegroundColor Yellow
$cmd = "cmd /c cd /d $akPath && powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$fixPath\vps_run_handlers.ps1`""
schtasks /create /tn "AK_Run_Handlers_Every_1h" /tr "$cmd" /sc hourly /ru SYSTEM /rl HIGHEST /f 2>&1 | Out-Null
Write-Host "  -> OK" -ForegroundColor Green

# Kiem tra
Write-Host "`n=== KIEM TRA TASKS ===" -ForegroundColor Cyan
Get-ScheduledTask | Where-Object TaskName -like "AK_*" | Format-Table TaskName,State -AutoSize

Write-Host "`n=== HOAN TAT ===" -ForegroundColor Cyan
