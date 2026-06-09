# vps_run_handlers.ps1 — Chay DAY1 handlers, push reports, Telegram notify (FIXED v2)
$ErrorActionPreference = "Continue"
$akPath = "C:\AK"
$logPath = "$akPath\logs"
$handlerLogPath = "$logPath\handlers"
$time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$datePrefix = Get-Date -Format "yyyyMMdd_HHmm"

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

# Set PYTHONPATH de handlers co the import services.*
$env:PYTHONPATH = $akPath
Write-Host "PYTHONPATH: $env:PYTHONPATH" -ForegroundColor Gray

Write-Host "=== RUN DAY1 HANDLERS ===" -ForegroundColor Cyan
Write-Host "Time: $time"

# Set env vars tu Machine scope (quan trong khi chay tu scheduled task SYSTEM user)
$env:TELEGRAM_BOT_TOKEN = [Environment]::GetEnvironmentVariable("TELEGRAM_BOT_TOKEN","Machine")
$env:TELEGRAM_WHITELIST = [Environment]::GetEnvironmentVariable("TELEGRAM_WHITELIST","Machine")
Write-Host "TELEGRAM_BOT_TOKEN: $([bool]$env:TELEGRAM_BOT_TOKEN)" -ForegroundColor Green
Write-Host "TELEGRAM_WHITELIST: $($env:TELEGRAM_WHITELIST)" -ForegroundColor Green

New-Item -ItemType Directory -Path $handlerLogPath -Force | Out-Null

$handlers = @(
    @{name="Forecast"; script="services\day1_forecast_handler.py"}
    @{name="Reality"; script="services\day1_reality_handler.py"}
    @{name="Lesson"; script="services\day1_lesson_handler.py"}
    @{name="Evidence"; script="services\day1_evidence_handler.py"}
    @{name="KACE"; script="services\day1_kace_handler.py"}
    @{name="EvidenceSummary"; script="services\day1_evidence_summary.py"}
    @{name="Baseline"; script="services\day1_baseline.py"}
    @{name="TelegramIntegration"; script="services\day1_telegram_integration.py"}
)

$ok = 0
$fail = 0
$errors = @()

foreach ($h in $handlers) {
    Write-Host "  [$($h.name)] Dang chay..." -ForegroundColor Yellow
    $logFile = "$handlerLogPath\$($datePrefix)_$($h.name).log"
    try {
        $output = & $pythonPath "-u" "$akPath\$($h.script)" 2>&1
        $exitCode = $LASTEXITCODE
        $output | Out-File -FilePath $logFile -Encoding UTF8
        if ($exitCode -eq 0) {
            Write-Host "    -> OK" -ForegroundColor Green
            $ok++
        } else {
            Write-Host "    -> FAIL (exit: $exitCode)" -ForegroundColor Red
            $fail++
            $errors += "$($h.name): exit=$exitCode"
        }
    } catch {
        Write-Host "    -> ERROR: $_" -ForegroundColor Red
        $fail++
        $errors += "$($h.name): $_"
        $_ | Out-File -FilePath "$logFile.error" -Encoding UTF8
    }
}

Write-Host "`n=== HANDLERS: $ok OK, $fail FAIL ===" -ForegroundColor Cyan
if ($errors.Count -gt 0) {
    Write-Host "Errors: $($errors -join '; ')" -ForegroundColor Red
}

# Push reports len GitHub
try {
    Write-Host "`nGit: push reports..." -ForegroundColor Yellow
    git -C $akPath add docs/reports/ evidence/ logs/handlers/ 2>&1 | Out-Null
    $status = git -C $akPath status --porcelain 2>&1
    if ($status.Trim()) {
        git -C $akPath commit -m "AUTO: handlers run $time" 2>&1 | Out-Null
        git -C $akPath push origin main 2>&1 | Out-Null
        Write-Host "  -> Pushed" -ForegroundColor Green
    } else {
        Write-Host "  -> Khong co thay doi" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  -> Git loi: $_" -ForegroundColor Red
}

# Ghi log tong hop
$summary = @"
[$time] HANDLERS: $ok OK, $fail FAIL
  Errors: $($errors -join '; ')
"@
$summary | Out-File -FilePath "$handlerLogPath\_summary.log" -Encoding UTF8 -Append

# Telegram notify
$statusMsg = if ($ok -gt 0) { "success" } else { "warning" }
& "$akPath\deploy\sync\send_telegram.ps1" -Message "Handlers: $ok OK, $fail FAIL ($time)" -Status $statusMsg

Write-Host "`n=== DONE ===" -ForegroundColor Cyan
