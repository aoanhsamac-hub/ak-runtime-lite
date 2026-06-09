param([string]$ReportPath = ".")

$results = @{}
$results["timestamp"] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")

$output = python C:\deploy\day1\validate_operational.py 2>&1

try {
    $parsed = $output | ConvertFrom-Json
    $results["checks"] = $parsed
} catch {
    $results["error"] = "$output"
}

$allPass = $results.checks.all_pass

$reportPath = "$ReportPath\DAY1_OPERATIONAL_VALIDATION_REPORT.md"
$md = @"
# DAY1_OPERATIONAL_VALIDATION_REPORT

## Timestamp
$($results.timestamp)

## Validation Checks
| Check | Status | Detail |
|-------|--------|--------|
"@
if ($results.checks) {
    foreach ($key in ($results.checks.PSObject.Properties.Name | Sort-Object)) {
        if ($key -eq "all_pass") { continue }
        $c = $results.checks.$key
        $pass = if ($c.pass -eq $true) { "PASS" } else { "FAIL" }
        $detail = if ($c.detail) { $c.detail } elseif ($c.error) { $c.error } else { "OK" }
        $md += "`n| $key | $pass | $detail |"
    }
}

$md += @"

## Overall Result

**Operational Validation: $(if ($allPass) { "PASS" } else { "FAIL" })**
"@
$md | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Phase H complete. Report: $reportPath" -ForegroundColor Green
