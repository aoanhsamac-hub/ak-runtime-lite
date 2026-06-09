# vps_health_check.ps1 — Kiem tra va tu dong khoi dong lai runtime
$akPath = "C:\AK"
$logPath = "$akPath\logs"

Write-Host "=== RUNTIME HEALTH CHECK ===" -ForegroundColor Cyan
$time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "Time: $time"

# 1. Kiem tra RAM
try {
    $ram = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
    $freeRAM = [math]::Round($ram.FreePhysicalMemory/1MB, 1)
    $totalRAM = [math]::Round($ram.TotalVisibleMemorySize/1MB, 1)
    Write-Host "RAM: $freeRAM GB / $totalRAM GB"
    if ($freeRAM -lt 0.3) {
        & "$akPath\deploy\sync\send_telegram.ps1" -Message "VPS: RAM thap ($freeRAM GB)" -Status warning
    }
} catch { Write-Host "RAM: Khong the doc" }

# 2. Kiem tra Python processes
$required = @(
    @{name="telegram_gateway"; script="services\telegram_gateway.py"},
    @{name="kingdom_scheduler"; script="services\kingdom_scheduler.py"},
    @{name="runtime_supervisor"; script="services\runtime_supervisor.py"}
)

$processes = Get-Process python* -ErrorAction SilentlyContinue
$pCount = $processes.Count
Write-Host "Python processes: $pCount"

$restarted = $false
foreach ($r in $required) {
    $found = $false
    $pids = @()
    foreach ($p in $processes) {
        $cmd = ""
        try { $cmd = $p.CommandLine } catch { try { $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId=$($p.Id)").CommandLine } catch {} }
        if ($cmd -like "*$($r.script)*") {
            $found = $true
            $pids += $p.Id
        }
    }
    if ($found) {
        Write-Host "  [OK] $($r.name) (PID: $($pids -join ','))" -ForegroundColor Green
    } else {
        Write-Host "  [DEAD] $($r.name) — dang khoi dong lai..." -ForegroundColor Red
        $logFile = "$logPath\$($r.name).log"
        $script = "$akPath\$($r.script)"
        if (Test-Path $script) {
            Start-Process -FilePath "python" -ArgumentList "-u `"$script`"" -WindowStyle Hidden -RedirectStandardOutput "$logFile.out" -RedirectStandardError "$logFile.err"
            $restarted = $true
        }
    }
}

if ($restarted) {
    Write-Host "`nCo process duoc khoi dong lai!" -ForegroundColor Yellow
    & "$akPath\deploy\sync\send_telegram.ps1" -Message "VPS: Runtime process duoc khoi dong lai" -Status warning
}

# 3. Kiem tra disk
try {
    $disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'" -ErrorAction SilentlyContinue
    $freeGB = [math]::Round($disk.FreeSpace/1GB, 1)
    $totalGB = [math]::Round($disk.Size/1GB, 1)
    Write-Host "Disk C: $freeGB GB / $totalGB GB"
    if ($freeGB -lt 5) {
        & "$akPath\deploy\sync\send_telegram.ps1" -Message "VPS: Disk C thap ($freeGB GB)" -Status warning
    }
} catch { Write-Host "Disk: Khong the doc" }

Write-Host "`n=== HEALTH CHECK DONE ===" -ForegroundColor Cyan
