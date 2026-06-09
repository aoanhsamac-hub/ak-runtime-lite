# AK-AUTO-RUNTIME-SYNC-01 :: VPS SETUP
# Chay tren VPS voi quyen Administrator

# KHONG hardcode secret. Doc tu environment variables hoac tham so.
param(
    [string]$GitHubUser = "aoanhsamac-hub",
    [string]$GitHubRepo = "ak-runtime-lite",
    [string]$GitHubToken = "",
    [string]$TelegramToken = "",
    [string]$TelegramWhitelist = ""
)

# Lay tu env var neu khong co tham so
if (-not $GitHubToken) { $GitHubToken = [Environment]::GetEnvironmentVariable("GITHUB_TOKEN","Machine") }
if (-not $TelegramToken) { $TelegramToken = [Environment]::GetEnvironmentVariable("TELEGRAM_BOT_TOKEN","Machine") }
if (-not $TelegramWhitelist) { $TelegramWhitelist = [Environment]::GetEnvironmentVariable("TELEGRAM_WHITELIST","Machine") }

if (-not $GitHubToken) { Write-Host "LOI: Thieu GitHubToken. Set env GITHUB_TOKEN hoac truyen tham so." -ForegroundColor Red; exit 1 }

$ErrorActionPreference = "Continue"
$akPath = "C:\AK"
$logPath = "$akPath\logs"
$deployPath = "$akPath\deploy\sync"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " AK-AUTO-RUNTIME-SYNC-01 :: VPS SETUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# === 1. Tao thu muc ===
Write-Host "[1/8] Tao thu muc..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path $logPath -Force | Out-Null
New-Item -ItemType Directory -Path $deployPath -Force | Out-Null
New-Item -ItemType Directory -Path $akPath\docs\reports -Force | Out-Null
New-Item -ItemType Directory -Path $akPath\evidence -Force | Out-Null

# === 2. Set Telegram env vars ===
Write-Host "[2/8] Set Telegram env vars..." -ForegroundColor Yellow
[Environment]::SetEnvironmentVariable("TELEGRAM_BOT_TOKEN", $TelegramToken, "Machine")
[Environment]::SetEnvironmentVariable("TELEGRAM_WHITELIST", $TelegramWhitelist, "Machine")
Write-Host "  -> TELEGRAM_BOT_TOKEN da set" -ForegroundColor Green
Write-Host "  -> TELEGRAM_WHITELIST da set" -ForegroundColor Green

# === 3. Set GitHub remote voi token ===
Write-Host "[3/8] Cau hinh Git remote..." -ForegroundColor Yellow
cd $akPath
$remoteUrl = "https://$GitHubUser`:$GitHubToken@github.com/$GitHubUser/$GitHubRepo.git"
git remote set-url origin $remoteUrl
Write-Host "  -> Remote origin da cau hinh voi token" -ForegroundColor Green

# === 4. Tao script pull source ===
Write-Host "[4/8] Tao script pull_source.ps1..." -ForegroundColor Yellow
$pullScript = @"
# pull_source.ps1 - VPS git pull tu GitHub
`$logFile = "$akPath\logs\git_pull.log"
`$startTime = Get-Date
Write-Host "=== GIT PULL ==="
cd "$akPath"
try {
    git fetch origin main 2>&1 | Out-Null
    `$localHash = git rev-parse HEAD
    `$remoteHash = git rev-parse origin/main
    if (`$localHash -ne `$remoteHash) {
        Write-Host "Co cap nhat moi. Dang pull..."
        git pull origin main 2>&1
        if (`$`? -or `$LASTEXITCODE -eq 0) {
            Write-Host "PULL THANH CONG"
            "`$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | PULL OK | `$remoteHash" | Out-File `$logFile -Append
            # Gui Telegram
            `$msg = "VPS: Git pull thanh cong - commit `$remoteHash"
            powershell -NoProfile -ExecutionPolicy Bypass -Command "& `"$deployPath\send_telegram.ps1`" -Message `"`$msg`" -Status success" 2>`$null
        } else {
            Write-Host "PULL THAT BAI" -ForegroundColor Red
            "`$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | PULL FAIL" | Out-File `$logFile -Append
            powershell -NoProfile -ExecutionPolicy Bypass -Command "& `"$deployPath\send_telegram.ps1`" -Message 'VPS: Git pull that bai' -Status error" 2>`$null
        }
    } else {
        Write-Host "Da o commit moi nhat (`$localHash)"
    }
} catch {
    Write-Host "LOI: `$_" -ForegroundColor Red
    "`$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | PULL ERROR | `$_" | Out-File `$logFile -Append
}
"@
Set-Content -Path "$deployPath\pull_source.ps1" -Value $pullScript -Encoding UTF8

# === 5. Tao script push reports ===
Write-Host "[5/8] Tao script push_reports.ps1..." -ForegroundColor Yellow
$pushScript = @"
# push_reports.ps1 - VPS git push reports len GitHub
`$logFile = "$akPath\logs\git_push.log"
`$startTime = Get-Date
Write-Host "=== GIT PUSH REPORTS ==="
cd "$akPath"
try {
    # Chi add reports, evidence, logs - khong add source code
    git add -A docs/reports/ evidence/ logs/ 2>&1 | Out-Null
    `$status = git status --porcelain
    if (`$status) {
        Write-Host "Co file moi. Dang commit va push..."
        git commit -m "auto-sync reports `$(Get-Date -Format 'yyyy-MM-dd HH:mm')" 2>&1 | Out-Null
        git push origin main 2>&1
        if (`$`? -or `$LASTEXITCODE -eq 0) {
            Write-Host "PUSH REPORTS THANH CONG"
            "`$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | PUSH OK" | Out-File `$logFile -Append
        } else {
            Write-Host "PUSH REPORTS THAT BAI" -ForegroundColor Red
            "`$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | PUSH FAIL" | Out-File `$logFile -Append
            powershell -NoProfile -ExecutionPolicy Bypass -Command "& `"$deployPath\send_telegram.ps1`" -Message 'VPS: Push reports that bai' -Status error" 2>`$null
        }
    } else {
        Write-Host "Khong co file moi"
    }
} catch {
    Write-Host "LOI: `$_" -ForegroundColor Red
    "`$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | PUSH ERROR | `$_" | Out-File `$logFile -Append
}
"@
Set-Content -Path "$deployPath\push_reports.ps1" -Value $pushScript -Encoding UTF8

# === 6. Tao send_telegram.ps1 tren VPS ===
Write-Host "[6/8] Tao send_telegram.ps1 tren VPS..." -ForegroundColor Yellow
$sendScript = @"
param(`$Message, `$Status)
`$botToken = [Environment]::GetEnvironmentVariable("TELEGRAM_BOT_TOKEN","Machine")
`$chatId = [Environment]::GetEnvironmentVariable("TELEGRAM_WHITELIST","Machine")
`$icons = @{info="ℹ️"; success="✅"; warning="⚠️"; error="❌"}
`$text = "`$(`$icons[`$Status]) [VPS] `$Message"
try {
    `$url = "https://api.telegram.org/bot`$botToken/sendMessage"
    `$body = @{chat_id=`$chatId; text=`$text; parse_mode="HTML"} | ConvertTo-Json -Compress
    Invoke-RestMethod -Uri `$url -Method Post -Body `$body -ContentType "application/json" -TimeoutSec 10 | Out-Null
    Write-Host "Telegram da gui" -ForegroundColor Green
} catch {
    Write-Host "Loi gui Telegram: `$_" -ForegroundColor Red
}
"@
Set-Content -Path "$deployPath\send_telegram.ps1" -Value $sendScript -Encoding UTF8

# === 7. Tao scheduled tasks ===
Write-Host "[7/8] Tao Windows Scheduled Tasks..." -ForegroundColor Yellow
$taskUser = "SYSTEM"

# Task 1: AK_Git_Pull_Every_30min
$action1 = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$deployPath\pull_source.ps1`""
$trigger1 = New-ScheduledTaskTrigger -Daily -At "00:00" -RepetitionInterval "00:30:00"
$settings1 = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew
$principal1 = New-ScheduledTaskPrincipal -UserId $taskUser -RunLevel Highest
Register-ScheduledTask -TaskName "AK_Git_Pull_Every_30min" -Action $action1 -Trigger $trigger1 -Settings $settings1 -Principal $principal1 -Force | Out-Null
Write-Host "  [OK] AK_Git_Pull_Every_30min" -ForegroundColor Green

# Task 2: AK_Push_Reports_Every_1h
$action2 = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$deployPath\push_reports.ps1`""
$trigger2 = New-ScheduledTaskTrigger -Daily -At "00:00" -RepetitionInterval "01:00:00"
$settings2 = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew
$principal2 = New-ScheduledTaskPrincipal -UserId $taskUser -RunLevel Highest
Register-ScheduledTask -TaskName "AK_Push_Reports_Every_1h" -Action $action2 -Trigger $trigger2 -Settings $settings2 -Principal $principal2 -Force | Out-Null
Write-Host "  [OK] AK_Push_Reports_Every_1h" -ForegroundColor Green

# Task 3: AK_System_Health_Every_5min
$action3 = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -Command `"Get-Process python* -ErrorAction SilentlyContinue | Format-Table Id,ProcessName -AutoSize; Get-CimInstance Win32_OperatingSystem | Select-Object @{N='FreeRAM';E={[math]::Round(`$_.FreePhysicalMemory/1MB,1)}} | Format-Table -AutoSize`""
$trigger3 = New-ScheduledTaskTrigger -Daily -At "00:00" -RepetitionInterval "00:05:00"
$settings3 = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew
$principal3 = New-ScheduledTaskPrincipal -UserId $taskUser -RunLevel Highest
Register-ScheduledTask -TaskName "AK_System_Health_Every_5min" -Action $action3 -Trigger $trigger3 -Settings $settings3 -Principal $principal3 -Force | Out-Null
Write-Host "  [OK] AK_System_Health_Every_5min" -ForegroundColor Green

# === 8. Kiem tra ===
Write-Host "[8/8] Kiem tra cau hinh..." -ForegroundColor Yellow
Write-Host "`nGit remote:" -ForegroundColor Cyan
git remote -v
Write-Host "`nScheduled tasks:" -ForegroundColor Cyan
Get-ScheduledTask -TaskName "AK_*" | Format-Table TaskName,State -AutoSize
Write-Host "`nTelegram vars:" -ForegroundColor Cyan
[Environment]::GetEnvironmentVariable("TELEGRAM_BOT_TOKEN","Machine") -replace ".{10}$","**********"
[Environment]::GetEnvironmentVariable("TELEGRAM_WHITELIST","Machine")

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host " VPS SETUP HOAN TAT!" -ForegroundColor Green
Write-Host " - Pull source: moi 30 phut" -ForegroundColor Green
Write-Host " - Push reports: moi 1 tieng" -ForegroundColor Green
Write-Host " - Health check: moi 5 phut" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
