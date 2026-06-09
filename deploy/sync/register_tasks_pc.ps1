# Them Git usr/bin vao PATH de tim ssh, tar, etc.
$gitBins = @("C:\Program Files\Git\usr\bin","C:\Program Files (x86)\Git\usr\bin","$env:LOCALAPPDATA\Programs\Git\usr\bin")
foreach ($p in $gitBins) { if (Test-Path "$p\ssh.exe") { $env:Path = "$p;$env:Path"; break } }

$ErrorActionPreference = "Stop"
$taskUser = "$env:USERDOMAIN\$env:USERNAME"
$scriptDir = "D:\AK\deploy\sync"

Write-Host "=== TAO SCHEDULED TASKS TREN PC ===" -ForegroundColor Cyan

# Ham tao task
function New-AkTask($name, $script, $repeat, $desc) {
    $scriptPath = "$scriptDir\$script"
    $action = "PowerShell.exe -NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""
    $trigger = New-ScheduledTaskTrigger -Daily -At "00:00" -RepetitionInterval $repeat
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew
    $principal = New-ScheduledTaskPrincipal -UserId $taskUser -RunLevel Limited
    $task = New-ScheduledTask -Action (New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"") -Trigger $trigger -Settings $settings -Principal $principal

    try {
        Register-ScheduledTask -TaskName $name -InputObject $task -Force | Out-Null
        Write-Host "  [OK] $name - $desc" -ForegroundColor Green
    } catch {
        Write-Host "  [FAIL] $name - $_" -ForegroundColor Red
    }
}

# 1. Push source moi 30 phut
New-AkTask -name "AK_Push_Source_Every_30min" -script "push_source.ps1" -repeat "00:30:00" -desc "Push source PC -> VPS moi 30 phut"

# 2. Pull reports moi 1 tieng
New-AkTask -name "AK_Pull_Reports_Every_1h" -script "pull_reports.ps1" -repeat "01:00:00" -desc "Pull reports VPS -> PC moi 1 tieng"

Write-Host "`nKiem tra task da tao:" -ForegroundColor Cyan
Get-ScheduledTask -TaskName "AK_*" | Format-Table TaskName,State,Triggers -AutoSize
