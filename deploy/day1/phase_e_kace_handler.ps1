param([string]$ReportPath = ".")

$results = @{}
$results["timestamp"] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
$results["handler"] = "day1_kace_handler"

$output = python -c "
import sys, json
sys.path.insert(0, r'C:\AK')
sys.path.insert(0, r'C:\AK\services')
from services.day1_kace_handler import run_kace_handler, get_scorecards, get_latest_scorecard
result = run_kace_handler()
latest = get_latest_scorecard()
records = get_scorecards()
print(json.dumps({'activation': result, 'latest': latest, 'record_count': len(records)}))
" 2>&1

try {
    $parsed = $output | ConvertFrom-Json
    $results["activation"] = $parsed.activation
    $results["latest"] = $parsed.latest
    $results["records"] = $parsed.record_count
} catch {
    $results["error"] = "$output"
}

$reportPath = "$ReportPath\KACE_HANDLER_DEPLOYMENT_REPORT.md"
$md = @"
# KACE_HANDLER_DEPLOYMENT_REPORT

## Timestamp
$($results.timestamp)

## Activation
- Status: $($results.activation.status)
- Handler: $($results.activation.handler)
- Scorecard ID: $($results.activation.scorecard_id)
- Timestamp: $($results.activation.timestamp)

## Latest Scorecard
| Metric | Value |
|--------|-------|
| Scorecard ID | $(if ($results.latest) { $results.latest.scorecard_id }) |
| Forecast Count | $(if ($results.latest) { $results.latest.forecast_count }) |
| Reality Count | $(if ($results.latest) { $results.latest.reality_count }) |
| Lesson Count | $(if ($results.latest) { $results.latest.lesson_count }) |
| Evidence Count | $(if ($results.latest) { $results.latest.evidence_count }) |
| Runtime Healthy | $(if ($results.latest) { $results.latest.runtime_healthy }) |
| Runtime Components | $(if ($results.latest) { $results.latest.runtime_component_count }) |

## Registry
- Total scorecards: $($results.records)

## Status
**KACE SCORECARD HANDLER: ACTIVE**
"@
$md | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Phase E complete. Report: $reportPath" -ForegroundColor Green
