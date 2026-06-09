<#
.SYNOPSIS
Phase G: Baseline Capture — CPU, RAM, Disk, MT5, Telegram, Scheduler, Runtime status.
.PARAMETER ReportPath
Directory to write DAY1_RUNTIME_BASELINE_REPORT.md
#>

param([string]$ReportPath = ".")

$results = @{}
$results["timestamp"] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
$results["hostname"] = hostname

# CPU
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
$results["cpu"] = @{ "name" = $cpu.Name; "cores" = $cpu.NumberOfCores; "load" = (Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average }

# RAM
$os = Get-CimInstance Win32_OperatingSystem
$results["ram"] = @{
    "total_mb" = [math]::Round($os.TotalVisibleMemorySize / 1KB, 0)
    "free_mb" = [math]::Round($os.FreePhysicalMemory / 1KB, 0)
    "used_mb" = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / 1KB, 0)
}

# Disk
$disks = Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3"
$diskData = @{}
foreach ($d in $disks) {
    $diskData[$d.DeviceID] = @{
        "size_gb" = [math]::Round($d.Size / 1GB, 1)
        "free_gb" = [math]::Round($d.FreeSpace / 1GB, 1)
    }
}
$results["disk"] = $diskData

# MT5 status
$mt5Proc = Get-Process -Name "terminal" -ErrorAction SilentlyContinue
$results["mt5"] = @{ "running" = ($mt5Proc -ne $null); "pids" = if ($mt5Proc) { @($mt5Proc.Id) } else { @() } }

# Python version
$pyVer = python --version 2>&1
$results["python"] = "$pyVer"

# AK services
$akPath = "D:\AK"
$svcCount = (Get-ChildItem "$akPath\services\*.py" -ErrorAction SilentlyContinue).Count
$results["services"] = @{ "path" = $akPath; "file_count" = $svcCount }

# Scheduler status
$schedStatus = python -c "
import sys; sys.path.insert(0, r'$akPath');
from services.kingdom_scheduler import RuntimeScheduler
s = RuntimeScheduler()
summ = s.summary()
print(f'jobs={summ[\"total_jobs\"]} hourly={summ[\"hourly\"]} daily={summ[\"daily\"]} weekly={summ[\"weekly\"]}')
" 2>&1
$results["scheduler"] = "$schedStatus"

$reportPath = "$ReportPath\DAY1_RUNTIME_BASELINE_REPORT.md"
$md = @"
# DAY1_RUNTIME_BASELINE_REPORT

## Timestamp
$($results.timestamp)

## Hostname
$($results.hostname)

## CPU
- **Model**: $($results.cpu.name)
- **Cores**: $($results.cpu.cores)
- **Load**: $($results.cpu.load)%

## RAM
| Metric | Value |
|--------|-------|
| Total | $($results.ram.total_mb) MB |
| Free | $($results.ram.free_mb) MB |
| Used | $($results.ram.used_mb) MB |

## Disk
| Drive | Size | Free |
|-------|------|------|
"@
foreach ($d in $results.disk.Keys) {
    $md += "`n| $d | $($results.disk[$d].size_gb) GB | $($results.disk[$d].free_gb) GB |"
}

$md += @"

## Runtime Services
- **Python**: $($results.python)
- **Service Files**: $($results.services.file_count) in $($results.services.path)
- **MT5 Terminal**: $(if ($results.mt5.running) { "Running (PID: $($results.mt5.pids -join ', '))" } else { "Not running" })
- **Scheduler**: $($results.scheduler)

## Overall
**Baseline Status: CAPTURED**
"@
$md | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Phase G complete. Report: $reportPath" -ForegroundColor Green
