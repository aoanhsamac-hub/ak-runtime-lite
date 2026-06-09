# Them Git usr/bin vao PATH de tim ssh, tar, etc.
$gitBins = @("C:\Program Files\Git\usr\bin","C:\Program Files (x86)\Git\usr\bin","$env:LOCALAPPDATA\Programs\Git\usr\bin")
foreach ($p in $gitBins) { if (Test-Path "$p\ssh.exe") { $env:Path = "$p;$env:Path"; break } }

$ErrorActionPreference = "Continue"

Write-Host "=== STOP RUNTIME ===" -ForegroundColor Cyan

if (-not (Test-Path "D:\AK\logs\.ssh_done")) {
    Write-Host "LOI: Chua chay setup_ssh.ps1" -ForegroundColor Red
    exit 1
}

Write-Host "Dang dung Python processes tren VPS..." -ForegroundColor Yellow
$stopped = ssh ak-vps "Get-Process python* -ErrorAction SilentlyContinue | Stop-Process -Force; echo STOPPED" 2>&1

Start-Sleep -Seconds 2
$running = ssh ak-vps "Get-Process python* -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count" 2>$null
if ($running -eq 0 -or -not $running) {
    Write-Host "Runtime da dung" -ForegroundColor Green
    & "D:\AK\deploy\sync\send_telegram.ps1" -Message "RUNTIME DA DUNG" -Status info
} else {
    Write-Host "Con $running process dang chay. Thu lai." -ForegroundColor Red
}
