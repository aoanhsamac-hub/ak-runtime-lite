# Them Git usr/bin vao PATH de tim ssh, tar, etc.
$gitBins = @("C:\Program Files\Git\usr\bin","C:\Program Files (x86)\Git\usr\bin","$env:LOCALAPPDATA\Programs\Git\usr\bin")
foreach ($p in $gitBins) { if (Test-Path "$p\ssh.exe") { $env:Path = "$p;$env:Path"; break } }

$ErrorActionPreference = "Continue"

Write-Host "=== RUNTIME STATUS ===" -ForegroundColor Cyan

$test = ssh -o BatchMode=yes -o ConnectTimeout=5 ak-vps "echo OK" 2>$null
if ($test -ne "OK") {
    Write-Host "Khong the ket noi VPS" -ForegroundColor Red
    exit 1
}

# Kiem tra cac qua trinh Python dang chay
Write-Host "Processes tren VPS:" -ForegroundColor Yellow
$processes = ssh ak-vps "Get-Process python* -ErrorAction SilentlyContinue | Format-Table Id,ProcessName,CPU,StartTime -AutoSize" 2>&1
Write-Host $processes

# Kiem tra RAM
Write-Host "`nRAM VPS:" -ForegroundColor Yellow
$ram = ssh ak-vps "Get-CimInstance Win32_OperatingSystem | Select-Object @{N='FreeGB';E={[math]::Round(\$_.FreePhysicalMemory/1MB,1)}},@{N='TotalGB';E={[math]::Round(\$_.TotalVisibleMemorySize/1MB,1)}} | Format-Table -AutoSize" 2>&1
Write-Host $ram

# Kiem tra disk
Write-Host "`nDisk C:" -ForegroundColor Yellow
$disk = ssh ak-vps "Get-CimInstance Win32_LogicalDisk -Filter 'DeviceID=\"C:\"' | Select-Object DeviceID,@{N='FreeGB';E={[math]::Round(\$_.FreeSpace/1GB,1)}},@{N='TotalGB';E={[math]::Round(\$_.Size/1GB,1)}} | Format-Table -AutoSize" 2>&1
Write-Host $disk

# Kiem tra scheduled tasks
Write-Host "`nScheduled Tasks (AK_*):" -ForegroundColor Yellow
$tasks = ssh ak-vps "Get-ScheduledTask -TaskName AK_* -ErrorAction SilentlyContinue | Format-Table TaskName,State -AutoSize" 2>&1
Write-Host $tasks
