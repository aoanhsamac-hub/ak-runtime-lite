# Them Git usr/bin vao PATH de tim ssh, tar, etc.
$gitBins = @("C:\Program Files\Git\usr\bin","C:\Program Files (x86)\Git\usr\bin","$env:LOCALAPPDATA\Programs\Git\usr\bin")
foreach ($p in $gitBins) { if (Test-Path "$p\ssh.exe") { $env:Path = "$p;$env:Path"; break } }

$ErrorActionPreference = "Stop"

Write-Host "=== SET TELEGRAM ENV VARS TREN VPS ===" -ForegroundColor Cyan

# Kiem tra SSH
$test = ssh -o BatchMode=yes -o ConnectTimeout=5 ak-vps "echo OK" 2>$null
if ($test -ne "OK") {
    Write-Host "LOI: Khong SSH duoc vao VPS." -ForegroundColor Red
    exit 1
}

$botToken = "8869703952:AAHZo6hujSaeuoSPijIGmoUH28NKhRI5Mo0"
$whitelist = "7636364211"

Write-Host "Dang set TELEGRAM_BOT_TOKEN va TELEGRAM_WHITELIST tren VPS..." -ForegroundColor Yellow

# Set env vars tren VPS qua SSH
ssh ak-vps "[Environment]::SetEnvironmentVariable('TELEGRAM_BOT_TOKEN','$botToken','Machine')" 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) { Write-Host "  [OK] TELEGRAM_BOT_TOKEN" -ForegroundColor Green }
else { Write-Host "  [FAIL] TELEGRAM_BOT_TOKEN" -ForegroundColor Red }

ssh ak-vps "[Environment]::SetEnvironmentVariable('TELEGRAM_WHITELIST','$whitelist','Machine')" 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) { Write-Host "  [OK] TELEGRAM_WHITELIST" -ForegroundColor Green }
else { Write-Host "  [FAIL] TELEGRAM_WHITELIST" -ForegroundColor Red }

# Kiem tra lai
Write-Host "`nKiem tra tren VPS:" -ForegroundColor Cyan
ssh ak-vps "[Environment]::GetEnvironmentVariable('TELEGRAM_BOT_TOKEN','Machine'); [Environment]::GetEnvironmentVariable('TELEGRAM_WHITELIST','Machine')" 2>&1

Write-Host "`nXong. Gui tin nhan thu de kiem tra..." -ForegroundColor Yellow
& "D:\AK\deploy\sync\send_telegram.ps1" -Message "AK-AUTO-RUNTIME-SYNC-01: Telegram env vars da duoc set tren VPS" -Status success
