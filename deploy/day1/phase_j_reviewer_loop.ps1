param([string]$ReportPath = ".")

$results = @{}
$results["timestamp"] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")

$output = python C:\deploy\day1\reviewer_day1.py 2>&1

try {
    $parsed = $output | ConvertFrom-Json
    $results["checks"] = $parsed
} catch {
    $results["error"] = "$output"
}

$allPass = $results.checks.all_pass

$reviewerPath = "$ReportPath\DAY1_HANDLER_REVIEWER_LOOP_REPORT.md"
$md = @"
# DAY1_HANDLER_REVIEWER_LOOP_REPORT

## Timestamp
$($results.timestamp)

## Reviewer Checks
| Check | Status | Detail |
|-------|--------|--------|
"@
if ($results.checks) {
    foreach ($key in ($results.checks.PSObject.Properties.Name | Sort-Object)) {
        if ($key -eq "all_pass") { continue }
        $c = $results.checks.$key
        $pass = if ($c.pass -eq $true) { "PASS" } else { "FAIL" }
        if ($c.count -ne $null) { $detail = "Count: $($c.count)" }
        elseif ($c.error) { $detail = "Error: $($c.error)" }
        elseif ($c.violation) { $detail = "Violation: $($c.violation)" }
        else { $detail = "OK" }
        $md += "`n| $key | $pass | $detail |"
    }
}

$md += @"

## Final Decision

**Decision: $(if ($allPass) { "GO" } else { "NO-GO" })**

"@

if ($allPass) {
$md += @"
**Q1-AUDIT-30D DAY-1 HANDLERS: ALL ACTIVE**

All handlers passed reviewer checks:
- Forecast handler active
- Reality handler active
- Lesson handler active
- Evidence handler active
- KACE handler active
- Telegram integration active
- No live trading
- No scheduler duplication
- No governance bypass
- Evidence immutable
"@
} else {
$md += @"
**Deployment HALTED.** Review failures before proceeding.
"@
}

$md | Out-File -FilePath $reviewerPath -Encoding UTF8

$completionPath = "$ReportPath\DAY1_HANDLER_COMPLETION_REPORT.md"
$comp = @"
# DAY1_HANDLER_COMPLETION_REPORT

## Status
**Q1-AUDIT-30D DAY-1 HANDLERS DEPLOYMENT: $(if ($allPass) { "COMPLETE" } else { "FAILED" })**

## Timestamp
$($results.timestamp)

## Deployed Handlers
| Handler | Status |
|---------|--------|
"@
if ($results.checks) {
    foreach ($key in ($results.checks.PSObject.Properties.Name | Sort-Object)) {
        if ($key -eq "all_pass") { continue }
        $c = $results.checks.$key
        $icon = if ($c.pass -eq $true) { "Active" } else { "Failed" }
        $comp += "`n| $key | $icon |"
    }
}

$comp += @"

## Timeline
- Deployment completed: $($results.timestamp)
- Q1-AUDIT-30D DAY-1: PREVIOUSLY ACTIVATED
- Handlers operational evidence collection: $(if ($allPass) { "ACTIVE" } else { "FAILED" })
"@

$comp | Out-File -FilePath $completionPath -Encoding UTF8

Write-Host "Phase J complete." -ForegroundColor Green
Write-Host "Reviewer report: $reviewerPath" -ForegroundColor Yellow
Write-Host "Completion report: $completionPath" -ForegroundColor Yellow
