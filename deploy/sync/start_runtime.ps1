# Them Git usr/bin vao PATH de tim ssh, tar, etc.
$gitBins = @("C:\Program Files\Git\usr\bin","C:\Program Files (x86)\Git\usr\bin","$env:LOCALAPPDATA\Programs\Git\usr\bin")
foreach ($p in $gitBins) { if (Test-Path "$p\ssh.exe") { $env:Path = "$p;$env:Path"; break } }

$ErrorActionPreference = "Continue"

Write-Host "=== START RUNTIME ===" -ForegroundColor Cyan

if (-not (Test-Path "D:\AK\logs\.ssh_done")) {
    Write-Host "LOI: Chua chay setup_ssh.ps1" -ForegroundColor Red
    exit 1
}

# Kiem tra python processes dang chay
$running = ssh ak-vps "Get-Process python* -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count" 2>$null
if ($running -gt 0) {
    Write-Host "Runtime dang chay ($running process). Bo qua." -ForegroundColor Yellow
    exit 0
}

# Chay supervisor tren VPS
Write-Host "Dang chay supervisor tren VPS..." -ForegroundColor Yellow
ssh ak-vps "cd C:\AK && start /B python -m services.supervisor 2>&1" 2>&1 | Out-Null

Start-Sleep -Seconds 3
$running2 = ssh ak-vps "Get-Process python* -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count" 2>$null
if ($running2 -gt 0) {
    Write-Host "Runtime da chay ($running2 process)" -ForegroundColor Green
    & "D:\AK\deploy\sync\send_telegram.ps1" -Message "RUNTIME DA KHOI DONG ($running2 process)" -Status success
} else {
    Write-Host "Khong the khoi dong runtime. Kiem tra VPS." -ForegroundColor Red
    & "D:\AK\deploy\sync\send_telegram.ps1" -Message "RUNTIME KHONG KHOI DONG DUOC" -Status error
}
