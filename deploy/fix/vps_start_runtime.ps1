# vps_start_runtime.ps1 — Khoi dong runtime handlers tren VPS
# Chay voi quyen Administrator

$ErrorActionPreference = "Continue"
$akPath = "C:\AK"
$logPath = "$akPath\logs"
$python = "python"
$startTime = Get-Date

Write-Host "=== AK-RUNTIME-HANDLER-AUTOSTART :: START RUNTIME ===" -ForegroundColor Cyan

# Tao thu muc logs neu chua co
New-Item -ItemType Directory -Path $logPath -Force | Out-Null

# Ham start process
function Start-AkProcess($name, $script, $args) {
    $logFile = "$logPath\$name.log"
    $running = Get-Process python* -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*$script*" }
    if ($running) {
        Write-Host "  [SKIP] $name da chay (PID: $($running.Id))" -ForegroundColor Yellow
        return $running
    }
    Write-Host "  [START] Dang khoi dong $name..." -ForegroundColor Green
    $p = Start-Process -FilePath $python -ArgumentList "-u `"$akPath\$script`"" -WindowStyle Hidden -PassThru -RedirectStandardOutput "$logFile.out" -RedirectStandardError "$logFile.err"
    Start-Sleep -Seconds 2
    $check = Get-Process -Id $p.Id -ErrorAction SilentlyContinue
    if ($check) {
        Write-Host "    -> PID: $($p.Id)" -ForegroundColor Green
    } else {
        Write-Host "    -> LOI: Khong the khoi dong" -ForegroundColor Red
    }
    return $p
}

# Start cac service
Write-Host "`n[1/3] Dang khoi dong Telegram gateway..." -ForegroundColor Yellow
Start-AkProcess -name "telegram_gateway" -script "services\telegram_gateway.py"

Write-Host "`n[2/3] Dang khoi dong Kingdom scheduler..." -ForegroundColor Yellow
Start-AkProcess -name "kingdom_scheduler" -script "services\kingdom_scheduler.py"

Write-Host "`n[3/3] Dang khoi dong Runtime supervisor..." -ForegroundColor Yellow
Start-AkProcess -name "runtime_supervisor" -script "services\runtime_supervisor.py"

# Kiem tra tong the
Start-Sleep -Seconds 2
$total = (Get-Process python* -ErrorAction SilentlyContinue).Count
Write-Host "`n=== RUNTIME DA KHOI DONG: $total Python processes ===" -ForegroundColor Cyan

# Ghi log
"$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | START RUNTIME | $total processes" | Out-File -FilePath "$logPath\runtime_start.log" -Encoding UTF8 -Append

# Telegram notify
$telegramScript = "$akPath\deploy\sync\send_telegram.ps1"
if (Test-Path $telegramScript) {
    & $telegramScript -Message "VPS: Runtime da khoi dong ($total processes)" -Status success
}
