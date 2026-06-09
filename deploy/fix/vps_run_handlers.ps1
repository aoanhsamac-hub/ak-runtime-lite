# vps_run_handlers.ps1 — Chay tat ca DAY1 handlers de tao evidence/report
$akPath = "C:\AK"
$logPath = "$akPath\logs\handlers"

Write-Host "=== RUN DAY1 HANDLERS ===" -ForegroundColor Cyan
New-Item -ItemType Directory -Path $logPath -Force | Out-Null

$handlers = @(
    @{name="Forecast"; script="services\day1_forecast_handler.py"},
    @{name="Reality"; script="services\day1_reality_handler.py"},
    @{name="Lesson"; script="services\day1_lesson_handler.py"},
    @{name="Evidence"; script="services\day1_evidence_handler.py"},
    @{name="KACE"; script="services\day1_kace_handler.py"},
    @{name="EvidenceSummary"; script="services\day1_evidence_summary.py"},
    @{name="Baseline"; script="services\day1_baseline.py"},
    @{name="TelegramIntegration"; script="services\day1_telegram_integration.py"}
)

$ok = 0
$fail = 0

foreach ($h in $handlers) {
    Write-Host "  [$($h.name)] Dang chay..." -ForegroundColor Yellow
    $logFile = "$logPath\$($h.name).log"
    try {
        $output = python "-u" "$akPath\$($h.script)" 2>&1
        $exitCode = $LASTEXITCODE
        if ($exitCode -eq 0) {
            Write-Host "    -> OK" -ForegroundColor Green
            $ok++
        } else {
            Write-Host "    -> FAIL (exit: $exitCode)" -ForegroundColor Red
            $fail++
        }
        $output | Out-File -FilePath $logFile -Encoding UTF8
    } catch {
        Write-Host "    -> ERROR: $_" -ForegroundColor Red
        $fail++
        $_ | Out-File -FilePath $logFile -Encoding UTF8
    }
}

Write-Host "`n=== HANDLERS: $ok OK, $fail FAIL ===" -ForegroundColor Cyan

# Push reports sau khi handlers chay
if ($ok -gt 0) {
    Write-Host "Dang push reports len GitHub..." -ForegroundColor Yellow
    cd $akPath
    git add docs/reports/ evidence/ logs/handlers/
    git commit -m "AUTO: handlers run $(Get-Date -Format 'yyyy-MM-dd HH:mm')" 2>$null
    git push origin main 2>&1 | Out-Null
    
    # Telegram notify
    & "$akPath\deploy\sync\send_telegram.ps1" -Message "VPS: Handlers chay xong ($ok OK, $fail FAIL)" -Status success
}
