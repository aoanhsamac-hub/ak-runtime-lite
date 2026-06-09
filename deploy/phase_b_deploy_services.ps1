<#
.SYNOPSIS
Phase B: Service Deployment — copy and validate all 10 runtime services.
.PARAMETER ReportPath
Directory to write PRODUCTION_SERVICE_DEPLOYMENT_REPORT.md
#>

param([string]$ReportPath = ".")

$results = @{}
$results["timestamp"] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
$results["services"] = @()

$serviceFiles = @(
    "telegram_gateway.py",
    "telegram_command_router.py",
    "telegram_notification_service.py",
    "kingdom_scheduler.py",
    "scheduler_registry.py",
    "runtime_supervisor.py",
    "heartbeat_monitor.py",
    "restart_manager.py",
    "runtime_guard.py",
    "stop_condition_manager.py",
    "backup_manager.py",
    "registry_backup_service.py",
    "evidence_backup_service.py",
    "secret_manager.py",
    "credential_validator.py"
)

$akPath = "D:\AK"

# Ensure service paths exist
$null = New-Item -ItemType Directory -Path "$akPath\services" -Force
$null = New-Item -ItemType Directory -Path "$akPath\data" -Force

# Check each service file exists
foreach ($file in $serviceFiles) {
    $path = "$akPath\services\$file"
    $exists = Test-Path $path
    $results["services"] += @{
        "file" = $file;
        "exists" = $exists;
        "status" = if ($exists) { "OK" } else { "MISSING" }
    }
    if (-not $exists) {
        Write-Warning "Service file missing: $file — must be copied from development PC"
    }
}

# Try importing each service
Write-Host "Validating service imports..." -ForegroundColor Yellow
$importResults = @()
foreach ($file in $serviceFiles) {
    $module = $file -replace '\.py$', ''
    try {
        $result = python -c "import services.$module; print('OK')" 2>&1
        $importResults += @{ "module" = $module; "status" = "OK"; "detail" = "$result" }
    } catch {
        $importResults += @{ "module" = $module; "status" = "FAIL"; "detail" = "$_" }
    }
}
$results["imports"] = $importResults

$failCount = ($results["services"] | Where-Object { $_.status -ne "OK" }).Count
$importFailCount = ($importResults | Where-Object { $_.status -ne "OK" }).Count

# Write report
$reportPath = "$ReportPath\PRODUCTION_SERVICE_DEPLOYMENT_REPORT.md"
$md = @"
# PRODUCTION_SERVICE_DEPLOYMENT_REPORT

## Timestamp
$($results.timestamp)

## Service Files
| File | Status |
|------|--------|
"@
foreach ($s in $results["services"]) {
    $icon = if ($s.status -eq "OK") { "✓" } else { "✗" }
    $md += "`n| $($s.file) | $icon $($s.status) |"
}

$md += @"

## Import Validation
| Module | Status |
|--------|--------|
"@
foreach ($im in $importResults) {
    $icon = if ($im.status -eq "OK") { "✓" } else { "✗" }
    $md += "`n| $($im.module) | $icon $($im.status) — $($im.detail) |"
}

$allOk = ($failCount -eq 0 -and $importFailCount -eq 0)
$md += @"

## Summary
- **15 service files checked**: $($results["services"].Count)
- **Files missing**: $failCount
- **Import failures**: $importFailCount
- **Status**: $(if ($allOk) { "ALL SERVICES READY" } else { "ISSUES DETECTED" })
"@
$md | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Phase B complete. Report: $reportPath" -ForegroundColor Green
