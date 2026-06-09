# Them Git usr/bin vao PATH de tim ssh, tar, etc.
$gitBins = @("C:\Program Files\Git\usr\bin","C:\Program Files (x86)\Git\usr\bin","$env:LOCALAPPDATA\Programs\Git\usr\bin")
foreach ($p in $gitBins) { if (Test-Path "$p\ssh.exe") { $env:Path = "$p;$env:Path"; break } }

$ErrorActionPreference = "Stop"
$logFile = "D:\AK\logs\runtime_update.log"

Write-Host "=== UPDATE RUNTIME ===" -ForegroundColor Cyan

if (-not (Test-Path "D:\AK\logs\.ssh_done")) {
    Write-Host "LOI: Chua chay setup_ssh.ps1" -ForegroundColor Red
    exit 1
}

# 1. Backup truoc khi update
Write-Host "[1/5] Backup runtime hien tai tren VPS..." -ForegroundColor Yellow
$backupName = "pre_update_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
ssh ak-vps "if exist C:\AK (mkdir C:\AK\.backup\$backupName 2>nul & robocopy C:\AK C:\AK\.backup\$backupName /E /XD .venv __pycache__ .backup /NFL /NDL /NJH /NJS)" 2>&1 | Out-Null
Write-Host "  -> Backup tai: C:\AK\.backup\$backupName" -ForegroundColor Green

# 2. Push source moi
Write-Host "[2/5] Push source moi tu PC len VPS..." -ForegroundColor Yellow
& "D:\AK\deploy\sync\push_source.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "LOI: Push source that bai. Rollback..." -ForegroundColor Red
    & "D:\AK\deploy\sync\send_telegram.ps1" -Message "UPDATE RUNTIME THAT BAI - Dang rollback" -Status error
    # Rollback: copy backup ve
    ssh ak-vps "robocopy C:\AK\.backup\$backupName C:\AK /E /XD .venv __pycache__ .backup /NFL /NDL /NJH /NJS" 2>&1 | Out-Null
    exit 1
}

# 3. Kiem tra commit hash
Write-Host "[3/5] Xac nhan source da duoc cap nhat..." -ForegroundColor Yellow
$hash = ssh ak-vps "cd C:\AK && git log -1 --format=%H 2>nul" 2>$null
if ($hash) {
    Write-Host "  -> Git commit: $hash" -ForegroundColor Green
} else {
    Write-Host "  -> (VPS chua co git repo local, bo qua)" -ForegroundColor DarkYellow
}

# 4. Restart runtime
Write-Host "[4/5] Restart runtime..." -ForegroundColor Yellow
& "D:\AK\deploy\sync\restart_runtime.ps1"

# 5. Kiem tra status
Write-Host "[5/5] Kiem tra runtime sau update..." -ForegroundColor Yellow
& "D:\AK\deploy\sync\status_runtime.ps1"

Write-Host "`n=== UPDATE RUNTIME HOAN TAT ===" -ForegroundColor Cyan
"$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | UPDATE OK | backup=$backupName" | Out-File -FilePath $logFile -Encoding UTF8 -Append
& "D:\AK\deploy\sync\send_telegram.ps1" -Message "UPDATE RUNTIME THANH CONG (backup: $backupName)" -Status success
