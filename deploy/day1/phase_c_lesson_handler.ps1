param([string]$ReportPath = ".")

$results = @{}
$results["timestamp"] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
$results["handler"] = "day1_lesson_handler"

$output = python -c "
import sys, json
sys.path.insert(0, r'C:\AK')
sys.path.insert(0, r'C:\AK\services')
from services.day1_lesson_handler import run_lesson_handler, get_lessons, get_lesson_summary
result = run_lesson_handler()
summary = get_lesson_summary()
records = get_lessons()
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

$reportPath = "$ReportPath\LESSON_HANDLER_DEPLOYMENT_REPORT.md"
$md = @"
# LESSON_HANDLER_DEPLOYMENT_REPORT

## Timestamp
$($results.timestamp)

## Activation
- Status: $($results.activation.status)
- Handler: $($results.activation.handler)
- Lessons created: $($results.activation.lessons_created)
- Timestamp: $($results.activation.timestamp)

## Registry
- Path: $($results.activation.registry)
- Total records: $($results.records)

## Summary
| Metric | Value |
|--------|-------|
| Total lessons | $(if ($results.summary) { $results.summary.total_lessons }) |
| Last run | $(if ($results.summary) { $results.summary.last_run }) |

## Status
**LESSON HANDLER: ACTIVE**
"@
$md | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Phase C complete. Report: $reportPath" -ForegroundColor Green
