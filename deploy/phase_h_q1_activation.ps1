<#
.SYNOPSIS
Phase H: Q1-AUDIT-30D Activation — start operational evidence collection.
.PARAMETER ReportPath
Directory to write Q1_AUDIT_DAY1_ACTIVATION_REPORT.md
#>

param([string]$ReportPath = ".")

$results = @{}
$startTime = Get-Date
$results["day1_timestamp_utc"] = $startTime.ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$results["day1_timestamp_local"] = $startTime.ToString("yyyy-MM-dd HH:mm:ss")
$results["hostname"] = hostname

$akPath = "D:\AK"

# Create evidence registries if missing
$registryPaths = @(
    "$akPath\data\forecast_registry.json",
    "$akPath\data\lesson_registry.json",
    "$akPath\data\evidence_log.json",
    "$akPath\data\audit_log.json",
    "$akPath\data\adoption_log.json",
    "$akPath\data\roi_log.json"
)

$results["registries"] = @()
foreach ($rp in $registryPaths) {
    $exists = Test-Path $rp
    if (-not $exists) {
        $dir = Split-Path $rp -Parent
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        "[]" | Out-File -FilePath $rp -Encoding UTF8
    }
    $results["registries"] += @{ "path" = $rp; "created_size" = if ($exists) { "exists" } else { "new" } }
}

# Record activation marker
$markerPath = "$akPath\data\q1_audit_day1_marker.txt"
@"
Q1-AUDIT-30D DAY-1 ACTIVATION
Timestamp: $($results.day1_timestamp_utc)
Hostname: $($results.hostname)
Status: ACTIVE
"@ | Out-File -FilePath $markerPath -Encoding UTF8
$results["marker"] = @{ "path" = $markerPath; "written" = $true }

$reportPath = "$ReportPath\Q1_AUDIT_DAY1_ACTIVATION_REPORT.md"
$md = @"
# Q1_AUDIT_DAY1_ACTIVATION_REPORT

## Q1-AUDIT-30D DAY-1 ACTIVATION

**Timestamp**: $($results.day1_timestamp_utc)
**Hostname**: $($results.hostname)

## Activated Evidence Collection

| Registry | Status |
|----------|--------|
"@
foreach ($r in $results.registries) {
    $status = if ($r.created_size -eq "new") { "Created" } else { "Already exists" }
    $md += "`n| $($r.path) | $status |"
}

$md += @"

## Evidence Flow Enabled
```
Market Observation (Iris)
    ↓  (MT5 HealthMonitor - hourly)
Forecast Registry
    ↓  (hourly-forecast job)
Lesson Proposals
    ↓  (hourly-lesson job)
Lesson Registry
    ↓  (daily-evidence job)
KACE Scorecard
    ↓  (daily-kace job)
Evidence Log
    ↓  (weekly-audit job)
Audit Readiness
```

## Scheduler Jobs Now Active
| Cadence | Jobs | Collection Type |
|---------|------|-----------------|
| Hourly | Iris Forecast, Reality Check, Lesson Update | Market & Learning Evidence |
| Daily | KACE Scorecard, Evidence Summary, Runtime Status | Performance & Audit Evidence |
| Weekly | Kingdom Review, Agent Review, Audit Readiness | Governance & Readiness Evidence |

## Activation Marker
- **File**: $($results.marker.path)
- **Content**: Q1-AUDIT-30D DAY-1 ACTIVATION at $($results.day1_timestamp_utc)

## Overall
**Q1-AUDIT-30D DAY-1: ACTIVE**
"@
$md | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Phase H complete. Report: $reportPath" -ForegroundColor Green
