# Them Git usr/bin vao PATH de tim ssh, tar, etc.
$gitBins = @("C:\Program Files\Git\usr\bin","C:\Program Files (x86)\Git\usr\bin","$env:LOCALAPPDATA\Programs\Git\usr\bin")
foreach ($p in $gitBins) { if (Test-Path "$p\ssh.exe") { $env:Path = "$p;$env:Path"; break } }

$ErrorActionPreference = "Continue"
$logFile = "D:\AK\logs\sync_pull.log"
$startTime = Get-Date

Write-Host "=== PULL REPORTS: VPS -> PC ===" -ForegroundColor Cyan
Write-Host "Bat dau: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

if (-not (Test-Path "D:\AK\logs\.ssh_done")) {
    Write-Host "LOI: Chua chay setup_ssh.ps1. Chay truoc." -ForegroundColor Red
    exit 1
}

# Kiem tra SSH
$test = ssh -o BatchMode=yes -o ConnectTimeout=5 ak-vps "echo OK" 2>$null
if ($test -ne "OK") {
    Write-Host "LOI: Khong SSH duoc vao VPS." -ForegroundColor Red
    & "D:\AK\deploy\sync\send_telegram.ps1" -Message "PULL REPORTS THAT BAI: Khong SSH duoc vao VPS" -Status error
    exit 1
}

# Tim tar.exe
$tarPaths = @(
    "C:\Program Files\Git\usr\bin\tar.exe",
    "C:\Program Files (x86)\Git\usr\bin\tar.exe",
    "$env:LOCALAPPDATA\Programs\Git\usr\bin\tar.exe"
)
$tarExe = $null
foreach ($p in $tarPaths) {
    if (Test-Path $p) { $tarExe = $p; break }
}
if (-not $tarExe) {
    Write-Host "LOI: Khong tim thay tar.exe tu Git Bash" -ForegroundColor Red
    exit 1
}

# Danh sach thu muc can sync tu VPS ve PC
$folders = @(
    @{remote="docs/reports"; local="D:\AK\docs\reports"},
    @{remote="evidence"; local="D:\AK\evidence"},
    @{remote="logs"; local="D:\AK\logs"}
)

$successCount = 0
$failCount = 0

foreach ($f in $folders) {
    Write-Host "  Pull $($f.remote)/ ..." -ForegroundColor Yellow
    
    if (-not (Test-Path $f.local)) { New-Item -ItemType Directory -Path $f.local -Force | Out-Null }
    
    # Kiem tra xem thu muc tren VPS co ton tai khong
    $exists = ssh ak-vps "if exist $targetDir\$($f.remote) (echo EXISTS)" 2>$null
    if ($exists -ne "EXISTS") {
        Write-Host "    -> Thu muc $($f.remote) chua ton tai tren VPS, bo qua" -ForegroundColor DarkYellow
        continue
    }
    
    # Tar tu VPS, pipe ve PC
    ssh ak-vps "cd C:/AK && tar -c --exclude='.venv' --exclude='*__.pycache__*' -C C:/AK $($f.remote)" 2>&1 | & $tarExe -x -C $f.local 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    -> OK" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host "    -> LOI (exit: $LASTEXITCODE)" -ForegroundColor Red
        $failCount++
    }
}

$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds

Write-Host "`nKet qua: $successCount thanh cong, $failCount that bai ($duration giay)" -ForegroundColor Cyan

"$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | PULL OK=${successCount} FAIL=${failCount} | ${duration}s" | Out-File -FilePath $logFile -Encoding UTF8 -Append

if ($failCount -eq 0) {
    & "D:\AK\deploy\sync\send_telegram.ps1" -Message "PULL REPORTS THANH CONG ($successCount thu muc, $duration giay)" -Status success
} else {
    & "D:\AK\deploy\sync\send_telegram.ps1" -Message "PULL REPORTS CO LOI ($failCount thu muc loi)" -Status warning
}
