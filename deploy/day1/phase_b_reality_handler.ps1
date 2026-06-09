param([string]$ReportPath = ".")

$results = @{}
$results["timestamp"] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
$results["handler"] = "day1_reality_handler"

$output = python -c "
import sys, json
sys.path.insert(0, r'C:\AK')
sys.path.insert(0, r'C:\AK\services')
from services.day1_reality_handler import run_reality_handler, get_benchmarks, get_benchmark_summary
result = run_reality_handler()
summary = get_benchmark_summary()
records = get_benchmarks()
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

$reportPath = "$ReportPath\REALITY_CHECK_HANDLER_DEPLOYMENT_REPORT.md"
$md = @"
# REALITY_CHECK_HANDLER_DEPLOYMENT_REPORT

## Timestamp
$($results.timestamp)

## Activation
- Status: $($results.activation.status)
- Handler: $($results.activation.handler)
- Benchmarked: $($results.activation.benchmarked)
- Timestamp: $($results.activation.timestamp)

## Registry
- Path: $($results.activation.registry)
- Total records: $($results.records)

## Summary
| Metric | Value |
|--------|-------|
| Total benchmarks | $(if ($results.summary) { $results.summary.total_benchmarks }) |
| Last run | $(if ($results.summary) { $results.summary.last_run }) |

## Status
**REALITY CHECK HANDLER: ACTIVE**
"@
$md | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Phase B complete. Report: $reportPath" -ForegroundColor Green
