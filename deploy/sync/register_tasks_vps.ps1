# Them Git usr/bin vao PATH de tim ssh, tar, etc.
$gitBins = @("C:\Program Files\Git\usr\bin","C:\Program Files (x86)\Git\usr\bin","$env:LOCALAPPDATA\Programs\Git\usr\bin")
foreach ($p in $gitBins) { if (Test-Path "$p\ssh.exe") { $env:Path = "$p;$env:Path"; break } }

$ErrorActionPreference = "Continue"

Write-Host "=== CAP NHAT SCHEDULED TASKS TREN VPS ===" -ForegroundColor Cyan

if (-not (Test-Path "D:\AK\logs\.ssh_done")) {
    Write-Host "LOI: Chua chay setup_ssh.ps1" -ForegroundColor Red
    exit 1
}

# Kiem tra SSH
$test = ssh -o BatchMode=yes -o ConnectTimeout=5 ak-vps "echo OK" 2>$null
if ($test -ne "OK") {
    Write-Host "LOI: Khong SSH duoc vao VPS" -ForegroundColor Red
    exit 1
}

# Script content se duoc gui qua SSH
$vpsScript = @'
# Tao AK local git repo neu chua co
$akPath = "C:\AK"
if (-not (Test-Path "$akPath\.git")) {
    Write-Host "Dang tao git repo local tren VPS..."
    cd $akPath
    git init
    git add -A
    git commit -m "Initial commit after sync $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" 2>$null
}

# Cap nhat task AK_Git_Pull_Every_30_Min
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -Command `"cd C:\AK; git add -A; git commit -m 'auto-sync $(Get-Date -Format yyyy-MM-dd HH:mm)' 2>`$null; echo SYNC_DONE`""
$trigger = New-ScheduledTaskTrigger -Daily -At "00:00" -RepetitionInterval "00:30:00"
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -RunLevel Highest
$task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal

try {
    Register-ScheduledTask -TaskName "AK_Git_Local_Tracking" -InputObject $task -Force | Out-Null
    Write-Host "[OK] AK_Git_Local_Tracking - moi 30 phut"
} catch {
    Write-Host "[FAIL] AK_Git_Local_Tracking - $_"
}

# Kiem tra cac task khac
$existing = Get-ScheduledTask -TaskName "AK_*" -ErrorAction SilentlyContinue
Write-Host "`nCac task AK_* hien tai:"
$existing | Format-Table TaskName,State -AutoSize

'@

Write-Host "Dang gui script cau hinh sang VPS..." -ForegroundColor Yellow
ssh ak-vps "powershell -NoProfile -ExecutionPolicy Bypass -Command `"$vpsScript`"" 2>&1

Write-Host "`n=== HOAN TAT VPS TASKS ===" -ForegroundColor Cyan
