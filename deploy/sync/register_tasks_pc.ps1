# register_tasks_pc.ps1 - Tao scheduled tasks tren PC (Git-based)
$ErrorActionPreference = "Continue"
$scriptDir = "D:\AK\deploy\sync"

Write-Host "=== TAO SCHEDULED TASKS TREN PC ===" -ForegroundColor Cyan

# Task 1: AK_Pull_Reports_From_GitHub - moi 1 tieng
$taskPath = "$scriptDir\pull_from_github.ps1"
schtasks /create /tn "AK_Pull_Reports_From_GitHub" /tr "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$taskPath`"" /sc minute /mo 60 /ru "%USERDOMAIN%\%USERNAME%" /rl LIMITED /f 2>&1 | Out-Null
Write-Host "  [OK] AK_Pull_Reports_From_GitHub - moi 1 tieng" -ForegroundColor Green

# Task 2: AK_System_Health_Every_5min - kiem tra RAM, cpu
schtasks /create /tn "AK_System_Health_Every_5min" /tr "powershell.exe -NoProfile -ExecutionPolicy Bypass -Command `"Get-Process python* -ErrorAction SilentlyContinue | Format-Table Id,ProcessName -AutoSize; Get-CimInstance Win32_OperatingSystem | Select-Object @{N='FreeRAM';E={[math]::Round(`$_.FreePhysicalMemory/1MB,1)}} | Format-Table -AutoSize`"" /sc minute /mo 5 /ru "%USERDOMAIN%\%USERNAME%" /rl LIMITED /f 2>&1 | Out-Null
Write-Host "  [OK] AK_System_Health_Every_5min - moi 5 phut" -ForegroundColor Green

Write-Host "`nKiem tra task da tao:" -ForegroundColor Cyan
schtasks /query /tn AK_* /v /fo list 2>$null | Select-String "TaskName|Schedule|Task To Run"
