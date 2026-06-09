# register_runtime_tasks_vps.ps1 — Tao scheduled tasks cho runtime tren VPS
$ErrorActionPreference = "Continue"
$akPath = "C:\AK"
$fixPath = "$akPath\deploy\fix"

Write-Host "=== AK-RUNTIME-HANDLER-AUTOSTART-FIX-01 ===" -ForegroundColor Cyan
Write-Host "Register runtime tasks tren VPS`n"

# Dam bao thu muc fix ton tai
New-Item -ItemType Directory -Path $fixPath -Force | Out-Null

# 1. copy scripts tu deploy/fix vao dung thu muc
Write-Host "[1/5] Copy scripts..." -ForegroundColor Yellow
Copy-Item "$fixPath\vps_start_runtime.ps1" "$akPath\deploy\sync\start_runtime.ps1" -Force
Copy-Item "$fixPath\vps_health_check.ps1" "$akPath\deploy\sync\health_check.ps1" -Force
Write-Host "  -> OK" -ForegroundColor Green

# 2. AK_Runtime_Start_At_Boot — chay khi boot
Write-Host "[2/5] Tao task AK_Runtime_Start_At_Boot..." -ForegroundColor Yellow
schtasks /create /tn "AK_Runtime_Start_At_Boot" /tr "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$akPath\deploy\sync\start_runtime.ps1`"" /sc onstart /ru SYSTEM /rl HIGHEST /f 2>&1 | Out-Null
Write-Host "  -> OK" -ForegroundColor Green

# 3. AK_Runtime_Health_Check_Every_5min (update)
Write-Host "[3/5] Update task AK_Runtime_Health_Check_Every_5min..." -ForegroundColor Yellow
schtasks /create /tn "AK_Runtime_Health_Check_Every_5min" /tr "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$akPath\deploy\sync\health_check.ps1`"" /sc minute /mo 5 /ru SYSTEM /rl HIGHEST /f 2>&1 | Out-Null
Write-Host "  -> OK" -ForegroundColor Green

# 4. AK_Run_Handlers_Every_1h — chay handler moi gio
Write-Host "[4/5] Tao task AK_Run_Handlers_Every_1h..." -ForegroundColor Yellow
schtasks /create /tn "AK_Run_Handlers_Every_1h" /tr "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$fixPath\vps_run_handlers.ps1`"" /sc hourly /ru SYSTEM /rl HIGHEST /f 2>&1 | Out-Null
Write-Host "  -> OK" -ForegroundColor Green

# 5. Kiem tra
Write-Host "[5/5] Kiem tra tat ca tasks..." -ForegroundColor Yellow
Get-ScheduledTask | Where-Object TaskName -like "AK_*" | Format-Table TaskName,State -AutoSize

Write-Host "`n=== HOAN TAT ===" -ForegroundColor Cyan
Write-Host "Cac task da duoc tao:" -ForegroundColor Green
Write-Host "  AK_Runtime_Start_At_Boot - Khoi dong runtime khi boot" -ForegroundColor Green
Write-Host "  AK_Runtime_Health_Check_Every_5min - Kiem tra va restart" -ForegroundColor Green
Write-Host "  AK_Run_Handlers_Every_1h - Chay handler moi gio" -ForegroundColor Green
Write-Host "  AK_Git_Pull_Every_30min - Pull source moi" -ForegroundColor Green
Write-Host "  AK_Push_Reports_Every_1h - Push reports len GitHub" -ForegroundColor Green
