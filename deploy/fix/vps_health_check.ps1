# vps_health_check.ps1 — Kiem tra runtime daemon, auto-restart neu die
$akPath = "C:\AK"
$logPath = "$akPath\logs"
$daemonScript = "$akPath\services\runtime_daemon.py"

Write-Host "=== RUNTIME HEALTH CHECK ===" -ForegroundColor Cyan
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

# Set env vars
$env:TELEGRAM_BOT_TOKEN = [Environment]::GetEnvironmentVariable("TELEGRAM_BOT_TOKEN","Machine")
$env:TELEGRAM_WHITELIST = [Environment]::GetEnvironmentVariable("TELEGRAM_WHITELIST","Machine")

# 1. RAM
try {
    $ram = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
    $freeRAM = [math]::Round($ram.FreePhysicalMemory/1MB, 1)
    $totalRAM = [math]::Round($ram.TotalVisibleMemorySize/1MB, 1)
    Write-Host "RAM: $freeRAM GB / $totalRAM GB"
    if ($freeRAM -lt 0.3) {
        & "$akPath\deploy\sync\send_telegram.ps1" -Message "VPS: RAM thap ($freeRAM GB)" -Status warning
    }
} catch { Write-Host "RAM: Khong the doc" }

# 2. Disk
try {
    $disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'" -ErrorAction SilentlyContinue
    $freeGB = [math]::Round($disk.FreeSpace/1GB, 1)
    $totalGB = [math]::Round($disk.Size/1GB, 1)
    Write-Host "Disk C: $freeGB GB / $totalGB GB"
    if ($freeGB -lt 5) {
        & "$akPath\deploy\sync\send_telegram.ps1" -Message "VPS: Disk C thap ($freeGB GB)" -Status warning
    }
} catch { Write-Host "Disk: Khong the doc" }

# 3. Check daemon
$daemonPids = @()
try {
    $procs = Get-Process python* -ErrorAction SilentlyContinue
    Write-Host "Python processes: $($procs.Count)"
    foreach ($p in $procs) {
        $cmd = ""
        try { $cmd = $p.CommandLine } catch { try { $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId=$($p.Id)").CommandLine } catch {} }
        if ($cmd -like "*runtime_daemon*") {
            $daemonPids += $p.Id
        }
    }
} catch { }

if ($daemonPids.Count -gt 0) {
    Write-Host "  [OK] Daemon running (PID: $($daemonPids -join ','))" -ForegroundColor Green
} else {
    Write-Host "  [DEAD] Daemon not running — restarting..." -ForegroundColor Red
    try {
        $logOut = "$logPath\daemon_restart.out"
        $logErr = "$logPath\daemon_restart.err"
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = "python"
        $psi.Arguments = "-u `"$daemonScript`""
        $psi.WorkingDirectory = $akPath
        $psi.UseShellExecute = $false
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
        $psi.CreateNoWindow = $true
        $psi.EnvironmentVariables["TELEGRAM_BOT_TOKEN"] = $env:TELEGRAM_BOT_TOKEN
        $psi.EnvironmentVariables["TELEGRAM_WHITELIST"] = $env:TELEGRAM_WHITELIST
        $p = [System.Diagnostics.Process]::Start($psi)
        Start-Sleep -Seconds 3
        if (!$p.HasExited) {
            Write-Host "  -> Restarted (PID: $($p.Id))" -ForegroundColor Green
            & "$akPath\deploy\sync\send_telegram.ps1" -Message "VPS: Daemon duoc khoi dong lai (PID $($p.Id))" -Status warning
        } else {
            Write-Host "  -> Restart FAILED" -ForegroundColor Red
            $p.StandardError.ReadToEnd() | Out-File -FilePath $logErr -Encoding UTF8
        }
    } catch {
        Write-Host "  -> Restart ERROR: $_" -ForegroundColor Red
    }
}

# 4. Git status
try {
    $gitDir = "$akPath\.git"
    if (Test-Path $gitDir) {
        $status = git -C $akPath status --porcelain 2>&1 | Out-String
        if ($status.Trim()) {
            Write-Host "Git: co file chua commit" -ForegroundColor Yellow
        } else {
            Write-Host "Git: sach" -ForegroundColor Green
        }
    }
} catch { }

Write-Host "=== HEALTH CHECK DONE ===" -ForegroundColor Cyan
