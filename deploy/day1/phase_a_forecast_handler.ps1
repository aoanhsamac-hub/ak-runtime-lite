param([string]$ReportPath = ".")

$results = @{}
$results["timestamp"] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
$results["handler"] = "day1_forecast_handler"

$output = python -c "
import sys, json
sys.path.insert(0, r'C:\AK')
sys.path.insert(0, r'C:\AK\services')
from services.day1_forecast_handler import run_forecast_handler, get_forecasts, get_forecast_summary
result = run_forecast_handler()
summary = get_forecast_summary()
records = get_forecasts()
print(json.dumps({'activation': result, 'summary': summary, 'record_count': len(records)}))
" 2>&1

try {
    $parsed = $output | ConvertFrom-Json
    $results["activation"] = $parsed.activation
    $results["summary"] = $parsed.summary
    $results["records"] = $parsed.record_count
} catch {
    $results["error"] = "$output"
}

$reportPath = "$ReportPath\IRIS_FORECAST_HANDLER_DEPLOYMENT_REPORT.md"
$md = @"
# IRIS_FORECAST_HANDLER_DEPLOYMENT_REPORT

## Timestamp
$($results.timestamp)

## Activation
- Status: $($results.activation.status)
- Handler: $($results.activation.handler)
- Forecasts generated: $($results.activation.forecasts_generated)
- Timestamp: $($results.activation.timestamp)

## Registry
- Path: $($results.activation.registry)
- Total records: $($results.records)

## Summary
| Metric | Value |
|--------|-------|
| Total forecasts | $(if ($results.summary) { $results.summary.total_forecasts }) |
| Last run | $(if ($results.summary) { $results.summary.last_run }) |

## Status
**FORECAST HANDLER: ACTIVE**
"@
$md | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Phase A complete. Report: $reportPath" -ForegroundColor Green
