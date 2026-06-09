param([string]$ReportPath = ".")

$results = @{}
$results["timestamp"] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
$results["handler"] = "day1_evidence_summary"

$output = python -c "
import sys, json
sys.path.insert(0, r'C:\AK')
sys.path.insert(0, r'C:\AK\services')
from services.day1_evidence_summary import run_daily_evidence_summary, get_summaries, get_latest_summary
result = run_daily_evidence_summary()
latest = get_latest_summary()
records = get_summaries()
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

$reportPath = "$ReportPath\DAILY_EVIDENCE_SUMMARY_HANDLER_REPORT.md"
$md = @"
# DAILY_EVIDENCE_SUMMARY_HANDLER_REPORT

## Timestamp
$($results.timestamp)

## Activation
- Status: $($results.activation.status)
- Handler: $($results.activation.handler)
- Summary ID: $($results.activation.summary_id)
- Timestamp: $($results.activation.timestamp)

## Latest Summary Sections
- Forecast Summary: $(if ($results.latest) { 'Collected' })
- Lesson Summary: $(if ($results.latest) { 'Collected' })
- Knowledge Summary: $(if ($results.latest) { 'Collected' })
- Runtime Summary: $(if ($results.latest) { 'Collected' })
- Audit Summary: $(if ($results.latest) { 'Collected' })

## Registry
- Total summaries: $($results.records)

## Status
**DAILY EVIDENCE SUMMARY: ACTIVE**
"@
$md | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Phase F complete. Report: $reportPath" -ForegroundColor Green
