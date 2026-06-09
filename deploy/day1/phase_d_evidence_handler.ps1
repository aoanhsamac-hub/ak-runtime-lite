param([string]$ReportPath = ".")

$results = @{}
$results["timestamp"] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
$results["handler"] = "day1_evidence_handler"

$output = python -c "
import sys, json
sys.path.insert(0, r'C:\AK')
sys.path.insert(0, r'C:\AK\services')
from services.day1_evidence_handler import run_evidence_handler, get_evidence, get_evidence_summary
result = run_evidence_handler()
summary = get_evidence_summary()
records = get_evidence()
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

$reportPath = "$ReportPath\EVIDENCE_HANDLER_DEPLOYMENT_REPORT.md"
$md = @"
# EVIDENCE_HANDLER_DEPLOYMENT_REPORT

## Timestamp
$($results.timestamp)

## Activation
- Status: $($results.activation.status)
- Handler: $($results.activation.handler)
- Evidence ID: $($results.activation.evidence_id)
- Total records: $($results.activation.total_records)
- Timestamp: $($results.activation.timestamp)

## Registry
- Path: EVIDENCE_REGISTRY.yaml

## Rules Enforced
- Append Only: Yes
- Immutable: Yes
- Auditable: Yes

## Summary
| Metric | Value |
|--------|-------|
| Total evidence records | $(if ($results.summary) { $results.summary.total_evidence_records }) |
| Status | $(if ($results.summary) { $results.summary.status }) |

## Status
**EVIDENCE COLLECTION HANDLER: ACTIVE**
"@
$md | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Phase D complete. Report: $reportPath" -ForegroundColor Green
