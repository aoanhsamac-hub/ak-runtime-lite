# vps_start_runtime.ps1 — Khoi dong runtime_daemon.py (single daemon process)
$ErrorActionPreference = "Continue"
$akPath = "C:\AK"
$logPath = "$akPath\logs"
$daemonScript = "$akPath\services\runtime_daemon.py"

Write-Host "=== AK-RUNTIME :: START DAEMON ===" -ForegroundColor Cyan
New-Item -ItemType Directory -Path $logPath -Force | Out-Null

# Set env vars
$env:TELEGRAM_BOT_TOKEN = [Environment]::GetEnvironmentVariable("TELEGRAM_BOT_TOKEN","Machine")
$env:TELEGRAM_WHITELIST = [Environment]::GetEnvironmentVariable("TELEGRAM_WHITELIST","Machine")

# Check if already running
$existing = Get-Process python* -ErrorAction SilentlyContinue | Where-Object {
    $cmd = ""
    try { $cmd = $_.CommandLine } catch { try { $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)").CommandLine } catch {} }
    $cmd -like "*runtime_daemon*"
}
if ($existing) {
    Write-Host "Daemon da chay (PID: $($existing.Id))" -ForegroundColor Yellow
    exit 0
}

# Tim Python path (quan trong khi chay tu SYSTEM user)
$pythonPath = "python"
try {
    $pythonPath = (Get-Command python).Source
} catch {
    $possiblePaths = @(
        "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:ProgramFiles\Python313\python.exe",
        "$env:ProgramFiles\Python312\python.exe",
        "$env:ProgramFiles\Python311\python.exe",
        "C:\Python313\python.exe",
        "C:\Python312\python.exe",
        "C:\Python311\python.exe"
    )
    foreach ($p in $possiblePaths) {
        if (Test-Path $p) { $pythonPath = $p; break }
    }
}
Write-Host "Python path: $pythonPath" -ForegroundColor Gray

# Test Python
Write-Host "[TEST] Python..." -ForegroundColor Yellow
& $pythonPath -c "print('OK')" 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Host "  LOI" -ForegroundColor Red; exit 1 }
Write-Host "  OK" -ForegroundColor Green

# Test import
Write-Host "[TEST] Import services..." -ForegroundColor Yellow
& $pythonPath -c "import sys; sys.path.insert(0,'$akPath'); from services.runtime_daemon import main; print('OK')" 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { 
    Write-Host "  LOI import" -ForegroundColor Red
    & $pythonPath -c "import sys; sys.path.insert(0,'$akPath'); import services.telegram_gateway; print('tg OK')" 2>&1
    exit 1
}
Write-Host "  OK" -ForegroundColor Green

# Start daemon
Write-Host "[START] runtime_daemon..." -ForegroundColor Yellow
$logOut = "$logPath\daemon.out"
$logErr = "$logPath\daemon.err"

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $pythonPath
$psi.Arguments = "-u `"$daemonScript`""
$psi.WorkingDirectory = $akPath
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
$psi.CreateNoWindow = $true
$psi.EnvironmentVariables["TELEGRAM_BOT_TOKEN"] = $env:TELEGRAM_BOT_TOKEN
$psi.EnvironmentVariables["TELEGRAM_WHITELIST"] = $env:TELEGRAM_WHITELIST

$p = [System.Diagnostics.Process]::Start($psi)
Start-Sleep -Seconds 4

if (!$p.HasExited) {
    Write-Host "  PID: $($p.Id)" -ForegroundColor Green
    $p.StandardOutput.ReadToEndAsync() | Out-Null
    $p.StandardError.ReadToEndAsync() | Out-Null
} else {
    $err = $p.StandardError.ReadToEnd()
    $out = $p.StandardOutput.ReadToEnd()
    $err | Out-File -FilePath $logErr -Encoding UTF8
    $out | Out-File -FilePath $logOut -Encoding UTF8
    Write-Host "  LOI: thoat ngay" -ForegroundColor Red
    if ($err) { Write-Host "  STDERR: $err" -ForegroundColor Red }
    if ($out) { Write-Host "  STDOUT: $out" -ForegroundColor Red }
    exit 1
}

Start-Sleep -Seconds 5
$totalPython = (Get-Process python* -ErrorAction SilentlyContinue).Count
$daemonRunning = (Get-Process python* -ErrorAction SilentlyContinue | Where-Object {
    $cmd = ""
    try { $cmd = $_.CommandLine } catch { try { $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)").CommandLine } catch {} }
    $cmd -like "*runtime_daemon*"
}).Count -gt 0

Write-Host "`nPython processes: $totalPython | Daemon: $daemonRunning" -ForegroundColor Cyan

"$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | START DAEMON | PID=$($p.Id)" | Out-File -FilePath "$logPath\runtime_start.log" -Encoding UTF8 -Append

if ($daemonRunning) {
    & "$akPath\deploy\sync\send_telegram.ps1" -Message "VPS: Runtime daemon da khoi dong (PID $($p.Id))" -Status success
}
