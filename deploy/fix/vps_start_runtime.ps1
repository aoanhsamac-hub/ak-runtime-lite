# vps_start_runtime.ps1 — Khoi dong runtime handlers tren VPS (FIXED v2)
$ErrorActionPreference = "Continue"
$akPath = "C:\AK"
$logPath = "$akPath\logs"
$startTime = Get-Date

Write-Host "=== AK-RUNTIME-HANDLER-AUTOSTART :: START RUNTIME v2 ===" -ForegroundColor Cyan
New-Item -ItemType Directory -Path $logPath -Force | Out-Null

# Set Telegram env vars cho process hien tai
$env:TELEGRAM_BOT_TOKEN = [Environment]::GetEnvironmentVariable("TELEGRAM_BOT_TOKEN","Machine")
$env:TELEGRAM_WHITELIST = [Environment]::GetEnvironmentVariable("TELEGRAM_WHITELIST","Machine")
Write-Host "TELEGRAM_BOT_TOKEN: $([bool]$env:TELEGRAM_BOT_TOKEN)" -ForegroundColor Green
Write-Host "TELEGRAM_WHITELIST: $($env:TELEGRAM_WHITELIST)" -ForegroundColor Green

# Ham start process
function Start-AkProcess($name, $scriptFile) {
    $logOut = "$logPath\$name.out"
    $logErr = "$logPath\$name.err"
    
    # Kiem tra da chay chua
    $existing = Get-Process python* -ErrorAction SilentlyContinue | Where-Object {
        $cmd = ""
        try { $cmd = $_.CommandLine } catch { try { $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)").CommandLine } catch {} }
        $cmd -like "*$scriptFile*"
    }
    if ($existing) {
        Write-Host "  [SKIP] $name da chay (PID: $($existing.Id))" -ForegroundColor Yellow
        return
    }
    
    Write-Host "  [START] $name..." -ForegroundColor Yellow
    Write-Host "    File: $akPath\$scriptFile" -ForegroundColor Gray
    
    # Chay tu C:\AK de dam bao import path
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "python"
    $psi.Arguments = "-u `"$akPath\$scriptFile`""
    $psi.WorkingDirectory = $akPath
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
    $psi.CreateNoWindow = $true
    $psi.EnvironmentVariables["TELEGRAM_BOT_TOKEN"] = $env:TELEGRAM_BOT_TOKEN
    $psi.EnvironmentVariables["TELEGRAM_WHITELIST"] = $env:TELEGRAM_WHITELIST
    
    $p = [System.Diagnostics.Process]::Start($psi)
    Start-Sleep -Seconds 3
    
    if (!$p.HasExited) {
        Write-Host "    -> PID: $($p.Id)" -ForegroundColor Green
    } else {
        $err = $p.StandardError.ReadToEnd()
        $out = $p.StandardOutput.ReadToEnd()
        Write-Host "    -> LOI: Process thoat ngay" -ForegroundColor Red
        if ($err) { Write-Host "    STDERR: $err" -ForegroundColor Red }
        if ($out) { Write-Host "    STDOUT: $out" -ForegroundColor Red }
        $err | Out-File -FilePath $logErr -Encoding UTF8
        $out | Out-File -FilePath $logOut -Encoding UTF8
    }
}

# Test Python truoc
Write-Host "`n[TEST] Kiem tra Python..." -ForegroundColor Yellow
try {
    $test = python -c "print('PYTHON_OK')" 2>&1
    Write-Host "  -> $test" -ForegroundColor Green
} catch {
    Write-Host "  -> LOI: Python khong chay duoc" -ForegroundColor Red
    exit 1
}

# Test import services
Write-Host "[TEST] Kiem tra import services..." -ForegroundColor Yellow
try {
    $importTest = python -c "import sys; sys.path.insert(0,'C:\\AK'); from services.telegram_gateway import TelegramGateway; print('IMPORT_OK')" 2>&1
    Write-Host "  -> $importTest" -ForegroundColor Green
} catch {
    Write-Host "  -> LOI: Import services that bai" -ForegroundColor Red
}

# Start cac service
Write-Host "`n[1/3] Dang khoi dong Telegram gateway..." -ForegroundColor Yellow
Start-AkProcess -name "telegram_gateway" -scriptFile "services\telegram_gateway.py"

Write-Host "[2/3] Dang khoi dong Kingdom scheduler..." -ForegroundColor Yellow
Start-AkProcess -name "kingdom_scheduler" -scriptFile "services\kingdom_scheduler.py"

Write-Host "[3/3] Dang khoi dong Runtime supervisor..." -ForegroundColor Yellow
Start-AkProcess -name "runtime_supervisor" -scriptFile "services\runtime_supervisor.py"

# Kiem tra
Start-Sleep -Seconds 2
$total = (Get-Process python* -ErrorAction SilentlyContinue).Count
Write-Host "`n=== RUNTIME: $total Python processes ===" -ForegroundColor Cyan

# Ghi log
"$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | START RUNTIME | $total processes" | Out-File -FilePath "$logPath\runtime_start.log" -Encoding UTF8 -Append

# Telegram notify
$telegramScript = "$akPath\deploy\sync\send_telegram.ps1"
if (Test-Path $telegramScript) {
    & $telegramScript -Message "VPS: Runtime da khoi dong ($total processes)" -Status success
}
