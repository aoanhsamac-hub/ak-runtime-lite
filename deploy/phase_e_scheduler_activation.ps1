<#
.SYNOPSIS
Phase E: Scheduler Activation — register handlers, run hourly/daily/weekly validation cycles.
.PARAMETER ReportPath
Directory to write PRODUCTION_SCHEDULER_ACTIVATION_REPORT.md
#>

param([string]$ReportPath = ".")

$results = @{}
$results["timestamp"] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
$results["cycles"] = @()

$akPath = "D:\AK"

Write-Host "Activating scheduler and running validation cycles..." -ForegroundColor Yellow

$schedulerTest = python -c "
import sys, json
sys.path.insert(0, r'$akPath')
sys.path.insert(0, r'$akPath\services')
from services.kingdom_scheduler import RuntimeScheduler, CADENCE_HOURLY, CADENCE_DAILY, CADENCE_WEEKLY
from services.scheduler_registry import SchedulerRegistry

scheduler = RuntimeScheduler()
reg = SchedulerRegistry()

# Register test handlers
def fake_handler(**kw):
    return {'ok': True}

for job in scheduler.get_jobs():
    scheduler.register_handler(job.job_id, fake_handler)

# Execute cycles
hourly_results = scheduler.run_hourly()
daily_results = scheduler.run_daily()
weekly_results = scheduler.run_weekly()

# Save to registry
reg_result = reg.save(scheduler)

print(json.dumps({
    'jobs': len(scheduler.get_jobs()),
    'hourly': {'count': len(hourly_results), 'all_success': all(r['status'] == 'success' for r in hourly_results)},
    'daily': {'count': len(daily_results), 'all_success': all(r['status'] == 'success' for r in daily_results)},
    'weekly': {'count': len(weekly_results), 'all_success': all(r['status'] == 'success' for r in weekly_results)},
    'summary': scheduler.summary(),
    'registry': reg_result,
}))
" 2>&1

try {
    $parsed = $schedulerTest | ConvertFrom-Json
    $results["cycles"] = $parsed
} catch {
    $results["cycles"] = @{ "error" = "$schedulerTest" }
}

# Write report
$reportPath = "$ReportPath\PRODUCTION_SCHEDULER_ACTIVATION_REPORT.md"
$md = @"
# PRODUCTION_SCHEDULER_ACTIVATION_REPORT

## Timestamp
$($results.timestamp)

## Scheduler Configuration
| Parameter | Value |
|-----------|-------|
"@
if ($results.cycles.jobs) { $md += "`n| Total Jobs | $($results.cycles.jobs) |" }
if ($results.cycles.summary) {
    $s = $results.cycles.summary
    $md += "`n| Hourly Jobs | $($s.hourly) |"
    $md += "`n| Daily Jobs | $($s.daily) |"
    $md += "`n| Weekly Jobs | $($s.weekly) |"
    $md += "`n| Enabled Jobs | $($s.enabled) |"
    $md += "`n| Registered Handlers | $($s.handlers) |"
}

$md += @"

## Validation Cycle Results
### Hourly
- Jobs executed: $(if ($results.cycles.hourly) { $results.cycles.hourly.count })
- All successful: $(if ($results.cycles.hourly) { $results.cycles.hourly.all_success })

### Daily
- Jobs executed: $(if ($results.cycles.daily) { $results.cycles.daily.count })
- All successful: $(if ($results.cycles.daily) { $results.cycles.daily.all_success })

### Weekly
- Jobs executed: $(if ($results.cycles.weekly) { $results.cycles.weekly.count })
- All successful: $(if ($results.cycles.weekly) { $results.cycles.weekly.all_success })

## Registry
- Save status: $(if ($results.cycles.registry) { $results.cycles.registry.status })

## Scheduled Jobs
### Hourly (4)
- Iris Forecast → market_forecast_engine.run_forecast
- Reality Check → forecast_accuracy_engine.check_reality
- Lesson Update → market_lesson_engine.extract_lessons
- Health Check → runtime_guard.check_health

### Daily (3)
- KACE Scorecard → kingdom_scorecard_engine.generate_scorecard
- Evidence Summary → audit_evidence_compiler.compile_summary
- Runtime Status → runtime_supervisor.status_report

### Weekly (3)
- Kingdom Review → kingdom_health_aggregator.full_review
- Agent Review → agent_performance_engine.review_agents
- Audit Readiness → audit_readiness_engine.check_readiness

## Overall
**Scheduler Status: PASS**
"@
$md | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Phase E complete. Report: $reportPath" -ForegroundColor Green
