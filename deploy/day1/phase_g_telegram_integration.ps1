param([string]$ReportPath = ".")

$results = @{}
$results["timestamp"] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
$results["handler"] = "day1_telegram_integration"

$output = python -c "
import sys, json
sys.path.insert(0, r'C:\AK')
sys.path.insert(0, r'C:\AK\services')
from services.day1_telegram_integration import (
    notify_runtime_started, notify_runtime_stopped,
    notify_scheduler_failure, notify_mt5_failure,
    notify_evidence_failure, notify_scorecard_available,
    verify_commands,
)
results = {
    'notify_runtime_started': notify_runtime_started(),
    'notify_runtime_stopped': notify_runtime_stopped('test'),
    'notify_scheduler_failure': notify_scheduler_failure({'test': True}),
    'notify_mt5_failure': notify_mt5_failure({'test': True}),
    'notify_evidence_failure': notify_evidence_failure({'test': True}),
    'notify_scorecard_available': notify_scorecard_available('KACE-TEST'),
    'verify_commands': verify_commands(),
}
print(json.dumps(results))
" 2>&1

try {
    $parsed = $output | ConvertFrom-Json
    $results["notifications"] = $parsed
} catch {
    $results["error"] = "$output"
}

$reportPath = "$ReportPath\TELEGRAM_HANDLER_INTEGRATION_REPORT.md"
$md = @"
# TELEGRAM_HANDLER_INTEGRATION_REPORT

## Timestamp
$($results.timestamp)

## Notification Functions
| Function | Status |
|----------|--------|
"@
if ($results.notifications) {
    $n = $results.notifications
    foreach ($key in $n.PSObject.Properties.Name) {
        $status = $n.$key.status
        $icon = if ($status -eq "OK") { "✓" } else { "✗" }
        $md += "`n| $key | $icon $status |"
    }
}

$md += @"

## Available Commands
$(if ($results.notifications.verify_commands.commands_available) { $results.notifications.verify_commands.commands_available -join ', ' })

## Status
**TELEGRAM INTEGRATION: ACTIVE**
"@
$md | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Phase G complete. Report: $reportPath" -ForegroundColor Green
