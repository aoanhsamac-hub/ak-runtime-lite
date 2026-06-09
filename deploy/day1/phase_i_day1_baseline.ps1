param([string]$ReportPath = ".")

$results = @{}
$results["timestamp"] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")

$output = python C:\deploy\day1\capture_baseline.py 2>&1

try {
    $parsed = $output | ConvertFrom-Json
    $results["activation"] = $parsed.activation
    $results["baseline"] = $parsed.baseline
} catch {
    $results["error"] = "$output"
}

$reportPath = "$ReportPath\DAY1_BASELINE_EVIDENCE_REPORT.md"
$md = @"
# DAY1_BASELINE_EVIDENCE_REPORT

## Timestamp
$($results.timestamp)

## Baseline
- Baseline ID: $($results.activation.baseline_id)
- Status: $($results.activation.status)
- Handler: $($results.activation.handler)
- Timestamp: $($results.activation.timestamp)

## Baseline Metrics

| Metric | Value |
|--------|-------|
| Forecast Count | $($results.baseline.forecast_count) |
| Reality Count | $($results.baseline.reality_count) |
| Lesson Count | $($results.baseline.lesson_count) |
| Evidence Count | $($results.baseline.evidence_count) |

## System Metrics
| Metric | Value |
|--------|-------|
| CPU | $($results.baseline.system_metrics.cpu_percent)% |
| RAM Available | $($results.baseline.system_metrics.ram_available_mb) MB |
| RAM Used | $($results.baseline.system_metrics.ram_percent_used)% |
| Disk Free | $($results.baseline.system_metrics.disk_free_gb) GB |

## Status
**DAY-1 BASELINE EVIDENCE: RECORDED**
"@
$md | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Phase I complete. Report: $reportPath" -ForegroundColor Green
